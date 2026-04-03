# OLAP vs OLTP: 데이터베이스 아키텍처의 두 축을 해부하다

> 트랜잭션과 분석, 두 세계의 내부 구조를 깊이 파헤치는 기술 블로그

---

## 들어가며: 왜 이 구분이 중요한가

데이터베이스를 다루는 엔지니어라면 OLTP(Online Transaction Processing)와 OLAP(Online Analytical Processing)라는 용어를 수없이 들어왔을 것이다. 하지만 단순히 "하나는 트랜잭션용, 하나는 분석용"이라는 교과서적 설명을 넘어서, 이 두 패러다임이 **왜 근본적으로 다른 설계 철학을 가질 수밖에 없는지**, 그 내부 구조(internals)를 깊이 이해하는 것은 현대 데이터 아키텍처를 설계하는 데 필수적이다.

이 글에서는 스토리지 엔진(Storage Engine)부터 동시성 제어(Concurrency Control), 쿼리 실행 모델(Query Execution Model), 그리고 최신 HTAP(Hybrid Transactional/Analytical Processing) 트렌드까지 아우르는 심층 분석을 다룬다.

---

## 1. 근본적 설계 목표의 차이

OLTP와 OLAP의 차이는 단순한 기능 차이가 아니라, **최적화 대상 자체가 다르다는 데서 출발**한다.

**OLTP**는 개별 레코드 수준의 읽기/쓰기 지연 시간(Latency)을 최소화하는 것이 목표다. 한 번의 요청에서 접근하는 행(row)의 수는 보통 1~수십 개에 불과하지만, 초당 수천에서 수만 건의 트랜잭션을 동시에 처리해야 한다. 핵심 지표는 **TPS(Transactions Per Second)**와 **p99 latency**이다.

**OLAP**는 대량 데이터에 대한 집계(Aggregation) 쿼리의 처리량(Throughput)을 극대화하는 것이 목표다. 한 번의 쿼리에서 수백만~수십억 행을 스캔하지만, 동시 쿼리 수는 상대적으로 적다. 핵심 지표는 **QPS(Queries Per Second)**와 **Scan Throughput (rows/sec)**이다.

이 근본적인 차이가 이하에서 다루는 모든 아키텍처적 분기점의 원인이 된다.

---

## 2. 스토리지 레이아웃: Row Store vs Column Store

### 2.1 Row-Oriented Storage (행 기반 저장)

OLTP 시스템의 대표적인 스토리지 방식이다. PostgreSQL, MySQL(InnoDB), Oracle 등이 이 방식을 사용한다.

```
Page 1: [Row1: id=1, name="Alice", age=30, city="Seoul"]
         [Row2: id=2, name="Bob",   age=25, city="Busan"]
         [Row3: id=3, name="Carol", age=35, city="Seoul"]
```

한 행(row)의 모든 컬럼이 물리적으로 인접해 저장된다. 이 구조의 이점은 명확하다:

- **Point Lookup이 빠르다**: `SELECT * FROM users WHERE id = 1` 같은 쿼리는 인덱스를 통해 해당 행이 위치한 단일 디스크 페이지(page)만 읽으면 된다. 모든 컬럼이 같은 페이지에 있으므로 I/O가 최소화된다.
- **단일 행 INSERT/UPDATE가 효율적이다**: 새 레코드를 추가할 때 한 페이지의 빈 슬롯(slot)에 기록하면 끝이다. 컬럼별로 다른 위치에 쓸 필요가 없다.

그러나 **분석 쿼리에서는 치명적인 비효율**이 발생한다. `SELECT AVG(age) FROM users`를 실행하면, `age` 컬럼만 필요한데도 `name`, `city` 등 불필요한 컬럼까지 디스크에서 읽어야 한다. 100개의 컬럼이 있는 테이블에서 2개의 컬럼만 필요한 쿼리를 실행하면, 이론적으로 I/O의 98%가 낭비된다.

