var Y = Object.defineProperty;
var T = Object.getOwnPropertySymbols;
var P = Object.prototype.hasOwnProperty, Q = Object.prototype.propertyIsEnumerable;
var C = (e, n, t) => n in e ? Y(e, n, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[n] = t, k = (e, n) => {
  for (var t in n || (n = {}))
    P.call(n, t) && C(e, t, n[t]);
  if (T)
    for (var t of T(n))
      Q.call(n, t) && C(e, t, n[t]);
  return e;
};
var M = (e, n, t) => (C(e, typeof n != "symbol" ? n + "" : n, t), t);
import { jsx as m, jsxs as $ } from "https://esm.sh/react@^18.2.0/jsx-runtime";
import { Card as X, ConfigProvider as G, Divider as H, Form as tt, Switch as et, Alert as nt } from "https://esm.sh/antd@^5.10.2";
import { createContext as ot, useMemo as A, useContext as rt, useState as B, useCallback as I, useEffect as L, Fragment as it, useRef as N, StrictMode as at } from "https://esm.sh/react@^18.2.0";
import * as ct from "https://esm.sh/@antv/g6@^4.8.23";
import { registerNode as st, registerEdge as lt } from "https://esm.sh/@antv/g6@^4.8.23";
import W from "https://esm.sh/color@^4.2.3";
import { Graph as dt } from "https://esm.sh/@antv/graphlib@^2.0.2";
import _ from "https://esm.sh/lodash@^4.17.21/isEqual";
import * as ft from "https://esm.sh/d3@^7.8.5";
import ut from "https://esm.sh/yaml@^2.3.4";
import { createRoot as ht } from "https://esm.sh/react-dom@^18.2.0/client";
function j(e) {
  return Array.isArray(e);
}
function V(e) {
  return typeof e == "object" && e !== null && !Object.hasOwn(e, "kind");
}
function E(e, n, t) {
  if ((n == null ? void 0 : n.ref) === void 0)
    return;
  const o = t == null ? void 0 : t[n.ref];
  if (o === void 0 || e !== void 0 && o.kind !== e)
    return;
  const r = Object.fromEntries(
    Object.entries(o).filter(
      ([, i]) => !j(i) && !V(i)
    )
  ), s = Object.fromEntries(
    Object.entries(o).filter(([, i]) => V(i) || j(i)).map(([i, a]) => {
      const c = a;
      let l, d;
      return j(c) ? (l = (f) => c[Number(f)], d = function* () {
        for (let f = 0; f < c.length; f++)
          yield [f, c[f]];
      }) : (l = (f) => c[String(f)], d = function* () {
        for (const [f, g] of Object.entries(c))
          yield [f, g];
      }), [i, {
        get: (f) => {
          const g = l(f);
          if (!g)
            return;
          const u = t == null ? void 0 : t[g.ref];
          if (u != null && u.kind)
            return E(u.kind, g, t);
        },
        ofKind: (f, g) => {
          const u = l(g);
          if (!u)
            return;
          const p = t == null ? void 0 : t[u.ref];
          if ((p == null ? void 0 : p.kind) === f)
            return E(f, u, t);
        },
        items: function* () {
          for (const [f, g] of d()) {
            const u = t == null ? void 0 : t[g.ref];
            if (!(u != null && u.kind))
              continue;
            const p = E(u.kind, g, t);
            p && (yield [f, p]);
          }
        },
        itemsOfKind: function* (f) {
          for (const [g, u] of d()) {
            const p = t == null ? void 0 : t[u.ref];
            if ((p == null ? void 0 : p.kind) !== f)
              continue;
            const F = E(f, u, t);
            F && (yield [g, F]);
          }
        }
      }];
    })
  );
  return k(k({}, r), s);
}
const K = ot({
  reify: () => {
  }
}), gt = ({
  timeline: e,
  children: n
}) => {
  const t = A(
    () => ({
      reify: (o, r) => E(o, r, e == null ? void 0 : e.variables)
    }),
    [e == null ? void 0 : e.variables]
  );
  return /* @__PURE__ */ m(K.Provider, { value: t, children: n });
};
function pt() {
  return rt(K);
}
function x(e) {
  return typeof e == "object" && e !== null && "data" in e && typeof e.data == "object" && e.data !== null && "kind" in e.data && typeof e.data.kind == "string";
}
function b({
  kind: e,
  render: n,
  options: t
}) {
  return k({
    kind: e,
    draw: (o, r) => {
      if (!x(o))
        throw new Error(
          `Unexpected model for shape ${e}: ${JSON.stringify(o)}`
        );
      const s = o.data, i = o._utils, a = n({ item: s, renderer: r, config: o, utils: i });
      return o.size = [a.attr("width"), a.attr("height")], a;
    }
  }, t);
}
function mt({
  nodes: e,
  edges: n
}) {
  const t = (o, r) => `${o}:${r.kind}`;
  return e.forEach((o) => st(t("node", o), o)), n.forEach((o) => lt(t("edge", o), o)), function(r, s) {
    var i, a, c, l;
    return {
      nodes: (a = (i = r.nodes) == null ? void 0 : i.map(
        (d) => ({
          id: d.id,
          type: t("node", d),
          data: d,
          _utils: s
        })
      )) != null ? a : [],
      edges: (l = (c = r.edges) == null ? void 0 : c.map(
        (d) => ({
          id: `${d.source}-${d.target}`,
          source: d.source,
          target: d.target,
          type: t("edge", d),
          data: d,
          _utils: s
        })
      )) != null ? l : []
    };
  };
}
function yt(e) {
  const { nodes: n = [], edges: t = [] } = e.save();
  return new dt({
    nodes: n.filter(x),
    edges: t.filter(x)
  });
}
function U(e, n, t, o) {
  const r = [...t.bind(e)(n)], s = [...r], i = new Set(r.map((a) => a.id));
  for (; r.length > 0; ) {
    const a = r.shift();
    if (!a)
      break;
    if (o && o(e.getNode(a.id)))
      continue;
    t.bind(e)(a.id).filter((l) => !i.has(l.id)).forEach((l) => {
      i.add(l.id), r.push(l), s.push(l);
    });
  }
  return s;
}
function xt(e, n) {
  [...n].forEach(
    (o) => e.getRelatedEdges(o, "both").forEach((r) => {
      n.has(r.source) && n.has(r.target) && n.add(r.id);
    })
  );
  const t = /* @__PURE__ */ new Set([
    ...e.getAllNodes().filter((o) => !n.has(o.id)).map((o) => o.id),
    ...e.getAllEdges().filter((o) => !n.has(o.id)).map((o) => o.id)
  ]);
  return { matched: n, unmatched: t };
}
const bt = (e, n) => {
  const t = new Set(
    (() => {
      switch (e.getNode(n).data.kind) {
        case "function":
          return e.getNeighbors(n);
        case "reveal":
          return e.getNeighbors(n);
        case "remote":
        case "local":
          return [
            ...U(e, n, e.getPredecessors),
            ...U(e, n, e.getSuccessors)
          ];
        default:
          return [];
      }
    })().map((o) => o.id)
  );
  return t.add(n), t;
}, kt = (e, n) => {
  const t = (r) => (s) => {
    switch (s.data.kind) {
      case "function":
        return _(s.data.location, r);
      case "remote":
        return _(s.data.data.location, r);
      case "local":
        return e.getSuccessors(s.id).some((i) => t(r)(i));
      default:
        return !1;
    }
  }, o = new Set(
    (() => {
      const r = e.getNode(n);
      switch (r.data.kind) {
        case "function":
          return e.getAllNodes().filter(t(r.data.location));
        case "remote":
          return e.getAllNodes().filter(t(r.data.data.location));
        case "local":
          return e.getAllNodes().filter((s) => s.data.kind === "local");
        default:
          return [];
      }
    })().map((r) => r.id)
  );
  return o.add(n), o;
};
class S {
  constructor(n) {
    M(this, "palette");
    M(this, "cache", /* @__PURE__ */ new Map());
    M(this, "names", /* @__PURE__ */ new Map());
    this.palette = n;
  }
  colorize(n) {
    const t = S.locationKey(n);
    let o = this.cache.get(t);
    return o || (o = this.makeColor(), this.cache.set(t, o)), this.names.set(t, this.locationName(n)), { background: o, foreground: this.foreground(o) };
  }
  colors() {
    return new Map(
      [...this.names.entries()].map(([n, t]) => [
        n,
        { name: t, color: this.cache.get(n) }
      ])
    );
  }
  locationName(n) {
    return `${n.type}[${n.parties.join(", ")}]`;
  }
  static locationKey(n) {
    var t;
    return [
      n.type,
      ...n.parties,
      ...Object.entries((t = n.parameters) != null ? t : {}).map(([o, r]) => `${o}=${r}`)
    ].join(":");
  }
  makeColor() {
    const n = this.cache.size, t = n % this.palette.length, o = Math.floor(n / this.palette.length);
    if (o === 0)
      return this.palette[t];
    const s = [
      // triadic
      120,
      240,
      // tetradic
      90,
      180,
      270
    ][o - 1];
    if (s === void 0)
      throw new Error("Too many colors");
    return new W(this.palette[t]).rotate(s).hex();
  }
  foreground(n, t = 0.2, o = "#ffffff", r = "#1d1d1d") {
    return new W(n).darken(t).isDark() ? o : r;
  }
}
function q(e) {
  return (n) => {
    switch (n.data.kind) {
      case "function":
        return e(n.data.location);
      case "local":
        return { background: "#1d1d1d", foreground: "#ffffff" };
      case "remote":
        return e(n.data.data.location);
      case "reveal":
        return { background: "#f04654", foreground: "#ffffff" };
      case "argument":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "return":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "transform":
        return e(n.data.destination);
      default:
        throw new Error(`Unknown shape kind: ${n.data.kind}`);
    }
  };
}
function Z({
  partition: e,
  colorize: n
}) {
  return (t) => {
    const o = (i) => {
      const a = yt(t), { matched: c, unmatched: l } = xt(a, e(a, i));
      c.forEach((d) => {
        const h = t.findById(String(d)), f = h.getModel();
        if (x(f)) {
          const { background: g, foreground: u } = n(f);
          t.updateItem(h, {
            colors: { background: g, foreground: u }
          });
        }
      }), l.forEach((d) => {
        const h = t.findById(String(d)), f = h.getModel();
        x(f) && t.updateItem(h, {
          colors: { background: "#d3d3d3", foreground: "#ffffff" }
        });
      });
    }, r = () => {
      [...t.getNodes(), ...t.getEdges()].forEach((i) => {
        const a = i.getModel();
        if (x(a)) {
          const { background: c, foreground: l } = n(a);
          t.updateItem(i, {
            colors: { background: c, foreground: l }
          });
        }
      });
    }, s = ({ item: i }) => {
      i && o(i.getID());
    };
    return {
      enable: () => {
        t.on("node:mouseenter", s), t.on("node:mouseleave", r);
      },
      disable: () => {
        t.off("node:mouseenter", s), t.off("node:mouseleave", r);
      },
      highlight: (i) => {
        i ? o(i) : r();
      }
    };
  };
}
function wt(e) {
  const [n, t] = B(e), [, o] = B(0), r = I(
    (...s) => {
      const i = n.colorize(...s);
      return o(n.colors().size), i;
    },
    [n]
  );
  return A(
    () => ({
      colorize: r,
      colors: n.colors.bind(n),
      reset: () => {
        o(0), t(e);
      }
    }),
    [r, n, e]
  );
}
function v(e, n = 20, t = "...", o = "start") {
  const r = e.trim();
  return r.length > n ? o === "start" ? `${r.slice(0, n)}${t}` : `${t}${r.slice(r.length - n)}` : e;
}
function J(e, {
  maxWidth: n = 20,
  maxLines: t = 1 / 0,
  placeholder: o = "..."
} = {}) {
  const r = e.split(`
`);
  return r.length > t && (r.splice(t, r.length - t), r[t - 1] = r[t - 1] + o), r.map((s) => v(s, n, o)).join(`
`);
}
function y(e, n, t = 20) {
  const o = e.split(n);
  if (!o.length)
    return "";
  const r = [];
  let s = o.shift();
  return s === void 0 ? "" : (o.forEach((i) => {
    (i + n).length > t ? (s && r.push(s), r.push(`${n}${i}`)) : (s + n + i).length > t ? (r.push(s), s = `${n}${i}`) : s += `${n}${i}`;
  }), s && r.push(s), r.join(`
`));
}
const Et = b({
  kind: "local",
  render: ({
    item: e,
    renderer: n,
    config: {
      colors: { foreground: t, background: o } = {
        foreground: "#ffffff",
        background: "#1d1d1d"
      }
    },
    utils: { reify: r }
  }) => {
    const s = r(void 0, e.data);
    let i = "";
    switch (s == null ? void 0 : s.kind) {
      case "dict":
      case "list":
      case "object":
        i = `${s.snapshot}`;
        break;
      case "function":
        i = `${s.name}()`;
        break;
    }
    i = i.trim();
    let a;
    e.data.name && i ? (a = `${e.data.name} = ${i}`, a.length > 12 && (a = `${e.data.name}
= ${i}`)) : a = i, a = J(a, { maxLines: 3, maxWidth: 15 });
    const c = n.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: o
      }
    }), l = n.addShape("text", {
      name: "label",
      attrs: {
        text: a,
        x: 0,
        y: 0,
        fontFamily: "Roboto Mono, monospace",
        fontSize: 12,
        lineHeight: 16.8,
        textAlign: "center",
        textBaseline: "middle",
        fill: t
      }
    }), { width: d, height: h, x: f, y: g } = l.getBBox();
    return c.attr("width", d + 10), c.attr("height", h + 10), c.attr("x", f - 5), c.attr("y", g - 5), c;
  }
}), St = b({
  kind: "remote",
  render: ({ item: e, renderer: n, config: { colors: t }, utils: { colorize: o } }) => {
    const { background: r, foreground: s } = t || o(e.data.location), i = `${e.data.location.type[0]}${e.data.numbering}`, a = n.addShape("circle", {
      name: "background",
      attrs: {
        x: 0,
        y: 0,
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: r
      }
    });
    n.addShape("text", {
      name: "label",
      attrs: {
        text: i,
        x: 0,
        y: 0,
        fontFamily: "Inter, sans-serif",
        fontWeight: 700,
        fontSize: 12,
        lineHeight: 16,
        textAlign: "center",
        textBaseline: "middle",
        fill: s
      }
    });
    const c = 40 + Math.floor(Math.log10(e.data.numbering || 0) / 2) * 5;
    return a.attr("width", c), a.attr("height", c), a.attr("x", 0), a.attr("y", 0), a.attr("r", c / 2), a;
  }
}), Mt = b({
  kind: "function",
  render: ({ item: e, renderer: n, config: { colors: t }, utils: { reify: o, colorize: r } }) => {
    const { background: s, foreground: i } = t || r(e.location), a = (() => {
      const u = e.location.parties.map((p) => p[0].toUpperCase()).join(",");
      if (e.function) {
        const p = o("function", e.function);
        if (p)
          return J(y(`let ${u} in ${p.name}`, ".", 24), {
            maxWidth: 24,
            maxLines: 2
          });
      }
      return `let ${u} in (anonymous)`;
    })(), c = n.addShape("rect", {
      name: "background",
      attrs: {
        radius: 8,
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: s,
        lineWidth: 2
      }
    }), l = n.addShape("text", {
      name: "label",
      attrs: {
        text: a,
        x: 0,
        y: 0,
        fontFamily: "Roboto Mono, monospace",
        fontSize: 12,
        fontWeight: 600,
        lineHeight: 14.4,
        letterSpacing: 0.5,
        textAlign: "center",
        textBaseline: "middle",
        fill: i
      }
    }), { width: d, height: h, x: f, y: g } = l.getBBox();
    return c.attr("width", d + 30), c.attr("height", h + 15), c.attr("x", f - 15), c.attr("y", g - 7.5), c;
  }
}), $t = b({
  kind: "reveal",
  render: ({
    renderer: e,
    config: {
      colors: { background: n, foreground: t } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const o = e.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: n
      }
    }), r = e.addShape("text", {
      name: "label",
      attrs: {
        text: "reveal",
        x: 0,
        y: 0,
        fontFamily: "Inter, sans-serif",
        fontSize: 12,
        fontWeight: 500,
        lineHeight: 16.8,
        textAlign: "center",
        textBaseline: "middle",
        fill: t
      }
    }), { width: s, height: i, x: a, y: c } = r.getBBox();
    return o.attr("width", s + 10), o.attr("height", i + 10), o.attr("x", a - 5), o.attr("y", c - 5), o;
  }
});
function R(e, n, t, o) {
  return Math.sqrt(Math.pow(t - e, 2) + Math.pow(o - n, 2));
}
function D(e, n, t, o) {
  const r = t - e, s = o - n;
  let i = Math.atan2(s, r);
  return r < 0 && (i -= Math.PI), i > 70 / 180 * Math.PI ? i - 1 / 2 * Math.PI : i < -70 / 180 * Math.PI ? i + 1 / 2 * Math.PI : i;
}
const zt = b({
  kind: "argument",
  render: ({
    item: e,
    renderer: n,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: o = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = n.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", o.x, o.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (e.name) {
      const a = v(e.name, 20), c = i.getPoint(0.5), l = n.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: r
        }
      }), d = n.addShape("text", {
        name: "label",
        attrs: {
          text: a,
          x: c.x,
          y: c.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: s
        }
      }), { width: h, height: f, x: g, y: u } = d.getBBox();
      l.attr("width", h + 5), l.attr("height", f + 5);
      const p = D(t.x, t.y, o.x, o.y);
      h > 30 && h < R(t.x, t.y, o.x, o.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), At = b({
  kind: "reveal",
  render: ({
    item: e,
    renderer: n,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: o = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = n.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", o.x, o.y]
        ],
        lineDash: [2]
      }
    });
    if (e.name) {
      const a = v(e.name, 20), c = i.getPoint(0.5), l = n.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: r
        }
      }), d = n.addShape("text", {
        name: "label",
        attrs: {
          text: a,
          x: c.x,
          y: c.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: s
        }
      }), { width: h, height: f, x: g, y: u } = d.getBBox();
      l.attr("width", h + 5), l.attr("height", f + 5);
      const p = D(t.x, t.y, o.x, o.y);
      h > 30 && h < R(t.x, t.y, o.x, o.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), vt = b({
  kind: "return",
  render: ({
    item: e,
    renderer: n,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: o = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = n.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", o.x, o.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (e.assignment) {
      const a = v(e.assignment, 20), c = i.getPoint(0.5), l = n.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: r
        }
      }), d = n.addShape("text", {
        name: "label",
        attrs: {
          text: a,
          x: c.x,
          y: c.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: s
        }
      }), { width: h, height: f, x: g, y: u } = d.getBBox();
      l.attr("width", h + 5), l.attr("height", f + 5);
      const p = D(t.x, t.y, o.x, o.y);
      h > 30 && h < R(t.x, t.y, o.x, o.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), Ct = b({
  kind: "transform",
  render: ({
    item: e,
    renderer: n,
    config: { startPoint: t = { x: 0, y: 0 }, endPoint: o = { x: 0, y: 0 }, colors: r },
    utils: { colorize: s }
  }) => {
    const { background: i } = r || s(e.destination), a = n.addShape("path", {
      name: "line-background",
      attrs: {
        stroke: i,
        lineWidth: 3,
        path: [
          ["M", t.x, t.y],
          ["L", o.x, o.y]
        ]
      }
    });
    return n.addShape("path", {
      name: "line-foreground",
      attrs: {
        stroke: "#ffffff",
        lineWidth: 1.5,
        path: [
          ["M", t.x, t.y],
          ["L", o.x, o.y]
        ]
      }
    }), a;
  }
});
function Nt() {
  return {
    fromGraph: mt({
      nodes: [Et, St, Mt, $t],
      edges: [zt, vt, Ct, At]
    })
  };
}
function O(e, n) {
  e.append("strong").text(n).style("font-size", "0.9rem"), e.append("hr").style("margin", "3px 0").style("border", 0).style("border-top", "1px solid #d3d3d3");
}
function w(e, n) {
  const t = e.append("div").style("display", "grid").style("gap", ".3rem").style("min-width", "0").style("grid-template-columns", "2fr 8fr").style("grid-auto-flow", "row").style("align-items", "baseline");
  n.forEach(([o, r]) => {
    t.append("span").text(o), t.append("code").style("font-weight", 700).style("word-break", "break-all").style("background", "none").text(r);
  });
}
function z(e, n) {
  e.append("div").style("background", "#f5f5f5").style("margin", "6px 0 0").style("max-height", "10vh").style("overflow", "auto").style("padding", "6px").append("pre").style("background", "none").style("overflow", "auto").style("white-space", "pre").style("word-break", "break-all").text(n);
}
function jt({ root: e }) {
  O(e, (t) => `Remote object #${t.data.numbering || "numbering ?"}`), w(e, [
    ["Device", (t) => t.data.location.type],
    [
      (t) => t.data.location.parties.length > 1 ? "Parties" : "Party",
      (t) => t.data.location.parties.join(", ")
    ]
  ]);
  const n = e.datum().data.location.parameters || {};
  Object.keys(n).length > 0 && z(e, () => ut.stringify({ properties: n }, { indent: 2 }));
}
function Bt({ root: e, reify: n }) {
  O(e, "Local value");
  const t = n(void 0, e.datum().data), o = e.datum();
  switch (t == null ? void 0 : t.kind) {
    case "object":
    case "list":
    case "dict":
      w(e.datum(t), [
        ["Name", o.data.name || "?"],
        ["Type", (r) => y(r.type, ".", 30)]
      ]), z(e.datum(t), (r) => r.snapshot);
      break;
    case "none":
      w(e.datum(t), [
        ["Name", o.data.name || "?"],
        ["Value", "None"]
      ]);
      break;
    case "function":
      w(e.datum(t), [
        ["Function", (r) => y(r.name, ".", 32)],
        ["Module", (r) => y(r.module || "?", ".", 32)],
        ["File", (r) => y(r.filename || "?", "/", 32)],
        ["Line", (r) => r.firstlineno || "?"]
      ]), z(e.datum(t), (r) => r.source || "(no source)");
      break;
  }
}
function It({ root: e, reify: n }) {
  O(e, "Code execution"), w(e, [
    ["Device", (o) => `${o.location.type}[${o.location.parties.join(", ")}]`],
    ["Frame #", (o) => o.epoch]
  ]);
  const t = n("function", e.datum().function);
  t && (w(e.datum(t), [
    ["Function", (o) => y(o.name, ".", 32)],
    ["Module", (o) => y(o.module || "?", ".", 32)],
    [
      "File",
      (o) => `${y(o.filename || "?", "/", 32)}, line ${o.firstlineno || "?"}`
    ]
  ]), z(e.datum(t), (o) => o.source || "(no source, likely a C function)"));
}
function Lt(e, n) {
  if (!x(e))
    return "";
  const t = document.createElement("div"), o = ft.select(t), { data: r } = e;
  switch (r.kind) {
    case "remote":
      jt({ root: o.datum(r), reify: n });
      break;
    case "local":
      Bt({ root: o.datum(r), reify: n });
      break;
    case "function":
      It({ root: o.datum(r), reify: n });
      break;
  }
  return o.style("box-sizing", "border-box").style("padding", "10px").style("margin", "0").style("display", "flex").style("flex-direction", "column").style("align-items", "stretch").style("gap", ".3rem").style("font-size", "0.8rem").style("color", "#333").style("border-radius", "4px").style("background-color", "#fff").style("min-width", "200px").style("max-width", "25vw").style(
    "box-shadow",
    "0px 1px 2px -2px rgba(0,0,0,0.08), 0px 3px 6px 0px rgba(0,0,0,0.06), 0px 5px 12px 4px rgba(0,0,0,0.03)"
  ), t.childNodes.length === 0 ? "" : t.outerHTML;
}
const { fromGraph: Rt } = Nt(), Dt = () => new S([
  "#79a25c",
  "#de4c8b",
  "#8271df",
  "#3398a6",
  "#c47d3a",
  "#b45dcb",
  "#4c99d8",
  "#df6a72"
]);
function Ot({
  graph: e,
  colorizer: n
}) {
  const t = A(
    () => Z({
      partition: kt,
      colorize: q(n.colorize)
    }),
    [n.colorize]
  ), o = I(() => {
    e.current && t(e.current).highlight(null);
  }, [e, t]), r = I(
    (a) => () => {
      if (!e.current)
        return;
      const c = e.current.getNodes().find((l) => {
        const d = l.getModel();
        if (!x(d))
          return !1;
        switch (d.data.kind) {
          case "function":
            return S.locationKey(d.data.location) === a;
          case "remote":
            return S.locationKey(d.data.data.location) === a;
          default:
            return !1;
        }
      });
      c && t(e.current).highlight(c.getID());
    },
    [e, t]
  ), [s, i] = B();
  return /* @__PURE__ */ m(
    "div",
    {
      style: {
        display: "grid",
        gridTemplateColumns: "20px 1fr",
        gridAutoRows: "20px",
        alignItems: "center",
        gap: "0.3rem"
      },
      onMouseLeave: (a) => {
        i(void 0), o(a);
      },
      children: [...n.colors()].map(([a, { name: c, color: l }]) => /* @__PURE__ */ $(it, { children: [
        /* @__PURE__ */ m(
          "div",
          {
            style: { width: 16, height: 16, margin: 2, backgroundColor: l },
            onMouseEnter: (d) => {
              r(a)(d), i(a);
            }
          }
        ),
        /* @__PURE__ */ m(
          "div",
          {
            onMouseEnter: (d) => {
              r(a)(d), i(a);
            },
            children: /* @__PURE__ */ m(
              "span",
              {
                style: {
                  fontFamily: "Inter, sans-serif",
                  fontWeight: s === a ? 700 : 400,
                  pointerEvents: "none"
                },
                children: c
              }
            )
          }
        )
      ] }, a))
    }
  );
}
function Ft() {
  const { reify: e } = pt(), n = wt(Dt), t = A(
    () => Z({
      partition: bt,
      colorize: q(n.colorize)
    }),
    [n.colorize]
  ), o = N(null), r = N(), s = N(!0);
  return L(() => {
    if (!o.current) {
      r.current = void 0;
      return;
    }
    const i = new ct.Graph({
      container: o.current,
      width: o.current.clientWidth,
      height: o.current.clientHeight,
      layout: {
        type: "dagre",
        ranksepFunc: (a) => {
          var c, l, d;
          return ((c = a.data) == null ? void 0 : c.kind) === "reveal" || ((l = a.data) == null ? void 0 : l.kind) === "remote" ? 2.5 : ((d = a.data) == null ? void 0 : d.kind) === "local" ? 5 : 10;
        },
        nodesep: 10
      },
      modes: {
        default: [
          { type: "scroll-canvas" },
          { type: "drag-canvas" },
          {
            type: "tooltip",
            formatText: (a) => s.current ? Lt(a, e) : "",
            offset: 10
          }
        ],
        highlighting: []
      },
      minZoom: 0.2,
      maxZoom: 3
    });
    return i.on("node:click", ({ item: a }) => {
      a && i.focusItem(a);
    }), t(i).enable(), r.current = i, () => {
      i.destroy();
    };
  }, [t, e]), L(() => {
    var c;
    const i = (c = o.current) == null ? void 0 : c.closest(".jp-LinkedOutputView"), a = new ResizeObserver(() => {
      var h;
      if (!o.current)
        return;
      const [l, d] = (() => i && i.clientHeight !== 0 ? [i.clientHeight, `${i.clientHeight}px`] : [
        o.current.clientHeight,
        `${o.current.clientHeight}px`
      ])();
      o.current.style.height = d, (h = r.current) == null || h.changeSize(o.current.clientWidth, l);
    });
    return o.current && a.observe(o.current), i && a.observe(i), () => {
      a.disconnect();
    };
  }, []), {
    container: o,
    graph: r,
    colorizer: n,
    tooltipEnabled: s,
    load: (i) => {
      var a, c;
      (a = r.current) == null || a.data(Rt(i, { reify: e, colorize: n.colorize })), (c = r.current) == null || c.render();
    }
  };
}
function Tt(e) {
  const { container: n, load: t, graph: o, colorizer: r, tooltipEnabled: s } = Ft();
  return L(() => {
    t(e);
  }, [e, t]), /* @__PURE__ */ $("div", { style: { position: "relative" }, children: [
    /* @__PURE__ */ m(
      "div",
      {
        style: { width: "100%", height: "80vh", minHeight: "600px" },
        ref: n
      }
    ),
    /* @__PURE__ */ m("div", { style: { position: "absolute", top: "1rem", right: "1rem" }, children: /* @__PURE__ */ $(X, { size: "small", style: { fontSize: ".8rem" }, children: [
      /* @__PURE__ */ $(G, { theme: { token: { marginLG: 8 } }, children: [
        /* @__PURE__ */ m(
          "span",
          {
            style: {
              fontWeight: 700,
              backgroundColor: "#f04654",
              color: "#ffffff",
              display: "inline-block",
              padding: "0.2rem 0.5rem",
              borderRadius: "0.2rem"
            },
            children: "DEVELOPER PREVIEW"
          }
        ),
        /* @__PURE__ */ m(H, {})
      ] }),
      /* @__PURE__ */ m(Ot, { graph: o, colorizer: r }),
      /* @__PURE__ */ m(G, { theme: { token: { marginLG: 8 } }, children: /* @__PURE__ */ m(H, {}) }),
      /* @__PURE__ */ m(
        tt.Item,
        {
          name: "tooltipEnabled",
          label: "Tooltip",
          style: {
            margin: 0,
            height: 20,
            display: "flex",
            alignItems: "center",
            fontSize: ".8rem"
          },
          colon: !1,
          children: /* @__PURE__ */ m(
            et,
            {
              size: "small",
              defaultChecked: s.current,
              onChange: (i) => {
                s.current = i;
              }
            }
          )
        }
      )
    ] }) })
  ] });
}
function Yt({ timeline: e }) {
  return /* @__PURE__ */ m(nt.ErrorBoundary, { message: /* @__PURE__ */ m("strong", { children: "Exception in cell output:" }), children: /* @__PURE__ */ m(gt, { timeline: e, children: /* @__PURE__ */ m(Tt, k({}, e.graph)) }) });
}
function Pt({
  elem: e,
  Component: n,
  props: t
}) {
  ht(e).render(
    /* @__PURE__ */ m(at, { children: /* @__PURE__ */ m(n, k({}, t)) })
  );
}
export {
  Yt as Visualization,
  Pt as render
};
