---
layout: fermented
title: " OLTP vs OLAP 아키텍처 해부: 리뷰"
date: 2026-04-03
categories:
  - development
tags:
  - database
  - OLTP
  - OLAP
  - architecture
description: claude-opus-4-6의 딥리서치 결과를 내가 리뷰한다면 어떨까?
pair: 2026-04-03-olap-vs-oltp-deep-dive-claude-opus-4-6
version: raw
feed: true
sitemap: true
---
최근에 면접을 보면서 OLTP와 OLAP의 차이를 질문 받는 경우가 많았습니다. 저는 단순 DB로 이해하고 질문에 답했지만, 용어에서와 같이 단순히 DB만 얘기하기보다는 정보를 처리하는 시스템 자체를 일컫는 말로써 온라인에서 실시간 처리가 중요한 서비스들(금융 거래, 쇼핑, 회원가입)을 지원하는 시스템이 OLTP입니다. OLAP는 이러한 개별 정보의 처리가 실시간성으로 중요한 경우가 아닌, 저장된 데이터를 빠르게 분석할 수 있도록 지원하는 시스템을 의미합니다. 대개 이 두 개의 기능의 목적에 따라 DB 선택이 달라지므로, DB의 종류를 나누는 말이 되기도 했습니다. 

- Online Transaction Processing
- Online Analytical Processing

데이터 자체는 동일하더라도, 저장하는 방식과 우리가 다루는 방식에 따라 우리가 얻게 되는 효과의 트레이드 오프가 존재하고, 이것을 잘 이해하는 것이 중요하다는 게 이 두 개를 공부하면서 얻게 되는 가장 큰 인사이트 같습니다. 우리가 다루게 되는 대부분의 서비스들은 OLTP위에 만들어지게 되고, 추가적으로 분석을 위한 data engineering과정에서 OLAP를 선택적으로 도입하게 된다고 이해하면 더 쉬운 설명이 될 것입니다.

---

## 1. 트랜잭션의 정의

트랜잭션(Transaction)은 데이터베이스의 상태를 변화시키는 하나의 논리적 작업 단위입니다.  트랜잭션이 시작되면, 트랜잭션이 활동 상태가 되어 commit이 발생하면 종료됩니다.  실행에 오류가 발생하면 실패하고, Rollback 연산이 수행되고 철회됩니다. 우리가 네이버스토어에 로그인하고 물건을 구입하기까지 유저, 로그, 상품, 배송 테이블 등 십 수 개의 트랜잭션을 발생시키고, 동시 접속자 수가 1000명이라면 1시간 동안 수 만개 이상의 트랜잭션이 발생합니다.

반대로, 오늘의 접속자 수를 측정하는 것은 COUNT()함수 하나로, 몇 명의 데이터 분석가 혹은 마케팅 담당자가, 하루에 한 번 혹은 주에 한 번 실행하면 재사용도 가능하고 얻을 수 있는 값입니다. 이러한 업무에서는 개별 변경이 아닌 아무리 데이터가 커지더라도 짧은 시간 안에 수행이 되는 것이 중요합니다. 이것이 분석과 서비스의 근본적인 차이입니다.

## 1.1 근본적 설계 목표의 차이

한 명 한 명의 사용자, 개별 레코드를 목표로 하는 DB는 주로 OLTP, 대량 데이터 집계(Aggregation) 쿼리의 속도가 중요하다면 OLAP입니다. 각각의 지표도 다릅니다.

| OLTP                    | OLAP                       |
| ----------------------- | -------------------------- |
| TPS(초당 트랜잭션 수)          | QPS(초당 쿼리 수)               |
| P99 latency(하위 1퍼센트 속도) | Scan Throughput (rows/sec) |
이러한 목적의 차이는 데이터를 저장하는 아키텍처의 차이를 만들게 됩니다.

---

## 2. 스토리지 레이아웃: Row Store vs Column Store

### 2.1 Row-Oriented Storage (행 기반 저장)

OLTP 시스템은 대표적으로 다음과 같은 행 중심 저장 방식을 취합니다.