### 2.2 Column-Oriented Storage (열 기반 저장)

OLAP 시스템의 핵심 저장 방식이다. ClickHouse, Apache Parquet, DuckDB, Amazon Redshift 등이 이 방식을 사용한다.

```
Column "id":   [1, 2, 3, 4, 5, ...]
Column "name": ["Alice", "Bob", "Carol", ...]
Column "age":  [30, 25, 35, ...]
Column "city": ["Seoul", "Busan", "Seoul", ...]
```

같은 컬럼의 값들이 물리적으로 연속 저장된다. 이 구조가 분석 쿼리에 압도적인 이유는 세 가지다:

**첫째, I/O 선택성(I/O Selectivity)**이 극대화된다. `SELECT SUM(revenue) FROM orders`를 실행할 때, `revenue` 컬럼 데이터만 디스크에서 읽는다. 100개 컬럼 중 1개만 읽으면 되므로 I/O가 **10~50배** 감소한다.

**둘째, 압축률(Compression Ratio)**이 비약적으로 향상된다. 같은 타입의 데이터가 연속 저장되면, 데이터 간 유사성(similarity)이 높아져 압축이 극히 효율적이 된다. 예를 들어:
- `city` 컬럼에 "Seoul"이 반복되면 **Dictionary Encoding**으로 정수 인덱스만 저장
- `age` 컬럼처럼 범위가 좁은 정수는 **Frame-of-Reference (FOR)** 인코딩으로 차이값(delta)만 저장
- **Run-Length Encoding (RLE)**으로 연속된 동일 값을 압축

일반적으로 컬럼 스토어는 행 스토어 대비 **3~10배** 높은 압축률을 달성한다.

**셋째, CPU 벡터화(Vectorized Execution)**와의 시너지이다. 컬럼 데이터가 메모리에 연속 배치되면 CPU의 SIMD(Single Instruction, Multiple Data) 명령어를 활용해 한 번의 CPU 사이클로 여러 값을 동시에 처리할 수 있다. 이는 집계 연산에서 **10~100배**의 성능 차이를 만든다.

### 2.3 Write Amplification 트레이드오프

컬럼 스토어의 약점은 **쓰기(Write) 성능**이다. 하나의 행을 삽입하려면 각 컬럼 파일에 개별적으로 값을 기록해야 한다. 100개 컬럼이 있다면 100번의 쓰기가 발생한다. 이것이 OLTP 워크로드에서 컬럼 스토어가 비효율적인 근본 이유이며, ClickHouse 같은 시스템이 **LSM-Tree 기반 MergeTree**를 사용해 작은 배치를 버퍼링한 뒤 백그라운드에서 병합(merge)하는 이유이기도 하다.

---

## 3. 인덱싱 전략의 분기

### 3.1 OLTP: B-Tree와 그 변종들

OLTP 시스템의 핵심 인덱스 구조는 **B-Tree(Balanced Tree)**이다. B-Tree는 다음과 같은 OLTP 특성에 최적화되어 있다:

- **O(log N) Point Lookup**: 키 값으로 특정 행을 찾는 데 트리 깊이만큼의 디스크 I/O만 필요
- **범위 스캔(Range Scan)**: 리프 노드(leaf node)가 정렬된 링크드 리스트로 연결되어, `WHERE price BETWEEN 100 AND 500` 같은 범위 쿼리에 효율적
- **In-place Update 지원**: 키 값이 변경되지 않으면 리프 노드의 포인터만 갱신

PostgreSQL은 B-Tree 외에도 GiST(Generalized Search Tree), GIN(Generalized Inverted Index), BRIN(Block Range Index) 등 다양한 인덱스를 지원하지만, 대부분의 OLTP 워크로드에서 B-Tree가 기본이다.

### 3.2 OLAP: Zone Map, Sparse Index, 그리고 Data Skipping

