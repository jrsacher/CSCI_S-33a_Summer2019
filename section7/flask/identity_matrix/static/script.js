// fileSaver.js
// https: //github.com/eligrey/FileSaver.js
(function (a, b) { if ("function" == typeof define && define.amd) define([], b); else if ("undefined" != typeof exports) b(); else { b(), a.FileSaver = { exports: {} }.exports } })(this, function () { "use strict"; function b(a, b) { return "undefined" == typeof b ? b = { autoBom: !1 } : "object" != typeof b && (console.warn("Deprecated: Expected third argument to be a object"), b = { autoBom: !b }), b.autoBom && /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(a.type) ? new Blob(["\uFEFF", a], { type: a.type }) : a } function c(b, c, d) { var e = new XMLHttpRequest; e.open("GET", b), e.responseType = "blob", e.onload = function () { a(e.response, c, d) }, e.onerror = function () { console.error("could not download file") }, e.send() } function d(a) { var b = new XMLHttpRequest; b.open("HEAD", a, !1); try { b.send() } catch (a) { } return 200 <= b.status && 299 >= b.status } function e(a) { try { a.dispatchEvent(new MouseEvent("click")) } catch (c) { var b = document.createEvent("MouseEvents"); b.initMouseEvent("click", !0, !0, window, 0, 0, 0, 80, 20, !1, !1, !1, !1, 0, null), a.dispatchEvent(b) } } var f = "object" == typeof window && window.window === window ? window : "object" == typeof self && self.self === self ? self : "object" == typeof global && global.global === global ? global : void 0, a = f.saveAs || ("object" != typeof window || window !== f ? function () { } : "download" in HTMLAnchorElement.prototype ? function (b, g, h) { var i = f.URL || f.webkitURL, j = document.createElement("a"); g = g || b.name || "download", j.download = g, j.rel = "noopener", "string" == typeof b ? (j.href = b, j.origin === location.origin ? e(j) : d(j.href) ? c(b, g, h) : e(j, j.target = "_blank")) : (j.href = i.createObjectURL(b), setTimeout(function () { i.revokeObjectURL(j.href) }, 4E4), setTimeout(function () { e(j) }, 0)) } : "msSaveOrOpenBlob" in navigator ? function (f, g, h) { if (g = g || f.name || "download", "string" != typeof f) navigator.msSaveOrOpenBlob(b(f, h), g); else if (d(f)) c(f, g, h); else { var i = document.createElement("a"); i.href = f, i.target = "_blank", setTimeout(function () { e(i) }) } } : function (a, b, d, e) { if (e = e || open("", "_blank"), e && (e.document.title = e.document.body.innerText = "downloading..."), "string" == typeof a) return c(a, b, d); var g = "application/octet-stream" === a.type, h = /constructor/i.test(f.HTMLElement) || f.safari, i = /CriOS\/[\d]+/.test(navigator.userAgent); if ((i || g && h) && "object" == typeof FileReader) { var j = new FileReader; j.onloadend = function () { var a = j.result; a = i ? a : a.replace(/^data:[^;]*;/, "data:attachment/file;"), e ? e.location.href = a : location = a, e = null }, j.readAsDataURL(a) } else { var k = f.URL || f.webkitURL, l = k.createObjectURL(a); e ? e.location = l : location.href = l, e = null, setTimeout(function () { k.revokeObjectURL(l) }, 4E4) } }); f.saveAs = a.saveAs = a, "undefined" != typeof module && (module.exports = a) });


function exportTableToCSV(filename) {
    let csv = [];
    let rows = document.querySelectorAll("table tr");

    for (let i = 0; i < rows.length; i++) {
        let row = [],
            cols = rows[i].querySelectorAll("td, th");

        for (let j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);

        csv.push(row.join(","));
    }
    // Add newlines for rows
    csv = csv.join('\r\n');

    // CSV file
    let csvFile = new Blob([csv], {
        type: "text/csv"
    });

    saveAs(csvFile, filename)
}


window.onload = function () {
    // 21-step gradient from red through white to blue
    const gradient = ["#FF0000", "#FF1919", "#FF3333", "#FF4C4C", "#FF6666",
        "#FF7F7F", "#FF9999", "#FFB2B2", "#FFCCCC", "#FFE5E5", "#FFFFFF",
        "#E5E5FF", "#CCCCFF", "#B2B2FF", "#9999FF", "#7F7FFF", "#6666FF",
        "#4C4CFF", "#3232FF", "#1919FF", "#0000FF"
    ];

    // Add background color to table cells
    document.querySelectorAll('td').forEach(function (cell) {
        // Get table value, divide by 5 and round to find index
        let val = Math.round(parseFloat(cell.innerHTML) / 5);
        // Pick color based on value
        cell.style.backgroundColor = gradient[val];
        // White text for darkest backgrounds
        if (val < 4 || val > 16) {
            cell.style.color = 'whitesmoke';
        }
    });

    // Convert cell headers to UniProt link
    document.querySelectorAll('th').forEach(function (head) {
        head.innerHTML = `<a href="https://www.uniprot.org/uniprot/${head.innerHTML}" target="_blank">${head.innerHTML}</a>`;
    });
}