```
Page 1: [Row1: id=1, name="Alice", age=30, city="Seoul"]
         [Row2: id=2, name="Bob",   age=25, city="Busan"]
         [Row3: id=3, name="Carol", age=35, city="Seoul"]
```

각각의 행이 모든 요소를 저장하고 있습니다. 마치 '백상훈'이라는 객체를 저장하고 있는 것처럼, 가장 자연스럽고 일반적인 저장 방식입니다. 5000만 명이 있더라도, 백상훈이라는 이름을 검색하고 한 사람을 찾는 것은 서울 송파구에서 찾으면 굉장히 빠르게 찾는 것처럼 빠르게 찾을 수 있습니다. 이를 Point Lookup이라 합니다.
그리고 하나의 행을 넣거나 업데이트 하는 것은 하나에만 국한해서 발생하므로 다른 데이터에 영향 없이 효율적으로 가능합니다.

그런데, 이제 평균 나이를 구하고 싶다면 문제가 발생합니다. 모든 행을 읽어야 하며, 우리가 관심 없는 정보들까지도 같이 들고 그 다음에 평균 나이를 구하게 됩니다. 이를 효율화하고 해결하는 것이 **인덱스**이지만, 근본적인 아키텍처에서 비효율적인 부분들이 발생합니다.
#### OLTP 예시들
- PostgreSQL
- MySQL
- Oracle

### 2.2 Column-Oriented Storage (열 기반 저장)

OLAP DB들이 분석에 특화될 수 있는 것이 바로 열 기반 저장이기 때문입니다. 앞에서 보여준 예시는 열 기반 저장 시스템에서는 다음과 같이 저장됩니다.

```
Column "id":   [1, 2, 3, 4, 5, ...]
Column "name": ["Alice", "Bob", "Carol", ...]
Column "age":  [30, 25, 35, ...]
Column "city": ["Seoul", "Busan", "Seoul", ...]
```

이렇게 나열되어 모여 있다는 것 이상으로, 같은 종류의 데이터들이 연속해서 저장되는 점은 그 이상의 가치를 가지고 있습니다. id는 연속된 숫자이므로 이론 상 1부터 N까지 자연수 등으로 요약이 가능하고, 나이 또한 차이 값만 저장하거나 숫자의 범위를 좁혀 저장하는 등 압축이 가능합니다. SUM, AVERAGE, COUNT 등의 함수도 다른 컬럼의 영향 없이 수행하므로 코스트를 낮추는 것 또한 가능합니다.

그런데, 앞서 말한 본질적인 차이에서 추가적으로 **CPU 벡터화(Vectorized Execution)** 라는 이점을 가지게 됩니다. 같은 종류의 데이터가 메모리에 연속 배치되어 CPU SIMD 명령어로 여러 값을 동시에 처리할 수 있습니다. SIMD 명령어 자체가 연산을 4~16배를 제공하고, 이를 각 DB vendor사가 최적화 해 사용함으로써 **수십 배**까지 성능차이로 연결합니다.
#### OLAP의 예시들
- Clickhouse
- Apache Parquet
- DuckDB
- Amazon Redshift

그러나 OLAP는 UPDATE와 INSERT에서 큰 약점을 가지고 있습니다. 하나의 행을 삽입하기 위해서는 컬럼 수 만큼 쓰기가 발생합니다. UPDATE는 로드 뿐만 아니라 안정성 측면에서도 어려운 챌린지가 됩니다. 따라서 DELETE, UPDATE 등의 규모에 따라 추가적으로 신경을 쓰는 것이 필요하고, 대규모 변경이 어렵습니다. 

etc) Clickhouse가 MergeTree엔진을 쓴다는 건 알겠지만, 다소 연결고리는 어렵네요.

---

## 3. 인덱싱 전략의 분기

### 3.1 OLTP: B-Tree와 그 변종들

OLTP 의 핵심 구조는 B-Tree(Balanced Tree)입니다. 저장된 데이터에서 Random하게 읽거나 작업들이 많은 경우에 이를 가장 효율화 하는 데이터 구조입니다.