OLAP 시스템은 전통적인 B-Tree 대신 **대량 스캔에 최적화된 인덱스**를 사용한다.

**Zone Map (Min/Max Index)**: 각 데이터 블록(보통 수천~수만 행)의 최솟값과 최댓값을 메타데이터로 저장한다. `WHERE date > '2025-01-01'` 쿼리가 들어오면, 최댓값이 2024-12-31인 블록은 아예 읽지 않고 건너뛴다(Data Skipping). ClickHouse에서는 이를 **Primary Key Index**라 부르며, 8192행 단위의 Granule마다 min/max를 기록한다.

**Sparse Index**: 모든 행이 아닌, 일정 간격(예: 8192행마다)의 키 값만 인덱스에 저장한다. 메모리 사용량이 극히 적어 수십억 행의 테이블도 인덱스가 메모리에 완전히 올라간다.

**Bloom Filter**: 특정 값이 블록에 존재하는지를 확률적으로 판단한다. False positive는 가능하지만 false negative는 없어, 불필요한 블록 스캔을 효과적으로 제거한다.

---

## 4. 동시성 제어(Concurrency Control)의 차이

### 4.1 OLTP: MVCC와 ACID의 세계

OLTP 시스템은 수천 개의 동시 트랜잭션이 같은 데이터를 읽고 쓰는 환경에서 **데이터 정합성(Data Consistency)**을 보장해야 한다. 이를 위한 핵심 메커니즘이 **MVCC(Multi-Version Concurrency Control)**이다.

MVCC의 핵심 원칙은 **"읽기는 쓰기를 차단하지 않고, 쓰기는 읽기를 차단하지 않는다(Reads don't block writes, writes don't block reads)"**는 것이다.

**PostgreSQL의 구현 방식**:
- 행을 업데이트하면 기존 행을 삭제 표시하고 새 버전(tuple)을 생성한다
- 각 행에 `xmin`(생성 트랜잭션 ID)과 `xmax`(삭제 트랜잭션 ID)를 기록한다
- 트랜잭션은 자신의 Snapshot 시점에서 보이는 행 버전만 읽는다
- VACUUM 프로세스가 더 이상 어떤 트랜잭션에서도 보이지 않는 죽은 튜플(dead tuple)을 정리한다

**MySQL InnoDB의 구현 방식**:
- Undo Log에 이전 버전을 저장하고, 현재 행에서 undo 체인을 따라가며 과거 버전을 재구성한다
- Clustered Index(B-Tree)에 최신 버전을 저장하고, 이전 버전은 undo segment에 유지한다

**Write-Ahead Logging (WAL)**은 ACID의 Durability를 보장하는 핵심 장치다. 모든 변경 사항은 실제 데이터 페이지에 반영되기 전에 WAL에 먼저 기록된다. 시스템 장애 시 WAL을 재생(replay)하여 커밋된 트랜잭션을 복구한다.

### 4.2 OLAP: Append-Only와 Batch Isolation

OLAP 시스템은 동시성 제어에 대한 요구사항이 근본적으로 다르다:

- **쓰기 패턴이 Bulk Insert/Append 위주**이다. 개별 행의 UPDATE/DELETE는 드물거나 아예 지원하지 않는다.
- **읽기는 거의 항상 Historical Data에 대한 Full Scan**이다.
- 따라서 행 수준의 Lock이나 MVCC 같은 복잡한 메커니즘이 불필요하다.

ClickHouse의 MergeTree 엔진은 이를 극단적으로 보여준다:
1. 데이터는 **Immutable Part** 단위로 디스크에 기록된다
2. 백그라운드 머지(merge) 프로세스가 작은 Part들을 큰 Part로 병합한다
3. UPDATE/DELETE는 "mutation"이라는 비동기 재작성(rewrite) 방식으로 처리된다
4. 읽기 쿼리는 현재 시점의 Part 목록에 대한 Snapshot을 잡고 실행한다

