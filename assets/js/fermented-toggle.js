document.addEventListener("DOMContentLoaded", function () {
  var tablist = document.querySelector(".fermented__tabs");
  if (!tablist) return;

  var tabs = tablist.querySelectorAll("[role=tab]");
  var panels = document.querySelectorAll(".fermented__panel");
  var container = document.querySelector(".fermented__panels");

  function activate(tab) {
    tabs.forEach(function (t) {
      t.setAttribute("aria-selected", "false");
      t.setAttribute("tabindex", "-1");
      t.classList.remove("fermented__tab--active");
    });
    tab.setAttribute("aria-selected", "true");
    tab.setAttribute("tabindex", "0");
    tab.classList.add("fermented__tab--active");

    var mode = tab.getAttribute("data-mode");

    if (mode === "compare") {
      container.setAttribute("data-view", "compare");
      panels.forEach(function (p) {
        p.classList.remove("fermented__panel--hidden");
      });
    } else {
      container.setAttribute("data-view", "single");
      var target = tab.getAttribute("aria-controls");
      panels.forEach(function (p) {
        if (p.id === target) {
          p.classList.remove("fermented__panel--hidden");
        } else {
          p.classList.add("fermented__panel--hidden");
        }
      });
    }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { activate(tab); });
    tab.addEventListener("keydown", function (e) {
      var idx = Array.prototype.indexOf.call(tabs, tab);
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        e.preventDefault();
        var next = e.key === "ArrowRight" ? (idx + 1) % tabs.length : (idx - 1 + tabs.length) % tabs.length;
        tabs[next].focus();
        activate(tabs[next]);
      }
    });
  });
});