- **O(log N) Point Lookup**: 키 값으로 특정 행을 찾는 데 트리 깊이만큼의 디스크 I/O만 필요
- **범위 스캔(Range Scan)**: 리프 노드가 정렬된 링크드 리스트로 연결되어, `WHERE price BETWEEN 100 AND 500` 같은 범위 쿼리에 효율적
- **In-place Update 지원**: 키 값이 변경되지 않으면 리프 노드의 포인터만 갱신

PostgreSQL은 B-Tree 외에도 GiST, GIN, BRIN 등 다양한 인덱스를 지원하지만, 랜덤 액세스는 B-Tree가 모두 기본이라고 할 수 있습니다. (MongoDB, Oracle, MySQL)

### 3.2 OLAP: Zone Map, Sparse Index, 그리고 Data Skipping

OLAP 시스템은 전통적인 B-Tree 대신 **대량 스캔에 최적화된 인덱스**를 사용한다.

**Zone Map (Min/Max Index)**: 각 데이터 블록(보통 수천~수만 행)의 최솟값과 최댓값을 메타데이터로 저장한다. `WHERE date > '2025-01-01'` 쿼리가 들어오면, 최댓값이 2024-12-31인 블록은 아예 읽지 않고 건너뛴다(Data Skipping). 

**Sparse Index**: 일부 OLAP 시스템(예: ClickHouse)은 모든 row가 아니라 일정 간격의 키 값만 인덱싱하여 메모리 사용량을 최소화한다. 이를 통해 대규모 데이터셋에서도 인덱스를 메모리에 유지할 수 있다.

**Bloom Filter (Optional)**:  특정 값의 존재 여부를 확률적으로 판단하여 불필요한 데이터 블록 접근을 줄인다. 일부 시스템에서 선택적으로 사용되는 보조 최적화 기법이다.

---

## 4. 동시성 제어(Concurrency Control)의 차이

### 4.1 OLTP: MVCC와 ACID의 세계

OLTP 시스템은 수천 개의 동시 트랜잭션이 같은 데이터를 읽고 쓰는 환경에서 **데이터 정합성(Data Consistency)**을 보장해야 한다. 이를 위한 핵심 메커니즘이 **MVCC(Multi-Version Concurrency Control)**이다.

MVCC의 핵심 원칙: **"읽기는 쓰기를 차단하지 않고, 쓰기는 읽기를 차단하지 않는다."**

**PostgreSQL의 구현 방식**:
- 행을 업데이트하면 기존 행을 삭제 표시하고 새 버전(tuple)을 생성한다
- 각 행의 헤더에 `xmin`(생성 트랜잭션 ID)과 `xmax`(삭제 트랜잭션 ID)를 기록한다
- 트랜잭션은 자신의 Snapshot 시점에서 보이는 행 버전만 읽는다
- VACUUM 프로세스가 더 이상 어떤 트랜잭션에서도 보이지 않는 죽은 튜플(dead tuple)을 정리한다

**MySQL InnoDB의 구현 방식**:
- Undo Log에 이전 버전을 저장하고, 현재 행에서 undo 체인을 따라가며 과거 버전을 재구성한다
- Clustered Index(B-Tree)에 최신 버전을 저장하고, 이전 버전은 undo segment에 유지한다

**Write-Ahead Logging (WAL)**은 ACID의 Durability를 보장하는 핵심 장치다. 모든 변경 사항은 데이터 페이지에 반영되기 전에 WAL에 먼저 기록된다. 시스템 장애 시 WAL을 재생(replay)하여 커밋된 트랜잭션을 복구한다.

### 4.2 OLAP: Append-Only와 Batch Isolation

OLAP 시스템은 동시성 제어에 대한 요구사항이 근본적으로 다르다:

- 쓰기 패턴이 **Bulk Insert/Append 위주**이다. 개별 행의 UPDATE/DELETE는 드물거나 아예 지원하지 않는다.
- 읽기는 거의 항상 **Historical Data에 대한 Full Scan**이다.
- 따라서 행 수준의 Lock이나 MVCC 같은 복잡한 메커니즘이 불필요하다.