이 Append-Only 설계 덕분에 Lock 경합이 거의 없고, 쓰기와 읽기가 서로를 방해하지 않는다.

---

## 5. 쿼리 실행 엔진의 차이

### 5.1 OLTP: Volcano/Iterator 모델

전통적인 OLTP 데이터베이스는 **Volcano 모델(또는 Iterator 모델)**을 사용한다. 쿼리 플랜의 각 연산자(operator)가 `next()` 함수를 호출하며 **한 번에 한 행(tuple-at-a-time)**씩 상위 연산자로 전달한다.

```
Project (name, age)
  └── Filter (age > 30)
        └── Scan (users)
```

이 모델은 구현이 단순하고, 한 행만 반환하는 OLTP 쿼리에서는 오버헤드가 미미하다. 하지만 수백만 행을 처리하는 분석 쿼리에서는 **함수 호출 오버헤드(function call overhead)**가 행의 수만큼 누적되어 심각한 병목이 된다.

### 5.2 OLAP: Vectorized Execution과 Batch Processing

현대 OLAP 엔진(ClickHouse, DuckDB, Velox 등)은 **Vectorized Execution** 모델을 채택한다. 한 번에 한 행이 아니라, **수천 개의 값으로 구성된 벡터(vector/batch)**를 단위로 처리한다.

```
┌─────────────────────────────────────────┐
│ Batch of 1024 values                    │
│ age: [30, 25, 35, 28, 42, 31, ...]     │
│                                          │
│ → SIMD Filter: age > 30                 │
│ → Result mask: [1, 0, 1, 0, 1, 1, ...] │
│                                          │
│ → Compact & pass to next operator       │
└─────────────────────────────────────────┘
```

이 방식의 이점:

- **함수 호출 오버헤드 감소**: `next()`를 100만 번 호출하는 대신, 1024행짜리 배치를 ~1000번 처리
- **CPU 캐시 효율**: 같은 타입의 데이터가 연속 메모리에 배치되어 L1/L2 캐시 히트율이 극대화
- **SIMD 활용**: AVX2/AVX-512 등의 SIMD 명령어로 한 CPU 사이클에 4~16개 값을 동시 비교/연산
- **브랜치 프리딕션 최적화**: 조건 평가를 비트마스크(bitmask)로 변환하여 CPU 분기 예측 실패(branch misprediction)를 회피

DuckDB는 이를 **"Vectorized Push-Based Execution"**이라 부르며, 벡터를 상위 연산자로 "밀어 올리는(push)" 방식으로 파이프라인 효율을 극대화한다.

---

## 6. 스키마 설계 철학

### 6.1 OLTP: 정규화(Normalization)

OLTP 스키마는 **제3정규형(3NF)** 이상으로 정규화되는 것이 원칙이다:

- 데이터 중복을 제거하여 UPDATE Anomaly를 방지
- 하나의 사실(fact)은 하나의 위치에만 저장
- 참조 무결성(Referential Integrity)을 외래 키(Foreign Key)로 강제

```sql
-- 정규화된 OLTP 스키마
CREATE TABLE customers (id INT PK, name VARCHAR, address_id INT FK);
CREATE TABLE addresses (id INT PK, city VARCHAR, street VARCHAR);
CREATE TABLE orders (id INT PK, customer_id INT FK, product_id INT FK, qty INT);
CREATE TABLE products (id INT PK, name VARCHAR, price DECIMAL);
```

이 설계는 트랜잭션의 정합성에는 이상적이지만, "지난 분기 서울 고객의 제품별 매출 합계"를 구하려면 4개 테이블의 JOIN이 필요해진다.

### 6.2 OLAP: 비정규화와 Star/Snowflake Schema

OLAP 스키마는 **분석 쿼리의 효율성**을 위해 의도적으로 비정규화(Denormalization)한다:

