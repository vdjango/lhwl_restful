/*
 UEditor Mini??
 version: 1.2.2
 build: Fri Feb 10 2017 15:00:06 GMT+0800 (CST)
*/
var $jscomp = { scope: {}, findInternal: function(g, B, w) { g instanceof String && (g = String(g)); for (var x = g.length, m = 0; m < x; m++) { var E = g[m]; if (B.call(w, E, m, g)) return { i: m, v: E } } return { i: -1, v: void 0 } } };
$jscomp.defineProperty = "function" == typeof Object.defineProperties ? Object.defineProperty : function(g, B, w) { if (w.get || w.set) throw new TypeError("ES3 does not support getters and setters.");
    g != Array.prototype && g != Object.prototype && (g[B] = w.value) };
$jscomp.getGlobal = function(g) { return "undefined" != typeof window && window === g ? g : "undefined" != typeof global && null != global ? global : g };
$jscomp.global = $jscomp.getGlobal(this);
$jscomp.polyfill = function(g, B, w, x) { if (B) { w = $jscomp.global;
        g = g.split("."); for (x = 0; x < g.length - 1; x++) { var m = g[x];
            m in w || (w[m] = {});
            w = w[m] } g = g[g.length - 1];
        x = w[g];
        B = B(x);
        B != x && null != B && $jscomp.defineProperty(w, g, { configurable: !0, writable: !0, value: B }) } };