ClickHouse의 MergeTree 엔진이 이를 극단적으로 보여준다:
1. 데이터는 **Immutable Part** 단위로 디스크에 기록된다
2. 백그라운드 머지 프로세스가 작은 Part들을 큰 Part로 병합한다
3. UPDATE/DELETE는 "mutation"이라는 비동기 재작성(rewrite) 방식으로 처리된다 — 기존 Part를 읽고, 변경을 적용한 뒤, 새 Part를 기록한다
4. 읽기 쿼리는 현재 시점의 Part 목록에 대한 Snapshot을 잡고 실행한다

이 Append-Only 설계 덕분에 Lock 경합이 거의 없고, 쓰기와 읽기가 서로를 방해하지 않는다.

---

## 5. 쿼리 실행 엔진의 차이

### 5.1 OLTP: Volcano/Iterator 모델

전통적인 OLTP 데이터베이스는 **Volcano 모델(Iterator 모델)**을 사용한다. 쿼리 플랜의 각 연산자가 `next()` 함수를 호출하며 **한 번에 한 행(tuple-at-a-time)**씩 상위 연산자로 전달한다.

```
Project (name, age)
  └── Filter (age > 30)
        └── Scan (users)
```

이 모델은 구현이 단순하고, 한 행만 반환하는 OLTP 쿼리에서는 오버헤드가 미미하다. 하지만 수백만 행을 처리하는 분석 쿼리에서는 함수 호출 오버헤드가 행 수만큼 누적되어 심각한 병목이 된다.

### 5.2 OLAP: Vectorized Execution과 Batch Processing

현대 OLAP 엔진(ClickHouse, DuckDB, Velox 등)은 **Vectorized Execution** 모델을 채택한다. 한 번에 한 행이 아니라, **수천 개의 값으로 구성된 벡터(batch)**를 단위로 처리한다.

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

- **함수 호출 오버헤드 감소**: `next()`를 100만 번 호출하는 대신, 1,024행짜리 배치를 ~1,000번 처리
- **CPU 캐시 효율**: 같은 타입의 데이터가 연속 메모리에 배치되어 L1/L2 캐시 히트율 극대화
- **SIMD 활용**: AVX2/AVX-512 등의 명령어로 한 CPU 사이클에 4~16개 값을 동시 비교/연산
- **브랜치 프리딕션 최적화**: 조건 평가를 비트마스크로 변환하여 CPU 분기 예측 실패를 회피

DuckDB는 이를 **Vectorized Push-Based Execution**이라 부른다. 전통적인 Volcano 모델이 상위 연산자가 하위에서 "당기는(pull)" 방식이라면, DuckDB는 벡터를 하위에서 상위로 "밀어 올리는(push)" 방식으로 파이프라인 효율을 극대화한다.

---

## 6. 스키마 설계 철학

### 6.1 OLTP: 정규화(Normalization)

OLTP 스키마는 **제3정규형(3NF)** 이상으로 정규화하는 것이 원칙이다:

- 데이터 중복을 제거하여 UPDATE Anomaly를 방지
- 하나의 사실(fact)은 하나의 위치에만 저장
- 참조 무결성을 외래 키(Foreign Key)로 강제

```sql
-- 정규화된 OLTP 스키마
CREATE TABLE customers (id INT PK, name VARCHAR, address_id INT FK);
CREATE TABLE addresses (id INT PK, city VARCHAR, street VARCHAR);
CREATE TABLE orders (id INT PK, customer_id INT FK, product_id INT FK, qty INT);
CREATE TABLE products (id INT PK, name VARCHAR, price DECIMAL);
```

이 설계는 트랜잭션의 정합성에 이상적이지만, "지난 분기 서울 고객의 제품별 매출 합계"를 구하려면 4개 테이블의 JOIN이 필요해진다.

### 6.2 OLAP: 비정규화와 Star/Snowflake Schema

OLAP 스키마는 **분석 쿼리의 효율성**을 위해 의도적으로 비정규화한다.

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

JOIN의 깊이가 항상 1단계(Fact → Dimension)이고, Fact Table의 넓은 스캔에 최적화된 구조이다. 현대 OLAP 엔진은 아예 **Wide Denormalized Table** 하나로 모든 데이터를 펼치는 경우도 많다.