**Star Schema**: 중앙의 Fact Table과 이를 둘러싼 Dimension Table로 구성된다.

```sql
-- Star Schema
CREATE TABLE fact_sales (
    date_key INT, customer_key INT, product_key INT,
    quantity INT, revenue DECIMAL, cost DECIMAL
);
CREATE TABLE dim_customer (customer_key INT PK, name VARCHAR, city VARCHAR, segment VARCHAR);
CREATE TABLE dim_product (product_key INT PK, name VARCHAR, category VARCHAR, brand VARCHAR);
CREATE TABLE dim_date (date_key INT PK, date DATE, month INT, quarter INT, year INT);
```

**이점**: JOIN의 깊이가 항상 1단계(Fact → Dimension)이고, Fact Table의 넓은 스캔에 최적화된 구조이다. 현대 OLAP 엔진은 아예 **Wide Denormalized Table** 하나로 모든 데이터를 펼치는 경우도 많다.

---

## 7. 전통적 OLAP의 진화: MOLAP → ROLAP → 현대 OLAP

### 7.1 MOLAP (Multidimensional OLAP)

초기 OLAP 시스템은 데이터를 **다차원 큐브(Multidimensional Cube)**로 사전 집계(Pre-Aggregation)하여 저장했다. Microsoft Analysis Services(SSAS), IBM Cognos 등이 대표적이다.

- 모든 차원(Dimension) 조합에 대한 집계값을 미리 계산하여 큐브에 저장
- 쿼리 시에는 미리 계산된 값을 즉시 반환하므로 응답 속도가 극히 빠름
- 그러나 차원의 수가 늘어나면 큐브의 크기가 기하급수적으로 증가하는 **"차원의 저주(Curse of Dimensionality)"** 문제가 발생
- 데이터 갱신 시 큐브 전체를 재구축해야 하는 경우가 많아 **실시간성이 떨어짐**

### 7.2 ROLAP (Relational OLAP)

ROLAP은 큐브 대신 **관계형 데이터베이스 위에서 SQL로 분석 쿼리**를 실행하는 방식이다.

- 사전 집계 없이 원본 데이터에 직접 쿼리
- MOLAP 대비 확장성이 우수하지만, 대규모 JOIN이 필요해 성능이 느림
- Materialized View를 통한 부분적 사전 집계로 성능을 보완

### 7.3 현대 OLAP: 컬럼 스토어 + 벡터화 실행

ClickHouse, DuckDB, Apache Druid, StarRocks 등 현대 OLAP 엔진은 MOLAP의 "사전 계산" 전략과 ROLAP의 "SQL 유연성"을 모두 뛰어넘었다:

- **컬럼 스토어 + 고효율 압축**으로 원본 데이터 스캔 자체가 충분히 빠름
- **벡터화 실행 엔진**으로 CPU 효율을 극대화
- **적응형 인덱싱(Adaptive Indexing)**으로 사전 정의 없이도 쿼리 패턴에 맞는 최적화를 자동 수행
- 결과적으로 큐브 사전 집계 없이도 **수십억 행에 대한 서브초(sub-second) 쿼리**가 가능해짐

---

## 8. HTAP: 두 세계의 융합 시도

### 8.1 HTAP의 등장 배경

Gartner가 2014년에 명명한 **HTAP(Hybrid Transactional/Analytical Processing)**는 OLTP와 OLAP를 단일 시스템에서 처리하겠다는 비전이다. 동기는 명확하다:

- ETL 파이프라인의 지연 시간(보통 수 시간~하루)을 제거
- 실시간 트랜잭션 데이터에 대한 즉각적인 분석
- 데이터 아키텍처의 복잡성 감소

### 8.2 주요 아키텍처 접근법

**Dual-Format Storage**: TiDB, SingleStoreDB(구 MemSQL) 등은 **Row Store + Column Store를 동시에 유지**한다. 트랜잭션은 Row Store에서 처리하고, 백그라운드로 Column Store에 복제(replicate)하여 분석 쿼리에 제공한다.

