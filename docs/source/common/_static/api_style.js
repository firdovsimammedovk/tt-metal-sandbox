/* api_style.js — transforms API pages to match Figma design (node 238:7535) */
(function () {
  "use strict";

  /* ─── helpers ────────────────────────────────────────────────── */
  function copyBtn() {
    var btn = document.createElement("button");
    btn.className = "tt-api-copy-btn";
    btn.title = "Copy";
    btn.innerHTML =
      '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">' +
      '<rect x="7" y="7" width="9" height="9" rx="1.5" stroke="#678583" stroke-width="1.5"/>' +
      '<path d="M13 7V5.5A1.5 1.5 0 0 0 11.5 4h-7A1.5 1.5 0 0 0 3 5.5v7A1.5 1.5 0 0 0 4.5 14H6" stroke="#678583" stroke-width="1.5" stroke-linecap="round"/>' +
      "</svg>";
    btn.addEventListener("click", function () {
      var text = btn.closest(".tt-api-sig-box")
        ? btn.closest(".tt-api-sig-box").textContent.replace(/\s+/g, " ").trim()
        : "";
      navigator.clipboard && navigator.clipboard.writeText(text);
      btn.innerHTML =
        '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 10l4 4 8-8" stroke="#1e86a9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      setTimeout(function () {
        btn.innerHTML =
          '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">' +
          '<rect x="7" y="7" width="9" height="9" rx="1.5" stroke="#678583" stroke-width="1.5"/>' +
          '<path d="M13 7V5.5A1.5 1.5 0 0 0 11.5 4h-7A1.5 1.5 0 0 0 3 5.5v7A1.5 1.5 0 0 0 4.5 14H6" stroke="#678583" stroke-width="1.5" stroke-linecap="round"/>' +
          "</svg>";
      }, 1500);
    });
    return btn;
  }

  function makeSection(title) {
    var section = document.createElement("div");
    section.className = "tt-api-section";
    var h = document.createElement("p");
    h.className = "tt-api-section-heading";
    h.textContent = title;
    section.appendChild(h);
    return section;
  }

  function makeParamRow(nameHtml, typeText, descText) {
    var row = document.createElement("div");
    row.className = "tt-api-param-row";

    var nameP = document.createElement("p");
    nameP.className = "tt-api-param-name";
    var nameSpan = document.createElement("span");
    nameSpan.className = "tt-param-name";
    nameSpan.innerHTML = nameHtml;
    nameP.appendChild(nameSpan);
    if (typeText) {
      var typeSpan = document.createElement("span");
      typeSpan.className = "tt-param-type";
      typeSpan.textContent = " (" + typeText + ")";
      nameP.appendChild(typeSpan);
    }
    row.appendChild(nameP);

    if (descText) {
      var descP = document.createElement("p");
      descP.className = "tt-api-param-desc";
      descP.textContent = descText;
      row.appendChild(descP);
    }
    return row;
  }

  /* ─── Transform Python `dl.py.data` (TTNN-style) ─────────────── */
  function transformPyData() {
    var blocks = document.querySelectorAll("dl.py.data, dl.py.function, dl.py.class, dl.py.method");
    blocks.forEach(function (dl) {
      var dt = dl.querySelector("dt.sig");
      var dd = dl.querySelector("dd");
      if (!dt || !dd) return;

      /* 1 — Signature box */
      dt.classList.add("tt-api-sig-box");
      var headerlink = dt.querySelector("a.headerlink");
      if (headerlink) headerlink.replaceWith(copyBtn());

      /* 2 — Description: first plain <p> */
      var allP = Array.from(dd.querySelectorAll(":scope > p"));
      var descP = allP.find(function (p) {
        return !p.classList.contains("rubric") && p.textContent.trim().length > 0;
      });
      if (descP) descP.classList.add("tt-api-description");

      /* 3 — field-list (Keyword Arguments + Returns) */
      var fieldList = dd.querySelector("dl.field-list");
      if (!fieldList) return;

      var insertBefore = fieldList;

      /* Keyword Arguments */
      var kwDt = fieldList.querySelector("dt.field-odd");
      var kwDd = fieldList.querySelector("dd.field-odd");
      if (kwDt && kwDd) {
        var kwSection = makeSection("Keyword Arguments");
        var kwList = document.createElement("div");
        kwList.className = "tt-api-param-list";

        var items = kwDd.querySelectorAll("li");
        items.forEach(function (li) {
          var p = li.querySelector("p");
          if (!p) return;
          var strong = p.querySelector("strong");
          var ems = p.querySelectorAll("em");
          var name = strong ? strong.textContent : "";
          var typeText = Array.from(ems).map(function (e) { return e.textContent; }).join("").replace(/,\s*/g, ", ");
          // Description = text after " – "
          var fullText = p.textContent;
          var dashIdx = fullText.indexOf(" – ");
          var desc = dashIdx !== -1 ? fullText.slice(dashIdx + 3).trim() : "";
          kwList.appendChild(makeParamRow(name, typeText, desc));
        });

        kwSection.appendChild(kwList);
        fieldList.parentNode.insertBefore(kwSection, insertBefore);
      }

      /* Returns */
      var retDt = fieldList.querySelector("dt.field-even");
      var retDd = fieldList.querySelector("dd.field-even");
      if (retDt && retDd) {
        var retSection = makeSection("Returns");
        var retList = document.createElement("div");
        retList.className = "tt-api-param-list";

        var retText = retDd.textContent.trim();
        // "TypeName – description"
        var dashIdx2 = retText.indexOf(" – ");
        var retName = dashIdx2 !== -1 ? retText.slice(0, dashIdx2).trim() : retText;
        var retDesc = dashIdx2 !== -1 ? retText.slice(dashIdx2 + 3).trim() : "";
        retList.appendChild(makeParamRow(retName, "", retDesc));
        retSection.appendChild(retList);
        fieldList.parentNode.insertBefore(retSection, insertBefore);
      }

      /* Hide the raw field-list */
      fieldList.style.display = "none";
    });
  }

  /* ─── Transform C++ `dl.cpp.*` (tt-metalium breathe) ─────────── */
  function transformCpp() {
    var blocks = document.querySelectorAll("dl.cpp.function, dl.cpp.type, dl.cpp.struct, dl.cpp.enum");
    blocks.forEach(function (dl) {
      var dt = dl.querySelector("dt.sig");
      var dd = dl.querySelector("dd");
      if (!dt || !dd) return;

      /* Signature box */
      dt.classList.add("tt-api-sig-box");
      var headerlink = dt.querySelector("a.headerlink");
      if (headerlink) headerlink.replaceWith(copyBtn());

      /* Description */
      var paragraphs = Array.from(dd.querySelectorAll(":scope > p"));
      var descPara = null, returnPara = null;
      paragraphs.forEach(function (p) {
        var text = p.textContent.trim();
        if (text.startsWith("Return value:")) { returnPara = p; }
        else if (!descPara && text.length > 0) { descPara = p; }
      });
      if (descPara) descPara.classList.add("tt-api-description");

      /* Parameters table */
      var table = dd.querySelector("table.docutils");
      if (table) {
        var rows = table.querySelectorAll("tbody tr");
        if (rows.length) {
          var section = makeSection("Parameters");
          var list = document.createElement("div");
          list.className = "tt-api-param-list";
          rows.forEach(function (row) {
            var cells = row.querySelectorAll("td");
            var name = (cells[0] && cells[0].textContent.trim()) || "";
            var desc = (cells[1] && cells[1].textContent.trim()) || "";
            var type = (cells[2] && cells[2].textContent.trim()) || "";
            list.appendChild(makeParamRow(name, type, desc));
          });
          section.appendChild(list);
          dd.insertBefore(section, table.closest("p") || table);
          (table.closest("p") || table).remove();
        }
      }

      /* Return value */
      if (returnPara) {
        var retText = returnPara.textContent.replace(/Return value:\s*/i, "").trim();
        var retSection = makeSection("Returns");
        var retList = document.createElement("div");
        retList.className = "tt-api-param-list";
        retList.appendChild(makeParamRow(retText, "", ""));
        retSection.appendChild(retList);
        dd.insertBefore(retSection, returnPara);
        returnPara.remove();
      }
    });
  }

  function run() {
    transformPyData();
    transformCpp();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