---

## 7. 전통적 OLAP의 진화: MOLAP → ROLAP → 현대 OLAP

### 7.1 MOLAP (Multidimensional OLAP)

초기 OLAP 시스템은 데이터를 **다차원 큐브(Multidimensional Cube)**로 사전 집계하여 저장했다. Microsoft Analysis Services(SSAS), IBM Cognos 등이 대표적이다.

- 모든 차원 조합에 대한 집계값을 미리 계산하여 큐브에 저장
- 쿼리 시 미리 계산된 값을 즉시 반환하므로 응답 속도가 극히 빠름
- 그러나 차원의 수가 늘어나면 큐브의 크기가 기하급수적으로 증가하는 **"차원의 저주(Curse of Dimensionality)"** 문제
- 데이터 갱신 시 큐브 전체를 재구축해야 하는 경우가 많아 실시간성이 떨어짐

### 7.2 ROLAP (Relational OLAP)

ROLAP은 큐브 대신 **관계형 데이터베이스 위에서 SQL로 분석 쿼리**를 실행하는 방식이다.

- 사전 집계 없이 원본 데이터에 직접 쿼리
- MOLAP 대비 확장성이 우수하지만, 대규모 JOIN이 필요해 성능이 느림
- Materialized View를 통한 부분적 사전 집계로 성능을 보완

### 7.3 현대 OLAP: 컬럼 스토어 + 벡터화 실행

ClickHouse, DuckDB, Apache Druid, StarRocks 등 현대 OLAP 엔진은 MOLAP의 사전 계산 전략과 ROLAP의 SQL 유연성을 모두 뛰어넘었다:

- **컬럼 스토어 + 고효율 압축**으로 원본 데이터 스캔 자체가 충분히 빠름
- **벡터화 실행 엔진**으로 CPU 효율을 극대화
- **적응형 인덱싱(Adaptive Indexing)**으로 쿼리 패턴에 맞는 최적화를 자동 수행
- 큐브 사전 집계 없이도 **수십억 행에 대한 서브초(sub-second) 쿼리**가 가능

---

## 8. HTAP: 두 세계의 융합 시도

### 8.1 HTAP의 등장 배경

Gartner가 2014년에 명명한 **HTAP(Hybrid Transactional/Analytical Processing)**는 OLTP와 OLAP를 단일 시스템에서 처리하겠다는 비전이다:

- ETL 파이프라인의 지연 시간(보통 수 시간~하루)을 제거
- 실시간 트랜잭션 데이터에 대한 즉각적인 분석
- 데이터 아키텍처의 복잡성 감소

### 8.2 주요 아키텍처 접근법

**Dual-Format Storage**: TiDB, SingleStoreDB(구 MemSQL) 등은 **Row Store + Column Store를 동시에 유지**한다. 트랜잭션은 Row Store에서 처리하고, 백그라운드로 Column Store에 복제하여 분석 쿼리에 제공한다.

**In-Memory Approach**: SAP HANA는 메인 메모리에 데이터를 두고, Row Store와 Column Store를 통합 관리한다. Delta Store에 신규 쓰기를 버퍼링한 뒤 주기적으로 Main Store에 병합한다.

**Lakehouse Hybrid**: Snowflake의 Hybrid Tables, Databricks의 Lakebase(Neon 기반 PostgreSQL 엔진) 등은 OLAP 플랫폼에 OLTP 기능을 추가하는 방향으로 HTAP에 접근하고 있다.

### 8.3 HTAP의 현실: 왜 아직 주류가 되지 못했는가

**단일 HTAP 엔진이 전용 OLTP + 전용 OLAP 조합을 대체한 사례는 극히 드물다.** 그 이유는 근본적이다:

1. **리소스 경합(Resource Contention)**: 무거운 분석 쿼리가 트랜잭션의 지연 시간을 증가시키거나, 그 반대 상황이 발생한다. CPU, 메모리, I/O를 두 워크로드가 공유하면 양쪽 모두 성능이 저하된다.