**In-Memory Approach**: SAP HANA는 메인 메모리에 데이터를 두고, Row Store와 Column Store를 통합 관리한다. Delta Store에 신규 쓰기를 버퍼링한 뒤 주기적으로 Main Store에 병합한다.

**Lakehouse Hybrid**: 2025년 이후 Snowflake의 Hybrid Tables, Databricks의 Lakebase(내장 PostgreSQL 엔진) 등은 OLAP 플랫폼에 OLTP 기능을 추가하는 방향으로 HTAP에 접근하고 있다.

### 8.3 HTAP의 현실: 왜 아직 주류가 되지 못했는가

2026년 현재, **단일 HTAP 엔진이 전용 OLTP + 전용 OLAP 조합을 대체한 사례는 극히 드물다**. 그 이유는 근본적이다:

1. **리소스 경합(Resource Contention)**: 무거운 분석 쿼리가 트랜잭션의 지연 시간을 증가시키거나, 그 반대 상황이 발생한다. CPU, 메모리, I/O를 두 워크로드가 공유하면 양쪽 모두 성능이 저하된다.

2. **최적화 상충**: Row Store에 최적화된 인덱스 구조(B-Tree)와 Column Store에 최적화된 구조(Zone Map, Sparse Index)는 근본적으로 다르다. 하나의 시스템이 양쪽 모두에서 최적을 달성하기 어렵다.

3. **운영 복잡성**: HTAP 시스템의 장애 도메인(failure domain)이 하나이므로, 분석 워크로드의 문제가 트랜잭션 시스템에 직접 영향을 미친다.

현재 가장 현실적인 아키텍처는 **CDC(Change Data Capture) 기반의 Near-Real-Time Pipeline**이다: PostgreSQL(OLTP) → Debezium(CDC) → Kafka(Streaming) → ClickHouse(OLAP). 이 구조에서 분석 지연 시간은 수초 수준이며, 각 시스템이 독립적으로 확장·운영된다.

---

## 9. 현대 OLAP 엔진 비교: ClickHouse vs DuckDB

2025~2026년 OLAP 생태계에서 가장 주목받는 두 엔진을 비교한다.

### 9.1 ClickHouse: 분산 실시간 분석의 강자

- **아키텍처**: 분산 클러스터 기반, 각 노드가 독립적으로 쿼리를 처리
- **스토리지 엔진**: MergeTree 계열 — 데이터를 정렬된 Immutable Part로 저장하고 백그라운드에서 지속적으로 병합
- **쿼리 실행**: Vectorized Execution + 컬럼 단위 처리
- **압축**: LZ4, ZSTD 등 고압축률 코덱 + 컬럼별 최적 코덱 자동 선택
- **강점**: 실시간 데이터 수집(초당 수백만 행)과 동시 분석 쿼리 처리

### 9.2 DuckDB: 임베디드 분석의 혁신

- **아키텍처**: 프로세스 내장형(In-Process), SQLite의 OLAP 버전
- **스토리지 엔진**: 독자적 컬럼 스토어 + Parquet/CSV 직접 쿼리 지원
- **쿼리 실행**: Vectorized Push-Based Execution — 벡터를 하향식이 아닌 상향식으로 밀어 올림
- **압축**: 경량 인코딩(Dictionary, FOR, Bit-Packing) 중심 — 쿼리 중 디코딩 비용 최소화
- **강점**: 설치 불필요, Python/R 통합, 로컬 데이터 분석에서 Pandas를 대체

### 9.3 선택 기준

| 기준 | ClickHouse | DuckDB |
|------|-----------|--------|
| 데이터 규모 | TB~PB | MB~수백 GB |
| 배포 모델 | 서버/클러스터 | 임베디드/로컬 |
| 실시간 수집 | 초당 수백만 행 | 배치 중심 |
| 동시 사용자 | 수백~수천 | 단일~소수 |
| 운영 복잡도 | 높음 | 거의 없음 |

