var q = Object.defineProperty;
var Z = (e, o, t) => o in e ? q(e, o, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[o] = t;
var S = (e, o, t) => (Z(e, typeof o != "symbol" ? o + "" : o, t), t);
import { jsx as m, jsxs as M } from "react/jsx-runtime";
import { Card as J, ConfigProvider as O, Divider as F, Form as Y, Switch as P, Alert as Q } from "antd";
import { createContext as X, useMemo as z, useContext as tt, useState as N, useCallback as j, useEffect as B, Fragment as et, useRef as v, StrictMode as nt } from "react";
import * as ot from "@antv/g6";
import { registerNode as rt, registerEdge as it } from "@antv/g6";
import T from "color";
import { Graph as at } from "@antv/graphlib";
import G from "lodash/isEqual";
import * as ct from "d3";
import st from "yaml";
import { createRoot as lt } from "react-dom/client";
function C(e) {
  return Array.isArray(e);
}
function H(e) {
  return typeof e == "object" && e !== null && !Object.hasOwn(e, "kind");
}
function w(e, o, t) {
  if ((o == null ? void 0 : o.ref) === void 0)
    return;
  const n = t == null ? void 0 : t[o.ref];
  if (n === void 0 || e !== void 0 && n.kind !== e)
    return;
  const r = Object.fromEntries(
    Object.entries(n).filter(
      ([, i]) => !C(i) && !H(i)
    )
  ), s = Object.fromEntries(
    Object.entries(n).filter(([, i]) => H(i) || C(i)).map(([i, a]) => {
      const c = a;
      let l, d;
      return C(c) ? (l = (f) => c[Number(f)], d = function* () {
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
            return w(u.kind, g, t);
        },
        ofKind: (f, g) => {
          const u = l(g);
          if (!u)
            return;
          const p = t == null ? void 0 : t[u.ref];
          if ((p == null ? void 0 : p.kind) === f)
            return w(f, u, t);
        },
        items: function* () {
          for (const [f, g] of d()) {
            const u = t == null ? void 0 : t[g.ref];
            if (!(u != null && u.kind))
              continue;
            const p = w(u.kind, g, t);
            p && (yield [f, p]);
          }
        },
        itemsOfKind: function* (f) {
          for (const [g, u] of d()) {
            const p = t == null ? void 0 : t[u.ref];
            if ((p == null ? void 0 : p.kind) !== f)
              continue;
            const D = w(f, u, t);
            D && (yield [g, D]);
          }
        }
      }];
    })
  );
  return { ...r, ...s };
}
const _ = X({
  reify: () => {
  }
}), dt = ({
  timeline: e,
  children: o
}) => {
  const t = z(
    () => ({
      reify: (n, r) => w(n, r, e == null ? void 0 : e.variables)
    }),
    [e == null ? void 0 : e.variables]
  );
  return /* @__PURE__ */ m(_.Provider, { value: t, children: o });
};
function ft() {
  return tt(_);
}
function x(e) {
  return typeof e == "object" && e !== null && "data" in e && typeof e.data == "object" && e.data !== null && "kind" in e.data && typeof e.data.kind == "string";
}
function b({
  kind: e,
  render: o,
  options: t
}) {
  return {
    kind: e,
    draw: (n, r) => {
      if (!x(n))
        throw new Error(
          `Unexpected model for shape ${e}: ${JSON.stringify(n)}`
        );
      const s = n.data, i = n._utils, a = o({ item: s, renderer: r, config: n, utils: i });
      return n.size = [a.attr("width"), a.attr("height")], a;
    },
    ...t
  };
}
function ut({
  nodes: e,
  edges: o
}) {
  const t = (n, r) => `${n}:${r.kind}`;
  return e.forEach((n) => rt(t("node", n), n)), o.forEach((n) => it(t("edge", n), n)), function(r, s) {
    var i, a;
    return {
      nodes: ((i = r.nodes) == null ? void 0 : i.map(
        (c) => ({
          id: c.id,
          type: t("node", c),
          data: c,
          _utils: s
        })
      )) ?? [],
      edges: ((a = r.edges) == null ? void 0 : a.map(
        (c) => ({
          id: `${c.source}-${c.target}`,
          source: c.source,
          target: c.target,
          type: t("edge", c),
          data: c,
          _utils: s
        })
      )) ?? []
    };
  };
}
function ht(e) {
  const { nodes: o = [], edges: t = [] } = e.save();
  return new at({
    nodes: o.filter(x),
    edges: t.filter(x)
  });
}
function W(e, o, t, n) {
  const r = [...t.bind(e)(o)], s = [...r], i = new Set(r.map((a) => a.id));
  for (; r.length > 0; ) {
    const a = r.shift();
    if (!a)
      break;
    if (n && n(e.getNode(a.id)))
      continue;
    t.bind(e)(a.id).filter((l) => !i.has(l.id)).forEach((l) => {
      i.add(l.id), r.push(l), s.push(l);
    });
  }
  return s;
}
function gt(e, o) {
  [...o].forEach(
    (n) => e.getRelatedEdges(n, "both").forEach((r) => {
      o.has(r.source) && o.has(r.target) && o.add(r.id);
    })
  );
  const t = /* @__PURE__ */ new Set([
    ...e.getAllNodes().filter((n) => !o.has(n.id)).map((n) => n.id),
    ...e.getAllEdges().filter((n) => !o.has(n.id)).map((n) => n.id)
  ]);
  return { matched: o, unmatched: t };
}
const pt = (e, o) => {
  const t = new Set(
    (() => {
      switch (e.getNode(o).data.kind) {
        case "function":
          return e.getNeighbors(o);
        case "reveal":
          return e.getNeighbors(o);
        case "remote":
        case "local":
          return [
            ...W(e, o, e.getPredecessors),
            ...W(e, o, e.getSuccessors)
          ];
        default:
          return [];
      }
    })().map((n) => n.id)
  );
  return t.add(o), t;
}, mt = (e, o) => {
  const t = (r) => (s) => {
    switch (s.data.kind) {
      case "function":
        return G(s.data.location, r);
      case "remote":
        return G(s.data.data.location, r);
      case "local":
        return e.getSuccessors(s.id).some((i) => t(r)(i));
      default:
        return !1;
    }
  }, n = new Set(
    (() => {
      const r = e.getNode(o);
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
  return n.add(o), n;
};
class E {
  constructor(o) {
    S(this, "palette");
    S(this, "cache", /* @__PURE__ */ new Map());
    S(this, "names", /* @__PURE__ */ new Map());
    this.palette = o;
  }
  colorize(o) {
    const t = E.locationKey(o);
    let n = this.cache.get(t);
    return n || (n = this.makeColor(), this.cache.set(t, n)), this.names.set(t, this.locationName(o)), { background: n, foreground: this.foreground(n) };
  }
  colors() {
    return new Map(
      [...this.names.entries()].map(([o, t]) => [
        o,
        { name: t, color: this.cache.get(o) }
      ])
    );
  }
  locationName(o) {
    return `${o.type}[${o.parties.join(", ")}]`;
  }
  static locationKey(o) {
    return [
      o.type,
      ...o.parties,
      ...Object.entries(o.parameters ?? {}).map(([t, n]) => `${t}=${n}`)
    ].join(":");
  }
  makeColor() {
    const o = this.cache.size, t = o % this.palette.length, n = Math.floor(o / this.palette.length);
    if (n === 0)
      return this.palette[t];
    const s = [
      // triadic
      120,
      240,
      // tetradic
      90,
      180,
      270
    ][n - 1];
    if (s === void 0)
      throw new Error("Too many colors");
    return new T(this.palette[t]).rotate(s).hex();
  }
  foreground(o, t = 0.2, n = "#ffffff", r = "#1d1d1d") {
    return new T(o).darken(t).isDark() ? n : r;
  }
}
function V(e) {
  return (o) => {
    switch (o.data.kind) {
      case "function":
        return e(o.data.location);
      case "local":
        return { background: "#1d1d1d", foreground: "#ffffff" };
      case "remote":
        return e(o.data.data.location);
      case "reveal":
        return { background: "#f04654", foreground: "#ffffff" };
      case "argument":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "return":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "transform":
        return e(o.data.destination);
      default:
        throw new Error(`Unknown shape kind: ${o.data.kind}`);
    }
  };
}
function U({
  partition: e,
  colorize: o
}) {
  return (t) => {
    const n = (i) => {
      const a = ht(t), { matched: c, unmatched: l } = gt(a, e(a, i));
      c.forEach((d) => {
        const h = t.findById(String(d)), f = h.getModel();
        if (x(f)) {
          const { background: g, foreground: u } = o(f);
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
          const { background: c, foreground: l } = o(a);
          t.updateItem(i, {
            colors: { background: c, foreground: l }
          });
        }
      });
    }, s = ({ item: i }) => {
      i && n(i.getID());
    };
    return {
      enable: () => {
        t.on("node:mouseenter", s), t.on("node:mouseleave", r);
      },
      disable: () => {
        t.off("node:mouseenter", s), t.off("node:mouseleave", r);
      },
      highlight: (i) => {
        i ? n(i) : r();
      }
    };
  };
}
function yt(e) {
  const [o, t] = N(e), [, n] = N(0), r = j(
    (...s) => {
      const i = o.colorize(...s);
      return n(o.colors().size), i;
    },
    [o]
  );
  return z(
    () => ({
      colorize: r,
      colors: o.colors.bind(o),
      reset: () => {
        n(0), t(e);
      }
    }),
    [r, o, e]
  );
}
function A(e, o = 20, t = "...", n = "start") {
  const r = e.trim();
  return r.length > o ? n === "start" ? `${r.slice(0, o)}${t}` : `${t}${r.slice(r.length - o)}` : e;
}
function K(e, {
  maxWidth: o = 20,
  maxLines: t = 1 / 0,
  placeholder: n = "..."
} = {}) {
  const r = e.split(`
`);
  return r.length > t && (r.splice(t, r.length - t), r[t - 1] = r[t - 1] + n), r.map((s) => A(s, o, n)).join(`
`);
}
function y(e, o, t = 20) {
  const n = e.split(o);
  if (!n.length)
    return "";
  const r = [];
  let s = n.shift();
  return s === void 0 ? "" : (n.forEach((i) => {
    (i + o).length > t ? (s && r.push(s), r.push(`${o}${i}`)) : (s + o + i).length > t ? (r.push(s), s = `${o}${i}`) : s += `${o}${i}`;
  }), s && r.push(s), r.join(`
`));
}
const xt = b({
  kind: "local",
  render: ({
    item: e,
    renderer: o,
    config: {
      colors: { foreground: t, background: n } = {
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
= ${i}`)) : a = i, a = K(a, { maxLines: 3, maxWidth: 15 });
    const c = o.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: n
      }
    }), l = o.addShape("text", {
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
}), bt = b({
  kind: "remote",
  render: ({ item: e, renderer: o, config: { colors: t }, utils: { colorize: n } }) => {
    const { background: r, foreground: s } = t || n(e.data.location), i = `${e.data.location.type[0]}${e.data.numbering}`, a = o.addShape("circle", {
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
    o.addShape("text", {
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
}), kt = b({
  kind: "function",
  render: ({ item: e, renderer: o, config: { colors: t }, utils: { reify: n, colorize: r } }) => {
    const { background: s, foreground: i } = t || r(e.location), a = (() => {
      const u = e.location.parties.map((p) => p[0].toUpperCase()).join(",");
      if (e.function) {
        const p = n("function", e.function);
        if (p)
          return K(y(`let ${u} in ${p.name}`, ".", 24), {
            maxWidth: 24,
            maxLines: 2
          });
      }
      return `let ${u} in (anonymous)`;
    })(), c = o.addShape("rect", {
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
    }), l = o.addShape("text", {
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
}), wt = b({
  kind: "reveal",
  render: ({
    renderer: e,
    config: {
      colors: { background: o, foreground: t } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const n = e.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: o
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
    return n.attr("width", s + 10), n.attr("height", i + 10), n.attr("x", a - 5), n.attr("y", c - 5), n;
  }
});
function I(e, o, t, n) {
  return Math.sqrt(Math.pow(t - e, 2) + Math.pow(n - o, 2));
}
function L(e, o, t, n) {
  const r = t - e, s = n - o;
  let i = Math.atan2(s, r);
  return r < 0 && (i -= Math.PI), i > 70 / 180 * Math.PI ? i - 1 / 2 * Math.PI : i < -70 / 180 * Math.PI ? i + 1 / 2 * Math.PI : i;
}
const Et = b({
  kind: "argument",
  render: ({
    item: e,
    renderer: o,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: n = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = o.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", n.x, n.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (e.name) {
      const a = A(e.name, 20), c = i.getPoint(0.5), l = o.addShape("rect", {
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
      }), d = o.addShape("text", {
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
      const p = L(t.x, t.y, n.x, n.y);
      h > 30 && h < I(t.x, t.y, n.x, n.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), St = b({
  kind: "reveal",
  render: ({
    item: e,
    renderer: o,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: n = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = o.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", n.x, n.y]
        ],
        lineDash: [2]
      }
    });
    if (e.name) {
      const a = A(e.name, 20), c = i.getPoint(0.5), l = o.addShape("rect", {
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
      }), d = o.addShape("text", {
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
      const p = L(t.x, t.y, n.x, n.y);
      h > 30 && h < I(t.x, t.y, n.x, n.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), Mt = b({
  kind: "return",
  render: ({
    item: e,
    renderer: o,
    config: {
      startPoint: t = { x: 0, y: 0 },
      endPoint: n = { x: 0, y: 0 },
      colors: { background: r, foreground: s } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const i = o.addShape("path", {
      name: "line",
      attrs: {
        stroke: r,
        lineWidth: 1,
        path: [
          ["M", t.x, t.y],
          ["L", n.x, n.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (e.assignment) {
      const a = A(e.assignment, 20), c = i.getPoint(0.5), l = o.addShape("rect", {
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
      }), d = o.addShape("text", {
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
      const p = L(t.x, t.y, n.x, n.y);
      h > 30 && h < I(t.x, t.y, n.x, n.y) - 20 && (l.rotateAtPoint(c.x, c.y, p), d.rotateAtPoint(c.x, c.y, p)), l.attr("x", g - 2.5), l.attr("y", u - 2.5);
    }
    return i;
  }
}), $t = b({
  kind: "transform",
  render: ({
    item: e,
    renderer: o,
    config: { startPoint: t = { x: 0, y: 0 }, endPoint: n = { x: 0, y: 0 }, colors: r },
    utils: { colorize: s }
  }) => {
    const { background: i } = r || s(e.destination), a = o.addShape("path", {
      name: "line-background",
      attrs: {
        stroke: i,
        lineWidth: 3,
        path: [
          ["M", t.x, t.y],
          ["L", n.x, n.y]
        ]
      }
    });
    return o.addShape("path", {
      name: "line-foreground",
      attrs: {
        stroke: "#ffffff",
        lineWidth: 1.5,
        path: [
          ["M", t.x, t.y],
          ["L", n.x, n.y]
        ]
      }
    }), a;
  }
});
function zt() {
  return {
    fromGraph: ut({
      nodes: [xt, bt, kt, wt],
      edges: [Et, Mt, $t, St]
    })
  };
}
function R(e, o) {
  e.append("strong").text(o).style("font-size", "0.9rem"), e.append("hr").style("margin", "3px 0").style("border", 0).style("border-top", "1px solid #d3d3d3");
}
function k(e, o) {
  const t = e.append("div").style("display", "grid").style("gap", ".3rem").style("min-width", "0").style("grid-template-columns", "2fr 8fr").style("grid-auto-flow", "row").style("align-items", "baseline");
  o.forEach(([n, r]) => {
    t.append("span").text(n), t.append("code").style("font-weight", 700).style("word-break", "break-all").style("background", "none").text(r);
  });
}
function $(e, o) {
  e.append("div").style("background", "#f5f5f5").style("margin", "6px 0 0").style("max-height", "10vh").style("overflow", "auto").style("padding", "6px").append("pre").style("background", "none").style("overflow", "auto").style("white-space", "pre").style("word-break", "break-all").text(o);
}
function At({ root: e }) {
  R(e, (t) => `Remote object #${t.data.numbering || "numbering ?"}`), k(e, [
    ["Device", (t) => t.data.location.type],
    [
      (t) => t.data.location.parties.length > 1 ? "Parties" : "Party",
      (t) => t.data.location.parties.join(", ")
    ]
  ]);
  const o = e.datum().data.location.parameters || {};
  Object.keys(o).length > 0 && $(e, () => st.stringify({ properties: o }, { indent: 2 }));
}
function vt({ root: e, reify: o }) {
  R(e, "Local value");
  const t = o(void 0, e.datum().data), n = e.datum();
  switch (t == null ? void 0 : t.kind) {
    case "object":
    case "list":
    case "dict":
      k(e.datum(t), [
        ["Name", n.data.name || "?"],
        ["Type", (r) => y(r.type, ".", 30)]
      ]), $(e.datum(t), (r) => r.snapshot);
      break;
    case "none":
      k(e.datum(t), [
        ["Name", n.data.name || "?"],
        ["Value", "None"]
      ]);
      break;
    case "function":
      k(e.datum(t), [
        ["Function", (r) => y(r.name, ".", 32)],
        ["Module", (r) => y(r.module || "?", ".", 32)],
        ["File", (r) => y(r.filename || "?", "/", 32)],
        ["Line", (r) => r.firstlineno || "?"]
      ]), $(e.datum(t), (r) => r.source || "(no source)");
      break;
  }
}
function Ct({ root: e, reify: o }) {
  R(e, "Code execution"), k(e, [
    ["Device", (n) => `${n.location.type}[${n.location.parties.join(", ")}]`],
    ["Frame #", (n) => n.epoch]
  ]);
  const t = o("function", e.datum().function);
  t && (k(e.datum(t), [
    ["Function", (n) => y(n.name, ".", 32)],
    ["Module", (n) => y(n.module || "?", ".", 32)],
    [
      "File",
      (n) => `${y(n.filename || "?", "/", 32)}, line ${n.firstlineno || "?"}`
    ]
  ]), $(e.datum(t), (n) => n.source || "(no source, likely a C function)"));
}
function Nt(e, o) {
  if (!x(e))
    return "";
  const t = document.createElement("div"), n = ct.select(t), { data: r } = e;
  switch (r.kind) {
    case "remote":
      At({ root: n.datum(r), reify: o });
      break;
    case "local":
      vt({ root: n.datum(r), reify: o });
      break;
    case "function":
      Ct({ root: n.datum(r), reify: o });
      break;
  }
  return n.style("box-sizing", "border-box").style("padding", "10px").style("margin", "0").style("display", "flex").style("flex-direction", "column").style("align-items", "stretch").style("gap", ".3rem").style("font-size", "0.8rem").style("color", "#333").style("border-radius", "4px").style("background-color", "#fff").style("min-width", "200px").style("max-width", "25vw").style(
    "box-shadow",
    "0px 1px 2px -2px rgba(0,0,0,0.08), 0px 3px 6px 0px rgba(0,0,0,0.06), 0px 5px 12px 4px rgba(0,0,0,0.03)"
  ), t.childNodes.length === 0 ? "" : t.outerHTML;
}
const { fromGraph: jt } = zt(), Bt = () => new E([
  "#79a25c",
  "#de4c8b",
  "#8271df",
  "#3398a6",
  "#c47d3a",
  "#b45dcb",
  "#4c99d8",
  "#df6a72"
]);
function It({
  graph: e,
  colorizer: o
}) {
  const t = z(
    () => U({
      partition: mt,
      colorize: V(o.colorize)
    }),
    [o.colorize]
  ), n = j(() => {
    e.current && t(e.current).highlight(null);
  }, [e, t]), r = j(
    (a) => () => {
      if (!e.current)
        return;
      const c = e.current.getNodes().find((l) => {
        const d = l.getModel();
        if (!x(d))
          return !1;
        switch (d.data.kind) {
          case "function":
            return E.locationKey(d.data.location) === a;
          case "remote":
            return E.locationKey(d.data.data.location) === a;
          default:
            return !1;
        }
      });
      c && t(e.current).highlight(c.getID());
    },
    [e, t]
  ), [s, i] = N();
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
        i(void 0), n(a);
      },
      children: [...o.colors()].map(([a, { name: c, color: l }]) => /* @__PURE__ */ M(et, { children: [
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
function Lt() {
  const { reify: e } = ft(), o = yt(Bt), t = z(
    () => U({
      partition: pt,
      colorize: V(o.colorize)
    }),
    [o.colorize]
  ), n = v(null), r = v(), s = v(!0);
  return B(() => {
    if (!n.current) {
      r.current = void 0;
      return;
    }
    const i = new ot.Graph({
      container: n.current,
      width: n.current.clientWidth,
      height: n.current.clientHeight,
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
            formatText: (a) => s.current ? Nt(a, e) : "",
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
  }, [t, e]), B(() => {
    var c;
    const i = (c = n.current) == null ? void 0 : c.closest(".jp-LinkedOutputView"), a = new ResizeObserver(() => {
      var h;
      if (!n.current)
        return;
      const [l, d] = (() => i && i.clientHeight !== 0 ? [i.clientHeight, `${i.clientHeight}px`] : [
        n.current.clientHeight,
        `${n.current.clientHeight}px`
      ])();
      n.current.style.height = d, (h = r.current) == null || h.changeSize(n.current.clientWidth, l);
    });
    return n.current && a.observe(n.current), i && a.observe(i), () => {
      a.disconnect();
    };
  }, []), {
    container: n,
    graph: r,
    colorizer: o,
    tooltipEnabled: s,
    load: (i) => {
      var a, c;
      (a = r.current) == null || a.data(jt(i, { reify: e, colorize: o.colorize })), (c = r.current) == null || c.render();
    }
  };
}
function Rt(e) {
  const { container: o, load: t, graph: n, colorizer: r, tooltipEnabled: s } = Lt();
  return B(() => {
    t(e);
  }, [e, t]), /* @__PURE__ */ M("div", { style: { position: "relative" }, children: [
    /* @__PURE__ */ m(
      "div",
      {
        style: { width: "100%", height: "80vh", minHeight: "600px" },
        ref: o
      }
    ),
    /* @__PURE__ */ m("div", { style: { position: "absolute", top: "1rem", right: "1rem" }, children: /* @__PURE__ */ M(J, { size: "small", style: { fontSize: ".8rem" }, children: [
      /* @__PURE__ */ M(O, { theme: { token: { marginLG: 8 } }, children: [
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
        /* @__PURE__ */ m(F, {})
      ] }),
      /* @__PURE__ */ m(It, { graph: n, colorizer: r }),
      /* @__PURE__ */ m(O, { theme: { token: { marginLG: 8 } }, children: /* @__PURE__ */ m(F, {}) }),
      /* @__PURE__ */ m(
        Y.Item,
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
            P,
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
function Kt({ timeline: e }) {
  return /* @__PURE__ */ m(Q.ErrorBoundary, { message: /* @__PURE__ */ m("strong", { children: "Exception in cell output:" }), children: /* @__PURE__ */ m(dt, { timeline: e, children: /* @__PURE__ */ m(Rt, { ...e.graph }) }) });
}
function qt({
  elem: e,
  Component: o,
  props: t
}) {
  lt(e).render(
    /* @__PURE__ */ m(nt, { children: /* @__PURE__ */ m(o, { ...t }) })
  );
}
export {
  Kt as Visualization,
  qt as render
};