$jscomp.polyfill("Array.prototype.find", function(g) { return g ? g : function(g, w) { return $jscomp.findInternal(this, g, w).v } }, "es6-impl", "es3");
(function(g) {
    function B(a, b, d) { var c;
        b = b.toLowerCase(); return (c = a.__allListeners || d && (a.__allListeners = {})) && (c[b] || d && (c[b] = [])) }

    function w(a, b, d, c, f, h) { c = c && a[b]; var e; for (!c && (c = a[d]); !c && (e = (e || a).parentNode);) { if ("BODY" == e.tagName || h && !h(e)) return null;
            c = e[d] } return c && f && !f(c) ? w(c, b, d, !1, f) : c } UMEDITOR_CONFIG = window.UMEDITOR_CONFIG || {};
    window.UM = { plugins: {}, commands: {}, I18N: {}, version: "1.2.2" };
    var x = UM.dom = {},
        m = UM.browser = function() {
            var a = navigator.userAgent.toLowerCase(),
                b = window.opera,
                d = {
                    ie: /(msie\s|trident.*rv:)([\w.]+)/.test(a),
                    opera: !!b && b.version,
                    webkit: -1 < a.indexOf(" applewebkit/"),
                    mac: -1 < a.indexOf("macintosh"),
                    quirks: "BackCompat" == document.compatMode
                };
            d.gecko = "Gecko" == navigator.product && !d.webkit && !d.opera && !d.ie;
            var c = 0;
            if (d.ie) {
                var c = a.match(/(?:msie\s([\w.]+))/),
                    f = a.match(/(?:trident.*rv:([\w.]+))/),
                    c = c && f && c[1] && f[1] ? Math.max(1 * c[1], 1 * f[1]) : c && c[1] ? 1 * c[1] : f && f[1] ? 1 * f[1] : 0;
                d.ie11Compat = 11 == document.documentMode;
                d.ie9Compat = 9 == document.documentMode;
                d.ie8 = !!document.documentMode;
                d.ie8Compat = 8 == document.documentMode;
                d.ie7Compat = 7 == c && !document.documentMode || 7 == document.documentMode;
                d.ie6Compat = 7 > c || d.quirks;
                d.ie9above = 8 < c;
                d.ie9below = 9 > c
            }
            d.gecko && (f = a.match(/rv:([\d\.]+)/)) && (f = f[1].split("."), c = 1E4 * f[0] + 100 * (f[1] || 0) + 1 * (f[2] || 0));
            /chrome\/(\d+\.\d)/i.test(a) && (d.chrome = +RegExp.$1);
            /(\d+\.\d)?(?:\.\d)?\s+safari\/?(\d+\.\d+)?/i.test(a) && !/chrome/i.test(a) && (d.safari = +(RegExp.$1 || RegExp.$2));
            d.opera && (c = parseFloat(b.version()));
            d.webkit && (c = parseFloat(a.match(/ applewebkit\/(\d+)/)[1]));
            d.version = c;
            d.isCompatible = !d.mobile && (d.ie && 6 <= c || d.gecko && 10801 <= c || d.opera && 9.5 <= c || d.air && 1 <= c || d.webkit && 522 <= c || !1);
            return d
        }(),
        E = m.ie,
        n = UM.utils = {
            each: function(a, b, d) { if (null != a)
                    if (a.length === +a.length)
                        for (var c = 0, f = a.length; c < f; c++) { if (!1 === b.call(d, a[c], c, a)) return !1 } else
                            for (c in a)
                                if (a.hasOwnProperty(c) && !1 === b.call(d, a[c], c, a)) return !1 },
            makeInstance: function(a) { var b = new Function;
                b.prototype = a;
                a = new b;
                b.prototype = null; return a },
            extend: function(a, b, d) { if (b)
                    for (var c in b) d && a.hasOwnProperty(c) || (a[c] = b[c]); return a },
            extend2: function(a) { for (var b = arguments, d = 1; d < b.length; d++) { var c = b[d],
                        f; for (f in c) a.hasOwnProperty(f) || (a[f] = c[f]) } return a },
            inherits: function(a, b) { var d = a.prototype,
                    c = n.makeInstance(b.prototype);
                n.extend(c, d, !0);
                a.prototype = c; return c.constructor = a },
            bind: function(a, b) { return function() { return a.apply(b, arguments) } },
            defer: function(a, b, d) { var c; return function() { d && clearTimeout(c);
                    c = setTimeout(a, b) } },
            indexOf: function(a, b, d) {
                var c = -1;
                d = this.isNumber(d) ? d : 0;
                this.each(a, function(a, h) {
                    if (h >= d && a === b) return c =
                        h, !1
                });
                return c
            },
            removeItem: function(a, b) { for (var d = 0, c = a.length; d < c; d++) a[d] === b && (a.splice(d, 1), d--) },
            trim: function(a) { return a.replace(/(^[ \t\n\r]+)|([ \t\n\r]+$)/g, "") },
            listToMap: function(a) { if (!a) return {};
                a = n.isArray(a) ? a : a.split(","); for (var b = 0, d, c = {}; d = a[b++];) c[d.toUpperCase()] = c[d] = 1; return c },
            unhtml: function(a, b) { return a ? a.replace(b || /[&<">'](?:(amp|lt|quot|gt|#39|nbsp);)?/g, function(a, b) { return b ? a : { "<": "&lt;", "&": "&amp;", '"': "&quot;", ">": "&gt;", "'": "&#39;" }[a] }) : "" },
            html: function(a) {
                return a ?
                    a.replace(/&((g|l|quo)t|amp|#39);/g, function(a) { return { "&lt;": "<", "&amp;": "&", "&quot;": '"', "&gt;": ">", "&#39;": "'" }[a] }) : ""
            },
            cssStyleToDomStyle: function() { var a = document.createElement("div").style,
                    b = { "float": void 0 != a.cssFloat ? "cssFloat" : void 0 != a.styleFloat ? "styleFloat" : "float" }; return function(a) { return b[a] || (b[a] = a.toLowerCase().replace(/-./g, function(a) { return a.charAt(1).toUpperCase() })) } }(),
            loadFile: function() {
                function a(a, c) { try { for (var d = 0, h; h = b[d++];)
                            if (h.doc === a && h.url == (c.src || c.href)) return h } catch (e) { return null } }
                var b = [];
                return function(d, c, f) {
                    var h = a(d, c);
                    if (h) h.ready ? f && f() : h.funs.push(f);
                    else if (b.push({ doc: d, url: c.src || c.href, funs: [f] }), !d.body) { f = []; for (var e in c) "tag" != e && f.push(e + '="' + c[e] + '"');
                        d.write("<" + c.tag + " " + f.join(" ") + " ></" + c.tag + ">") } else if (!c.id || !d.getElementById(c.id)) {
                        var l = d.createElement(c.tag);
                        delete c.tag;
                        for (e in c) l.setAttribute(e, c[e]);
                        l.onload = l.onreadystatechange = function() {
                            if (!this.readyState || /loaded|complete/.test(this.readyState)) {
                                h = a(d, c);
                                if (0 < h.funs.length) {
                                    h.ready =
                                        1;
                                    for (var b; b = h.funs.pop();) b()
                                }
                                l.onload = l.onreadystatechange = null
                            }
                        };
                        l.onerror = function() { throw Error("The load " + (c.href || c.src) + " fails,check the url settings of file umeditor.config.js "); };
                        d.getElementsByTagName("head")[0].appendChild(l)
                    }
                }
            }(),
            isEmptyObject: function(a) { if (null == a) return !0; if (this.isArray(a) || this.isString(a)) return 0 === a.length; for (var b in a)
                    if (a.hasOwnProperty(b)) return !1; return !0 },
            fixColor: function(a, b) {
                if (/color/i.test(a) && /rgba?/.test(b)) {
                    var d = b.split(",");
                    if (3 < d.length) return "";
                    b = "#";
                    for (var c = 0, f; f = d[c++];) f = parseInt(f.replace(/[^\d]/gi, ""), 10).toString(16), b += 1 == f.length ? "0" + f : f;
                    b = b.toUpperCase()
                }
                return b
            },
            clone: function(a, b) { var d;
                b = b || {}; for (var c in a) a.hasOwnProperty(c) && (d = a[c], "object" == typeof d ? (b[c] = n.isArray(d) ? [] : {}, n.clone(a[c], b[c])) : b[c] = d); return b },
            transUnitToPx: function(a) {
                if (!/(pt|cm)/.test(a)) return a;
                var b;
                a.replace(/([\d.]+)(\w+)/, function(d, c, f) { a = c;
                    b = f });
                switch (b) {
                    case "cm":
                        a = 25 * parseFloat(a); break;
                    case "pt":
                        a = Math.round(96 * parseFloat(a) / 72) }
                return a +
                    (a ? "px" : "")
            },
            cssRule: m.ie && 11 != m.version ? function(a, b, d) { var c;
                d = d || document;
                c = d.indexList ? d.indexList : d.indexList = {}; var f; if (c[a]) f = d.styleSheets[c[a]];
                else { if (void 0 === b) return "";
                    f = d.createStyleSheet("", d = d.styleSheets.length);
                    c[a] = d } if (void 0 === b) return f.cssText;
                f.cssText = b || "" } : function(a, b, d) {
                d = d || document;
                var c = d.getElementsByTagName("head")[0],
                    f;
                if (!(f = d.getElementById(a))) { if (void 0 === b) return "";
                    f = d.createElement("style");
                    f.id = a;
                    c.appendChild(f) }
                if (void 0 === b) return f.innerHTML;
                "" !== b ? f.innerHTML =
                    b : c.removeChild(f)
            },
            render: function(a, b) { return etpl.compile(a)(b) }
        };
    n.each("String Function Array Number RegExp Object".split(" "), function(a) { UM.utils["is" + a] = function(b) { return Object.prototype.toString.apply(b) == "[object " + a + "]" } });
    var I = UM.EventBase = function() {};
    I.prototype = {
        addListener: function(a, b) { a = n.trim(a).split(" "); for (var d = 0, c; c = a[d++];) B(this, c, !0).push(b) },
        removeListener: function(a, b) { a = n.trim(a).split(" "); for (var d = 0, c; c = a[d++];) n.removeItem(B(this, c) || [], b) },
        fireEvent: function() {
            for (var a =
                    arguments[0], a = n.trim(a).split(" "), b = 0, d; d = a[b++];) { var c = B(this, d),
                    f, h, e; if (c)
                    for (e = c.length; e--;)
                        if (c[e]) { h = c[e].apply(this, arguments); if (!0 === h) return h;
                            void 0 !== h && (f = h) }
                if (h = this["on" + d.toLowerCase()]) f = h.apply(this, arguments) }
            return f
        }
    };
    var p = x.dtd = function() {
            function a(a) { for (var b in a) a[b.toUpperCase()] = a[b]; return a }
            var b = n.extend2,
                d = a({ isindex: 1, fieldset: 1 }),
                c = a({ input: 1, button: 1, select: 1, textarea: 1, label: 1 }),
                f = b(a({ a: 1 }), c),
                h = b({ iframe: 1 }, f),
                e = a({
                    hr: 1,
                    ul: 1,
                    menu: 1,
                    div: 1,
                    blockquote: 1,
                    noscript: 1,
                    table: 1,
                    center: 1,
                    address: 1,
                    dir: 1,
                    pre: 1,
                    h5: 1,
                    dl: 1,
                    h4: 1,
                    noframes: 1,
                    h6: 1,
                    ol: 1,
                    h1: 1,
                    h3: 1,
                    h2: 1
                }),
                l = a({ ins: 1, del: 1, script: 1, style: 1 }),
                t = b(a({ b: 1, acronym: 1, bdo: 1, "var": 1, "#": 1, abbr: 1, code: 1, br: 1, i: 1, cite: 1, kbd: 1, u: 1, strike: 1, s: 1, tt: 1, strong: 1, q: 1, samp: 1, em: 1, dfn: 1, span: 1 }), l),
                v = b(a({ sub: 1, img: 1, embed: 1, object: 1, sup: 1, basefont: 1, map: 1, applet: 1, font: 1, big: 1, small: 1 }), t),
                r = b(a({ p: 1 }), v),
                c = b(a({ iframe: 1 }), v, c),
                v = a({
                    img: 1,
                    embed: 1,
                    noscript: 1,
                    br: 1,
                    kbd: 1,
                    center: 1,
                    button: 1,
                    basefont: 1,
                    h5: 1,
                    h4: 1,
                    samp: 1,
                    h6: 1,
                    ol: 1,
                    h1: 1,
                    h3: 1,
                    h2: 1,
                    form: 1,
                    font: 1,
                    "#": 1,
                    select: 1,
                    menu: 1,
                    ins: 1,
                    abbr: 1,
                    label: 1,
                    code: 1,
                    table: 1,
                    script: 1,
                    cite: 1,
                    input: 1,
                    iframe: 1,
                    strong: 1,
                    textarea: 1,
                    noframes: 1,
                    big: 1,
                    small: 1,
                    span: 1,
                    hr: 1,
                    sub: 1,
                    bdo: 1,
                    "var": 1,
                    div: 1,
                    object: 1,
                    sup: 1,
                    strike: 1,
                    dir: 1,
                    map: 1,
                    dl: 1,
                    applet: 1,
                    del: 1,
                    isindex: 1,
                    fieldset: 1,
                    ul: 1,
                    b: 1,
                    acronym: 1,
                    a: 1,
                    blockquote: 1,
                    i: 1,
                    u: 1,
                    s: 1,
                    tt: 1,
                    address: 1,
                    q: 1,
                    pre: 1,
                    p: 1,
                    em: 1,
                    dfn: 1
                }),
                q = b(a({ a: 0 }), c),
                y = a({ tr: 1 }),
                g = a({ "#": 1 }),
                k = b(a({ param: 1 }), v),
                u = b(a({ form: 1 }), d, h, e, r),
                m = a({ li: 1, ol: 1, ul: 1 }),
                p = a({ style: 1, script: 1 }),
                C = a({
                    base: 1,
                    link: 1,
                    meta: 1,
                    title: 1
                }),
                p = b(C, p),
                F = a({ head: 1, body: 1 }),
                z = a({ html: 1 }),
                D = a({ address: 1, blockquote: 1, center: 1, dir: 1, div: 1, dl: 1, fieldset: 1, form: 1, h1: 1, h2: 1, h3: 1, h4: 1, h5: 1, h6: 1, hr: 1, isindex: 1, menu: 1, noframes: 1, ol: 1, p: 1, pre: 1, table: 1, ul: 1 }),
                w = a({ area: 1, base: 1, basefont: 1, br: 1, col: 1, command: 1, dialog: 1, embed: 1, hr: 1, img: 1, input: 1, isindex: 1, keygen: 1, link: 1, meta: 1, param: 1, source: 1, track: 1, wbr: 1 });
            return a({
                $nonBodyContent: b(z, F, C),
                $block: D,
                $inline: q,
                $inlineWithA: b(a({ a: 1 }), q),
                $body: b(a({ script: 1, style: 1 }), D),
                $cdata: a({
                    script: 1,
                    style: 1
                }),
                $empty: w,
                $nonChild: a({ iframe: 1, textarea: 1 }),
                $listItem: a({ dd: 1, dt: 1, li: 1 }),
                $list: a({ ul: 1, ol: 1, dl: 1 }),
                $isNotEmpty: a({ table: 1, ul: 1, ol: 1, dl: 1, iframe: 1, area: 1, base: 1, col: 1, hr: 1, img: 1, embed: 1, input: 1, link: 1, meta: 1, param: 1, h1: 1, h2: 1, h3: 1, h4: 1, h5: 1, h6: 1 }),
                $removeEmpty: a({ a: 1, abbr: 1, acronym: 1, address: 1, b: 1, bdo: 1, big: 1, cite: 1, code: 1, del: 1, dfn: 1, em: 1, font: 1, i: 1, ins: 1, label: 1, kbd: 1, q: 1, s: 1, samp: 1, small: 1, span: 1, strike: 1, strong: 1, sub: 1, sup: 1, tt: 1, u: 1, "var": 1 }),
                $removeEmptyBlock: a({ p: 1, div: 1 }),
                $tableContent: a({
                    caption: 1,
                    col: 1,
                    colgroup: 1,
                    tbody: 1,
                    td: 1,
                    tfoot: 1,
                    th: 1,
                    thead: 1,
                    tr: 1,
                    table: 1
                }),
                $notTransContent: a({ pre: 1, script: 1, style: 1, textarea: 1 }),
                html: F,
                head: p,
                style: g,
                script: g,
                body: u,
                base: {},
                link: {},
                meta: {},
                title: g,
                col: {},
                tr: a({ td: 1, th: 1 }),
                img: {},
                embed: {},
                colgroup: a({ thead: 1, col: 1, tbody: 1, tr: 1, tfoot: 1 }),
                noscript: u,
                td: u,
                br: {},
                th: u,
                center: u,
                kbd: q,
                button: b(r, e),
                basefont: {},
                h5: q,
                h4: q,
                samp: q,
                h6: q,
                ol: m,
                h1: q,
                h3: q,
                option: g,
                h2: q,
                form: b(d, h, e, r),
                select: a({ optgroup: 1, option: 1 }),
                font: q,
                ins: q,
                menu: m,
                abbr: q,
                label: q,
                table: a({
                    thead: 1,
                    col: 1,
                    tbody: 1,
                    tr: 1,
                    colgroup: 1,
                    caption: 1,
                    tfoot: 1
                }),
                code: q,
                tfoot: y,
                cite: q,
                li: u,
                input: {},
                iframe: u,
                strong: q,
                textarea: g,
                noframes: u,
                big: q,
                small: q,
                span: a({ "#": 1, br: 1, b: 1, strong: 1, u: 1, i: 1, em: 1, sub: 1, sup: 1, strike: 1, span: 1 }),
                hr: q,
                dt: q,
                sub: q,
                optgroup: a({ option: 1 }),
                param: {},
                bdo: q,
                "var": q,
                div: u,
                object: k,
                sup: q,
                dd: u,
                strike: q,
                area: {},
                dir: m,
                map: b(a({ area: 1, form: 1, p: 1 }), d, l, e),
                applet: k,
                dl: a({ dt: 1, dd: 1 }),
                del: q,
                isindex: {},
                fieldset: b(a({ legend: 1 }), v),
                thead: y,
                ul: m,
                acronym: q,
                b: q,
                a: b(a({ a: 1 }), c),
                blockquote: b(a({
                    td: 1,
                    tr: 1,
                    tbody: 1,
                    li: 1
                }), u),
                caption: q,
                i: q,
                u: q,
                tbody: y,
                s: q,
                address: b(h, r),
                tt: q,
                legend: q,
                q: q,
                pre: b(t, f),
                p: b(a({ a: 1 }), q),
                em: q,
                dfn: q
            })
        }(),
        J = E && 9 > m.version ? { tabindex: "tabIndex", readonly: "readOnly", "for": "htmlFor", "class": "className", maxlength: "maxLength", cellspacing: "cellSpacing", cellpadding: "cellPadding", rowspan: "rowSpan", colspan: "colSpan", usemap: "useMap", frameborder: "frameBorder" } : { tabindex: "tabIndex", readonly: "readOnly" },
        K = n.listToMap("-webkit-box -moz-box block list-item table table-row-group table-header-group table-footer-group table-row table-column-group table-column table-cell table-caption".split(" ")),
        k = x.domUtils = {
            NODE_ELEMENT: 1,
            NODE_DOCUMENT: 9,
            NODE_TEXT: 3,
            NODE_COMMENT: 8,
            NODE_DOCUMENT_FRAGMENT: 11,
            POSITION_IDENTICAL: 0,
            POSITION_DISCONNECTED: 1,
            POSITION_FOLLOWING: 2,
            POSITION_PRECEDING: 4,
            POSITION_IS_CONTAINED: 8,
            POSITION_CONTAINS: 16,
            fillChar: E && "6" == m.version ? "\ufeff" : "\u200b",
            keys: { 8: 1, 46: 1, 16: 1, 17: 1, 18: 1, 37: 1, 38: 1, 39: 1, 40: 1, 13: 1 },
            breakParent: function(a, b) {
                var d, c = a,
                    f = a,
                    h, e;
                do {
                    c = c.parentNode;
                    h ? (d = c.cloneNode(!1), d.appendChild(h), h = d, d = c.cloneNode(!1), d.appendChild(e), e = d) : (h = c.cloneNode(!1), e = h.cloneNode(!1));
                    for (; d = f.previousSibling;) h.insertBefore(d, h.firstChild);
                    for (; d = f.nextSibling;) e.appendChild(d);
                    f = c
                } while (b !== c);
                d = b.parentNode;
                d.insertBefore(h, b);
                d.insertBefore(e, b);
                d.insertBefore(a, e);
                k.remove(b);
                return a
            },
            trimWhiteTextNode: function(a) {
                function b(b) { for (var c;
                        (c = a[b]) && 3 == c.nodeType && k.isWhitespace(c);) a.removeChild(c) } b("firstChild");
                b("lastChild") },
            getPosition: function(a, b) {
                if (a === b) return 0;
                var d, c = [a],
                    f = [b];
                for (d = a; d = d.parentNode;) { if (d === b) return 10;
                    c.push(d) }
                for (d = b; d = d.parentNode;) {
                    if (d ===
                        a) return 20;
                    f.push(d)
                }
                c.reverse();
                f.reverse();
                if (c[0] !== f[0]) return 1;
                for (d = -1; d++, c[d] === f[d];);
                a = c[d];
                for (b = f[d]; a = a.nextSibling;)
                    if (a === b) return 4;
                return 2
            },
            getNodeIndex: function(a, b) { for (var d = a, c = 0; d = d.previousSibling;) b && 3 == d.nodeType ? d.nodeType != d.nextSibling.nodeType && c++ : c++; return c },
            inDoc: function(a, b) { return 10 == k.getPosition(a, b) },
            findParent: function(a, b, d) { if (a && !k.isBody(a))
                    for (a = d ? a : a.parentNode; a;) { if (!b || b(a) || k.isBody(a)) return b && !b(a) && k.isBody(a) ? null : a;
                        a = a.parentNode }
                return null },
            findParentByTagName: function(a, b, d, c) { b = n.listToMap(n.isArray(b) ? b : [b]); return k.findParent(a, function(a) { return b[a.tagName] && !(c && c(a)) }, d) },
            findParents: function(a, b, d, c) { for (b = b && (d && d(a) || !d) ? [a] : []; a = k.findParent(a, d);) b.push(a); return c ? b : b.reverse() },
            insertAfter: function(a, b) { return a.parentNode.insertBefore(b, a.nextSibling) },
            remove: function(a, b) { var d = a.parentNode,
                    c; if (d) { if (b && a.hasChildNodes())
                        for (; c = a.firstChild;) d.insertBefore(c, a);
                    d.removeChild(a) } return a },
            getNextDomNode: function(a,
                b, d, c) { return w(a, "firstChild", "nextSibling", b, d, c) },
            getPreDomNode: function(a, b, d, c) { return w(a, "lastChild", "previousSibling", b, d, c) },
            isBookmarkNode: function(a) { return 1 == a.nodeType && a.id && /^_baidu_bookmark_/i.test(a.id) },
            getWindow: function(a) { a = a.ownerDocument || a; return a.defaultView || a.parentWindow },
            getCommonAncestor: function(a, b) {
                if (a === b) return a;
                for (var d = [a], c = [b], f = a, h = -1; f = f.parentNode;) { if (f === b) return f;
                    d.push(f) }
                for (f = b; f = f.parentNode;) { if (f === a) return f;
                    c.push(f) } d.reverse();
                for (c.reverse(); h++,
                    d[h] === c[h];);
                return 0 == h ? null : d[h - 1]
            },
            clearEmptySibling: function(a, b, d) {
                function c(a, b) { for (var c; a && !k.isBookmarkNode(a) && (k.isEmptyInlineElement(a) || !(new RegExp("[^\t\n\r" + k.fillChar + "]")).test(a.nodeValue));) c = a[b], k.remove(a), a = c }!b && c(a.nextSibling, "nextSibling");!d && c(a.previousSibling, "previousSibling") },
            split: function(a, b) {
                var d = a.ownerDocument;
                if (m.ie && b == a.nodeValue.length) { var c = d.createTextNode(""); return k.insertAfter(a, c) } c = a.splitText(b);
                m.ie8 && (d = d.createTextNode(""), k.insertAfter(c,
                    d), k.remove(d));
                return c
            },
            isWhitespace: function(a) { return !(new RegExp("[^ \t\n\r" + k.fillChar + "]")).test(a.nodeValue) },
            getXY: function(a) { for (var b = 0, d = 0; a.offsetParent;) d += a.offsetTop, b += a.offsetLeft, a = a.offsetParent; return { x: b, y: d } },
            isEmptyInlineElement: function(a) { if (1 != a.nodeType || !p.$removeEmpty[a.tagName]) return 0; for (a = a.firstChild; a;) { if (k.isBookmarkNode(a) || 1 == a.nodeType && !k.isEmptyInlineElement(a) || 3 == a.nodeType && !k.isWhitespace(a)) return 0;
                    a = a.nextSibling } return 1 },
            isBlockElm: function(a) {
                return 1 ==
                    a.nodeType && (p.$block[a.tagName] || K[k.getComputedStyle(a, "display")]) && !p.$nonChild[a.tagName]
            },
            getElementsByTagName: function(a, b, d) { if (d && n.isString(d)) { var c = d;
                    d = function(a) { var b = !1;
                        g.each(n.trim(c).replace(/[ ]{2,}/g, " ").split(" "), function(l, c) { if (g(a).hasClass(c)) return b = !0, !1 }); return b } } b = n.trim(b).replace(/[ ]{2,}/g, " ").split(" "); for (var f = [], h = 0, e; e = b[h++];) { e = a.getElementsByTagName(e); for (var l = 0, t; t = e[l++];) d && !d(t) || f.push(t) } return f },
            unSelectable: E && m.ie9below || m.opera ? function(a) {
                a.onselectstart =
                    function() { return !1 };
                a.onclick = a.onkeyup = a.onkeydown = function() { return !1 };
                a.unselectable = "on";
                a.setAttribute("unselectable", "on");
                for (var b = 0, d; d = a.all[b++];) switch (d.tagName.toLowerCase()) {
                    case "iframe":
                    case "textarea":
                    case "input":
                    case "select":
                        break;
                    default:
                        d.unselectable = "on", a.setAttribute("unselectable", "on") }
            } : function(a) { a.style.MozUserSelect = a.style.webkitUserSelect = a.style.msUserSelect = a.style.KhtmlUserSelect = "none" },
            removeAttributes: function(a, b) {
                b = n.isArray(b) ? b : n.trim(b).replace(/[ ]{2,}/g,
                    " ").split(" ");
                for (var d = 0, c; c = b[d++];) { c = J[c] || c; switch (c) {
                        case "className":
                            a[c] = ""; break;
                        case "style":
                            a.style.cssText = "", a.getAttributeNode("style") && !m.ie && a.removeAttributeNode(a.getAttributeNode("style")) } a.removeAttribute(c) }
            },
            createElement: function(a, b, d) { return k.setAttributes(a.createElement(b), d) },
            setAttributes: function(a, b) {
                for (var d in b)
                    if (b.hasOwnProperty(d)) {
                        var c = b[d];
                        switch (d) {
                            case "class":
                                a.className = c;
                                break;
                            case "style":
                                a.style.cssText = a.style.cssText + ";" + c;
                                break;
                            case "innerHTML":
                                a[d] =
                                    c;
                                break;
                            case "value":
                                a.value = c;
                                break;
                            default:
                                a.setAttribute(J[d] || d, c)
                        }
                    }
                return a
            },
            getComputedStyle: function(a, b) { return n.transUnitToPx(n.fixColor(b, g(a).css(b))) },
            preventDefault: function(a) { a.preventDefault ? a.preventDefault() : a.returnValue = !1 },
            removeStyle: function(a, b) {
                m.ie ? ("color" == b && (b = "(^|;)" + b), a.style.cssText = a.style.cssText.replace(new RegExp(b + "[^:]*:[^;]+;?", "ig"), "")) : a.style.removeProperty ? a.style.removeProperty(b) : a.style.removeAttribute(n.cssStyleToDomStyle(b));
                a.style.cssText || k.removeAttributes(a, ["style"])
            },
            getStyle: function(a, b) { var d = a.style[n.cssStyleToDomStyle(b)]; return n.fixColor(b, d) },
            setStyle: function(a, b, d) { a.style[n.cssStyleToDomStyle(b)] = d;
                n.trim(a.style.cssText) || this.removeAttributes(a, "style") },
            removeDirtyAttr: function(a) { for (var b = 0, d, c = a.getElementsByTagName("*"); d = c[b++];) d.removeAttribute("_moz_dirty");
                a.removeAttribute("_moz_dirty") },
            getChildCount: function(a, b) { var d = 0,
                    c = a.firstChild; for (b = b || function() { return 1 }; c;) b(c) && d++, c = c.nextSibling; return d },
            isEmptyNode: function(a) {
                return !a.firstChild ||
                    0 == k.getChildCount(a, function(a) { return !k.isBr(a) && !k.isBookmarkNode(a) && !k.isWhitespace(a) })
            },
            isBr: function(a) { return 1 == a.nodeType && "BR" == a.tagName },
            isEmptyBlock: function(a, b) { if (1 != a.nodeType) return 0;
                b = b || new RegExp("[ \t\r\n" + k.fillChar + "]", "g"); if (0 < a[m.ie ? "innerText" : "textContent"].replace(b, "").length) return 0; for (var d in p.$isNotEmpty)
                    if (a.getElementsByTagName(d).length) return 0; return 1 },
            isCustomeNode: function(a) { return 1 == a.nodeType && a.getAttribute("_ue_custom_node_") },
            fillNode: function(a,
                b) { var d = m.ie ? a.createTextNode(k.fillChar) : a.createElement("br");
                b.innerHTML = "";
                b.appendChild(d) },
            isBoundaryNode: function(a, b) { for (var d; !k.isBody(a);)
                    if (d = a, a = a.parentNode, d !== a[b]) return !1; return !0 },
            isFillChar: function(a, b) { return 3 == a.nodeType && !a.nodeValue.replace(new RegExp((b ? "^" : "") + k.fillChar), "").length },
            isBody: function(a) { return g(a).hasClass("edui-body-container") }
        },
        H = new RegExp(k.fillChar, "g");
    (function() {
        function a(a, b, c, e) {
            1 == b.nodeType && (p.$empty[b.tagName] || p.$nonChild[b.tagName]) &&
                (c = k.getNodeIndex(b) + (a ? 0 : 1), b = b.parentNode);
            a ? (e.startContainer = b, e.startOffset = c, e.endContainer || e.collapse(!0)) : (e.endContainer = b, e.endOffset = c, e.startContainer || e.collapse(!1));
            e.collapsed = e.startContainer && e.endContainer && e.startContainer === e.endContainer && e.startOffset == e.endOffset;
            return e
        }

        function b(a, b) {
            try {
                if (h && k.inDoc(h, a))
                    if (h.nodeValue.replace(H, "").length) h.nodeValue = h.nodeValue.replace(H, "");
                    else {
                        var l = h.parentNode;
                        for (k.remove(h); l && k.isEmptyInlineElement(l) && (m.safari ? !(k.getPosition(l,
                                b) & k.POSITION_CONTAINS) : !l.contains(b));) h = l.parentNode, k.remove(l), l = h
                    }
            } catch (r) {}
        }

        function d(a, b) { var l; for (a = a[b]; a && k.isFillChar(a);) l = a[b], k.remove(a), a = l }
        var c = 0,
            f = k.fillChar,
            h, e = x.Range = function(a, b) { this.startContainer = this.startOffset = this.endContainer = this.endOffset = null;
                this.document = a;
                this.collapsed = !0;
                this.body = b };
        e.prototype = {
            deleteContents: function() {
                var a;
                if (!this.collapsed) {
                    a = this.startContainer;
                    var b = this.endContainer,
                        c = this.startOffset,
                        e = this.endOffset,
                        d = this.document,
                        f = d.createDocumentFragment(),
                        h, g;
                    1 == a.nodeType && (a = a.childNodes[c] || (h = a.appendChild(d.createTextNode(""))));
                    1 == b.nodeType && (b = b.childNodes[e] || (g = b.appendChild(d.createTextNode(""))));
                    if (a === b && 3 == a.nodeType) f.appendChild(d.createTextNode(a.substringData(c, e - c))), a.deleteData(c, e - c), this.collapse(!0);
                    else {
                        for (var u, n, p = f, C = k.findParents(a, !0), F = k.findParents(b, !0), z = 0; C[z] == F[z];) z++;
                        for (var D = z, w; w = C[D]; D++) {
                            u = w.nextSibling;
                            w == a ? h || (3 == this.startContainer.nodeType ? (p.appendChild(d.createTextNode(a.nodeValue.slice(c))), a.deleteData(c,
                                a.nodeValue.length - c)) : p.appendChild(a)) : (n = w.cloneNode(!1), p.appendChild(n));
                            for (; u && u !== b && u !== F[D];) w = u.nextSibling, p.appendChild(u), u = w;
                            p = n
                        }
                        p = f;
                        C[z] || (p.appendChild(C[z - 1].cloneNode(!1)), p = p.firstChild);
                        for (D = z; c = F[D]; D++) { u = c.previousSibling;
                            c == b ? g || 3 != this.endContainer.nodeType || (p.appendChild(d.createTextNode(b.substringData(0, e))), b.deleteData(0, e)) : (n = c.cloneNode(!1), p.appendChild(n)); if (D != z || !C[z])
                                for (; u && u !== a;) c = u.previousSibling, p.insertBefore(u, p.firstChild), u = c;
                            p = n } this.setStartBefore(F[z] ?
                            C[z] ? F[z] : C[z - 1] : F[z - 1]).collapse(!0);
                        h && k.remove(h);
                        g && k.remove(g)
                    }
                }
                m.webkit && (a = this.startContainer, 3 != a.nodeType || a.nodeValue.length || (this.setStartBefore(a).collapse(!0), k.remove(a)));
                return this
            },
            inFillChar: function() { var a = this.startContainer; return this.collapsed && 3 == a.nodeType && a.nodeValue.replace(new RegExp("^" + k.fillChar), "").length + 1 == a.nodeValue.length ? !0 : !1 },
            setStart: function(b, c) { return a(!0, b, c, this) },
            setEnd: function(b, c) { return a(!1, b, c, this) },
            setStartAfter: function(a) {
                return this.setStart(a.parentNode,
                    k.getNodeIndex(a) + 1)
            },
            setStartBefore: function(a) { return this.setStart(a.parentNode, k.getNodeIndex(a)) },
            setEndAfter: function(a) { return this.setEnd(a.parentNode, k.getNodeIndex(a) + 1) },
            setEndBefore: function(a) { return this.setEnd(a.parentNode, k.getNodeIndex(a)) },
            setStartAtFirst: function(a) { return this.setStart(a, 0) },
            setStartAtLast: function(a) { return this.setStart(a, 3 == a.nodeType ? a.nodeValue.length : a.childNodes.length) },
            setEndAtFirst: function(a) { return this.setEnd(a, 0) },
            setEndAtLast: function(a) {
                return this.setEnd(a,
                    3 == a.nodeType ? a.nodeValue.length : a.childNodes.length)
            },
            selectNode: function(a) { return this.setStartBefore(a).setEndAfter(a) },
            selectNodeContents: function(a) { return this.setStart(a, 0).setEndAtLast(a) },
            cloneRange: function() { return (new e(this.document)).setStart(this.startContainer, this.startOffset).setEnd(this.endContainer, this.endOffset) },
            collapse: function(a) {
                a ? (this.endContainer = this.startContainer, this.endOffset = this.startOffset) : (this.startContainer = this.endContainer, this.startOffset = this.endOffset);
                this.collapsed = !0;
                return this
            },
            shrinkBoundary: function(a) {
                function b(a) { return 1 == a.nodeType && !k.isBookmarkNode(a) && !p.$empty[a.tagName] && !p.$nonChild[a.tagName] } for (var c, l = this.collapsed; 1 == this.startContainer.nodeType && (c = this.startContainer.childNodes[this.startOffset]) && b(c);) this.setStart(c, 0); if (l) return this.collapse(!0); if (!a)
                    for (; 1 == this.endContainer.nodeType && 0 < this.endOffset && (c = this.endContainer.childNodes[this.endOffset - 1]) && b(c);) this.setEnd(c, c.childNodes.length); return this },
            trimBoundary: function(a) {
                this.txtToElmBoundary();
                var b = this.startContainer,
                    c = this.startOffset,
                    l = this.collapsed,
                    e = this.endContainer;
                if (3 == b.nodeType) { if (0 == c) this.setStartBefore(b);
                    else if (c >= b.nodeValue.length) this.setStartAfter(b);
                    else { var d = k.split(b, c);
                        b === e ? this.setEnd(d, this.endOffset - c) : b.parentNode === e && (this.endOffset += 1);
                        this.setStartBefore(d) } if (l) return this.collapse(!0) } a || (c = this.endOffset, e = this.endContainer, 3 == e.nodeType && (0 == c ? this.setEndBefore(e) : (c < e.nodeValue.length && k.split(e, c), this.setEndAfter(e))));
                return this
            },
            txtToElmBoundary: function(a) {
                function b(a,
                    b) { var c = a[b + "Container"],
                        l = a[b + "Offset"]; if (3 == c.nodeType)
                        if (!l) a["set" + b.replace(/(\w)/, function(a) { return a.toUpperCase() }) + "Before"](c);
                        else if (l >= c.nodeValue.length) a["set" + b.replace(/(\w)/, function(a) { return a.toUpperCase() }) + "After"](c) }
                if (a || !this.collapsed) b(this, "start"), b(this, "end");
                return this
            },
            insertNode: function(a) {
                var b = a,
                    c = 1;
                11 == a.nodeType && (b = a.firstChild, c = a.childNodes.length);
                this.trimBoundary(!0);
                var l = this.startContainer,
                    e = l.childNodes[this.startOffset];
                e ? l.insertBefore(a, e) :
                    l.appendChild(a);
                b.parentNode === this.endContainer && (this.endOffset += c);
                return this.setStartBefore(b)
            },
            setCursor: function(a, b) { return this.collapse(!a).select(b) },
            createBookmark: function(a, b) {
                var l, e = this.document.createElement("span");
                e.style.cssText = "display:none;line-height:0px;";
                e.appendChild(this.document.createTextNode("\u200d"));
                e.id = "_baidu_bookmark_start_" + (b ? "" : c++);
                this.collapsed || (l = e.cloneNode(!0), l.id = "_baidu_bookmark_end_" + (b ? "" : c++));
                this.insertNode(e);
                l && this.collapse().insertNode(l).setEndBefore(l);
                this.setStartAfter(e);
                return { start: a ? e.id : e, end: l ? a ? l.id : l : null, id: a }
            },
            moveToBookmark: function(a) { var b = a.id ? this.document.getElementById(a.start) : a.start;
                a = a.end && a.id ? this.document.getElementById(a.end) : a.end;
                this.setStartBefore(b);
                k.remove(b);
                a ? (this.setEndBefore(a), k.remove(a)) : this.collapse(!0); return this },
            adjustmentBoundary: function() {
                if (!this.collapsed) {
                    for (; !k.isBody(this.startContainer) && this.startOffset == this.startContainer[3 == this.startContainer.nodeType ? "nodeValue" : "childNodes"].length &&
                        this.startContainer[3 == this.startContainer.nodeType ? "nodeValue" : "childNodes"].length;) this.setStartAfter(this.startContainer);
                    for (; !k.isBody(this.endContainer) && !this.endOffset && this.endContainer[3 == this.endContainer.nodeType ? "nodeValue" : "childNodes"].length;) this.setEndBefore(this.endContainer)
                }
                return this
            },
            getClosedNode: function() {
                var a;
                if (!this.collapsed) {
                    var b = this.cloneRange().adjustmentBoundary().shrinkBoundary();
                    b.collapsed || 1 != b.startContainer.nodeType || b.startContainer !== b.endContainer ||
                        1 != b.endOffset - b.startOffset || (b = b.startContainer.childNodes[b.startOffset]) && 1 == b.nodeType && (p.$empty[b.tagName] || p.$nonChild[b.tagName]) && (a = b)
                }
                return a
            },
            select: m.ie ? function(a, c) {
                var l;
                this.collapsed || this.shrinkBoundary();
                var e = this.getClosedNode();
                if (e && !c) { try { l = this.document.body.createControlRange(), l.addElement(e), l.select() } catch (G) {} return this }
                var e = this.createBookmark(),
                    t = e.start;
                l = this.document.body.createTextRange();
                l.moveToElementText(t);
                l.moveStart("character", 1);
                if (!this.collapsed) {
                    var g =
                        this.document.body.createTextRange(),
                        t = e.end;
                    g.moveToElementText(t);
                    l.setEndPoint("EndToEnd", g)
                } else if (!a && 3 != this.startContainer.nodeType) { var g = this.document.createTextNode(f),
                        A = this.document.createElement("span");
                    A.appendChild(this.document.createTextNode(f));
                    t.parentNode.insertBefore(A, t);
                    t.parentNode.insertBefore(g, t);
                    b(this.document, g);
                    h = g;
                    d(A, "previousSibling");
                    d(t, "nextSibling");
                    l.moveStart("character", -1);
                    l.collapse(!0) } this.moveToBookmark(e);
                A && k.remove(A);
                try { l.select() } catch (G) {}
                return this
            } : function(a) {
                function c(a) {
                    function b(b, c, e) { 3 == b.nodeType && b.nodeValue.length < c && (a[e + "Offset"] = b.nodeValue.length) } b(a.startContainer, a.startOffset, "start");
                    b(a.endContainer, a.endOffset, "end") }
                var e = k.getWindow(this.document),
                    l = e.getSelection();
                m.gecko ? this.body.focus() : e.focus();
                if (l) {
                    l.removeAllRanges();
                    this.collapsed && !a && (a = e = this.startContainer, 1 == e.nodeType && (a = e.childNodes[this.startOffset]), 3 == e.nodeType && this.startOffset || (a ? a.previousSibling && 3 == a.previousSibling.nodeType : e.lastChild &&
                        3 == e.lastChild.nodeType) || (a = this.document.createTextNode(f), this.insertNode(a), b(this.document, a), d(a, "previousSibling"), d(a, "nextSibling"), h = a, this.setStart(a, m.webkit ? 1 : 0).collapse(!0)));
                    e = this.document.createRange();
                    if (this.collapsed && m.opera && 1 == this.startContainer.nodeType)
                        if (a = this.startContainer.childNodes[this.startOffset]) { for (; a && k.isBlockElm(a);)
                                if (1 == a.nodeType && a.childNodes[0]) a = a.childNodes[0];
                                else break;
                            a && this.setStartBefore(a).collapse(!0) } else(a = this.startContainer.lastChild) &&
                            k.isBr(a) && this.setStartBefore(a).collapse(!0);
                    c(this);
                    e.setStart(this.startContainer, this.startOffset);
                    e.setEnd(this.endContainer, this.endOffset);
                    l.addRange(e)
                }
                return this
            },
            createAddress: function(a, b) {
                function c(a) {
                    for (var c = a ? l.startContainer : l.endContainer, e = k.findParents(c, !0, function(a) { return !k.isBody(a) }), d = [], f = 0, h; h = e[f++];) d.push(k.getNodeIndex(h, b));
                    e = 0;
                    if (b)
                        if (3 == c.nodeType) {
                            for (c = c.previousSibling; c && 3 == c.nodeType;) e += c.nodeValue.replace(H, "").length, c = c.previousSibling;
                            e += a ? l.startOffset :
                                l.endOffset
                        } else if (c = c.childNodes[a ? l.startOffset : l.endOffset]) e = k.getNodeIndex(c, b);
                    else
                        for (c = a ? l.startContainer : l.endContainer, a = c.firstChild; a;)
                            if (k.isFillChar(a)) a = a.nextSibling;
                            else if (e++, 3 == a.nodeType)
                        for (; a && 3 == a.nodeType;) a = a.nextSibling;
                    else a = a.nextSibling;
                    else e = a ? k.isFillChar(c) ? 0 : l.startOffset : l.endOffset;
                    0 > e && (e = 0);
                    d.push(e);
                    return d
                }
                var e = {},
                    l = this;
                e.startAddress = c(!0);
                a || (e.endAddress = l.collapsed ? [].concat(e.startAddress) : c());
                return e
            },
            moveToAddress: function(a, b) {
                function c(a,
                    b) { for (var c = e.body, l, d, f = 0, h, t = a.length; f < t; f++)
                        if (h = a[f], l = c, c = c.childNodes[h], !c) { d = h; break }
                    b ? c ? e.setStartBefore(c) : e.setStart(l, d) : c ? e.setEndBefore(c) : e.setEnd(l, d) }
                var e = this;
                c(a.startAddress, !0);
                !b && a.endAddress && c(a.endAddress);
                return e
            },
            equals: function(a) { for (var b in this)
                    if (this.hasOwnProperty(b) && this[b] !== a[b]) return !1; return !0 },
            scrollIntoView: function() {
                var a = g('<span style="padding:0;margin:0;display:block;border:0">&nbsp;</span>');
                this.cloneRange().insertNode(a.get(0));
                var b = g(window).scrollTop(),
                    c = g(window).height(),
                    e = a.offset().top;
                if (e < b - c || e > b + c) e > b + c ? window.scrollTo(0, e - c + a.height()) : window.scrollTo(0, b - e);
                a.remove()
            },
            getOffset: function() { var a = this.createBookmark(),
                    b = g(a.start).css("display", "inline-block").offset();
                this.moveToBookmark(a); return b }
        }
    })();
    (function() {
        function a(a, b) {
            var c = k.getNodeIndex;
            a = a.duplicate();
            a.collapse(b);
            var e = a.parentElement();
            if (!e.hasChildNodes()) return { container: e, offset: 0 };
            for (var l = e.children, d, f = a.duplicate(), r = 0, g = l.length - 1, y = -1; r <= g;) {
                y = Math.floor((r +
                    g) / 2);
                d = l[y];
                f.moveToElementText(d);
                var A = f.compareEndPoints("StartToStart", a);
                if (0 < A) g = y - 1;
                else if (0 > A) r = y + 1;
                else return { container: e, offset: c(d) }
            }
            if (-1 == y) { f.moveToElementText(e);
                f.setEndPoint("StartToStart", a);
                f = f.text.replace(/(\r\n|\r)/g, "\n").length;
                l = e.childNodes; if (!f) return d = l[l.length - 1], { container: d, offset: d.nodeValue.length }; for (c = l.length; 0 < f;) f -= l[--c].nodeValue.length; return { container: l[c], offset: -f } } f.collapse(0 < A);
            f.setEndPoint(0 < A ? "StartToStart" : "EndToStart", a);
            f = f.text.replace(/(\r\n|\r)/g,
                "\n").length;
            if (!f) return p.$empty[d.tagName] || p.$nonChild[d.tagName] ? { container: e, offset: c(d) + (0 < A ? 0 : 1) } : { container: d, offset: 0 < A ? 0 : d.childNodes.length };
            for (; 0 < f;) try { l = d, d = d[0 < A ? "previousSibling" : "nextSibling"], f -= d.nodeValue.length } catch (G) { return { container: e, offset: c(l) } }
            return { container: d, offset: 0 < A ? -f : d.nodeValue.length + f }
        }

        function b(b, d) {
            if (b.item) d.selectNode(b.item(0));
            else {
                var c = a(b, !0);
                d.setStart(c.container, c.offset);
                0 != b.compareEndPoints("StartToEnd", b) && (c = a(b, !1), d.setEnd(c.container,
                    c.offset))
            }
            return d
        }

        function d(a, b) { var c; try { c = a.getNative(b).createRange() } catch (l) { return null } var e = c.item ? c.item(0) : c.parentElement(); return (e.ownerDocument || e) === a.document ? c : null }(x.Selection = function(a, b) { var c = this;
            c.document = a;
            c.body = b; if (m.ie9below) g(b).on("beforedeactivate", function() { c._bakIERange = c.getIERange() }).on("activate", function() { try { var a = d(c);
                    a && c.rangeInBody(a) || !c._bakIERange || c._bakIERange.select() } catch (l) {} c._bakIERange = null }) }).prototype = {
            hasNativeRange: function() {
                var a;
                if (!m.ie || m.ie9above) { a = this.getNative(); if (!a.rangeCount) return !1;
                    a = a.getRangeAt(0) } else a = d(this);
                return this.rangeInBody(a)
            },
            getNative: function(a) { var b = this.document; try { return b ? m.ie9below || a ? b.selection : k.getWindow(b).getSelection() : null } catch (h) { return null } },
            getIERange: function(a) { var b = d(this, a); return b && this.rangeInBody(b, a) || !this._bakIERange ? b : this._bakIERange },
            rangeInBody: function(a, b) {
                var c = m.ie9below || b ? a.item ? a.item() : a.parentElement() : a.startContainer;
                return c === this.body || k.inDoc(c,
                    this.body)
            },
            cache: function() { this.clear();
                this._cachedRange = this.getRange();
                this._cachedStartElement = this.getStart();
                this._cachedStartElementPath = this.getStartElementPath() },
            getStartElementPath: function() { if (this._cachedStartElementPath) return this._cachedStartElementPath; var a = this.getStart(); return a ? k.findParents(a, !0, null, !0) : [] },
            clear: function() { this._cachedStartElementPath = this._cachedRange = this._cachedStartElement = null },
            isFocus: function() { return this.hasNativeRange() },
            getRange: function() {
                function a(a) {
                    for (var b =
                            d.body.firstChild, c = a.collapsed; b && b.firstChild;) a.setStart(b, 0), b = b.firstChild;
                    a.startContainer || a.setStart(d.body, 0);
                    c && a.collapse(!0)
                }
                var d = this;
                if (null != d._cachedRange) return this._cachedRange;
                var h = new x.Range(d.document, d.body);
                if (m.ie9below) { var e = d.getIERange(); if (e && this.rangeInBody(e)) try { b(e, h) } catch (t) { a(h) } else a(h) } else {
                    var l = d.getNative();
                    if (l && l.rangeCount && d.rangeInBody(l.getRangeAt(0))) e = l.getRangeAt(0), l = l.getRangeAt(l.rangeCount - 1), h.setStart(e.startContainer, e.startOffset).setEnd(l.endContainer,
                        l.endOffset), h.collapsed && k.isBody(h.startContainer) && !h.startOffset && a(h);
                    else { if (this._bakRange && (this._bakRange.startContainer === this.body || k.inDoc(this._bakRange.startContainer, this.body))) return this._bakRange;
                        a(h) }
                }
                return this._bakRange = h
            },
            getStart: function() {
                if (this._cachedStartElement) return this._cachedStartElement;
                var a = m.ie9below ? this.getIERange() : this.getRange(),
                    b, d;
                if (m.ie9below) {
                    if (!a) return this.document.body.firstChild;
                    if (a.item) return a.item(0);
                    b = a.duplicate();
                    0 < b.text.length && b.moveStart("character",
                        1);
                    b.collapse(1);
                    b = b.parentElement();
                    for (d = a = a.parentElement(); a = a.parentNode;)
                        if (a == b) { b = d; break }
                } else if (b = a.startContainer, 1 == b.nodeType && b.hasChildNodes() && (b = b.childNodes[Math.min(b.childNodes.length - 1, a.startOffset)]), 3 == b.nodeType) return b.parentNode;
                return b
            },
            getText: function() { var a; return this.isFocus() && (a = this.getNative()) ? (a = m.ie9below ? a.createRange() : a.getRangeAt(0), m.ie9below ? a.text : a.toString()) : "" }
        }
    })();
    (function() {
        function a(a, b) {
            var c;
            if (b.textarea)
                if (n.isString(b.textarea))
                    for (var e =
                            0, d, l = k.getElementsByTagName(a, "textarea"); d = l[e++];) { if (d.id == "umeditor_textarea_" + b.options.textarea) { c = d; break } } else c = b.textarea;
            c || (a.appendChild(c = k.createElement(document, "textarea", { name: b.options.textarea, id: "umeditor_textarea_" + b.options.textarea, style: "display:none" })), b.textarea = c);
            c.value = b.hasContents() ? b.options.allHtmlEnabled ? b.getAllHtml() : b.getContent(null, null, !0) : ""
        }

        function b(a) {
            for (var b in UM.plugins) - 1 == a.options.excludePlugins.indexOf(b) && (UM.plugins[b].call(a), a.plugins[b] =
                1);
            a.langIsReady = !0;
            a.fireEvent("langReady")
        }

        function d(a) { for (var b in a) return b }
        var c = 0,
            f, h = UM.Editor = function(a) {
                var e = this;
                e.uid = c++;
                I.call(e);
                e.commands = {};
                e.options = n.extend(n.clone(a || {}), UMEDITOR_CONFIG, !0);
                e.shortcutkeys = {};
                e.inputRules = [];
                e.outputRules = [];
                e.setOpt({
                    isShow: !0,
                    initialContent: "",
                    initialStyle: "",
                    autoClearinitialContent: !1,
                    textarea: "editorValue",
                    focus: !1,
                    focusInEnd: !0,
                    autoClearEmptyNode: !0,
                    fullscreen: !1,
                    readonly: !1,
                    zIndex: 999,
                    enterTag: "p",
                    lang: "zh-cn",
                    langPath: e.options.UMEDITOR_HOME_URL +
                        "lang/",
                    theme: "default",
                    themePath: e.options.UMEDITOR_HOME_URL + "themes/",
                    allHtmlEnabled: !1,
                    autoSyncData: !0,
                    autoHeightEnabled: !0,
                    excludePlugins: ""
                });
                e.plugins = {};
                n.isEmptyObject(UM.I18N) ? n.loadFile(document, { src: e.options.langPath + e.options.lang + "/" + e.options.lang + ".js", tag: "script", type: "text/javascript", defer: "defer" }, function() { b(e) }) : (e.options.lang = d(UM.I18N), b(e))
            };
        h.prototype = {
            ready: function(a) { a && (this.isReady ? a.apply(this) : this.addListener("ready", a)) },
            setOpt: function(a, b) {
                var c = {};
                n.isString(a) ?
                    c[a] = b : c = a;
                n.extend(this.options, c, !0)
            },
            getOpt: function(a) { return this.options[a] || "" },
            destroy: function() {
                this.fireEvent("destroy");
                var a = this.container.parentNode;
                a === document.body && (a = this.container);
                var b = this.textarea;
                b ? b.style.display = "" : (b = document.createElement("textarea"), a.parentNode.insertBefore(b, a));
                b.style.width = this.body.offsetWidth + "px";
                b.style.height = this.body.offsetHeight + "px";
                b.value = this.getContent();
                b.id = this.key;
                a.contains(b) && g(b).insertBefore(a);
                a.innerHTML = "";
                k.remove(a);
                UM.clearCache(this.id);
                for (var c in this) this.hasOwnProperty(c) && delete this[c]
            },
            initialCont: function(a) {
                if (a) {
                    a.getAttribute("name") && (this.options.textarea = a.getAttribute("name"));
                    if (a && /script|textarea/ig.test(a.tagName)) {
                        var b = document.createElement("div");
                        a.parentNode.insertBefore(b, a);
                        this.options.initialContent = UM.htmlparser(a.value || a.innerHTML || this.options.initialContent).toHtml();
                        a.className && (b.className = a.className);
                        a.style.cssText && (b.style.cssText = a.style.cssText);
                        /textarea/i.test(a.tagName) ? (this.textarea =
                            a, this.textarea.style.display = "none") : (a.parentNode.removeChild(a), a.id && (b.id = a.id));
                        a = b;
                        a.innerHTML = ""
                    }
                    return a
                }
                return null
            },
            render: function(a) {
                var b = this.options,
                    c = function(b) { return parseInt(g(a).css(b)) };
                n.isString(a) && (a = document.getElementById(a));
                a && (this.id = a.getAttribute("id"), UM.setEditor(this), n.cssRule("edui-style-body", this.options.initialStyle, document), a = this.initialCont(a), a.className += " edui-body-container", b.minFrameWidth = b.initialFrameWidth ? b.initialFrameWidth : b.initialFrameWidth =
                    g(a).width() || UM.defaultWidth, b.initialFrameHeight ? b.minFrameHeight = b.initialFrameHeight : b.initialFrameHeight = b.minFrameHeight = g(a).height() || UM.defaultHeight, a.style.width = /%$/.test(b.initialFrameWidth) ? "100%" : b.initialFrameWidth - c("padding-left") - c("padding-right") + "px", c = /%$/.test(b.initialFrameHeight) ? "100%" : b.initialFrameHeight - c("padding-top") - c("padding-bottom"), this.options.autoHeightEnabled ? (a.style.minHeight = c + "px", a.style.height = "", m.ie && 6 >= m.version && (a.style.height = c, a.style.setExpression("height",
                        "this.scrollHeight <= " + c + ' ? "' + c + 'px" : "auto"'))) : g(a).height(c), a.style.zIndex = b.zIndex, this._setup(a))
            },
            _setup: function(b) {
                var c = this,
                    d = c.options;
                b.contentEditable = !0;
                document.body.spellcheck = !1;
                c.document = document;
                c.window = document.defaultView || document.parentWindow;
                c.body = b;
                c.$body = g(b);
                c.selection = new x.Selection(document, c.body);
                c._isEnabled = !1;
                var e;
                m.gecko && (e = this.selection.getNative()) && e.removeAllRanges();
                this._initEvents();
                for (var f = b.parentNode; f && !k.isBody(f); f = f.parentNode)
                    if ("FORM" ==
                        f.tagName) { c.form = f; if (c.options.autoSyncData) g(b).on("blur", function() { a(f, c) });
                        else g(f).on("submit", function() { a(this, c) }); break }
                if (d.initialContent)
                    if (d.autoClearinitialContent) { var h = c.execCommand;
                        c.execCommand = function() { c.fireEvent("firstBeforeExecCommand"); return h.apply(c, arguments) };
                        this._setDefaultContent(d.initialContent) } else this.setContent(d.initialContent, !1, !0);
                k.isEmptyNode(c.body) && (c.body.innerHTML = "<p>" + (m.ie ? "" : "<br/>") + "</p>");
                d.focus && setTimeout(function() {
                    c.focus(c.options.focusInEnd);
                    !c.options.autoClearinitialContent && c._selectionChange()
                }, 0);
                c.container || (c.container = b.parentNode);
                c._bindshortcutKeys();
                c.isReady = 1;
                c.fireEvent("ready");
                d.onready && d.onready.call(c);
                if (!m.ie || m.ie9above) g(c.body).on("blur focus", function(a) { var b = c.selection.getNative(); if ("blur" == a.type) 0 < b.rangeCount && (c._bakRange = b.getRangeAt(0));
                    else { try { c._bakRange && b.addRange(c._bakRange) } catch (G) {} c._bakRange = null } });
                !d.isShow && c.setHide();
                d.readonly && c.setDisabled()
            },
            sync: function(b) {
                (b = b ? document.getElementById(b) :
                    k.findParent(this.body.parentNode, function(a) { return "FORM" == a.tagName }, !0)) && a(b, this)
            },
            setHeight: function(a, b) {!b && (this.options.initialFrameHeight = a);
                this.options.autoHeightEnabled ? (g(this.body).css({ "min-height": a + "px" }), m.ie && 6 >= m.version && this.container && (this.container.style.height = a, this.container.style.setExpression("height", "this.scrollHeight <= " + a + ' ? "' + a + 'px" : "auto"'))) : g(this.body).height(a);
                this.fireEvent("resize") },
            setWidth: function(a) {
                this.$container && this.$container.width(a);
                g(this.body).width(a -
                    1 * g(this.body).css("padding-left").replace("px", "") - 1 * g(this.body).css("padding-right").replace("px", ""));
                this.fireEvent("resize")
            },
            addshortcutkey: function(a, b) { var c = {};
                b ? c[a] = b : c = a;
                n.extend(this.shortcutkeys, c) },
            _bindshortcutKeys: function() {
                var a = this,
                    b = this.shortcutkeys;
                a.addListener("keydown", function(c, d) {
                    var e = d.keyCode || d.which,
                        f;
                    for (f in b)
                        for (var l = b[f].split(","), h = 0, t; t = l[h++];) {
                            t = t.split(":");
                            var g = t[0];
                            t = t[1];
                            if (/^(ctrl)(\+shift)?\+(\d+)$/.test(g.toLowerCase()) || /^(\d+)$/.test(g))
                                if ("ctrl" ==
                                    RegExp.$1 && (d.ctrlKey || d.metaKey) && ("" != RegExp.$2 ? d[RegExp.$2.slice(1) + "Key"] : 1) && e == RegExp.$3 || e == RegExp.$1) - 1 != a.queryCommandState(f, t) && a.execCommand(f, t), k.preventDefault(d)
                        }
                })
            },
            getContent: function(a, b, c, d, f) { a && n.isFunction(a) && (b = a); if (b ? !b() : !this.hasContents()) return "";
                this.fireEvent("beforegetcontent");
                a = UM.htmlparser(this.body.innerHTML, d);
                this.filterOutputRule(a);
                this.fireEvent("aftergetcontent", a); return a.toHtml(f) },
            getAllHtml: function() {
                var a = [];
                this.fireEvent("getAllHtml", a);
                if (m.ie &&
                    8 < m.version) { var b = "";
                    n.each(this.document.styleSheets, function(a) { b += a.href ? '<link rel="stylesheet" type="text/css" href="' + a.href + '" />' : "<style>" + a.cssText + "</style>" });
                    n.each(this.document.getElementsByTagName("script"), function(a) { b += a.outerHTML }) }
                return "<html><head>" + (this.options.charset ? '<meta http-equiv="Content-Type" content="text/html; charset=' + this.options.charset + '"/>' : "") + (b || this.document.getElementsByTagName("head")[0].innerHTML) + a.join("\n") + "</head><body " + (E && 9 > m.version ? 'class="view"' :
                    "") + ">" + this.getContent(null, null, !0) + "</body></html>"
            },
            getPlainTxt: function() { var a = new RegExp(k.fillChar, "g"),
                    b = this.body.innerHTML.replace(/[\n\r]/g, ""),
                    b = b.replace(/<(p|div)[^>]*>(<br\/?>|&nbsp;)<\/\1>/gi, "\n").replace(/<br\/?>/gi, "\n").replace(/<[^>/]+>/g, "").replace(/(\n)?<\/([^>]+)>/g, function(a, b, c) { return p.$block[c] ? "\n" : b ? b : "" }); return b.replace(a, "").replace(/\u00a0/g, " ").replace(/&nbsp;/g, " ") },
            getContentTxt: function() {
                return this.body[m.ie ? "innerText" : "textContent"].replace(new RegExp(k.fillChar,
                    "g"), "").replace(/\u00a0/g, " ")
            },
            setContent: function(b, c, d) {
                this.fireEvent("beforesetcontent", b);
                b = UM.htmlparser(b);
                this.filterInputRule(b);
                b = b.toHtml();
                this.body.innerHTML = (c ? this.body.innerHTML : "") + b;
                if ("p" == this.options.enterTag)
                    if (c = this.body.firstChild, !c || 1 == c.nodeType && (p.$cdata[c.tagName] || "DIV" == c.tagName && c.getAttribute("cdata_tag") || k.isCustomeNode(c)) && c === this.body.lastChild) this.body.innerHTML = "<p>" + (m.ie ? "&nbsp;" : "<br/>") + "</p>" + this.body.innerHTML;
                    else
                        for (var e = this.document.createElement("p"); c;) {
                            for (; c &&
                                (3 == c.nodeType || 1 == c.nodeType && p.p[c.tagName] && !p.$cdata[c.tagName]);) b = c.nextSibling, e.appendChild(c), c = b;
                            if (e.firstChild)
                                if (c) c.parentNode.insertBefore(e, c), e = this.document.createElement("p");
                                else { this.body.appendChild(e); break }
                            c = c.nextSibling
                        }
                this.fireEvent("aftersetcontent");
                this.fireEvent("contentchange");
                !d && this._selectionChange();
                this._bakRange = this._bakIERange = this._bakNativeRange = null;
                var f;
                m.gecko && (f = this.selection.getNative()) && f.removeAllRanges();
                this.options.autoSyncData && this.form &&
                    a(this.form, this)
            },
            focus: function(a) { try { var b = this.selection.getRange();
                    a ? b.setStartAtLast(this.body.lastChild).setCursor(!1, !0) : b.select(!0);
                    this.fireEvent("focus") } catch (t) {} },
            blur: function() { var a = this.selection.getNative();
                a.empty ? a.empty() : a.removeAllRanges();
                this.fireEvent("blur") },
            isFocus: function() { return !0 === this.fireEvent("isfocus") ? !0 : this.selection.isFocus() },
            _initEvents: function() {
                var a = this,
                    b = function() { a._proxyDomEvent.apply(a, arguments) };
                g(a.body).on("click contextmenu mousedown keydown keyup keypress mouseup mouseover mouseout selectstart",
                    b).on("focus blur", b).on("mouseup keydown", function(b) { "keydown" == b.type && (b.ctrlKey || b.metaKey || b.shiftKey || b.altKey) || 2 != b.button && a._selectionChange(250, b) })
            },
            _proxyDomEvent: function(a) { return this.fireEvent(a.type.replace(/^on/, ""), a) },
            _selectionChange: function(a, b) {
                var c = this,
                    d = !1,
                    e, l;
                m.ie && 9 > m.version && b && "mouseup" == b.type && !this.selection.getRange().collapsed && (d = !0, e = b.clientX, l = b.clientY);
                clearTimeout(f);
                f = setTimeout(function() {
                    if (c.selection.getNative()) {
                        var a;
                        if (d && "None" == c.selection.getNative().type) {
                            a =
                                c.document.body.createTextRange();
                            try { a.moveToPoint(e, l) } catch (G) { a = null }
                        }
                        var f;
                        a && (f = c.selection.getIERange, c.selection.getIERange = function() { return a });
                        c.selection.cache();
                        f && (c.selection.getIERange = f);
                        c.selection._cachedRange && c.selection._cachedStartElement && (c.fireEvent("beforeselectionchange"), c.fireEvent("selectionchange", !!b), c.fireEvent("afterselectionchange"), c.selection.clear())
                    }
                }, a || 50)
            },
            _callCmdFn: function(a, b) {
                b = Array.prototype.slice.call(b, 0);
                var c = b.shift().toLowerCase(),
                    d, e;
                e = (d =
                    this.commands[c] || UM.commands[c]) && d[a];
                if (!(d && e || "queryCommandState" != a)) return 0;
                if (e) return e.apply(this, [c].concat(b))
            },
            execCommand: function(a) {
                if (!this.isFocus()) { var b = this.selection._bakRange;
                    b ? b.select() : this.focus(!0) } a = a.toLowerCase();
                var c, b = this.commands[a] || UM.commands[a];
                if (!b || !b.execCommand) return null;
                b.notNeedUndo || this.__hasEnterExecCommand ? (c = this._callCmdFn("execCommand", arguments), this.__hasEnterExecCommand || b.ignoreContentChange || this._ignoreContentChange || this.fireEvent("contentchange")) :
                    (this.__hasEnterExecCommand = !0, -1 != this.queryCommandState.apply(this, arguments) && (this.fireEvent("saveScene"), this.fireEvent("beforeexeccommand", a), c = this._callCmdFn("execCommand", arguments), b.ignoreContentChange || this._ignoreContentChange || this.fireEvent("contentchange"), this.fireEvent("afterexeccommand", a), this.fireEvent("saveScene")), this.__hasEnterExecCommand = !1);
                this.__hasEnterExecCommand || b.ignoreContentChange || this._ignoreContentChange || this._selectionChange();
                return c
            },
            queryCommandState: function(a) {
                try {
                    return this._callCmdFn("queryCommandState",
                        arguments)
                } catch (l) { return 0 }
            },
            queryCommandValue: function(a) { try { return this._callCmdFn("queryCommandValue", arguments) } catch (l) { return null } },
            hasContents: function(a) { if (a)
                    for (var b = 0, c; c = a[b++];)
                        if (0 < this.body.getElementsByTagName(c).length) return !0; if (!k.isEmptyBlock(this.body)) return !0;
                a = ["div"]; for (b = 0; c = a[b++];) { c = k.getElementsByTagName(this.body, c); for (var d = 0, e; e = c[d++];)
                        if (k.isCustomeNode(e)) return !0 } return !1 },
            reset: function() { this.fireEvent("reset") },
            isEnabled: function() { return 1 != this._isEnabled },
            setEnabled: function() { var a;
                this.body.contentEditable = !0; if (this.lastBk) { a = this.selection.getRange(); try { a.moveToBookmark(this.lastBk), delete this.lastBk } catch (l) { a.setStartAtFirst(this.body).collapse(!0) } a.select(!0) } this.bkqueryCommandState && (this.queryCommandState = this.bkqueryCommandState, delete this.bkqueryCommandState);
                this._bkproxyDomEvent && (this._proxyDomEvent = this._bkproxyDomEvent, delete this._bkproxyDomEvent);
                this.fireEvent("setEnabled") },
            enable: function() { return this.setEnabled() },
            setDisabled: function(a,
                b) { var c = this;
                c.body.contentEditable = !1;
                c._except = a ? n.isArray(a) ? a : [a] : [];
                c.lastBk || (c.lastBk = c.selection.getRange().createBookmark(!0));
                c.bkqueryCommandState || (c.bkqueryCommandState = c.queryCommandState, c.queryCommandState = function(a) { return -1 != n.indexOf(c._except, a) ? c.bkqueryCommandState.apply(c, arguments) : -1 });
                b || c._bkproxyDomEvent || (c._bkproxyDomEvent = c._proxyDomEvent, c._proxyDomEvent = function() { return !1 });
                c.fireEvent("selectionchange");
                c.fireEvent("setDisabled", c._except) },
            disable: function(a) { return this.setDisabled(a) },
            _setDefaultContent: function() {
                function a() { var b = this;
                    b.document.getElementById("initContent") && (b.body.innerHTML = "<p>" + (E ? "" : "<br/>") + "</p>", b.removeListener("firstBeforeExecCommand focus", a), setTimeout(function() { b.focus();
                        b._selectionChange() }, 0)) } return function(b) { this.body.innerHTML = '<p id="initContent">' + b + "</p>";
                    this.addListener("firstBeforeExecCommand focus", a) } }(),
            setShow: function() {
                var a = this.selection.getRange();
                if ("none" == this.container.style.display) {
                    try {
                        a.moveToBookmark(this.lastBk),
                            delete this.lastBk
                    } catch (l) { a.setStartAtFirst(this.body).collapse(!0) } setTimeout(function() { a.select(!0) }, 100);
                    this.container.style.display = ""
                }
            },
            show: function() { return this.setShow() },
            setHide: function() { this.lastBk || (this.lastBk = this.selection.getRange().createBookmark(!0));
                this.container.style.display = "none" },
            hide: function() { return this.setHide() },
            getLang: function(a) {
                var b = UM.I18N[this.options.lang];
                if (!b) throw Error("not import language file");
                a = (a || "").split(".");
                for (var c = 0, d;
                    (d = a[c++]) && (b = b[d],
                        b););
                return b
            },
            getContentLength: function(a, b) { var c = this.getContent(!1, !1, !0).length; if (a) { b = (b || []).concat(["hr", "img", "iframe"]); for (var c = this.getContentTxt().replace(/[\t\r\n]+/g, "").length, d = 0, e; e = b[d++];) c += this.body.getElementsByTagName(e).length } return c },
            addInputRule: function(a, b) { a.ignoreUndo = b;
                this.inputRules.push(a) },
            filterInputRule: function(a, b) { for (var c = 0, d; d = this.inputRules[c++];) b && d.ignoreUndo || d.call(this, a) },
            addOutputRule: function(a, b) { a.ignoreUndo = b;
                this.outputRules.push(a) },
            filterOutputRule: function(a, b) { for (var c = 0, d; d = this.outputRules[c++];) b && d.ignoreUndo || d.call(this, a) }
        };
        n.inherits(h, I)
    })();
    UM.filterWord = function() {
        function a(a) { return a = a.replace(/[\d.]+\w+/g, function(a) { return n.transUnitToPx(a) }) }

        function b(b) {
            return b.replace(/[\t\r\n]+/g, " ").replace(/\x3c!--[\s\S]*?--\x3e/ig, "").replace(/<v:shape [^>]*>[\s\S]*?.<\/v:shape>/gi, function(b) {
                if (m.opera) return "";
                try {
                    if (/Bitmap/i.test(b)) return "";
                    var c = b.match(/width:([ \d.]*p[tx])/i)[1],
                        d = b.match(/height:([ \d.]*p[tx])/i)[1],
                        e = b.match(/src=\s*"([^"]*)"/i)[1];
                    return '<img width="' + a(c) + '" height="' + a(d) + '" src="' + e + '" />'
                } catch (l) { return "" }
            }).replace(/<\/?div[^>]*>/g, "").replace(/v:\w+=(["']?)[^'"]+\1/g, "").replace(/<(!|script[^>]*>.*?<\/script(?=[>\s])|\/?(\?xml(:\w+)?|xml|meta|link|style|\w+:\w+)(?=[\s\/>]))[^>]*>/gi, "").replace(/<p [^>]*class="?MsoHeading"?[^>]*>(.*?)<\/p>/gi, "<p><strong>$1</strong></p>").replace(/\s+(class|lang|align)\s*=\s*(['"]?)([\w-]+)\2/ig, function(a, b, d, e) {
                return "class" == b && "MsoListParagraph" ==
                    e ? a : ""
            }).replace(/<(font|span)[^>]*>(\s*)<\/\1>/gi, function(a, b, d) { return d.replace(/[\t\r\n ]+/g, " ") }).replace(/(<[a-z][^>]*)\sstyle=(["'])([^\2]*?)\2/gi, function(b, d, h, e) {
                b = [];
                e = e.replace(/^\s+|\s+$/, "").replace(/&#39;/g, "'").replace(/&quot;/gi, "'").split(/;\s*/g);
                h = 0;
                for (var c; c = e[h]; h++) {
                    var f, g = c.split(":");
                    if (2 == g.length && (c = g[0].toLowerCase(), f = g[1].toLowerCase(), !(/^(background)\w*/.test(c) && 0 == f.replace(/(initial|\s)/g, "").length || /^(margin)\w*/.test(c) && /^0\w+$/.test(f)))) {
                        switch (c) {
                            case "mso-padding-alt":
                            case "mso-padding-top-alt":
                            case "mso-padding-right-alt":
                            case "mso-padding-bottom-alt":
                            case "mso-padding-left-alt":
                            case "mso-margin-alt":
                            case "mso-margin-top-alt":
                            case "mso-margin-right-alt":
                            case "mso-margin-bottom-alt":
                            case "mso-margin-left-alt":
                            case "mso-height":
                            case "mso-width":
                            case "mso-vertical-align-alt":
                                /<table/.test(d) ||
                                    (b[h] = c.replace(/^mso-|-alt$/g, "") + ":" + a(f));
                                continue;
                            case "horiz-align":
                                b[h] = "text-align:" + f;
                                continue;
                            case "vert-align":
                                b[h] = "vertical-align:" + f;
                                continue;
                            case "font-color":
                            case "mso-foreground":
                                b[h] = "color:" + f;
                                continue;
                            case "mso-background":
                            case "mso-highlight":
                                b[h] = "background:" + f;
                                continue;
                            case "mso-default-height":
                                b[h] = "min-height:" + a(f);
                                continue;
                            case "mso-default-width":
                                b[h] = "min-width:" + a(f);
                                continue;
                            case "mso-padding-between-alt":
                                b[h] = "border-collapse:separate;border-spacing:" + a(f);
                                continue;
                            case "text-line-through":
                                if ("single" == f || "double" == f) b[h] = "text-decoration:line-through";
                                continue;
                            case "mso-zero-height":
                                "yes" == f && (b[h] = "display:none");
                                continue;
                            case "margin":
                                if (!/[1-9]/.test(f)) continue
                        }
                        /^(mso|column|font-emph|lang|layout|line-break|list-image|nav|panose|punct|row|ruby|sep|size|src|tab-|table-border|text-(?:decor|trans)|top-bar|version|vnd|word-break)/.test(c) || /text\-indent|padding|margin/.test(c) && /\-[\d.]+/.test(f) || (b[h] = c + ":" + g[1])
                    }
                }
                return d + (b.length ? ' style="' + b.join(";").replace(/;{2,}/g,
                    ";") + '"' : "")
            }).replace(/[\d.]+(cm|pt)/g, function(a) { return n.transUnitToPx(a) })
        }
        return function(a) { return /(class="?Mso|style="[^"]*\bmso\-|w:WordDocument|<(v|o):|lang=)/ig.test(a) ? b(a) : a }
    }();
    (function() {
        function a(a, b, c) { a.push("\n"); return b + (c ? 1 : -1) }

        function b(a, b) { for (var c = 0; c < b; c++) a.push("    ") }

        function d(f, e, l, h) {
            switch (f.type) {
                case "root":
                    for (var r = 0, g; g = f.children[r++];) l && "element" == g.type && !p.$inlineWithA[g.tagName] && 1 < r && (a(e, h, !0), b(e, h)), d(g, e, l, h);
                    break;
                case "text":
                    "pre" == f.parentNode.tagName ?
                        e.push(f.data) : e.push(k[f.parentNode.tagName] ? n.html(f.data) : f.data.replace(/[ ]{2}/g, " &nbsp;"));
                    break;
                case "element":
                    c(f, e, l, h);
                    break;
                case "comment":
                    e.push("\x3c!--" + f.data + "--\x3e")
            }
            return e
        }

        function c(c, f, e, l) {
            var h = "";
            if (c.attrs) { var h = [],
                    r = c.attrs,
                    g; for (g in r) h.push(g + (void 0 !== r[g] ? '="' + (t[g] ? n.html(r[g]).replace(/["]/g, function(a) { return "&quot;" }) : n.unhtml(r[g])) + '"' : ""));
                h = h.join(" ") } f.push("<" + c.tagName + (h ? " " + h : "") + (p.$empty[c.tagName] ? "/" : "") + ">");
            e && !p.$inlineWithA[c.tagName] && "pre" !=
                c.tagName && c.children && c.children.length && (l = a(f, l, !0), b(f, l));
            if (c.children && c.children.length)
                for (h = 0; r = c.children[h++];) e && "element" == r.type && !p.$inlineWithA[r.tagName] && 1 < h && (a(f, l), b(f, l)), d(r, f, e, l);
            p.$empty[c.tagName] || (e && !p.$inlineWithA[c.tagName] && "pre" != c.tagName && c.children && c.children.length && (l = a(f, l), b(f, l)), f.push("</" + c.tagName + ">"))
        }

        function f(a, b) { var c; if ("element" == a.type && a.getAttr("id") == b) return a; if (a.children && a.children.length)
                for (var d = 0; c = a.children[d++];)
                    if (c = f(c, b)) return c }

        function h(a, b, c) { "element" == a.type && a.tagName == b && c.push(a); if (a.children && a.children.length)
                for (var d = 0, f; f = a.children[d++];) h(f, b, c) }

        function e(a, b) { if (a.children && a.children.length)
                for (var c = 0, d; d = a.children[c];) e(d, b), d.parentNode && (d.children && d.children.length && b(d), d.parentNode && c++);
            else b(a) }
        var l = UM.uNode = function(a) { this.type = a.type;
                this.data = a.data;
                this.tagName = a.tagName;
                this.parentNode = a.parentNode;
                this.attrs = a.attrs || {};
                this.children = a.children },
            t = { href: 1, src: 1, _src: 1, _href: 1, cdata_data: 1 },
            k = { style: 1, script: 1 };
        l.createElement = function(a) { return /[<>]/.test(a) ? UM.htmlparser(a).children[0] : new l({ type: "element", children: [], tagName: a }) };
        l.createText = function(a, b) { return new UM.uNode({ type: "text", data: b ? a : n.unhtml(a || "") }) };
        l.prototype = {
            toHtml: function(a) { var b = [];
                d(this, b, a, 0); return b.join("") },
            innerHTML: function(a) {
                if ("element" != this.type || p.$empty[this.tagName]) return this;
                if (n.isString(a)) {
                    if (this.children)
                        for (var b = 0, c; c = this.children[b++];) c.parentNode = null;
                    this.children = [];
                    a = UM.htmlparser(a);
                    for (b = 0; c = a.children[b++];) this.children.push(c), c.parentNode = this;
                    return this
                }
                a = new UM.uNode({ type: "root", children: this.children });
                return a.toHtml()
            },
            innerText: function(a, b) { if ("element" != this.type || p.$empty[this.tagName]) return this; if (a) { if (this.children)
                        for (var c = 0, d; d = this.children[c++];) d.parentNode = null;
                    this.children = [];
                    this.appendChild(l.createText(a, b)); return this } return this.toHtml().replace(/<[^>]+>/g, "") },
            getData: function() { return "element" == this.type ? "" : this.data },
            firstChild: function() {
                return this.children ?
                    this.children[0] : null
            },
            lastChild: function() { return this.children ? this.children[this.children.length - 1] : null },
            previousSibling: function() { for (var a = this.parentNode, b = 0, c; c = a.children[b]; b++)
                    if (c === this) return 0 == b ? null : a.children[b - 1] },
            nextSibling: function() { for (var a = this.parentNode, b = 0, c; c = a.children[b++];)
                    if (c === this) return a.children[b] },
            replaceChild: function(a, b) {
                if (this.children) {
                    a.parentNode && a.parentNode.removeChild(a);
                    for (var c = 0, d; d = this.children[c]; c++)
                        if (d === b) return this.children.splice(c,
                            1, a), b.parentNode = null, a.parentNode = this, a
                }
            },
            appendChild: function(a) { if ("root" == this.type || "element" == this.type && !p.$empty[this.tagName]) { this.children || (this.children = []);
                    a.parentNode && a.parentNode.removeChild(a); for (var b = 0, c; c = this.children[b]; b++)
                        if (c === a) { this.children.splice(b, 1); break }
                    this.children.push(a);
                    a.parentNode = this; return a } },
            insertBefore: function(a, b) {
                if (this.children) {
                    a.parentNode && a.parentNode.removeChild(a);
                    for (var c = 0, d; d = this.children[c]; c++)
                        if (d === b) return this.children.splice(c,
                            0, a), a.parentNode = this, a
                }
            },
            insertAfter: function(a, b) { if (this.children) { a.parentNode && a.parentNode.removeChild(a); for (var c = 0, d; d = this.children[c]; c++)
                        if (d === b) return this.children.splice(c + 1, 0, a), a.parentNode = this, a } },
            removeChild: function(a, b) { if (this.children)
                    for (var c = 0, d; d = this.children[c]; c++)
                        if (d === a) { this.children.splice(c, 1);
                            d.parentNode = null; if (b && d.children && d.children.length)
                                for (var f = 0, e; e = d.children[f]; f++) this.children.splice(c + f, 0, e), e.parentNode = this; return d } },
            getAttr: function(a) {
                return this.attrs &&
                    this.attrs[a.toLowerCase()]
            },
            setAttr: function(a, b) { if (a)
                    if (this.attrs || (this.attrs = {}), n.isObject(a))
                        for (var c in a) a[c] ? this.attrs[c.toLowerCase()] = a[c] : delete this.attrs[c];
                    else b ? this.attrs[a.toLowerCase()] = b : delete this.attrs[a];
                else delete this.attrs },
            hasAttr: function(a) { a = this.getAttr(a); return null !== a && void 0 !== a },
            getIndex: function() { for (var a = this.parentNode, b = 0, c; c = a.children[b]; b++)
                    if (c === this) return b; return -1 },
            getNodeById: function(a) {
                var b;
                if (this.children && this.children.length)
                    for (var c =
                            0; b = this.children[c++];)
                        if (b = f(b, a)) return b
            },
            getNodesByTagName: function(a) { a = n.trim(a).replace(/[ ]{2,}/g, " ").split(" "); var b = [],
                    c = this;
                n.each(a, function(a) { if (c.children && c.children.length)
                        for (var d = 0, f; f = c.children[d++];) h(f, a, b) }); return b },
            getStyle: function(a) { var b = this.getAttr("style"); return b ? (a = b.match(new RegExp("(^|;)\\s*" + a + ":([^;]+)", "i"))) && a[0] ? a[2] : "" : "" },
            setStyle: function(a, b) {
                function c(a, b) {
                    d = d.replace(new RegExp("(^|;)\\s*" + a + ":([^;]+;?)", "gi"), "$1");
                    b && (d = a + ":" + n.unhtml(b) +
                        ";" + d)
                }
                var d = this.getAttr("style");
                d || (d = "");
                if (n.isObject(a))
                    for (var f in a) c(f, a[f]);
                else c(a, b);
                this.setAttr("style", n.trim(d))
            },
            hasClass: function(a) { if (this.hasAttr("class")) { var b = this.getAttr("class").split(/\s+/),
                        c = !1;
                    g.each(b, function(b, d) { d === a && (c = !0) }); return c } return !1 },
            addClass: function(a) { var b = null,
                    c = !1;
                this.hasAttr("class") ? (b = this.getAttr("class"), b = b.split(/\s+/), b.forEach(function(b) { b === a && (c = !0) }), !c && b.push(a), this.setAttr("class", b.join(" "))) : this.setAttr("class", a) },
            removeClass: function(a) {
                if (this.hasAttr("class")) {
                    var b =
                        this.getAttr("class"),
                        b = b.replace(new RegExp("\\b" + a + "\\b", "g"), "");
                    this.setAttr("class", n.trim(b).replace(/[ ]{2,}/g, " "))
                }
            },
            traversal: function(a) { this.children && this.children.length && e(this, a); return this }
        }
    })();
    UM.htmlparser = function(a, b) {
        function d(a, b) { if (r[a.tagName]) { var c = g.createElement(r[a.tagName]);
                a.appendChild(c);
                c.appendChild(g.createText(b)) } else a.appendChild(g.createText(b)) }

        function c(a, b, d) {
            var f;
            if (f = v[b]) {
                for (var e = a, t;
                    "root" != e.type;) {
                    if (n.isArray(f) ? -1 != n.indexOf(f, e.tagName) :
                        f == e.tagName) { a = e;
                        t = !0; break } e = e.parentNode
                }
                t || (a = c(a, n.isArray(f) ? f[0] : f))
            }
            f = new g({ parentNode: a, type: "element", tagName: b.toLowerCase(), children: p.$empty[b] ? null : [] });
            if (d) { for (e = {}; t = h.exec(d);) e[t[1].toLowerCase()] = l[t[1].toLowerCase()] ? t[2] || t[3] || t[4] : n.unhtml(t[2] || t[3] || t[4]);
                f.attrs = e } a.children.push(f);
            return p.$empty[b] ? a : f
        }
        var f = /<(?:(?:\/([^>]+)>)|(?:!--([\S|\s]*?)--\x3e)|(?:([^\s\/>]+)\s*((?:(?:"[^"]*")|(?:'[^']*')|[^"'<>])*)\/?>))/g,
            h = /([\w\-:.]+)(?:(?:\s*=\s*(?:(?:"([^"]*)")|(?:'([^']*)')|([^\s>]+)))|(?=\s|$))/g,
            e = { b: 1, code: 1, i: 1, u: 1, strike: 1, s: 1, tt: 1, strong: 1, q: 1, samp: 1, em: 1, span: 1, sub: 1, img: 1, sup: 1, font: 1, big: 1, small: 1, iframe: 1, a: 1, br: 1, pre: 1 };
        a = a.replace(new RegExp(k.fillChar, "g"), "");
        b || (a = a.replace(new RegExp("[\\r\\t\\n" + (b ? "" : " ") + "]*</?(\\w+)\\s*(?:[^>]*)>[\\r\\t\\n" + (b ? "" : " ") + "]*", "g"), function(a, c) { return c && e[c.toLowerCase()] ? a.replace(/(^[\n\r]+)|([\n\r]+$)/g, "") : a.replace(new RegExp("^[\\r\\n" + (b ? "" : " ") + "]+"), "").replace(new RegExp("[\\r\\n" + (b ? "" : " ") + "]+$"), "") }));
        for (var l = { href: 1, src: 1 },
                g = UM.uNode, v = { td: "tr", tr: ["tbody", "thead", "tfoot"], tbody: "table", th: "tr", thead: "table", tfoot: "table", caption: "table", li: ["ul", "ol"], dt: "dl", dd: "dl", option: "select" }, r = { ol: "li", ul: "li" }, q, y = 0, m = 0, G = new g({ type: "root", children: [] }), u = G; q = f.exec(a);) {
            y = q.index;
            try {
                if (y > m && d(u, a.slice(m, y)), q[3]) p.$cdata[u.tagName] ? d(u, q[0]) : u = c(u, q[3].toLowerCase(), q[4]);
                else if (q[1]) {
                    if ("root" != u.type)
                        if (p.$cdata[u.tagName] && !p.$cdata[q[1]]) d(u, q[0]);
                        else {
                            for (y = u;
                                "element" == u.type && u.tagName != q[1].toLowerCase();)
                                if (u =
                                    u.parentNode, "root" == u.type) throw u = y, "break";
                            u = u.parentNode
                        }
                } else q[2] && u.children.push(new g({ type: "comment", data: q[2], parentNode: u }))
            } catch (L) {} m = f.lastIndex
        }
        m < a.length && d(u, a.slice(m));
        return G
    };
    UM.filterNode = function() {
        function a(b, d) {
            switch (b.type) {
                case "element":
                    var c;
                    if (c = d[b.tagName])
                        if ("-" === c) b.parentNode.removeChild(b);
                        else if (n.isFunction(c)) {
                        var f = b.parentNode,
                            h = b.getIndex();
                        c(b);
                        if (b.parentNode) { if (b.children)
                                for (c = 0; h = b.children[c];) a(h, d), h.parentNode && c++ } else
                            for (c = h; h = f.children[c];) a(h,
                                d), h.parentNode && c++
                    } else { if ((c = c.$) && b.attrs) { var h = {},
                                e; for (f in c) { e = b.getAttr(f); if ("style" == f && n.isArray(c[f])) { var l = [];
                                    n.each(c[f], function(a) { var c;
                                        (c = b.getStyle(a)) && l.push(a + ":" + c) });
                                    e = l.join(";") } e && (h[f] = e) } b.attrs = h } if (b.children)
                            for (c = 0; h = b.children[c];) a(h, d), h.parentNode && c++ } else if (p.$cdata[b.tagName]) b.parentNode.removeChild(b);
                    else
                        for (f = b.parentNode, h = b.getIndex(), b.parentNode.removeChild(b, !0), c = h; h = f.children[c];) a(h, d), h.parentNode && c++;
                    break;
                case "comment":
                    b.parentNode.removeChild(b)
            }
        }
        return function(b, d) { if (n.isEmptyObject(d)) return b; var c;
            (c = d["-"]) && n.each(c.split(" "), function(a) { d[a] = "-" });
            c = 0; for (var f; f = b.children[c];) a(f, d), f.parentNode && c++; return b }
    }();
    UM.commands.inserthtml = {
        execCommand: function(a, b, d) {
            var c = this,
                f;
            if (b && !0 !== c.fireEvent("beforeinserthtml", b)) {
                f = c.selection.getRange();
                a = f.document.createElement("div");
                a.style.display = "inline";
                d || (b = UM.htmlparser(b), c.options.filterRules && UM.filterNode(b, c.options.filterRules), c.filterInputRule(b), b = b.toHtml());
                a.innerHTML =
                    n.trim(b);
                if (!f.collapsed && (b = f.startContainer, k.isFillChar(b) && f.setStartBefore(b), b = f.endContainer, k.isFillChar(b) && f.setEndAfter(b), f.txtToElmBoundary(), f.endContainer && 1 == f.endContainer.nodeType && (b = f.endContainer.childNodes[f.endOffset]) && k.isBr(b) && f.setEndAfter(b), 0 == f.startOffset && (b = f.startContainer, k.isBoundaryNode(b, "firstChild") && (b = f.endContainer, f.endOffset == (3 == b.nodeType ? b.nodeValue.length : b.childNodes.length) && k.isBoundaryNode(b, "lastChild") && (c.body.innerHTML = "<p>" + (m.ie ? "" : "<br/>") +
                        "</p>", f.setStart(c.body.firstChild, 0).collapse(!0)))), !f.collapsed && f.deleteContents(), 1 == f.startContainer.nodeType)) { b = f.startContainer.childNodes[f.startOffset]; var h; if (b && k.isBlockElm(b) && (h = b.previousSibling) && k.isBlockElm(h)) { for (f.setEnd(h, h.childNodes.length).collapse(); b.firstChild;) h.appendChild(b.firstChild);
                        k.remove(b) } }
                var e, l;
                d = 0;
                var g;
                f.inFillChar() && (b = f.startContainer, k.isFillChar(b) ? (f.setStartBefore(b).collapse(!0), k.remove(b)) : k.isFillChar(b, !0) && (b.nodeValue = b.nodeValue.replace(H,
                    ""), f.startOffset--, f.collapsed && f.collapse(!0)));
                for (; b = a.firstChild;) {
                    if (d) { for (e = c.document.createElement("p"); b && (3 == b.nodeType || !p.$block[b.tagName]);) g = b.nextSibling, e.appendChild(b), b = g;
                        e.firstChild && (b = e) } f.insertNode(b);
                    g = b.nextSibling;
                    if (!d && b.nodeType == k.NODE_ELEMENT && k.isBlockElm(b) && (e = k.findParent(b, function(a) { return k.isBlockElm(a) })) && "body" != e.tagName.toLowerCase() && (!p[e.tagName][b.nodeName] || b.parentNode !== e)) {
                        if (p[e.tagName][b.nodeName])
                            for (l = b.parentNode; l !== e;) h = l, l = l.parentNode;
                        else h = e;
                        k.breakParent(b, h || l);
                        h = b.previousSibling;
                        k.trimWhiteTextNode(h);
                        h.childNodes.length || k.remove(h);
                        !m.ie && (v = b.nextSibling) && k.isBlockElm(v) && v.lastChild && !k.isBr(v.lastChild) && v.appendChild(c.document.createElement("br"));
                        d = 1
                    }
                    var v = b.nextSibling;
                    if (!a.firstChild && v && k.isBlockElm(v)) { f.setStart(v, 0).collapse(!0); break } f.setEndAfter(b).collapse()
                }
                b = f.startContainer;
                g && k.isBr(g) && k.remove(g);
                if (k.isBlockElm(b) && k.isEmptyNode(b))
                    if (g = b.nextSibling) k.remove(b), 1 == g.nodeType && p.$block[g.tagName] &&
                        f.setStart(g, 0).collapse(!0).shrinkBoundary();
                    else try { b.innerHTML = m.ie ? k.fillChar : "<br/>" } catch (q) { f.setStartBefore(b), k.remove(b) }
                try { if (m.ie9below && 1 == f.startContainer.nodeType && !f.startContainer.childNodes[f.startOffset] && (h = f.startContainer.childNodes[f.startOffset - 1]) && 1 == h.nodeType && p.$empty[h.tagName]) { var r = this.document.createTextNode(k.fillChar);
                        f.insertNode(r).setStart(r, 0).collapse(!0) } setTimeout(function() { f.select(!0) }) } catch (q) {} setTimeout(function() {
                    f = c.selection.getRange();
                    f.scrollIntoView();
                    c.fireEvent("afterinserthtml")
                }, 200)
            }
        }
    };
    UM.commands.insertimage = {
        execCommand: function(a, b) {
            b = n.isArray(b) ? b : [b];
            if (b.length) {
                var d = [],
                    c, f;
                f = b[0];
                if (1 == b.length) c = '<img src="' + f.src + '" ' + (f._src ? ' _src="' + f._src + '" ' : "") + (f.width ? 'width="' + f.width + '" ' : "") + (f.height ? ' height="' + f.height + '" ' : "") + ("left" == f.floatStyle || "right" == f.floatStyle ? ' style="float:' + f.floatStyle + ';"' : "") + (f.title && "" != f.title ? ' title="' + f.title + '"' : "") + (f.border && "0" != f.border ? ' border="' + f.border + '"' : "") + (f.alt && "" != f.alt ?
                    ' alt="' + f.alt + '"' : "") + (f.hspace && "0" != f.hspace ? ' hspace = "' + f.hspace + '"' : "") + (f.vspace && "0" != f.vspace ? ' vspace = "' + f.vspace + '"' : "") + "/>", "center" == f.floatStyle && (c = '<p style="text-align: center">' + c + "</p>"), d.push(c);
                else
                    for (var h = 0; f = b[h++];) c = "<p " + ("center" == f.floatStyle ? 'style="text-align: center" ' : "") + '><img src="' + f.src + '" ' + (f.width ? 'width="' + f.width + '" ' : "") + (f._src ? ' _src="' + f._src + '" ' : "") + (f.height ? ' height="' + f.height + '" ' : "") + ' style="' + (f.floatStyle && "center" != f.floatStyle ? "float:" +
                        f.floatStyle + ";" : "") + (f.border || "") + '" ' + (f.title ? ' title="' + f.title + '"' : "") + " /></p>", d.push(c);
                this.execCommand("insertHtml", d.join(""), !0)
            }
        }
    };
    UM.plugins.justify = function() {
        var a = this;
        g.each(["justifyleft", "justifyright", "justifycenter", "justifyfull"], function(b, d) {
            a.commands[d] = {
                execCommand: function(a) { return this.document.execCommand(a) },
                queryCommandValue: function(a) { var b = this.document.queryCommandValue(a); return !0 === b || "true" === b ? a.replace(/justify/, "") : "" },
                queryCommandState: function(a) {
                    return this.document.queryCommandState(a) ?
                        1 : 0
                }
            }
        })
    };
    UM.plugins.font = function() {
        var a = this,
            b = { forecolor: "forecolor", backcolor: "backcolor", fontsize: "fontsize", fontfamily: "fontname" },
            d = { forecolor: "color", backcolor: "background-color", fontsize: "font-size", fontfamily: "font-family" },
            c = { forecolor: "color", fontsize: "size", fontfamily: "face" };
        a.setOpt({
            fontfamily: [{ name: "songti", val: "\u5b8b\u4f53,SimSun" }, { name: "yahei", val: "\u5fae\u8f6f\u96c5\u9ed1,Microsoft YaHei" }, { name: "kaiti", val: "\u6977\u4f53,\u6977\u4f53_GB2312, SimKai" }, { name: "heiti", val: "\u9ed1\u4f53, SimHei" },
                { name: "lishu", val: "\u96b6\u4e66, SimLi" }, { name: "andaleMono", val: "andale mono" }, { name: "arial", val: "arial, helvetica,sans-serif" }, { name: "arialBlack", val: "arial black,avant garde" }, { name: "comicSansMs", val: "comic sans ms" }, { name: "impact", val: "impact,chicago" }, { name: "timesNewRoman", val: "times new roman" }, { name: "sans-serif", val: "sans-serif" }
            ],
            fontsize: [10, 12, 16, 18, 24, 32, 48]
        });
        a.addOutputRule(function(a) {
            n.each(a.getNodesByTagName("font"), function(a) {
                if ("font" == a.tagName) {
                    var b = [],
                        c;
                    for (c in a.attrs) switch (c) {
                        case "size":
                            var d =
                                a.attrs[c];
                            g.each({ 10: "1", 12: "2", 16: "3", 18: "4", 24: "5", 32: "6", 48: "7" }, function(a, b) { if (b == d) return d = a, !1 });
                            b.push("font-size:" + d + "px");
                            break;
                        case "color":
                            b.push("color:" + a.attrs[c]);
                            break;
                        case "face":
                            b.push("font-family:" + a.attrs[c]);
                            break;
                        case "style":
                            b.push(a.attrs[c])
                    }
                    a.attrs = { style: b.join(";") }
                }
                a.tagName = "span";
                "span" == a.parentNode.tagName && 1 == a.parentNode.children.length && (g.each(a.attrs, function(b, c) { a.parentNode.attrs[b] = "style" == b ? a.parentNode.attrs[b] + c : c }), a.parentNode.removeChild(a, !0))
            })
        });
        for (var f in b)(function(f) {
            a.commands[f] = {
                execCommand: function(a, c) {
                    if ("transparent" != c) {
                        var f = this.selection.getRange();
                        if (f.collapsed) { var e = g("<span></span>").css(d[a], c)[0];
                            f.insertNode(e).setStart(e, 0).setCursor() } else {
                            "fontsize" == a && (c = { 10: "1", 12: "2", 16: "3", 18: "4", 24: "5", 32: "6", 48: "7" }[(c + "").replace(/px/, "")]);
                            this.document.execCommand(b[a], !1, c);
                            m.gecko && g.each(this.$body.find("a"), function(a, b) {
                                var c = b.parentNode;
                                if (c.lastChild === c.firstChild && /FONT|SPAN/.test(c.tagName)) {
                                    var d = c.cloneNode(!1);
                                    d.innerHTML = b.innerHTML;
                                    g(b).html("").append(d).insertBefore(c);
                                    g(c).remove()
                                }
                            });
                            if (!m.ie) { var e = this.selection.getNative().getRangeAt(0).commonAncestorContainer,
                                    f = this.selection.getRange(),
                                    l = f.createBookmark(!0);
                                g(e).find("a").each(function(a, b) { var c = b.parentNode; "FONT" == c.nodeName && (c = c.cloneNode(!1), c.innerHTML = b.innerHTML, g(b).html("").append(c)) });
                                f.moveToBookmark(l).select() }
                            return !0
                        }
                    }
                },
                queryCommandValue: function(b) {
                    var f = a.selection.getStart(),
                        e = g(f).css(d[b]);
                    void 0 === e && (e = g(f).attr(c[b]));
                    return e ? n.fixColor(b, e).replace(/px/, "") : ""
                },
                queryCommandState: function(a) { return this.queryCommandValue(a) }
            }
        })(f)
    };
    UM.plugins.link = function() {
        this.setOpt("autourldetectinie", !1);
        m.ie && !1 === this.options.autourldetectinie && this.addListener("keyup", function(a, b) {
            var d = b.keyCode;
            if (13 == d || 32 == d) {
                var c = this.selection.getRange().startContainer;
                13 == d ? "P" == c.nodeName && (d = c.previousSibling) && 1 == d.nodeType && (d = d.lastChild) && "A" == d.nodeName && !d.getAttribute("_href") && k.remove(d, !0) : 32 == d && 3 == c.nodeType && /^\s$/.test(c.nodeValue) &&
                    (c = c.previousSibling) && "A" == c.nodeName && !c.getAttribute("_href") && k.remove(c, !0)
            }
        });
        this.addOutputRule(function(a) { g.each(a.getNodesByTagName("a"), function(a, d) { var b = d.getAttr("_href"); /^(ftp|https?|\/|file)/.test(b) || (b = "http://" + b);
                d.setAttr("href", b);
                d.setAttr("_href"); "" == d.getAttr("title") && d.setAttr("title") }) });
        this.addInputRule(function(a) { g.each(a.getNodesByTagName("a"), function(a, d) { d.setAttr("_href", d.getAttr("href")) }) });
        this.commands.link = {
            execCommand: function(a, b) {
                var d = this.selection.getRange();
                b._href && (b._href = n.unhtml(b._href, /[<">'](?:(amp|lt|quot|gt|#39|nbsp);)?/g));
                b.href && (b.href = n.unhtml(b.href, /[<">'](?:(amp|lt|quot|gt|#39|nbsp);)?/g));
                if (d.collapsed) { var c = d.startContainer;
                    (c = k.findParentByTagName(c, "a", !0)) ? (g(c).attr(b), d.selectNode(c).select()) : d.insertNode(g("<a>" + b.href + "</a>").attr(b)[0]).select() } else this.document.execCommand("createlink", !1, "_umeditor_link"), n.each(k.getElementsByTagName(this.body, "a", function(a) { return "_umeditor_link" == a.getAttribute("href") }), function(a) {
                    "_umeditor_link" ==
                    g(a).text() && g(a).text(b.href);
                    k.setAttributes(a, b);
                    d.selectNode(a).select()
                })
            },
            queryCommandState: function() { return this.queryCommandValue("link") ? 1 : 0 },
            queryCommandValue: function() { var a = this.selection.getStartElementPath(),
                    b;
                g.each(a, function(a, c) { if ("A" == c.nodeName) return b = c, !1 }); return b }
        };
        this.commands.unlink = { execCommand: function() { this.document.execCommand("unlink") } }
    };
    UM.commands.print = {
        execCommand: function() {
            var a = "editor_print_" + +new Date;
            g('<iframe src="" id="' + a + '" name="' + a + '" frameborder="0"></iframe>').attr("id",
                a).css({ width: "0px", height: "0px", overflow: "hidden", "float": "left", position: "absolute", top: "-10000px", left: "-10000px" }).appendTo(this.$container.find(".edui-dialog-container"));
            var b = window.open("", a, "").document;
            b.open();
            b.write("<html><head></head><body><div>" + this.getContent(null, null, !0) + "</div><script>setTimeout(function(){window.print();setTimeout(function(){window.parent.$('#" + a + "').remove();},100);},200);\x3c/script></body></html>");
            b.close()
        },
        notNeedUndo: 1
    };
    UM.plugins.paragraph = function() {
        this.setOpt("paragraph", { p: "", h1: "", h2: "", h3: "", h4: "", h5: "", h6: "" });
        this.commands.paragraph = { execCommand: function(a, b) { return this.document.execCommand("formatBlock", !1, "<" + b + ">") }, queryCommandValue: function() { try { var a = this.document.queryCommandValue("formatBlock") } catch (b) {} return a } }
    };
    UM.plugins.horizontal = function() {
        var a = this;
        a.commands.horizontal = {
            execCommand: function() {
                this.document.execCommand("insertHorizontalRule");
                var b = a.selection.getRange().txtToElmBoundary(!0),
                    d = b.startContainer;
                if (k.isBody(b.startContainer))(d =
                    b.startContainer.childNodes[b.startOffset]) || (d = g("<p></p>").appendTo(b.startContainer).html(m.ie ? "&nbsp;" : "<br/>")[0]), b.setStart(d, 0).setCursor();
                else {
                    for (; p.$inline[d.tagName] && d.lastChild === d.firstChild;) { var c = d.parentNode;
                        c.appendChild(d.firstChild);
                        c.removeChild(d);
                        d = c }
                    for (; p.$inline[d.tagName];) d = d.parentNode;
                    1 == d.childNodes.length && "HR" == d.lastChild.nodeName ? (c = d.lastChild, g(c).insertBefore(d), b.setStart(d, 0).setCursor()) : (c = g("hr", d)[0], k.breakParent(c, d), (d = c.previousSibling) && k.isEmptyBlock(d) &&
                        g(d).remove(), b.setStart(c.nextSibling, 0).setCursor())
                }
            }
        }
    };
    UM.commands.cleardoc = { execCommand: function() { var a = this,
                b = a.selection.getRange();
            a.body.innerHTML = "<p>" + (E ? "" : "<br/>") + "</p>";
            b.setStart(a.body.firstChild, 0).setCursor(!1, !0);
            setTimeout(function() { a.fireEvent("clearDoc") }, 0) } };
    UM.plugins.undo = function() {
        function a(a, b) { if (a.length != b.length) return 0; for (var c = 0, d = a.length; c < d; c++)
                if (a[c] != b[c]) return 0; return 1 }

        function b() { this.undoManger.save() }
        var d, c = this.options.maxUndoCount || 20,
            f = this.options.maxInputCount ||
            20,
            h = new RegExp(k.fillChar + "|</hr>", "gi"),
            e = { ol: 1, ul: 1, table: 1, tbody: 1, tr: 1, body: 1 },
            l = this.options.autoClearEmptyNode;
        this.undoManger = new function() {
            this.list = [];
            this.index = 0;
            this.hasRedo = this.hasUndo = !1;
            this.undo = function() { if (this.hasUndo)
                    if (this.list[this.index - 1] || 1 != this.list.length) { for (; this.list[this.index].content == this.list[this.index - 1].content;)
                            if (this.index--, 0 == this.index) return this.restore(0);
                        this.restore(--this.index) } else this.reset() };
            this.redo = function() {
                if (this.hasRedo) {
                    for (; this.list[this.index].content ==
                        this.list[this.index + 1].content;)
                        if (this.index++, this.index == this.list.length - 1) return this.restore(this.index);
                    this.restore(++this.index)
                }
            };
            this.restore = function() {
                var a = this.editor,
                    b = this.list[this.index],
                    c = UM.htmlparser(b.content.replace(h, ""));
                a.options.autoClearEmptyNode = !1;
                a.filterInputRule(c, !0);
                a.options.autoClearEmptyNode = l;
                a.body.innerHTML = c.toHtml();
                a.fireEvent("afterscencerestore");
                m.ie && n.each(k.getElementsByTagName(a.document, "td th caption p"), function(b) {
                    k.isEmptyNode(b) && k.fillNode(a.document,
                        b)
                });
                try { var d = (new x.Range(a.document, a.body)).moveToAddress(b.address); if (m.ie && d.collapsed && 1 == d.startContainer.nodeType) { var f = d.startContainer.childNodes[d.startOffset];
                        (!f || 1 == f.nodeType && p.$empty[f]) && d.insertNode(a.document.createTextNode(" ")).collapse(!0) } d.select(e[d.startContainer.nodeName.toLowerCase()]) } catch (M) {} this.update();
                this.clearKey();
                a.fireEvent("reset", !0)
            };
            this.getScene = function() {
                var a = this.editor,
                    b = a.selection.getRange().createAddress(!1, !0);
                a.fireEvent("beforegetscene");
                var c = UM.htmlparser(a.body.innerHTML, !0);
                a.options.autoClearEmptyNode = !1;
                a.filterOutputRule(c, !0);
                a.options.autoClearEmptyNode = l;
                c = c.toHtml();
                m.ie && (c = c.replace(/>&nbsp;</g, "><").replace(/\s*</g, "<").replace(/>\s*/g, ">"));
                a.fireEvent("aftergetscene");
                return { address: b, content: c }
            };
            this.save = function(b, f) {
                clearTimeout(d);
                var e = this.getScene(f),
                    l = this.list[this.index],
                    h;
                if (h = l && l.content == e.content) b ? l = 1 : (l = l.address, h = e.address, l = l.collapsed != h.collapsed ? 0 : a(l.startAddress, h.startAddress) && a(l.endAddress,
                    h.endAddress) ? 1 : 0), h = l;
                h || (this.list = this.list.slice(0, this.index + 1), this.list.push(e), this.list.length > c && this.list.shift(), this.index = this.list.length - 1, this.clearKey(), this.update())
            };
            this.update = function() { this.hasRedo = !!this.list[this.index + 1];
                this.hasUndo = !!this.list[this.index - 1] };
            this.reset = function() { this.list = [];
                this.index = 0;
                this.hasRedo = this.hasUndo = !1;
                this.clearKey() };
            this.clearKey = function() { v = 0 }
        };
        this.undoManger.editor = this;
        this.addListener("saveScene", function() {
            var a = Array.prototype.splice.call(arguments,
                1);
            this.undoManger.save.apply(this.undoManger, a)
        });
        this.addListener("beforeexeccommand", b);
        this.addListener("afterexeccommand", b);
        this.addListener("reset", function(a, b) { b || this.undoManger.reset() });
        this.commands.redo = this.commands.undo = { execCommand: function(a) { this.undoManger[a]() }, queryCommandState: function(a) { return this.undoManger["has" + ("undo" == a.toLowerCase() ? "Undo" : "Redo")] ? 0 : -1 }, notNeedUndo: 1 };
        var t = { 16: 1, 17: 1, 18: 1, 37: 1, 38: 1, 39: 1, 40: 1 },
            v = 0,
            r = !1;
        this.addListener("ready", function() {
            g(this.body).on("compositionstart",
                function() { r = !0 }).on("compositionend", function() { r = !1 })
        });
        this.addshortcutkey({ Undo: "ctrl+90", Redo: "ctrl+89,shift+ctrl+z" });
        var q = !0;
        this.addListener("keydown", function(a, b) {
            var c = this;
            if (!(t[b.keyCode || b.which] || b.ctrlKey || b.metaKey || b.shiftKey || b.altKey)) {
                var e = function(a) { a.selection.getRange().collapsed && a.fireEvent("contentchange");
                    a.undoManger.save(!1, !0);
                    a.fireEvent("selectionchange") };
                r || (c.selection.getRange().collapsed ? (0 == c.undoManger.list.length && c.undoManger.save(!0), clearTimeout(d),
                    d = setTimeout(function() { if (r) var a = setInterval(function() { r || (e(c), clearInterval(a)) }, 300);
                        else e(c) }, 200), v++, v >= f && e(c)) : (c.undoManger.save(!1, !0), q = !1))
            }
        });
        this.addListener("keyup", function(a, b) { t[b.keyCode || b.which] || b.ctrlKey || b.metaKey || b.shiftKey || b.altKey || r || q || (this.undoManger.save(!1, !0), q = !0) })
    };
    UM.plugins.paste = function() {
        function a(a) {
            var b = this.document;
            if (!b.getElementById("baidu_pastebin")) {
                var c = this.selection.getRange(),
                    d = c.createBookmark(),
                    l = b.createElement("div");
                l.id = "baidu_pastebin";
                m.webkit && l.appendChild(b.createTextNode(k.fillChar + k.fillChar));
                this.body.appendChild(l);
                d.start.style.display = "";
                l.style.cssText = "position:absolute;width:1px;height:1px;overflow:hidden;left:-1000px;white-space:nowrap;top:" + g(d.start).position().top + "px";
                c.selectNodeContents(l).select(!0);
                setTimeout(function() {
                    if (m.webkit)
                        for (var f = 0, e = b.querySelectorAll("#baidu_pastebin"), h; h = e[f++];)
                            if (k.isEmptyNode(h)) k.remove(h);
                            else { l = h; break }
                    try { l.parentNode.removeChild(l) } catch (q) {} c.moveToBookmark(d).select(!0);
                    a(l)
                }, 0)
            }
        }

        function b(a) {
            var b;
            if (a.firstChild) {
                var c = k.getElementsByTagName(a, "span");
                b = 0;
                for (var e; e = c[b++];) "_baidu_cut_start" != e.id && "_baidu_cut_end" != e.id || k.remove(e);
                if (m.webkit) {
                    e = a.querySelectorAll("div br");
                    for (b = 0; c = e[b++];) c = c.parentNode, "DIV" == c.tagName && 1 == c.childNodes.length && (c.innerHTML = "<p><br/></p>", k.remove(c));
                    c = a.querySelectorAll("#baidu_pastebin");
                    for (b = 0; e = c[b++];) {
                        var l = d.document.createElement("p");
                        for (e.parentNode.insertBefore(l, e); e.firstChild;) l.appendChild(e.firstChild);
                        k.remove(e)
                    }
                    e = a.querySelectorAll("meta");
                    for (b = 0; c = e[b++];) k.remove(c);
                    e = a.querySelectorAll("br");
                    for (b = 0; c = e[b++];) /^apple-/i.test(c.className) && k.remove(c)
                }
                if (m.gecko)
                    for (e = a.querySelectorAll("[_moz_dirty]"), b = 0; c = e[b++];) c.removeAttribute("_moz_dirty");
                if (!m.ie)
                    for (e = a.querySelectorAll("span.Apple-style-span"), b = 0; c = e[b++];) k.remove(c, !0);
                b = a.innerHTML;
                b = UM.filterWord(b);
                a = UM.htmlparser(b);
                d.options.filterRules && UM.filterNode(a, d.options.filterRules);
                d.filterInputRule(a);
                m.webkit && ((b = a.lastChild()) &&
                    "element" == b.type && "br" == b.tagName && a.removeChild(b), n.each(d.body.querySelectorAll("div"), function(a) { k.isEmptyBlock(a) && k.remove(a) }));
                b = { html: a.toHtml() };
                d.fireEvent("beforepaste", b, a);
                b.html && (d.execCommand("insertHtml", b.html, !0), d.fireEvent("afterpaste", b))
            }
        }
        var d = this;
        d.addListener("ready", function() {
            g(d.body).on("cut", function() {!d.selection.getRange().collapsed && d.undoManger && d.undoManger.save() }).on(m.ie || m.opera ? "keydown" : "paste", function(c) {
                (!m.ie && !m.opera || (c.ctrlKey || c.metaKey) && "86" ==
                    c.keyCode) && a.call(d, function(a) { b(a) })
            })
        })
    };
    UM.plugins.list = function() {
        this.setOpt({ insertorderedlist: { decimal: "", "lower-alpha": "", "lower-roman": "", "upper-alpha": "", "upper-roman": "" }, insertunorderedlist: { circle: "", disc: "", square: "" } });
        this.addInputRule(function(a) { n.each(a.getNodesByTagName("li"), function(a) { 0 == a.children.length && a.parentNode.removeChild(a) }) });
        this.commands.insertorderedlist = this.commands.insertunorderedlist = {
            execCommand: function(a) {
                this.document.execCommand(a);
                a = this.selection.getRange();
                var b = a.createBookmark(!0);
                this.$body.find("ol,ul").each(function(a, b) {
                    var c = b.parentNode;
                    "P" == c.tagName && c.lastChild === c.firstChild && (g(b).children().each(function(a, b) { var d = c.cloneNode(!1);
                        g(d).append(b.innerHTML);
                        g(b).html("").append(d) }), g(b).insertBefore(c), g(c).remove());
                    p.$inline[c.tagName] && ("SPAN" == c.tagName && g(b).children().each(function(a, b) {
                        var d = c.cloneNode(!1);
                        if ("P" != b.firstChild.nodeName) { for (; b.firstChild;) d.appendChild(b.firstChild);
                            g("<p></p>").appendTo(b).append(d) } else {
                            for (; b.firstChild;) d.appendChild(b.firstChild);
                            g(b.firstChild).append(d)
                        }
                    }), k.remove(c, !0))
                });
                a.moveToBookmark(b).select();
                return !0
            },
            queryCommandState: function(a) { return this.document.queryCommandState(a) }
        }
    };
    (function() {
        var a = {
            textarea: function(a, d) {
                var b = d.ownerDocument.createElement("textarea");
                b.style.cssText = "resize:none;border:0;padding:0;margin:0;overflow-y:auto;outline:0";
                m.ie && 8 > m.version && (b.style.width = d.offsetWidth + "px", b.style.height = d.offsetHeight + "px", d.onresize = function() {
                    b.style.width = d.offsetWidth + "px";
                    b.style.height = d.offsetHeight +
                        "px"
                });
                d.appendChild(b);
                return { container: b, setContent: function(a) { b.value = a }, getContent: function() { return b.value }, select: function() { var a;
                        m.ie ? (a = b.createTextRange(), a.collapse(!0), a.select()) : (b.setSelectionRange(0, 0), b.focus()) }, dispose: function() { d.removeChild(b);
                        d = b = d.onresize = null } }
            }
        };
        UM.plugins.source = function() {
            var b = this,
                d = !1,
                c;
            this.options.sourceEditor = "textarea";
            b.setOpt({ sourceEditorFirst: !1 });
            var f = b.getContent,
                h;
            b.commands.source = {
                execCommand: function() {
                    if (d = !d) {
                        h = b.selection.getRange().createAddress(!1, !0);
                        b.undoManger && b.undoManger.save(!0);
                        m.gecko && (b.body.contentEditable = !1);
                        b.body.style.cssText += ";position:absolute;left:-32768px;top:-32768px;";
                        b.fireEvent("beforegetcontent");
                        var e = UM.htmlparser(b.body.innerHTML);
                        b.filterOutputRule(e);
                        e.traversal(function(a) { if ("element" == a.type) switch (a.tagName) {
                                case "td":
                                case "th":
                                case "caption":
                                    a.children && 1 == a.children.length && "br" == a.firstChild().tagName && a.removeChild(a.firstChild()); break;
                                case "pre":
                                    a.innerText(a.innerText().replace(/&nbsp;/g, " ")) } });
                        b.fireEvent("aftergetcontent");
                        e = e.toHtml(!0);
                        c = a.textarea(b, b.body.parentNode);
                        c.setContent(e);
                        g(c.container).width(g(b.body).width() + parseInt(g(b.body).css("padding-left")) + parseInt(g(b.body).css("padding-right"))).height(g(b.body).height());
                        setTimeout(function() { c.select() });
                        b.getContent = function() { return c.getContent() || "<p>" + (m.ie ? "" : "<br/>") + "</p>" }
                    } else {
                        b.$body.css({ position: "", left: "", top: "" });
                        e = c.getContent() || "<p>" + (m.ie ? "" : "<br/>") + "</p>";
                        e = e.replace(RegExp("[\\r\\t\\n ]*</?(\\w+)\\s*(?:[^>]*)>",
                            "g"), function(a, b) { return b && !p.$inlineWithA[b.toLowerCase()] ? a.replace(/(^[\n\r\t ]*)|([\n\r\t ]*$)/g, "") : a.replace(/(^[\n\r\t]*)|([\n\r\t]*$)/g, "") });
                        b.setContent(e);
                        c.dispose();
                        c = null;
                        b.getContent = f;
                        b.body.firstChild || (b.body.innerHTML = "<p>" + (m.ie ? "" : "<br/>") + "</p>");
                        b.undoManger && b.undoManger.save(!0);
                        m.gecko && (b.body.contentEditable = !0);
                        try { b.selection.getRange().moveToAddress(h).select() } catch (t) {}
                    }
                    this.fireEvent("sourcemodechanged", d)
                },
                queryCommandState: function() { return d | 0 },
                notNeedUndo: 1
            };
            var e = b.queryCommandState;
            b.queryCommandState = function(a) { a = a.toLowerCase(); return d ? a in { source: 1, fullscreen: 1 } ? e.apply(this, arguments) : -1 : e.apply(this, arguments) }
        }
    })();
    UM.plugins.enterkey = function() {
        var a, b = this,
            d = b.options.enterTag;
        b.addListener("keyup", function(c, d) {
            if (13 == (d.keyCode || d.which)) {
                var f = b.selection.getRange(),
                    e = f.startContainer,
                    l;
                if (m.ie) b.fireEvent("saveScene", !0, !0);
                else {
                    if (/h\d/i.test(a)) {
                        if (m.gecko) k.findParentByTagName(e, "h1 h2 h3 h4 h5 h6 blockquote caption table".split(" "), !0) || (b.document.execCommand("formatBlock", !1, "<p>"), l = 1);
                        else if (1 == e.nodeType) { var e = b.document.createTextNode(""),
                                g;
                            f.insertNode(e); if (g = k.findParentByTagName(e, "div", !0)) { for (l = b.document.createElement("p"); g.firstChild;) l.appendChild(g.firstChild);
                                g.parentNode.insertBefore(l, g);
                                k.remove(g);
                                f.setStartBefore(e).setCursor();
                                l = 1 } k.remove(e) } b.undoManger && l && b.undoManger.save()
                    }
                    m.opera && f.select()
                }
            }
        });
        b.addListener("keydown", function(c, f) {
            if (13 == (f.keyCode || f.which))
                if (b.fireEvent("beforeenterkeydown")) k.preventDefault(f);
                else {
                    b.fireEvent("saveScene", !0, !0);
                    a = "";
                    var h = b.selection.getRange();
                    if (!h.collapsed) { var e = h.startContainer,
                            l = h.endContainer,
                            e = k.findParentByTagName(e, "td", !0),
                            l = k.findParentByTagName(l, "td", !0); if (e && l && e !== l || !e && l || e && !l) { f.preventDefault ? f.preventDefault() : f.returnValue = !1; return } }
                    "p" != d || m.ie || ((e = k.findParentByTagName(h.startContainer, "ol ul p h1 h2 h3 h4 h5 h6 blockquote caption".split(" "), !0)) || m.opera ? (a = e.tagName, "p" == e.tagName.toLowerCase() && m.gecko && k.removeDirtyAttr(e)) : (b.document.execCommand("formatBlock", !1, "<p>"), m.gecko && (h = b.selection.getRange(), (e = k.findParentByTagName(h.startContainer, "p", !0)) && k.removeDirtyAttr(e))))
                }
        });
        m.ie && b.addListener("setDisabled", function() { g(b.body).find("p").each(function(a, b) { k.isEmptyBlock(b) && (b.innerHTML = "&nbsp;") }) })
    };
    UM.commands.preview = {
        execCommand: function() {
            var a = window.open("", "_blank", "").document,
                b = this.getContent(null, null, !0),
                d = this.getOpt("UMEDITOR_HOME_URL"),
                d = -1 != b.indexOf("mathquill-embedded-latex") ? '<link rel="stylesheet" href="' + d + 'third-party/mathquill/mathquill.css"/><script src="' +
                d + 'third-party/jquery.min.js">\x3c/script><script src="' + d + 'third-party/mathquill/mathquill.min.js">\x3c/script>' : "";
            a.open();
            a.write("<html><head>" + d + "</head><body><div>" + b + "</div></body></html>");
            a.close()
        },
        notNeedUndo: 1
    };
    UM.plugins.basestyle = function() {
        var a = this;
        a.addshortcutkey({ Bold: "ctrl+66", Italic: "ctrl+73", Underline: "ctrl+shift+85", strikeThrough: "ctrl+shift+83" });
        a.addOutputRule(function(a) {
            g.each(a.getNodesByTagName("b i u strike s"), function(a, b) {
                switch (b.tagName) {
                    case "b":
                        b.tagName = "strong";
                        break;
                    case "i":
                        b.tagName = "em";
                        break;
                    case "u":
                        b.tagName = "span";
                        b.setStyle("text-decoration", "underline");
                        break;
                    case "s":
                    case "strike":
                        b.tagName = "span", b.setStyle("text-decoration", "line-through")
                }
            })
        });
        g.each("bold underline superscript subscript italic strikethrough".split(" "), function(b, d) {
            a.commands[d] = {
                execCommand: function(a) {
                    var b = this.selection.getRange();
                    return b.collapsed && 1 != this.queryCommandState(a) ? (a = this.document.createElement({
                        bold: "strong",
                        underline: "u",
                        superscript: "sup",
                        subscript: "sub",
                        italic: "em",
                        strikethrough: "strike"
                    }[a]), b.insertNode(a).setStart(a, 0).setCursor(!1), !0) : this.document.execCommand(a)
                },
                queryCommandState: function(a) {
                    if (m.gecko) return this.document.queryCommandState(a);
                    var b = this.selection.getStartElementPath(),
                        c = !1;
                    g.each(b, function(b, d) {
                        switch (a) {
                            case "bold":
                                if ("STRONG" == d.nodeName || "B" == d.nodeName) return c = 1, !1;
                                break;
                            case "underline":
                                if ("U" == d.nodeName || "SPAN" == d.nodeName && "underline" == g(d).css("text-decoration")) return c = 1, !1;
                                break;
                            case "superscript":
                                if ("SUP" ==
                                    d.nodeName) return c = 1, !1;
                                break;
                            case "subscript":
                                if ("SUB" == d.nodeName) return c = 1, !1;
                                break;
                            case "italic":
                                if ("EM" == d.nodeName || "I" == d.nodeName) return c = 1, !1;
                                break;
                            case "strikethrough":
                                if ("S" == d.nodeName || "STRIKE" == d.nodeName || "SPAN" == d.nodeName && "line-through" == g(d).css("text-decoration")) return c = 1, !1
                        }
                    });
                    return c
                }
            }
        })
    };
    UM.plugins.video = function() {
        function a(a, b, h, e, l, g) {
            return g ? '<embed type="application/x-shockwave-flash" class="edui-faked-video" pluginspage="http://www.macromedia.com/go/getflashplayer" src="' +
                a + '" width="' + b + '" height="' + h + '"' + (l ? ' style="float:' + l + '"' : "") + ' wmode="transparent" play="true" loop="false" menu="false" allowscriptaccess="never" allowfullscreen="true" >' : "<img " + (e ? 'id="' + e + '"' : "") + ' width="' + b + '" height="' + h + '" _url="' + a + '" class="edui-faked-video" src="' + d.options.UMEDITOR_HOME_URL + 'themes/default/images/spacer.gif" style="background:url(' + d.options.UMEDITOR_HOME_URL + "themes/default/images/videologo.gif) no-repeat center center; border:1px solid gray;" + (l ? "float:" + l + ";" :
                    "") + '" />'
        }

        function b(b, d) { n.each(b.getNodesByTagName(d ? "img" : "embed"), function(b) { if ("edui-faked-video" == b.getAttr("class")) { var c = a(d ? b.getAttr("_url") : b.getAttr("src"), b.getAttr("width"), b.getAttr("height"), null, b.getStyle("float") || "", d);
                    b.parentNode.replaceChild(UM.uNode.createElement(c), b) } }) }
        var d = this;
        d.addOutputRule(function(a) { b(a, !0) });
        d.addInputRule(function(a) { b(a) });
        d.commands.insertvideo = {
            execCommand: function(b, f) {
                f = n.isArray(f) ? f : [f];
                for (var c = [], e = 0, l, g = f.length; e < g; e++) l = f[e], l.url =
                    n.unhtml(l.url, /[<">'](?:(amp|lt|quot|gt|#39|nbsp);)?/g), c.push(a(l.url, l.width || 420, l.height || 280, "tmpVedio" + e, l.align, !1));
                d.execCommand("inserthtml", c.join(""), !0)
            },
            queryCommandState: function() { var a = d.selection.getRange().getClosedNode(); return a && "edui-faked-video" == a.className ? 1 : 0 }
        }
    };
    UM.plugins.selectall = function() {
        this.commands.selectall = {
            execCommand: function() {
                var a = this.body,
                    b = this.selection.getRange();
                b.selectNodeContents(a);
                k.isEmptyBlock(a) && (m.opera && a.firstChild && 1 == a.firstChild.nodeType &&
                    b.setStartAtFirst(a.firstChild), b.collapse(!0));
                b.select(!0)
            },
            notNeedUndo: 1
        };
        this.addshortcutkey({ selectAll: "ctrl+65" })
    };
    UM.plugins.removeformat = function() {
        this.setOpt({ removeFormatTags: "b,big,code,del,dfn,em,font,i,ins,kbd,q,samp,small,span,strike,strong,sub,sup,tt,u,var", removeFormatAttributes: "class,style,lang,width,height,align,hspace,valign" });
        this.commands.removeformat = {
            execCommand: function(a, b, d, c, f) {
                function h(a) {
                    if (3 == a.nodeType || "span" != a.tagName.toLowerCase()) return 0;
                    if (m.ie) {
                        var b = a.attributes;
                        if (b.length) { a = 0; for (var c = b.length; a < c; a++)
                                if (b[a].specified) return 0; return 1 }
                    }
                    return !a.attributes.length
                }

                function e(a) {
                    var b = a.createBookmark();
                    a.collapsed && a.enlarge(!0);
                    if (!f) { var c = k.findParentByTagName(a.startContainer, "a", !0);
                        c && a.setStartBefore(c);
                        (c = k.findParentByTagName(a.endContainer, "a", !0)) && a.setEndAfter(c) } v = a.createBookmark();
                    for (c = v.start;
                        (r = c.parentNode) && !k.isBlockElm(r);) k.breakParent(c, r), k.clearEmptySibling(c);
                    if (v.end) {
                        for (c = v.end;
                            (r = c.parentNode) && !k.isBlockElm(r);) k.breakParent(c,
                            r), k.clearEmptySibling(c);
                        for (var c = k.getNextDomNode(v.start, !1, q), e; c && c != v.end;) e = k.getNextDomNode(c, !0, q), p.$empty[c.tagName.toLowerCase()] || k.isBookmarkNode(c) || (l.test(c.tagName) ? d ? (k.removeStyle(c, d), h(c) && "text-decoration" != d && k.remove(c, !0)) : k.remove(c, !0) : p.$tableContent[c.tagName] || p.$list[c.tagName] || (k.removeAttributes(c, g), h(c) && k.remove(c, !0))), c = e
                    }
                    c = v.start.parentNode;
                    !k.isBlockElm(c) || p.$tableContent[c.tagName] || p.$list[c.tagName] || k.removeAttributes(c, g);
                    c = v.end.parentNode;
                    v.end &&
                        k.isBlockElm(c) && !p.$tableContent[c.tagName] && !p.$list[c.tagName] && k.removeAttributes(c, g);
                    a.moveToBookmark(v).moveToBookmark(b);
                    c = a.startContainer;
                    for (e = a.collapsed; 1 == c.nodeType && k.isEmptyNode(c) && p.$removeEmpty[c.tagName];) b = c.parentNode, a.setStartBefore(c), a.startContainer === a.endContainer && a.endOffset--, k.remove(c), c = b;
                    if (!e)
                        for (c = a.endContainer; 1 == c.nodeType && k.isEmptyNode(c) && p.$removeEmpty[c.tagName];) b = c.parentNode, a.setEndBefore(c), k.remove(c), c = b
                }
                var l = new RegExp("^(?:" + (b || this.options.removeFormatTags).replace(/,/g,
                        "|") + ")$", "i"),
                    g = d ? [] : (c || this.options.removeFormatAttributes).split(",");
                a = new x.Range(this.document);
                var v, r, q = function(a) { return 1 == a.nodeType };
                a = this.selection.getRange();
                a.collapsed || (e(a), a.select())
            }
        }
    };
    UM.plugins.keystrokes = function() {
        var a = this,
            b = !0;
        a.addListener("keydown", function(d, c) {
            var f = c.keyCode || c.which,
                h = a.selection.getRange();
            if (!(h.collapsed || c.ctrlKey || c.shiftKey || c.altKey || c.metaKey) && (65 <= f && 90 >= f || 48 <= f && 57 >= f || 96 <= f && 111 >= f || { 13: 1, 8: 1, 46: 1 }[f])) {
                var e = h.startContainer;
                k.isFillChar(e) &&
                    h.setStartBefore(e);
                e = h.endContainer;
                k.isFillChar(e) && h.setEndAfter(e);
                h.txtToElmBoundary();
                h.endContainer && 1 == h.endContainer.nodeType && (e = h.endContainer.childNodes[h.endOffset]) && k.isBr(e) && h.setEndAfter(e);
                if (0 == h.startOffset && (e = h.startContainer, k.isBoundaryNode(e, "firstChild") && (e = h.endContainer, h.endOffset == (3 == e.nodeType ? e.nodeValue.length : e.childNodes.length) && k.isBoundaryNode(e, "lastChild")))) {
                    a.fireEvent("saveScene");
                    a.body.innerHTML = "<p>" + (m.ie ? "" : "<br/>") + "</p>";
                    h.setStart(a.body.firstChild,
                        0).setCursor(!1, !0);
                    a._selectionChange();
                    return
                }
            }
            if (8 == f) {
                h = a.selection.getRange();
                b = h.collapsed;
                if (a.fireEvent("delkeydown", c)) return;
                var l;
                h.collapsed && h.inFillChar() && (e = h.startContainer, k.isFillChar(e) ? (h.setStartBefore(e).shrinkBoundary(!0).collapse(!0), k.remove(e)) : (e.nodeValue = e.nodeValue.replace(new RegExp("^" + k.fillChar), ""), h.startOffset--, h.collapse(!0).select(!0)));
                if (e = h.getClosedNode()) {
                    a.fireEvent("saveScene");
                    h.setStartBefore(e);
                    k.remove(e);
                    h.setCursor();
                    a.fireEvent("saveScene");
                    k.preventDefault(c);
                    return
                }
                if (!m.ie && (e = k.findParentByTagName(h.startContainer, "table", !0), l = k.findParentByTagName(h.endContainer, "table", !0), e && !l || !e && l || e !== l)) { c.preventDefault(); return } e = h.startContainer;
                h.collapsed && 1 == e.nodeType && (e = e.childNodes[h.startOffset - 1]) && 1 == e.nodeType && "BR" == e.tagName && (a.fireEvent("saveScene"), h.setStartBefore(e).collapse(!0), k.remove(e), h.select(), a.fireEvent("saveScene"));
                if (m.chrome && h.collapsed) {
                    for (; 0 == h.startOffset && !k.isEmptyBlock(h.startContainer);) h.setStartBefore(h.startContainer);
                    (e = h.startContainer.childNodes[h.startOffset - 1]) && "BR" == e.nodeName && (h.setStartBefore(e), a.fireEvent("saveScene"), g(e).remove(), h.setCursor(), a.fireEvent("saveScene"))
                }
            }
            if (m.gecko && 46 == f && (f = a.selection.getRange(), f.collapsed && (e = f.startContainer, k.isEmptyBlock(e)))) { for (f = e.parentNode; 1 == k.getChildCount(f) && !k.isBody(f);) e = f, f = f.parentNode;
                e === f.lastChild && c.preventDefault() }
        });
        a.addListener("keyup", function(a, c) {
            var d;
            if (8 == (c.keyCode || c.which) && !this.fireEvent("delkeyup")) {
                d = this.selection.getRange();
                if (d.collapsed) { var h; if ((h = k.findParentByTagName(d.startContainer, "h1 h2 h3 h4 h5 h6".split(" "), !0)) && k.isEmptyBlock(h)) { var e = h.previousSibling; if (e && "TABLE" != e.nodeName) { k.remove(h);
                            d.setStartAtLast(e).setCursor(!1, !0); return } if ((e = h.nextSibling) && "TABLE" != e.nodeName) { k.remove(h);
                            d.setStartAtFirst(e).setCursor(!1, !0); return } } k.isBody(d.startContainer) && (h = k.createElement(this.document, "p", { innerHTML: m.ie ? k.fillChar : "<br/>" }), d.insertNode(h).setStart(h, 0).setCursor(!1, !0)) }!b && (3 == d.startContainer.nodeType ||
                    1 == d.startContainer.nodeType && k.isEmptyBlock(d.startContainer)) && (m.ie ? (h = d.document.createElement("span"), d.insertNode(h).setStartBefore(h).collapse(!0), d.select(), k.remove(h)) : d.select())
            }
        })
    };
    UM.plugins.autosave = function() {
        function a(a) { var e;
            20 > new Date - d || (a.hasContents() ? (d = new Date, a._saveFlag = null, e = b.body.innerHTML, !1 !== a.fireEvent("beforeautosave", { content: e }) && (f.saveLocalData(c, e), a.fireEvent("afterautosave", { content: e }))) : c && f.removeItem(c)) }
        var b = this,
            d = new Date,
            c = null;
        b.setOpt("saveInterval",
            500);
        var f = UM.LocalStorage = function() {
            function a() {
                var a = document.createElement("div");
                a.style.display = "none";
                if (!a.addBehavior) return null;
                a.addBehavior("#default#userdata");
                return {
                    getItem: function(b) { var d = null; try { document.body.appendChild(a), a.load(c), d = a.getAttribute(b), document.body.removeChild(a) } catch (q) {} return d },
                    setItem: function(b, d) { document.body.appendChild(a);
                        a.setAttribute(b, d);
                        a.save(c);
                        document.body.removeChild(a) },
                    removeItem: function(b) {
                        document.body.appendChild(a);
                        a.removeAttribute(b);
                        a.save(c);
                        document.body.removeChild(a)
                    }
                }
            }
            var b = window.localStorage || a() || null,
                c = "localStorage";
            return { saveLocalData: function(a, c) { return b && c ? (b.setItem(a, c), !0) : !1 }, getLocalData: function(a) { return b ? b.getItem(a) : null }, removeItem: function(a) { b && b.removeItem(a) } }
        }();
        b.addListener("ready", function() { var a;
            a = b.key ? b.key + "-drafts-data" : (b.container.parentNode.id || "ue-common") + "-drafts-data";
            c = (location.protocol + location.host + location.pathname).replace(/[.:\/]/g, "_") + a });
        b.addListener("contentchange",
            function() { c && (b._saveFlag && window.clearTimeout(b._saveFlag), 0 < b.options.saveInterval ? b._saveFlag = window.setTimeout(function() { a(b) }, b.options.saveInterval) : a(b)) });
        b.commands.clearlocaldata = { execCommand: function(a, b) { c && f.getLocalData(c) && f.removeItem(c) }, notNeedUndo: !0, ignoreContentChange: !0 };
        b.commands.getlocaldata = { execCommand: function(a, b) { return c ? f.getLocalData(c) || "" : "" }, notNeedUndo: !0, ignoreContentChange: !0 };
        b.commands.drafts = {
            execCommand: function(a, d) {
                c && (b.body.innerHTML = f.getLocalData(c) ||
                    "<p>" + (m.ie ? "&nbsp;" : "<br/>") + "</p>", b.focus(!0))
            },
            queryCommandState: function() { return c ? null === f.getLocalData(c) ? -1 : 0 : -1 },
            notNeedUndo: !0,
            ignoreContentChange: !0
        }
    };
    UM.plugins.autoupload = function() {
        var a = this;
        a.setOpt("pasteImageEnabled", !0);
        a.setOpt("dropFileEnabled", !0);
        var b = function(b, c) {
            var d = new FormData;
            d.append(c.options.imageFieldName || "upfile", b, b.name || "blob." + b.type.substr(6));
            d.append("type", "ajax");
            var h = new XMLHttpRequest;
            h.open("post", a.options.imageUrl, !0);
            h.setRequestHeader("X-Requested-With",
                "XMLHttpRequest");
            h.addEventListener("load", function(b) { try { var d = eval("(" + b.target.response + ")").url,
                        e = a.options.imagePath + d;
                    c.execCommand("insertimage", { src: e, _src: e }) } catch (v) {} });
            h.send(d)
        };
        a.addListener("ready", function() {
            if (window.FormData && window.FileReader) {
                var d = function(c) {
                    var d = !1;
                    "paste" == c.type ? (c = c.originalEvent, c = c.clipboardData && c.clipboardData.items && 1 == c.clipboardData.items.length && /^image\//.test(c.clipboardData.items[0].type) ? c.clipboardData.items : null) : (c = c.originalEvent, c = c.dataTransfer &&
                        c.dataTransfer.files ? c.dataTransfer.files : null);
                    if (c) { for (var h = c.length, e; h--;) e = c[h], e.getAsFile && (e = e.getAsFile()), e && 0 < e.size && /image\/\w+/i.test(e.type) && (b(e, a), d = !0); if (d) return !1 }
                };
                a.getOpt("pasteImageEnabled") && a.$body.on("paste", d);
                a.getOpt("dropFileEnabled") && a.$body.on("drop", d);
                a.$body.on("dragover", function(a) { if ("Files" == a.originalEvent.dataTransfer.types[0]) return !1 })
            }
        })
    };
    UM.plugins.formula = function() {
        function a() { return d.$body.find("iframe.edui-formula-active")[0] || null }

        function b() {
            var b =
                a();
            b && b.contentWindow.formula.blur()
        }
        var d = this;
        d.addInputRule(function(a) { g.each(a.getNodesByTagName("span"), function(a, b) { if (b.hasClass("mathquill-embedded-latex")) { for (var c, f = ""; c = b.firstChild();) f += c.data, b.removeChild(c);
                    b.tagName = "iframe";
                    b.setAttr({ frameborder: "0", src: d.getOpt("UMEDITOR_HOME_URL") + "dialogs/formula/formula.html", "data-latex": n.unhtml(f) }) } }) });
        d.addOutputRule(function(a) {
            g.each(a.getNodesByTagName("iframe"), function(a, b) {
                b.hasClass("mathquill-embedded-latex") && (b.tagName =
                    "span", b.appendChild(UM.uNode.createText(b.getAttr("data-latex"))), b.setAttr({ frameborder: "", src: "", "data-latex": "" }))
            })
        });
        d.addListener("click", function() { b() });
        d.addListener("afterexeccommand", function(a, d) { "formula" != d && b() });
        d.commands.formula = {
            execCommand: function(b, f) {
                var c = a();
                c ? c.contentWindow.formula.insertLatex(f) : (d.execCommand("inserthtml", '<span class="mathquill-embedded-latex">' + f + "</span>"), m.ie && m.ie9below && setTimeout(function() {
                    var a = d.selection.getRange(),
                        b = a.startContainer;
                    1 != b.nodeType ||
                        b.childNodes[a.startOffset] || (a.insertNode(d.document.createTextNode(" ")), a.setCursor())
                }, 100))
            },
            queryCommandState: function(a) { return 0 },
            queryCommandValue: function(b) { return (b = a()) && b.contentWindow.formula.getLatex() }
        }
    };
    UM.plugins.xssFilter = function() {
        function a(a) { var b = a.tagName,
                c = a.attrs; if (!d.hasOwnProperty(b)) return a.parentNode.removeChild(a), !1;
            UM.utils.each(c, function(c, e) {-1 === UM.utils.indexOf(d[b], e) && a.setAttr(e) }) }
        var b = UMEDITOR_CONFIG,
            d = b.whiteList;
        d && b.xssFilterRules && (this.options.filterRules =
            function() { var b = {};
                UM.utils.each(d, function(c, d) { b[d] = function(b) { return a(b) } }); return b }());
        var c = [];
        UM.utils.each(d, function(a, b) { c.push(b) });
        d && b.inputXssFilter && this.addInputRule(function(b) { b.traversal(function(b) { if ("element" !== b.type) return !1;
                a(b) }) });
        d && b.outputXssFilter && this.addOutputRule(function(b) { b.traversal(function(b) { if ("element" !== b.type) return !1;
                a(b) }) })
    };
    (function(a) {
        function b(b, c, d) {
            b.prototype = a.extend2(a.extend({}, c), (UM.ui[d] || f).prototype, !0);
            b.prototype.supper = (UM.ui[d] ||
                f).prototype;
            UM.ui[d] && UM.ui[d].prototype.defaultOpt && (b.prototype.defaultOpt = a.extend({}, UM.ui[d].prototype.defaultOpt, b.prototype.defaultOpt || {}));
            return b
        }

        function d(b, c) { a["edui" + c] = b;
            a.fn["edui" + c] = function(c) { var d, e = Array.prototype.slice.call(arguments, 1);
                this.each(function(f, l) { var g = a(l),
                        h = g.edui();
                    h || (b(c && a.isPlainObject(c) ? c : {}, g), g.edui(h)); if ("string" == a.type(c))
                        if ("this" == c) d = h;
                        else { d = h[c].apply(h, e); if (d !== h && void 0 !== d) return !1;
                            d = null } }); return null !== d ? d : this } } a.parseTmpl = function(a,
            b) { var c = "var __p=[],print=function(){__p.push.apply(__p,arguments);};with(obj||{}){__p.push('" + a.replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/<%=([\s\S]+?)%>/g, function(a, b) { return "',obj." + b.replace(/\\'/g, "'") + ",'" }).replace(/<%([\s\S]+?)%>/g, function(a, b) { return "');" + b.replace(/\\'/g, "'").replace(/[\r\n\t]/g, " ") + "__p.push('" }).replace(/\r/g, "\\r").replace(/\n/g, "\\n").replace(/\t/g, "\\t") + "');}return __p.join('');",
                c = new Function("obj", c); return b ? c(b) : c };
        a.extend2 = function(b, c) {
            for (var d =
                    arguments, e = "boolean" == a.type(d[d.length - 1]) ? d[d.length - 1] : !1, f = "boolean" == a.type(d[d.length - 1]) ? d.length - 1 : d.length, l = 1; l < f; l++) { var g = d[l],
                    h; for (h in g) e && b.hasOwnProperty(h) || (b[h] = g[h]) }
            return b
        };
        a.IE6 = !!window.ActiveXObject && 6 == parseFloat(navigator.userAgent.match(/msie (\d+)/i)[1]);
        var c = [],
            f = function() {};
        f.prototype = {
            on: function(b, c) { this.root().on(b, a.proxy(c, this)); return this },
            off: function(b, c) { this.root().off(b, a.proxy(c, this)); return this },
            trigger: function(a, b) {
                return !1 === this.root().trigger(a,
                    b) ? !1 : this
            },
            root: function(a) { return this._$el || (this._$el = a) },
            destroy: function() {},
            data: function(a, b) { return void 0 !== b ? (this.root().data("edui" + a, b), this) : this.root().data("edui" + a) },
            register: function(b, d, f) { c.push({ evtname: b, $els: a.isArray(d) ? d : [d], handler: a.proxy(f, d) }) }
        };
        a.fn.edui = function(a) { return a ? this.data("eduiwidget", a) : this.data("eduiwidget") };
        var g = 1;
        UM.ui = {
            define: function(c, f, h) {
                var e = UM.ui[c] = b(function(b, d) {
                    var f = function() {};
                    a.extend(f.prototype, e.prototype, { guid: c + g++, widgetName: c });
                    f = new f;
                    if ("string" == a.type(b)) return f.init && f.init({}), f.root().edui(f), f.root().find("a").click(function(a) { a.preventDefault() }), f.root()["edui" + c].apply(f.root(), arguments);
                    d && f.root(d);
                    f.init && f.init(!b || a.isPlainObject(b) ? a.extend2(b || {}, f.defaultOpt || {}, !0) : b);
                    try { f.root().find("a").click(function(a) { a.preventDefault() }) } catch (A) {}
                    return f.root().edui(f)
                }, f, h);
                d(e, c)
            }
        };
        a(function() {
            a(document).on("click mouseup mousedown dblclick mouseover", function(b) {
                a.each(c, function(c, d) {
                    d.evtname == b.type &&
                        a.each(d.$els, function(c, f) { f[0] === b.target || a.contains(f[0], b.target) || d.handler(b) })
                })
            })
        })
    })(jQuery);
    UM.ui.define("button", {
        tpl: '<<%if : !${texttype}%>div class="edui-btn edui-btn-${icon} <%if : ${name}%>edui-btn-name-${name}<%/if%>" unselectable="on" onmousedown="return false" <%else%>a class="edui-text-btn"<%/if%><% if: ${title} %> data-original-title="${title}" <%/if%>> <% if: ${icon} %><div unselectable="on" class="edui-icon-${icon} edui-icon"></div><%/if%><%if: ${text} %><span unselectable="on" onmousedown="return false" class="edui-button-label">${text}</span><%/if%><%if: ${caret} && ${text}%><span class="edui-button-spacing"></span><%/if%><% if: ${caret} %><span unselectable="on" onmousedown="return false" class="edui-caret"></span><%/if%></<%if: !${texttype}%>div<%else%>a<%/if%>>',
        defaultOpt: { text: "", title: "", icon: "", width: "", caret: !1, texttype: !1, click: function() {} },
        init: function(a) { var b = this;
            b.root(g(UM.utils.render(b.tpl, a))).click(function(d) { b.wrapclick(a.click, d) });
            b.root().hover(function() { b.root().hasClass("edui-disabled") || b.root().toggleClass("edui-hover") }); return b },
        wrapclick: function(a, b) { this.disabled() || (this.root().trigger("wrapclick"), g.proxy(a, this, b)()); return this },
        label: function(a) {
            if (void 0 === a) return this.root().find(".edui-button-label").text();
            this.root().find(".edui-button-label").text(a);
            return this
        },
        disabled: function(a) { if (void 0 === a) return this.root().hasClass("edui-disabled");
            this.root().toggleClass("edui-disabled", a);
            this.root().hasClass("edui-disabled") && this.root().removeClass("edui-hover"); return this },
        active: function(a) { if (void 0 === a) return this.root().hasClass("edui-active");
            this.root().toggleClass("edui-active", a); return this },
        mergeWith: function(a) {
            var b = this;
            b.data("$mergeObj", a);
            a.edui().data("$mergeObj", b.root());
            g.contains(document.body, a[0]) || a.appendTo(b.root());
            b.on("click",
                function() { b.wrapclick(function() { a.edui().show() }) }).register("click", b.root(), function(b) { a.hide() })
        }
    });
    (function() { UM.ui.define("toolbar", { tpl: '<div class="edui-toolbar"  ><div class="edui-btn-toolbar" unselectable="on" onmousedown="return false"  ></div></div>', init: function() { var a = this.root(g(this.tpl));
                this.data("$btnToolbar", a.find(".edui-btn-toolbar")) }, appendToBtnmenu: function(a) { var b = this.data("$btnToolbar");
                a = g.isArray(a) ? a : [a];
                g.each(a, function(a, c) { b.append(c) }) } }) })();
    UM.ui.define("menu", {
        show: function(a, b, d, c, f) { d = d || "position";!1 !== this.trigger("beforeshow") && (this.root().css(g.extend({ display: "block" }, a ? { top: a[d]().top + ("right" == b ? 0 : a.outerHeight()) - (c || 0), left: a[d]().left + ("right" == b ? a.outerWidth() : 0) - (f || 0) } : {})), this.trigger("aftershow")) },
        hide: function(a) { var b;!1 !== this.trigger("beforehide") && ((b = this.root().data("parentmenu")) && (b.data("parentmenu") || a) && b.edui().hide(), this.root().css("display", "none"), this.trigger("afterhide")) },
        attachTo: function(a) {
            var b = this;
            a.data("$mergeObj") ||
                (a.data("$mergeObj", b.root()), a.on("wrapclick", function(a) { b.show() }), b.register("click", a, function(a) { b.hide() }), b.data("$mergeObj", a))
        }
    });
    UM.ui.define("dropmenu", {
        tmpl: '<ul class="edui-dropdown-menu" aria-labelledby="dropdownMenu" ><%for: ${data} as ${ci}%><%if: ${ci.divider}%><li class="edui-divider"></li><%else%><li class="${ci.active} || ${ci.disabled}" data-value="${ci.value}"><a href="#" tabindex="-1"><em class="edui-dropmenu-checkbox"><i class="edui-icon-ok"></i></em>${ci.label}</a></li><%/if%><%/for%></ul>',
        defaultOpt: { data: [], click: function() {} },
        init: function(a) { var b = this,
                d = { click: 1, mouseover: 1, mouseout: 1 };
            this.root(g(UM.utils.render(this.tmpl, a))).on("click", 'li[class!="edui-disabled edui-divider edui-dropdown-submenu"]', function(c) { g.proxy(a.click, b, c, g(this).data("value"), g(this))() }).find("li").each(function(c, f) { var h = g(this); if (!h.hasClass("edui-disabled edui-divider edui-dropdown-submenu")) { var e = a.data[c];
                    g.each(d, function(a) { e[a] && h[a](function(c) { g.proxy(e[a], f)(c, e, b.root) }) }) } }) },
        disabled: function(a) {
            g("li[class!=edui-divider]",
                this.root()).each(function() { var b = g(this);!0 === a ? b.addClass("edui-disabled") : g.isFunction(a) ? b.toggleClass("edui-disabled", a(li)) : b.removeClass("edui-disabled") })
        },
        val: function(a) { var b;
            g('li[class!="edui-divider edui-disabled edui-dropdown-submenu"]', this.root()).each(function() { var d = g(this); if (void 0 === a) { if (d.find("em.edui-dropmenu-checked").length) return b = d.data("value"), !1 } else d.find("em").toggleClass("edui-dropmenu-checked", d.data("value") == a) }); if (void 0 === a) return b },
        addSubmenu: function(a,
            b, d) { d = d || 0; var c = g("li[class!=edui-divider]", this.root());
            a = g('<li class="edui-dropdown-submenu"><a tabindex="-1" href="#">' + a + "</a></li>").append(b);
            0 <= d && d < c.length ? a.insertBefore(c[d]) : 0 > d ? a.insertBefore(c[0]) : d >= c.length && a.appendTo(c) }
    }, "menu");
    UM.ui.define("splitbutton", {
        tpl: '<div class="edui-splitbutton <%if: ${name}%>edui-splitbutton-${name}<%/if%>"  unselectable="on" <%if: ${title}%>data-original-title="${title}"<%/if%>><div class="edui-btn"  unselectable="on" ><%if: ${icon}%><div  unselectable="on" class="edui-icon-${icon} edui-icon"></div><%/if%><%if: ${text}%>${text}<%/if%></div><div  unselectable="on" class="edui-btn edui-dropdown-toggle" ><div  unselectable="on" class="edui-caret"></div></div></div>',
        defaultOpt: { text: "", title: "", click: function() {} },
        init: function(a) { var b = this;
            b.root(g(UM.utils.render(b.tpl, a)));
            b.root().find(".edui-btn:first").click(function(d) { b.disabled() || g.proxy(a.click, b)() });
            b.root().find(".edui-dropdown-toggle").click(function() { b.disabled() || b.trigger("arrowclick") });
            b.root().hover(function() { b.root().hasClass("edui-disabled") || b.root().toggleClass("edui-hover") }); return b },
        wrapclick: function(a, b) { this.disabled() || g.proxy(a, this, b)(); return this },
        disabled: function(a) {
            if (void 0 ===
                a) return this.root().hasClass("edui-disabled");
            this.root().toggleClass("edui-disabled", a).find(".edui-btn").toggleClass("edui-disabled", a);
            return this
        },
        active: function(a) { if (void 0 === a) return this.root().hasClass("edui-active");
            this.root().toggleClass("edui-active", a).find(".edui-btn:first").toggleClass("edui-active", a); return this },
        mergeWith: function(a) {
            var b = this;
            b.data("$mergeObj", a);
            a.edui().data("$mergeObj", b.root());
            g.contains(document.body, a[0]) || a.appendTo(b.root());
            b.root().delegate(".edui-dropdown-toggle",
                "click",
                function() { b.wrapclick(function() { a.edui().show() }) });
            b.register("click", b.root().find(".edui-dropdown-toggle"), function(b) { a.hide() })
        }
    });
    UM.ui.define("colorsplitbutton", {
        tpl: '<div class="edui-splitbutton <%if : ${name}%>edui-splitbutton-${name}<%/if%>"  unselectable="on" <%if: ${title}%>data-original-title="${title}"<%/if%>><div class="edui-btn"  unselectable="on" ><%if: ${icon}%><div unselectable="on" class="edui-icon-${icon} edui-icon"></div><%/if%><div class="edui-splitbutton-color-label" <%if: ${color}%>style="background: ${color}"<%/if%>></div><%if: ${text}%>${text}<%/if%></div><div  unselectable="on" class="edui-btn edui-dropdown-toggle" ><div  unselectable="on" class="edui-caret"></div></div></div>',
        defaultOpt: { color: "" },
        init: function(a) { this.supper.init.call(this, a) },
        colorLabel: function() { return this.root().find(".edui-splitbutton-color-label") }
    }, "splitbutton");
    UM.ui.define("popup", {
        tpl: '<div class="edui-dropdown-menu edui-popup"<%if:!${stopprop}%>onmousedown="return false"<%/if%>><div class="edui-popup-body" unselectable="on" onmousedown="return false">${subtpl|raw}</div><div class="edui-popup-caret"></div></div>',
        defaultOpt: { stopprop: !1, subtpl: "", width: "", height: "" },
        init: function(a) {
            this.root(g(UM.utils.render(this.tpl,
                a)));
            return this
        },
        mergeTpl: function(a) { return UM.utils.render(this.tpl, { subtpl: a }) },
        show: function(a, b) {
            b || (b = {});
            var d = b.fnname || "position";
            !1 !== this.trigger("beforeshow") && (this.root().css(g.extend({ display: "block" }, a ? { top: a[d]().top + ("right" == b.dir ? 0 : a.outerHeight()) - (b.offsetTop || 0), left: a[d]().left + ("right" == b.dir ? a.outerWidth() : 0) - (b.offsetLeft || 0), position: "absolute" } : {})), this.root().find(".edui-popup-caret").css({ top: b.caretTop || 0, left: b.caretLeft || 0, position: "absolute" }).addClass(b.caretDir ||
                "up"), this.trigger("aftershow"))
        },
        hide: function() { this.root().css("display", "none");
            this.trigger("afterhide") },
        attachTo: function(a, b) { var d = this;
            a.data("$mergeObj") || (a.data("$mergeObj", d.root()), a.on("wrapclick", function(c) { d.show(a, b) }), d.register("click", a, function(a) { d.hide() }), d.data("$mergeObj", a)) },
        getBodyContainer: function() { return this.root().find(".edui-popup-body") }
    });
    UM.ui.define("scale", {
        tpl: '<div class="edui-scale" unselectable="on"><span class="edui-scale-hand0"></span><span class="edui-scale-hand1"></span><span class="edui-scale-hand2"></span><span class="edui-scale-hand3"></span><span class="edui-scale-hand4"></span><span class="edui-scale-hand5"></span><span class="edui-scale-hand6"></span><span class="edui-scale-hand7"></span></div>',
        defaultOpt: { $doc: g(document), $wrap: g(document) },
        init: function(a) { a.$doc && (this.defaultOpt.$doc = a.$doc);
            a.$wrap && (this.defaultOpt.$wrap = a.$wrap);
            this.root(g(UM.utils.render(this.tpl, a)));
            this.initStyle();
            this.startPos = this.prePos = { x: 0, y: 0 };
            this.dragId = -1; return this },
        initStyle: function() { n.cssRule("edui-style-scale", ".edui-scale{display:none;position:absolute;border:1px solid #38B2CE;cursor:hand;}.edui-scale span{position:absolute;left:0;top:0;width:7px;height:7px;overflow:hidden;font-size:0px;display:block;background-color:#3C9DD0;}.edui-scale .edui-scale-hand0{cursor:nw-resize;top:0;margin-top:-4px;left:0;margin-left:-4px;}.edui-scale .edui-scale-hand1{cursor:n-resize;top:0;margin-top:-4px;left:50%;margin-left:-4px;}.edui-scale .edui-scale-hand2{cursor:ne-resize;top:0;margin-top:-4px;left:100%;margin-left:-3px;}.edui-scale .edui-scale-hand3{cursor:w-resize;top:50%;margin-top:-4px;left:0;margin-left:-4px;}.edui-scale .edui-scale-hand4{cursor:e-resize;top:50%;margin-top:-4px;left:100%;margin-left:-3px;}.edui-scale .edui-scale-hand5{cursor:sw-resize;top:100%;margin-top:-3px;left:0;margin-left:-4px;}.edui-scale .edui-scale-hand6{cursor:s-resize;top:100%;margin-top:-3px;left:50%;margin-left:-4px;}.edui-scale .edui-scale-hand7{cursor:se-resize;top:100%;margin-top:-3px;left:100%;margin-left:-3px;}") },
        _eventHandler: function(a) {
            var b = this.defaultOpt.$doc;
            switch (a.type) {
                case "mousedown":
                    var d = a.target || a.srcElement; - 1 != d.className.indexOf("edui-scale-hand") && (this.dragId = d.className.slice(-1), this.startPos.x = this.prePos.x = a.clientX, this.startPos.y = this.prePos.y = a.clientY, b.bind("mousemove", g.proxy(this._eventHandler, this)));
                    break;
                case "mousemove":
                    -1 != this.dragId && (this.updateContainerStyle(this.dragId, { x: a.clientX - this.prePos.x, y: a.clientY - this.prePos.y }), this.prePos.x = a.clientX, this.prePos.y = a.clientY,
                        this.updateTargetElement());
                    break;
                case "mouseup":
                    -1 != this.dragId && (this.dragId = -1, this.updateTargetElement(), this.data("$scaleTarget").parent() && this.attachTo(this.data("$scaleTarget"))), b.unbind("mousemove", g.proxy(this._eventHandler, this))
            }
        },
        updateTargetElement: function() { var a = this.root(),
                b = this.data("$scaleTarget");
            b.css({ width: a.width(), height: a.height() });
            this.attachTo(b) },
        updateContainerStyle: function(a, b) {
            var d = this.root(),
                c, f = [
                    [0, 0, -1, -1],
                    [0, 0, 0, -1],
                    [0, 0, 1, -1],
                    [0, 0, -1, 0],
                    [0, 0, 1, 0],
                    [0, 0, -1,
                        1
                    ],
                    [0, 0, 0, 1],
                    [0, 0, 1, 1]
                ];
            0 != f[a][0] && (c = parseInt(d.offset().left) + b.x, d.css("left", this._validScaledProp("left", c)));
            0 != f[a][1] && (c = parseInt(d.offset().top) + b.y, d.css("top", this._validScaledProp("top", c)));
            0 != f[a][2] && (c = d.width() + f[a][2] * b.x, d.css("width", this._validScaledProp("width", c)));
            0 != f[a][3] && (c = d.height() + f[a][3] * b.y, d.css("height", this._validScaledProp("height", c)))
        },
        _validScaledProp: function(a, b) {
            var d = this.root(),
                c = this.defaultOpt.$doc,
                f = function(a, c, d) { return a + c > d ? d - c : b };
            b = isNaN(b) ?
                0 : b;
            switch (a) {
                case "left":
                    return 0 > b ? 0 : f(b, d.width(), c.width());
                case "top":
                    return 0 > b ? 0 : f(b, d.height(), c.height());
                case "width":
                    return 0 >= b ? 1 : f(b, d.offset().left, c.width());
                case "height":
                    return 0 >= b ? 1 : f(b, d.offset().top, c.height()) }
        },
        show: function(a) { a && this.attachTo(a);
            this.root().bind("mousedown", g.proxy(this._eventHandler, this));
            this.defaultOpt.$doc.bind("mouseup", g.proxy(this._eventHandler, this));
            this.root().show();
            this.trigger("aftershow") },
        hide: function() {
            this.root().unbind("mousedown", g.proxy(this._eventHandler,
                this));
            this.defaultOpt.$doc.unbind("mouseup", g.proxy(this._eventHandler, this));
            this.root().hide();
            this.trigger("afterhide")
        },
        attachTo: function(a) { var b = a.offset(),
                d = this.root(),
                c = this.defaultOpt.$wrap,
                f = c.offset();
            this.data("$scaleTarget", a);
            this.root().css({ position: "absolute", width: a.width(), height: a.height(), left: b.left - f.left - parseInt(c.css("border-left-width")) - parseInt(d.css("border-left-width")), top: b.top - f.top - parseInt(c.css("border-top-width")) - parseInt(d.css("border-top-width")) }) },
        getScaleTarget: function() { return this.data("$scaleTarget")[0] }
    });
    UM.ui.define("colorpicker", {
        tpl: function(a) {
            for (var b = "ffffff 000000 eeece1 1f497d 4f81bd c0504d 9bbb59 8064a2 4bacc6 f79646 f2f2f2 7f7f7f ddd9c3 c6d9f0 dbe5f1 f2dcdb ebf1dd e5e0ec dbeef3 fdeada d8d8d8 595959 c4bd97 8db3e2 b8cce4 e5b9b7 d7e3bc ccc1d9 b7dde8 fbd5b5 bfbfbf 3f3f3f 938953 548dd4 95b3d7 d99694 c3d69b b2a2c7 92cddc fac08f a5a5a5 262626 494429 17365d 366092 953734 76923c 5f497a 31859b e36c09 7f7f7f 0c0c0c 1d1b10 0f243e 244061 632423 4f6128 3f3151 205867 974806 c00000 ff0000 ffc000 ffff00 92d050 00b050 00b0f0 0070c0 002060 7030a0 ".split(" "),
                    d = '<div unselectable="on" onmousedown="return false" class="edui-colorpicker<%if : ${name}%> edui-colorpicker-${name}<%/if%>" ><table unselectable="on" onmousedown="return false"><tr><td colspan="10">' + a.lang_themeColor + '</td> </tr><tr class="edui-colorpicker-firstrow" >', c = 0; c < b.length; c++) c && 0 === c % 10 && (d += "</tr>" + (60 == c ? '<tr><td colspan="10">' + a.lang_standardColor + "</td></tr>" : "") + "<tr" + (60 == c ? ' class="edui-colorpicker-firstrow"' : "") + ">"), d += 70 > c ? '<td><a unselectable="on" onmousedown="return false" title="' +
                b[c] + '" class="edui-colorpicker-colorcell" data-color="#' + b[c] + '" style="background-color:#' + b[c] + ";border:solid #ccc;" + (10 > c || 60 <= c ? "border-width:1px;" : 10 <= c && 20 > c ? "border-width:1px 1px 0 1px;" : "border-width:0 1px 0 1px;") + '"></a></td>' : "";
            return d + "</tr></table></div>"
        },
        init: function(a) { var b = this;
            b.root(g(UM.utils.render(b.supper.mergeTpl(b.tpl(a)), a)));
            b.root().on("click", function(a) { b.trigger("pickcolor", g(a.target).data("color")) }) }
    }, "popup");
    (function() {
        UM.ui.define("combobox", function() {
            return {
                tpl: '<ul class="dropdown-menu edui-combobox-menu<%if: ${comboboxName} !==\'\'%> edui-combobox-${comboboxName}<%/if%>" unselectable="on" onmousedown="return false" role="menu" aria-labelledby="dropdownMenu"><%if: ${autoRecord} %><%for : ${recordStack} as ${recordItem}, ${index}%><%var : style = ${itemStyles}[${recordItem}]%><%var : record = ${items}[${recordItem}]%><li class="${itemClassName}<%if: ${selected} == ${recordItem}%> edui-combobox-checked<%/if%>" data-item-index="${recordItem}" unselectable="on" onmousedown="return false"><span class="edui-combobox-icon" unselectable="on" onmousedown="return false"></span><label class="${labelClassName}" style="${style}" unselectable="on" onmousedown="return false">${record}</label></li><%/for%><%if: ${index} %><li class="edui-combobox-item-separator"></li><%/if%><%/if%><%for: ${items} as ${item}, ${itemIndex}%><%var : labelStyle = ${itemStyles}[${itemIndex}]%><li class="${itemClassName}<%if: ${selected} == ${item} %> edui-combobox-checked<%/if%> edui-combobox-item-${itemIndex}" data-item-index="${itemIndex}" unselectable="on" onmousedown="return false"><span class="edui-combobox-icon" unselectable="on" onmousedown="return false"></span><label class="${labelClassName}" style="${labelStyle}" unselectable="on" onmousedown="return false">${item}</label></li><%/for%></ul>',
                defaultOpt: { recordStack: [], items: [], value: [], comboboxName: "", selected: "", autoRecord: !0, recordCount: 5 },
                init: function(a) { g.extend(this._optionAdaptation(a), this._createItemMapping(a.recordStack, a.items), { itemClassName: "edui-combobox-item", iconClass: "edui-combobox-checked-icon", labelClassName: "edui-combobox-item-label" });
                    this._transStack(a);
                    this.root(g(UM.utils.render(this.tpl, a)));
                    this.data("options", a).initEvent() },
                initEvent: function() { this.initSelectItem();
                    this.initItemActive() },
                initSelectItem: function() {
                    var a =
                        this;
                    a.root().delegate(".edui-combobox-item", "click", function() { var b = g(this),
                            d = b.attr("data-item-index");
                        a.trigger("comboboxselect", { index: d, label: b.find(".edui-combobox-item-label").text(), value: a.data("options").value[d] }).select(d);
                        a.hide(); return !1 })
                },
                initItemActive: function() { var a = { mouseenter: "addClass", mouseleave: "removeClass" }; if (g.IE6) this.root().delegate(".edui-combobox-item", "mouseenter mouseleave", function(b) { g(this)[a[b.type]]("edui-combobox-item-hover") }).one("afterhide", function() {}) },
                select: function(a) { var b = this.data("options").itemCount,
                        d = this.data("options").autowidthitem;
                    d && !d.length && (d = this.data("options").items); if (0 == b) return null;
                    0 > a ? a = b + a % b : a >= b && (a = b - 1);
                    this.trigger("changebefore", d[a]);
                    this._update(a);
                    this.trigger("changeafter", d[a]); return null },
                selectItemByLabel: function(a) { var b = this.data("options").itemMapping,
                        d = this,
                        c = null;!g.isArray(a) && (a = [a]);
                    g.each(a, function(a, g) { c = b[g]; if (void 0 !== c) return d.select(c), !1 }) },
                _transStack: function(a) {
                    var b = [],
                        d = -1,
                        c = -1;
                    g.each(a.recordStack,
                        function(f, h) { d = a.itemMapping[h];
                            g.isNumeric(d) && (b.push(d), h == a.selected && (c = d)) });
                    a.recordStack = b;
                    a.selected = c;
                    b = null
                },
                _optionAdaptation: function(a) { if (!("itemStyles" in a)) { a.itemStyles = []; for (var b = 0, d = a.items.length; b < d; b++) a.itemStyles.push("") } a.autowidthitem = a.autowidthitem || a.items;
                    a.itemCount = a.items.length; return a },
                _createItemMapping: function(a, b) {
                    var d = {},
                        c = { recordStack: [], mapping: {} };
                    g.each(b, function(a, b) { d[b] = a });
                    c.itemMapping = d;
                    g.each(a, function(a, b) {
                        void 0 !== d[b] && (c.recordStack.push(d[b]),
                            c.mapping[b] = d[b])
                    });
                    return c
                },
                _update: function(a) { var b = this.data("options"),
                        d = [],
                        c = null;
                    g.each(b.recordStack, function(b, c) { c != a && d.push(+c) });
                    d.unshift(+a);
                    d.length > b.recordCount && (d.length = b.recordCount);
                    b.recordStack = d;
                    b.selected = +a;
                    c = g(UM.utils.render(this.tpl, b));
                    this.root().html(c.html());
                    d = c = null }
            }
        }(), "menu")
    })();
    (function() {
        UM.ui.define("buttoncombobox", function() {
            return {
                defaultOpt: { label: "", title: "" },
                init: function(a) {
                    var b = this,
                        d = g.eduibutton({
                            caret: !0,
                            name: a.comboboxName,
                            title: a.title,
                            text: a.label,
                            click: function() { b.show(this.root()) }
                        });
                    b.supper.init.call(b, a);
                    b.on("changebefore", function(a, b) { d.eduibutton("label", b) });
                    b.data("button", d);
                    b.attachTo(d)
                },
                button: function() { return this.data("button") }
            }
        }(), "combobox")
    })();
    UM.ui.define("modal", {
        tpl: '<div class="edui-modal" tabindex="-1" ><div class="edui-modal-header"><div class="edui-close" data-hide="modal"></div><h3 class="edui-title">${title}</h3></div><div class="edui-modal-body"  style="<%if: ${width}%>width:${width}px;<%/if%><%if: ${height}%>height:${height}px;<%/if%>"> </div><% if: ${cancellabel} || ${oklabel} %><div class="edui-modal-footer"><div class="edui-modal-tip"></div><%if: ${oklabel}%><div class="edui-btn edui-btn-primary" data-ok="modal">${oklabel}</div><%/if%><%if: ${cancellabel}%><div class="edui-btn" data-hide="modal">${cancellabel}</div><%/if%></div><%/if%></div>',
        defaultOpt: { title: "", cancellabel: "", oklabel: "", width: "", height: "", backdrop: !0, keyboard: !0 },
        init: function(a) { this.root(g(UM.utils.render(this.tpl, a || {})));
            this.data("options", a); if (a.okFn) this.on("ok", g.proxy(a.okFn, this)); if (a.cancelFn) this.on("beforehide", g.proxy(a.cancelFn, this));
            this.root().delegate('[data-hide="modal"]', "click", g.proxy(this.hide, this)).delegate('[data-ok="modal"]', "click", g.proxy(this.ok, this));
            g('[data-hide="modal"],[data-ok="modal"]', this.root()).hover(function() { g(this).toggleClass("edui-hover") }) },
        toggle: function() { return this[this.data("isShown") ? "hide" : "show"]() },
        show: function() { var a = this;
            a.trigger("beforeshow");
            a.data("isShown") || (a.data("isShown", !0), a.escape(), a.backdrop(function() { a.autoCenter();
                a.root().show().focus().trigger("aftershow") })) },
        showTip: function(a) { g(".edui-modal-tip", this.root()).html(a).fadeIn() },
        hideTip: function(a) { g(".edui-modal-tip", this.root()).fadeOut(function() { g(this).html("") }) },
        autoCenter: function() {
            !g.IE6 && this.root().css("margin-left", -(this.root().width() /
                2))
        },
        hide: function() { this.trigger("beforehide");
            this.data("isShown") && (this.data("isShown", !1), this.escape(), this.hideModal()) },
        escape: function() { var a = this; if (a.data("isShown") && a.data("options").keyboard) a.root().on("keyup", function(b) { 27 == b.which && a.hide() });
            else a.data("isShown") || a.root().off("keyup") },
        hideModal: function() { var a = this;
            a.root().hide();
            a.backdrop(function() { a.removeBackdrop();
                a.trigger("afterhide") }) },
        removeBackdrop: function() {
            this.$backdrop && this.$backdrop.remove();
            this.$backdrop =
                null
        },
        backdrop: function(a) { this.data("isShown") && this.data("options").backdrop && (this.$backdrop = g('<div class="edui-modal-backdrop" />').click("static" == this.data("options").backdrop ? g.proxy(this.root()[0].focus, this.root()[0]) : g.proxy(this.hide, this)));
            this.trigger("afterbackdrop");
            a && a() },
        attachTo: function(a) { var b = this;
            a.data("$mergeObj") || (a.data("$mergeObj", b.root()), a.on("click", function() { b.toggle(a) }), b.data("$mergeObj", a)) },
        ok: function() {
            this.trigger("beforeok");
            !1 !== this.trigger("ok", this) &&
                this.hide()
        },
        getBodyContainer: function() { return this.root().find(".edui-modal-body") }
    });
    UM.ui.define("tooltip", {
        tpl: '<div class="edui-tooltip" unselectable="on" onmousedown="return false"><div class="edui-tooltip-arrow" unselectable="on" onmousedown="return false"></div><div class="edui-tooltip-inner" unselectable="on" onmousedown="return false"></div></div>',
        init: function(a) { this.root(g(UM.utils.render(this.tpl, a || {}))) },
        content: function(a) { a = g(a.currentTarget).attr("data-original-title");
            this.root().find(".edui-tooltip-inner").text(a) },
        position: function(a) { a = g(a.currentTarget);
            this.root().css(g.extend({ display: "block" }, a ? { top: a.outerHeight(), left: (a.outerWidth() - this.root().outerWidth()) / 2 } : {})) },
        show: function(a) { g(a.currentTarget).hasClass("edui-disabled") || (this.content(a), this.root().appendTo(g(a.currentTarget)), this.position(a), this.root().css("display", "block")) },
        hide: function() { this.root().css("display", "none") },
        attachTo: function(a) {
            function b(a) {
                var b = this;
                g.contains(document.body, b.root()[0]) || b.root().appendTo(a);
                b.data("tooltip",
                    b.root());
                a.each(function() { if (g(this).attr("data-original-title")) g(this).on("mouseenter", g.proxy(b.show, b)).on("mouseleave click", g.proxy(b.hide, b)) })
            }
            var d = this;
            "undefined" === g.type(a) ? g("[data-original-title]").each(function(a, f) { b.call(d, g(f)) }) : a.data("tooltip") || b.call(d, a)
        }
    });
    UM.ui.define("tab", {
        init: function(a) { var b = this,
                d = a.selector;
            g.type(d) && (b.root(g(d, a.context)), b.data("context", a.context), g(d, b.data("context")).on("click", function(a) { b.show(a) })) },
        show: function(a) {
            var b = this,
                d = g(a.target),
                c = d.closest("ul"),
                f, h;
            f = (f = d.attr("data-context")) && f.replace(/.*(?=#[^\s]*$)/, "");
            a = d.parent("li");
            a.length && !a.hasClass("edui-active") && (h = c.find(".edui-active:last a")[0], a = g.Event("beforeshow", { target: d[0], relatedTarget: h }), b.trigger(a), a.isDefaultPrevented() || (f = g(f, b.data("context")), b.activate(d.parent("li"), c), b.activate(f, f.parent(), function() { b.trigger({ type: "aftershow", relatedTarget: h }) })))
        },
        activate: function(a, b, d) {
            if (void 0 === a) return g(".edui-tab-item.edui-active", this.root()).index();
            b.find("> .edui-active").removeClass("edui-active");
            a.addClass("edui-active");
            d && d()
        }
    });
    UM.ui.define("separator", { tpl: '<div class="edui-separator" unselectable="on" onmousedown="return false" ></div>', init: function(a) { this.root(g(g.parseTmpl(this.tpl, a))); return this } });
    (function() {
        var a = {},
            b = {},
            d = [],
            c = {},
            f = {},
            h = {},
            e = null;
        n.extend(UM, {
            defaultWidth: 500,
            defaultHeight: 500,
            registerUI: function(b, c) { n.each(b.split(/\s+/), function(b) { a[b] = c }) },
            setEditor: function(a) {!b[a.id] && (b[a.id] = a) },
            registerWidget: function(a,
                b, d) { c[a] = g.extend2(b, { $root: "", _preventDefault: !1, root: function(a) { return this.$root || (this.$root = a) }, preventDefault: function() { this._preventDefault = !0 }, clear: !1 });
                d && (f[a] = d) },
            getWidgetData: function(a) { return c[a] },
            setWidgetBody: function(a, b, d) {
                d._widgetData || n.extend(d, { _widgetData: {}, getWidgetData: function(a) { return this._widgetData[a] }, getWidgetCallback: function(a) { var c = this; return function() { return f[a].apply(c, [c, b].concat(Array.prototype.slice.call(arguments, 0))) } } });
                var e = c[a];
                if (!e) return null;
                e = d._widgetData[a];
                e || (e = c[a], e = d._widgetData[a] = "function" == g.type(e) ? e : n.clone(e));
                e.root(b.edui().getBodyContainer());
                e.initContent(d, b);
                e._preventDefault || e.initEvent(d, b);
                e.width && b.width(e.width)
            },
            setActiveWidget: function(a) {},




            getEditor: function(a, c) {
                var d = b[a] || (b[a] = this.createEditor(a, c));
                e = e ? Math.max(d.getOpt("zIndex"), e) : d.getOpt("zIndex");
                return d
            },
            setTopEditor: function(a) {
                g.each(b, function(b, c) {
                    a == c ? a.$container && a.$container.css("zIndex", e + 1) : c.$container && c.$container.css("zIndex",
                        c.getOpt("zIndex"))
                })
            },
            clearCache: function(a) { b[a] && delete b[a] },
            delEditor: function(a) { var c;
                (c = b[a]) && c.destroy() },
            ready: function(a) { d.push(a) },
            createEditor: function(a, b) {
                function c() {
                    var b = this.createUI("#" + a, e);
                    e.key = a;
                    e.ready(function() { g.each(d, function(a, b) { g.proxy(b, e)() }) });
                    var c = e.options;
                    c.minFrameWidth = c.initialFrameWidth ? c.initialFrameWidth : c.initialFrameWidth = e.$body.width() || UM.defaultWidth;
                    b.css({ width: c.initialFrameWidth, zIndex: e.getOpt("zIndex") });
                    UM.browser.ie && 6 === UM.browser.version &&
                        document.execCommand("BackgroundImageCache", !1, !0);
                    e.render(a);
                    g.eduitooltip && g.eduitooltip("attachTo", g("[data-original-title]", b)).css("z-index", e.getOpt("zIndex") + 1);
                    b.find("a").click(function(a) { a.preventDefault() });
                    e.fireEvent("afteruiready")
                }
                var e = new UM.Editor(b);
                e.langIsReady ? g.proxy(c, this)() : e.addListener("langReady", g.proxy(c, this));
                return e
            },
            createUI: function(b, c) {
                var d = g(b),
                    e = g('<div class="edui-container"><div class="edui-editor-body"></div></div>').insertBefore(d);
                c.$container = e;
                c.container =
                    e[0];
                c.$body = d;
                m.ie && m.ie9above && g('<span style="padding:0;margin:0;height:0;width:0"></span>').insertAfter(e);
                g.each(a, function(a, b) { var d = b.call(c, a);
                    d && (h[a] = d) });
                e.find(".edui-editor-body").append(d).before(this.createToolbar(c.options, c));
                e.find(".edui-toolbar").append(g('<div class="edui-dialog-container"></div>'));
                return e
            },
            createToolbar: function(a, b) {
                var c = g.eduitoolbar(),
                    d = c.edui();
                if (a.toolbar && a.toolbar.length) {
                    var e = [];
                    g.each(a.toolbar, function(a, b) {
                        g.each(b.split(/\s+/), function(a, b) {
                            if ("|" ==
                                b) g.eduiseparator && e.push(g.eduiseparator());
                            else { var c = h[b]; "fullscreen" == b ? c && e.unshift(c) : c && e.push(c) }
                        });
                        e.length && d.appendToBtnmenu(e)
                    })
                } else c.find(".edui-btn-toolbar").remove();
                return c
            }
        })
    })();
    UM.registerUI("bold italic redo undo underline strikethrough superscript subscript insertorderedlist insertunorderedlist cleardoc selectall link unlink print preview justifyleft justifycenter justifyright justifyfull removeformat horizontal drafts", function(a) {
        var b = this,
            d = g.eduibutton({
                icon: a,
                click: function() { b.execCommand(a) },
                title: this.getLang("labelMap")[a] || ""
            });
        this.addListener("selectionchange", function() { var b = this.queryCommandState(a);
            d.edui().disabled(-1 == b).active(1 == b) });
        return d
    });
    (function() {
        function a(a) { var b = this; if (!a) throw Error("invalid params, notfound editor");
            b.editor = a;
            e[a.uid] = this;
            a.addListener("destroy", function() { delete e[a.uid];
                b.editor = null }) }
        var b = {},
            d = "width height position top left margin padding overflowX overflowY".split(" "),
            c = {},
            f = {},
            h = {},
            e = {};
        UM.registerUI("fullscreen", function(b) {
            var c =
                this,
                d = g.eduibutton({ icon: "fullscreen", title: c.options.labelMap && c.options.labelMap[b] || c.getLang("labelMap." + b), click: function() { c.execCommand(b);
                        UM.setTopEditor(c) } });
            c.addListener("selectionchange", function() { var a = this.queryCommandState(b);
                d.edui().disabled(-1 == a).active(1 == a) });
            c.addListener("ready", function() { c.options.fullscreen && a.getInstance(c).toggle() });
            return d
        });
        UM.commands.fullscreen = {
            execCommand: function(b) { a.getInstance(this).toggle() },
            queryCommandState: function(a) { return this._edui_fullscreen_status },
            notNeedUndo: 1
        };
        a.prototype = {
            toggle: function() { var a = this.editor,
                    b = this.isFullState();
                a.fireEvent("beforefullscreenchange", !b);
                this.update(!b);
                b ? this.revert() : this.enlarge();
                a.fireEvent("afterfullscreenchange", !b); "true" === a.body.contentEditable && a.fireEvent("fullscreenchanged", !b);
                a.fireEvent("selectionchange") },
            enlarge: function() { this.saveSataus();
                this.setDocumentStatus();
                this.resize() },
            revert: function() {
                var a = this.editor.options,
                    a = /%$/.test(a.initialFrameHeight) ? "100%" : a.initialFrameHeight - this.getStyleValue("padding-top") -
                    this.getStyleValue("padding-bottom") - this.getStyleValue("border-width");
                g.IE6 && this.getEditorHolder().style.setExpression("height", "this.scrollHeight <= " + a + ' ? "' + a + 'px" : "auto"');
                this.revertContainerStatus();
                this.revertContentAreaStatus();
                this.revertDocumentStatus()
            },
            update: function(a) { this.editor._edui_fullscreen_status = a },
            resize: function() {
                var a, b, c, d = 0,
                    e = this.editor,
                    f, h;
                this.isFullState() && (a = g(window), b = a.width(), a = a.height(), h = this.getEditorHolder(), c = parseInt(k.getComputedStyle(h, "border-width"),
                    10) || 0, c += parseInt(k.getComputedStyle(e.container, "border-width"), 10) || 0, d += parseInt(k.getComputedStyle(h, "padding-left"), 10) + parseInt(k.getComputedStyle(h, "padding-right"), 10) || 0, g.IE6 && h.style.setExpression("height", null), f = this.getBound(), g(e.container).css({ width: b + "px", height: a + "px", position: g.IE6 ? "absolute" : "fixed", top: f.top, left: f.left, margin: 0, padding: 0, overflowX: "hidden", overflowY: "hidden" }), g(h).css({
                    width: b - 2 * c - d + "px",
                    height: a - 2 * c - (e.options.withoutToolbar ? 0 : g(".edui-toolbar", e.container).outerHeight()) -
                        g(".edui-bottombar", e.container).outerHeight() + "px",
                    overflowX: "hidden",
                    overflowY: "auto"
                }))
            },
            saveSataus: function() { for (var a = this.editor.container.style, c, e = {}, f = 0, g = d.length; f < g; f++) c = d[f], e[c] = a[c];
                b[this.editor.uid] = e;
                this.saveContentAreaStatus();
                this.saveDocumentStatus() },
            saveContentAreaStatus: function() { var a = g(this.getEditorHolder());
                c[this.editor.uid] = { width: a.css("width"), overflowX: a.css("overflowX"), overflowY: a.css("overflowY"), height: a.css("height") } },
            saveDocumentStatus: function() {
                var a =
                    g(this.getEditorDocumentBody());
                f[this.editor.uid] = { overflowX: a.css("overflowX"), overflowY: a.css("overflowY") };
                h[this.editor.uid] = { overflowX: g(this.getEditorDocumentElement()).css("overflowX"), overflowY: g(this.getEditorDocumentElement()).css("overflowY") }
            },
            revertContainerStatus: function() { g(this.editor.container).css(this.getEditorStatus()) },
            revertContentAreaStatus: function() { var a = this.getEditorHolder(),
                    b = this.getContentAreaStatus();
                this.supportMin() && (delete b.height, a.style.height = null);
                g(a).css(b) },
            revertDocumentStatus: function() { var a = this.getDocumentStatus();
                g(this.getEditorDocumentBody()).css("overflowX", a.body.overflowX);
                g(this.getEditorDocumentElement()).css("overflowY", a.html.overflowY) },
            setDocumentStatus: function() { g(this.getEditorDocumentBody()).css({ overflowX: "hidden", overflowY: "hidden" });
                g(this.getEditorDocumentElement()).css({ overflowX: "hidden", overflowY: "hidden" }) },
            isFullState: function() { return !!this.editor._edui_fullscreen_status },
            getEditorStatus: function() { return b[this.editor.uid] },
            getContentAreaStatus: function() { return c[this.editor.uid] },
            getEditorDocumentElement: function() { return this.editor.container.ownerDocument.documentElement },
            getEditorDocumentBody: function() { return this.editor.container.ownerDocument.body },
            getEditorHolder: function() { return this.editor.body },
            getDocumentStatus: function() { return { body: f[this.editor.uid], html: h[this.editor.uid] } },
            supportMin: function() { var a;
                this._support || (a = document.createElement("div"), this._support = "minWidth" in a.style); return this._support },
            getBound: function() { var a = { html: !0, body: !0 },
                    b = { top: 0, left: 0 },
                    c; if (!g.IE6) return b;
                (c = this.editor.container.offsetParent) && !a[c.nodeName.toLowerCase()] && (a = c.getBoundingClientRect(), b.top = -a.top, b.left = -a.left); return b },
            getStyleValue: function(a) { return parseInt(k.getComputedStyle(this.getEditorHolder(), a)) }
        };
        g.extend(a, {
            listen: function() {
                var b = null;
                a._hasFullscreenListener || (a._hasFullscreenListener = !0, g(window).on("resize", function() {
                    null !== b && (window.clearTimeout(b), b = null);
                    b = window.setTimeout(function() {
                        for (var a in e) e[a].resize();
                        b = null
                    }, 50)
                }))
            },
            getInstance: function(b) { e[b.uid] || new a(b); return e[b.uid] }
        });
        a.listen()
    })();
    UM.registerUI("link image video map formula", function(a) {
        var b = this,
            d, c, f = { title: b.options.labelMap && b.options.labelMap[a] || b.getLang("labelMap." + a), url: b.options.UMEDITOR_HOME_URL + "dialogs/" + a + "/" + a + ".js" },
            h = g.eduibutton({ icon: a, title: this.getLang("labelMap")[a] || "" });
        n.loadFile(document, { src: f.url, tag: "script", type: "text/javascript", defer: "defer" }, function() {
            var e = UM.getWidgetData(a);
            if (e) {
                if (e.buttons) {
                    var l =
                        e.buttons.ok;
                    l && (f.oklabel = l.label || b.getLang("ok"), l.exec && (f.okFn = function() { return g.proxy(l.exec, null, b, c)() }));
                    var k = e.buttons.cancel;
                    k && (f.cancellabel = k.label || b.getLang("cancel"), k.exec && (f.cancelFn = function() { return g.proxy(k.exec, null, b, c)() }))
                }
                e.width && (f.width = e.width);
                e.height && (f.height = e.height);
                c = g.eduimodal(f);
                c.attr("id", "edui-dialog-" + a).addClass("edui-dialog-" + a).find(".edui-modal-body").addClass("edui-dialog-" + a + "-body");
                c.edui().on("beforehide", function() {
                    var a = b.selection.getRange();
                    a.equals(d) && a.select()
                }).on("beforeshow", function() { var e, f = this.root(),
                        h;
                    d = b.selection.getRange();
                    f.parent()[0] || b.$container.find(".edui-dialog-container").append(f);
                    g.IE6 && (e = g(window).width(), g(window).height(), h = f.parents(".edui-toolbar")[0].getBoundingClientRect(), f.css({ position: "absolute", margin: 0, left: (e - f.width()) / 2 - h.left, top: 100 - h.top }));
                    UM.setWidgetBody(a, c, b);
                    UM.setTopEditor(b) }).on("afterbackdrop", function() {
                    this.$backdrop.css("zIndex", b.getOpt("zIndex") + 1).appendTo(b.$container.find(".edui-dialog-container"));
                    c.css("zIndex", b.getOpt("zIndex") + 2)
                }).on("beforeok", function() { try { d.select() } catch (v) {} }).attachTo(h)
            }
        });
        b.addListener("selectionchange", function() { var b = this.queryCommandState(a);
            h.edui().disabled(-1 == b).active(1 == b) });
        return h
    });
    UM.registerUI("emotion formula", function(a) {
        var b = this,
            d = b.options.UMEDITOR_HOME_URL + "dialogs/" + a + "/" + a + ".js",
            c = g.eduibutton({ icon: a, title: this.getLang("labelMap")[a] || "" });
        n.loadFile(document, { src: d, tag: "script", type: "text/javascript", defer: "defer" }, function() {
            var f = { url: d },
                h = UM.getWidgetData(a);
            h.width && (f.width = h.width);
            h.height && (f.height = h.height);
            g.eduipopup(f).css("zIndex", b.options.zIndex + 1).addClass("edui-popup-" + a).edui().on("beforeshow", function() { var c = this.root();
                c.parent().length || b.$container.find(".edui-dialog-container").append(c);
                UM.setWidgetBody(a, c, b);
                UM.setTopEditor(b) }).attachTo(c, { offsetTop: -5, offsetLeft: 10, caretLeft: 11, caretTop: -8 });
            b.addListener("selectionchange", function() {
                var b = this.queryCommandState(a);
                c.edui().disabled(-1 == b).active(1 ==
                    b)
            })
        });
        return c
    });
    UM.registerUI("imagescale", function() {
        var a = this,
            b;
        a.setOpt("imageScaleEnabled", !0);
        m.webkit && a.getOpt("imageScaleEnabled") && (a.addListener("click", function(d, c) {
            var f = a.selection.getRange().getClosedNode(),
                h = c.target;
            if (f && "IMG" == f.tagName && h == f) {
                if (!b) {
                    b = g.eduiscale({ $wrap: a.$container }).css("zIndex", a.options.zIndex);
                    a.$container.append(b);
                    var e = function() { b.edui().hide() },
                        k = function(a) { var b = a.target || a.srcElement;
                            b && -1 == b.className.indexOf("edui-scale") && e(a) },
                        m;
                    b.edui().on("aftershow",
                        function() { g(document).bind("keydown", e);
                            g(document).bind("mousedown", k);
                            a.selection.getNative().removeAllRanges() }).on("afterhide", function() { g(document).unbind("keydown", e);
                        g(document).unbind("mousedown", k); var c = b.edui().getScaleTarget();
                        c.parentNode && a.selection.getRange().selectNode(c).select() }).on("mousedown", function(c) { a.selection.getNative().removeAllRanges();
                        (c = c.target || c.srcElement) && -1 == c.className.indexOf("edui-scale-hand") && (m = setTimeout(function() { b.edui().hide() }, 200)) }).on("mouseup",
                        function(a) {
                            (a = a.target || a.srcElement) && -1 == a.className.indexOf("edui-scale-hand") && clearTimeout(m) })
                }
                b.edui().show(g(f))
            } else b && "none" != b.css("display") && b.edui().hide()
        }), a.addListener("click", function(b, c) { "IMG" == c.target.tagName && (new x.Range(a.document, a.body)).selectNode(c.target).select() }))
    });
    UM.registerUI("autofloat", function() {
        var a = this,
            b = a.getLang();
        a.setOpt({ autoFloatEnabled: !0, topOffset: 0 });
        var d = a.options.topOffset;
        !1 !== a.options.autoFloatEnabled && a.ready(function() {
            function c() {
                var a =
                    document.body.style;
                a.backgroundImage = 'url("about:blank")';
                a.backgroundAttachment = "fixed"
            }

            function f() { v.parentNode && v.parentNode.removeChild(v);
                r.style.cssText = p }

            function h() {
                var b = a.container,
                    c;
                try { c = b.getBoundingClientRect() } catch (z) { c = { left: 0, top: 0, height: 0, width: 0 } }
                for (var g = Math.round(c.top), h = Math.round(c.bottom - c.top), n;
                    (n = b.ownerDocument) !== document && (b = k.getWindow(n).frameElement);) c = b.getBoundingClientRect(), g += c.top;
                b = a.options.toolbarTopOffset || 0;
                0 > g && g + h - r.offsetHeight > b ? y || (g = k.getXY(r),
                    h = k.getComputedStyle(r, "position"), b = k.getComputedStyle(r, "left"), r.style.width = r.offsetWidth + "px", r.style.zIndex = 1 * a.options.zIndex + 1, r.parentNode.insertBefore(v, r), e || l && m.ie ? ("absolute" != r.style.position && (r.style.position = "absolute"), r.style.top = (document.body.scrollTop || document.documentElement.scrollTop) - q + d + "px") : "fixed" != r.style.position && (r.style.position = "fixed", r.style.top = d + "px", ("absolute" == h || "relative" == h) && parseFloat(b) && (r.style.left = g.x + "px"))) : f()
            }
            var e = m.ie && 6 >= m.version,
                l = m.quirks,
                p, v = document.createElement("div"),
                r, q, y = !1,
                w = n.defer(function() { h() }, m.ie ? 200 : 100, !0);
            a.addListener("destroy", function() { g(window).off("scroll resize", h);
                a.removeListener("keydown", w) });
            var x;
            UM.ui ? x = 1 : (alert(b.autofloatMsg), x = 0);
            x && (r = g(".edui-toolbar", a.container)[0], a.addListener("afteruiready", function() { setTimeout(function() { q = g(r).offset().top }, 100) }), p = r.style.cssText, v.style.height = r.offsetHeight + "px", e && c(), g(window).on("scroll resize", h), a.addListener("keydown", w), a.addListener("resize",
                function() { f();
                    v.style.height = r.offsetHeight + "px";
                    h() }), a.addListener("beforefullscreenchange", function(a, b) { b && (f(), y = b) }), a.addListener("fullscreenchanged", function(a, b) { b || h();
                y = b }), a.addListener("sourcemodechanged", function(a, b) { setTimeout(function() { h() }, 0) }), a.addListener("clearDoc", function() { setTimeout(function() { h() }, 0) }))
        })
    });
    UM.registerUI("source", function(a) {
        var b = this;
        b.addListener("fullscreenchanged", function() { b.$container.find("textarea").width(b.$body.width() - 10).height(b.$body.height()) });
        var d = g.eduibutton({ icon: a, click: function() { b.execCommand(a);
                UM.setTopEditor(b) }, title: this.getLang("labelMap")[a] || "" });
        this.addListener("selectionchange", function() { var b = this.queryCommandState(a);
            d.edui().disabled(-1 == b).active(1 == b) });
        return d
    });
    UM.registerUI("paragraph fontfamily fontsize", function(a) {
        function b(a, c) {
            var d = g("<span>").html(a).css({ display: "inline", position: "absolute", top: -1E7, left: -1E5 }).appendTo(document.body),
                e = d.width();
            d.remove();
            if (50 > e) return a;
            a = a.slice(0, c ? -4 : -1);
            return a.length ?
                b(a + "...", !0) : "..."
        }

        function d(a) { var c = [],
                d; for (d in a.items) a.value.push(d), c.push(d), a.autowidthitem.push(b(d));
            a.items = c;
            a.autoRecord = !1; return a }

        function c(a) { for (var c, d = [], e = 0, f = a.items.length; e < f; e++) c = a.items[e].val, d.push(c.split(/\s*,\s*/)[0]), a.itemStyles.push("font-family: " + c), a.value.push(c), a.autowidthitem.push(b(d[e]));
            a.items = d; return a }

        function f(a) {
            var b, c = [];
            a.itemStyles = [];
            a.value = [];
            for (var d = 0, e = a.items.length; d < e; d++) b = a.items[d], c.push(b), a.itemStyles.push("font-size: " +
                b + "px");
            a.value = a.items;
            a.items = c;
            a.autoRecord = !1;
            return a
        }
        var h = this,
            e = h.options.labelMap && h.options.labelMap[a] || h.getLang("labelMap." + a),
            e = { label: e, title: e, comboboxName: a, items: h.options[a] || [], itemStyles: [], value: [], autowidthitem: [] },
            k = null,
            m = null;
        if (0 == e.items.length) return null;
        switch (a) {
            case "paragraph":
                e = d(e); break;
            case "fontfamily":
                e = c(e); break;
            case "fontsize":
                e = f(e) } k = g.eduibuttoncombobox(e).css("zIndex", h.getOpt("zIndex") + 1);
        m = k.edui();
        m.on("comboboxselect", function(b, c) {
            h.execCommand(a,
                c.value)
        }).on("beforeshow", function() { 0 === k.parent().length && k.appendTo(h.$container.find(".edui-dialog-container"));
            UM.setTopEditor(h) });
        this.addListener("selectionchange", function(b) { b = this.queryCommandState(a); var c = this.queryCommandValue(a);
            m.button().edui().disabled(-1 == b).active(1 == b);
            c && (c = c.replace(/['"]/g, "").toLowerCase().split(/['|"]?\s*,\s*[\1]?/), m.selectItemByLabel(c)) });
        return m.button().addClass("edui-combobox")
    });
    UM.registerUI("forecolor backcolor", function(a) {
        var b = this,
            d = null,
            c =
            null,
            f = null;
        this.addListener("selectionchange", function() { var b = this.queryCommandState(a);
            f.edui().disabled(-1 == b).active(1 == b) });
        f = g.eduicolorsplitbutton({ icon: a, caret: !0, name: a, title: b.getLang("labelMap")[a], click: function() { b.execCommand(a, k.getComputedStyle(c[0], "background-color")) } });
        c = f.edui().colorLabel();
        d = g.eduicolorpicker({ name: a, lang_clearColor: b.getLang("clearColor") || "", lang_themeColor: b.getLang("themeColor") || "", lang_standardColor: b.getLang("standardColor") || "" }).on("pickcolor", function(d,
            e) { window.setTimeout(function() { c.css("backgroundColor", e);
                b.execCommand(a, e) }, 0) }).on("show", function() { UM.setActiveWidget(colorPickerWidget.root()) }).css("zIndex", b.getOpt("zIndex") + 1);
        f.edui().on("arrowclick", function() { d.parent().length || b.$container.find(".edui-dialog-container").append(d);
            d.edui().show(f, { caretDir: "down", offsetTop: -5, offsetLeft: 8, caretLeft: 11, caretTop: -8 });
            UM.setTopEditor(b) }).register("click", f, function() { d.edui().hide() });
        return f
    })
})(jQuery);