---

## 10. 핵심 비교 요약

| 구분 | OLTP | OLAP |
|------|------|------|
| **목적** | 트랜잭션 처리 (Transaction Processing) | 분석 쿼리 처리 (Analytical Processing) |
| **쿼리 패턴** | Point Read/Write, 소량 행 | Full Scan, Aggregation, 대량 행 |
| **스토리지** | Row-Oriented | Column-Oriented |
| **인덱스** | B-Tree, Hash Index | Zone Map, Sparse Index, Bloom Filter |
| **동시성 제어** | MVCC, 2PL, WAL | Append-Only, Snapshot Isolation |
| **스키마** | 정규화 (3NF+) | 비정규화 (Star/Snowflake Schema) |
| **실행 모델** | Tuple-at-a-time (Volcano) | Vectorized Batch Processing |
| **핵심 지표** | TPS, p99 Latency | Scan Throughput, QPS |
| **대표 시스템** | PostgreSQL, MySQL, Oracle | ClickHouse, DuckDB, Snowflake, Redshift |
| **데이터 신선도** | 실시간 (Real-time) | 배치~준실시간 (Batch~Near-Real-Time) |

---

## 마치며: 어떤 선택을 해야 하는가

OLTP와 OLAP는 "어느 쪽이 더 좋은가"의 문제가 아니라, **워크로드의 본질이 무엇인가**에 따라 결정되는 아키텍처적 선택이다.

현실적으로 대부분의 프로덕션 환경은 **두 시스템을 모두 운영**한다. OLTP 데이터베이스가 실시간 트랜잭션을 처리하고, CDC 파이프라인을 통해 OLAP 시스템에 데이터를 공급하는 것이 2026년 현재 가장 검증된 아키텍처이다. HTAP의 비전은 매력적이지만, 전용 시스템의 조합이 여전히 성능과 안정성 면에서 우위에 있다.

중요한 것은 각 시스템의 **내부 구조를 이해하고, 왜 그런 설계가 되었는지를 아는 것**이다. Row Store가 왜 Point Lookup에 빠른지, Column Store가 왜 집계에 압도적인지, MVCC가 왜 OLTP에서는 필수이지만 OLAP에서는 불필요한지 — 이러한 원리를 이해하면 기술 선택의 근거가 명확해진다.

---

### References

- [OLTP vs OLAP in 2026 — ClickHouse](https://clickhouse.com/resources/engineering/oltp-vs-olap)
- [Unifying OLTP and OLAP: HTAP databases — ClickHouse](https://clickhouse.com/resources/engineering/unifying-oltp-and-olap)
- [OLAP databases: what's new in 2026 — Tinybird](https://www.tinybird.co/blog/best-database-for-olap)
- [OLTP vs OLAP — AWS](https://aws.amazon.com/compare/the-difference-between-olap-and-oltp/)
- [Columnar vs Row-based Storage — DEV Community](https://dev.to/alexmercedcoder/columnar-vs-row-based-data-structures-in-oltp-and-olap-systems-20c8)
- [How MVCC databases work internally — Medium](https://kousiknath.medium.com/how-mvcc-databases-work-internally-84a27a380283)
- [HTAP Databases: A Survey — arXiv](https://arxiv.org/pdf/2404.15670)
- [In-Process Analytical Data Management with DuckDB — InfoQ](https://www.infoq.com/articles/analytical-data-management-duckdb/)
- [ClickHouse Architecture Overview — ClickHouse Docs](https://clickhouse.com/docs/academic_overview)
- [DuckDB vs ClickHouse — Bedda Blog](https://www.metatech.dev/blog/2025-04-27-duckdb-vs-clickhouse-real-time-analytics-performance-showdown)