2. **최적화 상충**: Row Store에 최적화된 인덱스 구조(B-Tree)와 Column Store에 최적화된 구조(Zone Map, Sparse Index)는 근본적으로 다르다. 하나의 시스템이 양쪽 모두에서 최적을 달성하기 어렵다.

3. **운영 복잡성**: HTAP 시스템의 장애 도메인이 하나이므로, 분석 워크로드의 문제가 트랜잭션 시스템에 직접 영향을 미친다.

현재 가장 현실적인 아키텍처는 **CDC(Change Data Capture) 기반의 Near-Real-Time Pipeline**이다:

```
PostgreSQL(OLTP) → Debezium(CDC) → Kafka(Streaming) → ClickHouse(OLAP)
```

이 구조에서 분석 지연 시간은 수초 수준이며, 각 시스템이 독립적으로 확장·운영된다.

---

## 9. 현대 OLAP 엔진 비교: ClickHouse vs DuckDB

### 9.1 ClickHouse: 분산 실시간 분석의 강자

- **아키텍처**: 분산 클러스터 기반, 각 노드가 독립적으로 쿼리를 처리
- **스토리지 엔진**: MergeTree 계열 — 정렬된 Immutable Part로 저장하고 백그라운드에서 지속 병합
- **쿼리 실행**: Vectorized Execution + 컬럼 단위 처리
- **압축**: LZ4, ZSTD 등 + 컬럼별 최적 코덱 자동 선택
- **강점**: 실시간 데이터 수집(초당 수백만 행)과 동시 분석 쿼리 처리

### 9.2 DuckDB: 임베디드 분석의 혁신

- **아키텍처**: 프로세스 내장형(In-Process), SQLite의 OLAP 버전
- **스토리지 엔진**: 독자적 컬럼 스토어 + Parquet/CSV 직접 쿼리 지원
- **쿼리 실행**: Vectorized Push-Based Execution
- **압축**: 경량 인코딩(Dictionary, FOR, Bit-Packing) 중심 — 디코딩 비용 최소화
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
| **목적** | 트랜잭션 처리 | 분석 쿼리 처리 |
| **쿼리 패턴** | Point Read/Write, 소량 행 | Full Scan, Aggregation, 대량 행 |
| **스토리지** | Row-Oriented | Column-Oriented |
| **인덱스** | B-Tree, Hash Index | Zone Map, Sparse Index, Bloom Filter |
| **동시성 제어** | MVCC, 2PL, WAL | Append-Only, Snapshot Isolation |
| **스키마** | 정규화 (3NF+) | 비정규화 (Star/Snowflake Schema) |
| **실행 모델** | Tuple-at-a-time (Volcano) | Vectorized Batch Processing |
| **핵심 지표** | TPS, p99 Latency | Scan Throughput, QPS |
| **대표 시스템** | PostgreSQL, MySQL, Oracle | ClickHouse, DuckDB, Snowflake, Redshift |
| **데이터 신선도** | 실시간 | 배치~준실시간 |

---

## 어떤 선택을 해야 하는가

OLTP와 OLAP는 "어느 쪽이 더 좋은가"의 문제가 아니다. **워크로드의 본질이 무엇인가**에 따라 결정되는 아키텍처적 선택이다.

대부분의 프로덕션 환경은 두 시스템을 모두 운영한다. OLTP 데이터베이스가 실시간 트랜잭션을 처리하고, CDC 파이프라인을 통해 OLAP 시스템에 데이터를 공급하는 것이 가장 검증된 아키텍처이다. HTAP의 비전은 매력적이지만, 전용 시스템의 조합이 여전히 성능과 안정성 면에서 우위에 있다.

중요한 것은 각 시스템의 **내부 구조를 이해하고, 왜 그런 설계가 되었는지를 아는 것**이다. Row Store가 왜 Point Lookup에 빠른지, Column Store가 왜 집계에 압도적인지, MVCC가 왜 OLTP에서는 필수이지만 OLAP에서는 불필요한지 — 이 원리를 이해하면 기술 선택의 근거가 명확해진다.

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
- [Databricks Lakebase — Databricks Docs](https://www.databricks.com/product/lakebase)
