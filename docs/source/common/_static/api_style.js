/* api_style.js — transforms breathe C++ API pages to match Figma design */
(function () {
  "use strict";

  function transformApiPage() {
    // Support both C++ (breathe: dl.cpp.function) and Python (autodoc: dl.py.function)
    var fnBlocks = document.querySelectorAll("dl.cpp.function, dl.cpp.type, dl.cpp.struct, dl.cpp.enum, dl.py.function, dl.py.class, dl.py.method");
    if (!fnBlocks.length) return;

    fnBlocks.forEach(function (dl) {
      var dt = dl.querySelector("dt.sig");
      var dd = dl.querySelector("dd");
      if (!dt || !dd) return;

      /* ── 1. Wrap signature in code-box ─────────────────────── */
      dt.classList.add("tt-api-sig-box");
      var headerlink = dt.querySelector("a.headerlink");
      if (headerlink) {
        var copyBtn = document.createElement("button");
        copyBtn.className = "tt-api-copy-btn";
        copyBtn.title = "Copy";
        copyBtn.innerHTML =
          '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">' +
          '<rect x="7" y="7" width="9" height="9" rx="1.5" stroke="#678583" stroke-width="1.5"/>' +
          '<path d="M13 7V5.5A1.5 1.5 0 0 0 11.5 4h-7A1.5 1.5 0 0 0 3 5.5v7A1.5 1.5 0 0 0 4.5 14H6" stroke="#678583" stroke-width="1.5" stroke-linecap="round"/>' +
          "</svg>";
        copyBtn.addEventListener("click", function () {
          var text = dt.textContent.replace(/\s+/g, " ").trim();
          navigator.clipboard && navigator.clipboard.writeText(text);
          copyBtn.innerHTML =
            '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">' +
            '<path d="M4 10l4 4 8-8" stroke="#1e86a9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
            "</svg>";
          setTimeout(function () {
            copyBtn.innerHTML =
              '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">' +
              '<rect x="7" y="7" width="9" height="9" rx="1.5" stroke="#678583" stroke-width="1.5"/>' +
              '<path d="M13 7V5.5A1.5 1.5 0 0 0 11.5 4h-7A1.5 1.5 0 0 0 3 5.5v7A1.5 1.5 0 0 0 4.5 14H6" stroke="#678583" stroke-width="1.5" stroke-linecap="round"/>' +
              "</svg>";
          }, 1500);
        });
        headerlink.replaceWith(copyBtn);
      }

      /* ── 2. Collect dd paragraphs ───────────────────────────── */
      var paragraphs = Array.from(dd.querySelectorAll(":scope > p"));
      var descPara = null;
      var returnPara = null;
      var paramPara = null;

      paragraphs.forEach(function (p) {
        var text = p.textContent.trim();
        if (text.startsWith("Return value:")) {
          returnPara = p;
        } else if (p.querySelector("table.docutils")) {
          paramPara = p;
        } else if (!descPara && text.length > 0) {
          descPara = p;
        }
      });

      if (descPara) descPara.classList.add("tt-api-description");

      /* ── 3. Parameters table → styled list ─────────────────── */
      if (paramPara) {
        var table = paramPara.querySelector("table.docutils");
        if (table) {
          var rows = table.querySelectorAll("tbody tr");
          if (rows.length) {
            var section = document.createElement("div");
            section.className = "tt-api-section";

            var heading = document.createElement("h2");
            heading.className = "tt-api-section-heading";
            heading.textContent = "Parameters";
            section.appendChild(heading);

            var list = document.createElement("div");
            list.className = "tt-api-param-list";

            rows.forEach(function (row) {
              var cells = row.querySelectorAll("td");
              if (!cells.length) return;
              var argName = (cells[0] && cells[0].textContent.trim()) || "";
              var argDesc = (cells[1] && cells[1].textContent.trim()) || "";
              var argType = (cells[2] && cells[2].textContent.trim()) || "";

              var rowDiv = document.createElement("div");
              rowDiv.className = "tt-api-param-row";

              var nameP = document.createElement("p");
              nameP.className = "tt-api-param-name";
              var nameSpan = document.createElement("span");
              nameSpan.className = "tt-param-name";
              nameSpan.textContent = argName;
              nameP.appendChild(nameSpan);
              if (argType) {
                var typeSpan = document.createElement("span");
                typeSpan.className = "tt-param-type";
                typeSpan.textContent = " (" + argType + ")";
                nameP.appendChild(typeSpan);
              }
              rowDiv.appendChild(nameP);

              if (argDesc) {
                var descP = document.createElement("p");
                descP.className = "tt-api-param-desc";
                descP.textContent = argDesc;
                rowDiv.appendChild(descP);
              }
              list.appendChild(rowDiv);
            });

            section.appendChild(list);
            dd.insertBefore(section, paramPara);
            paramPara.remove();
          }
        }
      }

      /* ── 4. Return value → styled section ──────────────────── */
      if (returnPara) {
        var returnText = returnPara.textContent.replace(/Return value:\s*/i, "").trim();

        var retSection = document.createElement("div");
        retSection.className = "tt-api-section";

        var retHeading = document.createElement("h2");
        retHeading.className = "tt-api-section-heading";
        retHeading.textContent = "Returns";
        retSection.appendChild(retHeading);

        var retList = document.createElement("div");
        retList.className = "tt-api-param-list";

        var retRow = document.createElement("div");
        retRow.className = "tt-api-param-row";

        var retTypeP = document.createElement("p");
        retTypeP.className = "tt-api-param-name";
        var retSpan = document.createElement("span");
        retSpan.className = "tt-param-name";
        retSpan.textContent = returnText;
        retTypeP.appendChild(retSpan);
        retRow.appendChild(retTypeP);
        retList.appendChild(retRow);
        retSection.appendChild(retList);

        dd.insertBefore(retSection, returnPara);
        returnPara.remove();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", transformApiPage);
  } else {
    transformApiPage();
  }
})();
