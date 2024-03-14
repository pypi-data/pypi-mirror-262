var __defProp = Object.defineProperty;
var __getOwnPropSymbols = Object.getOwnPropertySymbols;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __propIsEnum = Object.prototype.propertyIsEnumerable;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __spreadValues = (a, b) => {
  for (var prop in b || (b = {}))
    if (__hasOwnProp.call(b, prop))
      __defNormalProp(a, prop, b[prop]);
  if (__getOwnPropSymbols)
    for (var prop of __getOwnPropSymbols(b)) {
      if (__propIsEnum.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    }
  return a;
};
var __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};
import { jsxDEV } from "https://esm.sh/react@^18.2.0/jsx-dev-runtime";
import { Card, ConfigProvider, Divider, Form, Switch, Alert } from "https://esm.sh/antd@^5.10.2";
import { createContext, useMemo, useContext, useState, useCallback, useEffect, Fragment, useRef, StrictMode } from "https://esm.sh/react@^18.2.0";
import * as G6 from "https://esm.sh/@antv/g6@^4.8.23";
import { registerNode, registerEdge } from "https://esm.sh/@antv/g6@^4.8.23";
import Color from "https://esm.sh/color@^4.2.3";
import { Graph } from "https://esm.sh/@antv/graphlib@^2.0.2";
import isEqual from "https://esm.sh/lodash@^4.17.21/isEqual";
import * as d3 from "https://esm.sh/d3@^7.8.5";
import YAML from "https://esm.sh/yaml@^2.3.4";
import { createRoot } from "https://esm.sh/react-dom@^18.2.0/client";
function isReferenceList(value) {
  return Array.isArray(value);
}
function isReferenceMap(value) {
  return typeof value === "object" && value !== null && !Object.hasOwn(value, "kind");
}
function reify(rootKind, rootRef, variables) {
  if ((rootRef == null ? void 0 : rootRef.ref) === void 0) {
    return void 0;
  }
  const root = variables == null ? void 0 : variables[rootRef.ref];
  if (root === void 0) {
    return void 0;
  }
  if (rootKind !== void 0 && root.kind !== rootKind) {
    return void 0;
  }
  const staticItems = Object.fromEntries(
    Object.entries(root).filter(
      ([, value]) => !isReferenceList(value) && !isReferenceMap(value)
    )
  );
  const deferredItems = Object.fromEntries(
    Object.entries(root).filter(([, value]) => isReferenceMap(value) || isReferenceList(value)).map(([rootKey, _]) => {
      const lookup = _;
      let getReference;
      let iterKeys;
      if (isReferenceList(lookup)) {
        getReference = (k) => lookup[Number(k)];
        iterKeys = function* () {
          for (let i = 0; i < lookup.length; i++) {
            yield [i, lookup[i]];
          }
        };
      } else {
        getReference = (k) => lookup[String(k)];
        iterKeys = function* () {
          for (const [k, v] of Object.entries(lookup)) {
            yield [k, v];
          }
        };
      }
      const resolver = {
        get: (item) => {
          const ref = getReference(item);
          if (!ref) {
            return void 0;
          }
          const value = variables == null ? void 0 : variables[ref.ref];
          if (!(value == null ? void 0 : value.kind)) {
            return void 0;
          }
          return reify(value.kind, ref, variables);
        },
        ofKind: (kind, item) => {
          const ref = getReference(item);
          if (!ref) {
            return void 0;
          }
          const value = variables == null ? void 0 : variables[ref.ref];
          if ((value == null ? void 0 : value.kind) !== kind) {
            return void 0;
          }
          return reify(kind, ref, variables);
        },
        items: function* () {
          for (const [key, ref] of iterKeys()) {
            const value = variables == null ? void 0 : variables[ref.ref];
            if (!(value == null ? void 0 : value.kind)) {
              continue;
            }
            const reified = reify(value.kind, ref, variables);
            if (!reified) {
              continue;
            }
            yield [key, reified];
          }
        },
        itemsOfKind: function* (key) {
          for (const [subkey, ref] of iterKeys()) {
            const value = variables == null ? void 0 : variables[ref.ref];
            if ((value == null ? void 0 : value.kind) !== key) {
              continue;
            }
            const reified = reify(key, ref, variables);
            if (!reified) {
              continue;
            }
            yield [subkey, reified];
          }
        }
      };
      return [rootKey, resolver];
    })
  );
  return __spreadValues(__spreadValues({}, staticItems), deferredItems);
}
const DataProviderContext = createContext({
  reify: () => void 0
});
const DataProvider = ({
  timeline,
  children
}) => {
  const value = useMemo(
    () => ({
      reify: (kind, ref) => reify(kind, ref, timeline == null ? void 0 : timeline.variables)
    }),
    [timeline == null ? void 0 : timeline.variables]
  );
  return /* @__PURE__ */ jsxDEV(DataProviderContext.Provider, { value, children }, void 0, false, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/DataProvider/index.tsx",
    lineNumber: 20,
    columnNumber: 5
  }, globalThis);
};
function useDataProvider() {
  return useContext(DataProviderContext);
}
function isTrusted(data) {
  return typeof data === "object" && data !== null && "data" in data && typeof data["data"] === "object" && data["data"] !== null && "kind" in data["data"] && typeof data["data"]["kind"] === "string";
}
function defineShape({
  kind,
  render: render2,
  options
}) {
  return __spreadValues({
    kind,
    draw: (config, renderer) => {
      if (!isTrusted(config)) {
        throw new Error(
          `Unexpected model for shape ${kind}: ${JSON.stringify(config)}`
        );
      }
      const item = config.data;
      const utils = config._utils;
      const shape = render2({ item, renderer, config, utils });
      config.size = [shape.attr("width"), shape.attr("height")];
      return shape;
    }
  }, options);
}
function registerShapes({
  nodes,
  edges
}) {
  const shapeIdentifier = (type, data) => `${type}:${data.kind}`;
  nodes.forEach((node) => registerNode(shapeIdentifier("node", node), node));
  edges.forEach((edge) => registerEdge(shapeIdentifier("edge", edge), edge));
  return function fromGraph2(graph, _utils) {
    var _a, _b, _c, _d;
    return {
      nodes: (_b = (_a = graph.nodes) == null ? void 0 : _a.map(
        (node) => ({
          id: node.id,
          type: shapeIdentifier("node", node),
          data: node,
          _utils
        })
      )) != null ? _b : [],
      edges: (_d = (_c = graph.edges) == null ? void 0 : _c.map(
        (edge) => ({
          id: `${edge.source}-${edge.target}`,
          source: edge.source,
          target: edge.target,
          type: shapeIdentifier("edge", edge),
          data: edge,
          _utils
        })
      )) != null ? _d : []
    };
  };
}
function toPureGraph(graph) {
  const { nodes = [], edges = [] } = graph.save();
  return new Graph({
    nodes: nodes.filter(isTrusted),
    edges: edges.filter(isTrusted)
  });
}
function recursive(graph, origin, filterer, stopWhen) {
  const queue = [...filterer.bind(graph)(origin)];
  const all = [...queue];
  const seen = new Set(queue.map((n) => n.id));
  while (queue.length > 0) {
    const node = queue.shift();
    if (!node) {
      break;
    }
    if (stopWhen && stopWhen(graph.getNode(node.id))) {
      continue;
    }
    const successors = filterer.bind(graph)(node.id).filter((n) => !seen.has(n.id));
    successors.forEach((n) => {
      seen.add(n.id);
      queue.push(n);
      all.push(n);
    });
  }
  return all;
}
function completePartition(graph, matched) {
  [...matched].forEach(
    (v) => graph.getRelatedEdges(v, "both").forEach((e) => {
      if (matched.has(e.source) && matched.has(e.target)) {
        matched.add(e.id);
      }
    })
  );
  const unmatched = /* @__PURE__ */ new Set([
    ...graph.getAllNodes().filter((n) => !matched.has(n.id)).map((n) => n.id),
    ...graph.getAllEdges().filter((e) => !matched.has(e.id)).map((e) => e.id)
  ]);
  return { matched, unmatched };
}
const partitionByEntityType = (graph, id) => {
  const matched = new Set(
    (() => {
      switch (graph.getNode(id).data.kind) {
        case "function":
          return graph.getNeighbors(id);
        case "reveal":
          return graph.getNeighbors(id);
        case "remote":
        case "local":
          return [
            ...recursive(graph, id, graph.getPredecessors),
            ...recursive(graph, id, graph.getSuccessors)
          ];
        default:
          return [];
      }
    })().map((v) => v.id)
  );
  matched.add(id);
  return matched;
};
const partitionByLocation = (graph, id) => {
  const byLocation = (location) => (node) => {
    switch (node.data.kind) {
      case "function":
        return isEqual(node.data.location, location);
      case "remote":
        return isEqual(node.data.data.location, location);
      case "local":
        return graph.getSuccessors(node.id).some((v) => byLocation(location)(v));
      default:
        return false;
    }
  };
  const matched = new Set(
    (() => {
      const node = graph.getNode(id);
      switch (node.data.kind) {
        case "function":
          return graph.getAllNodes().filter(byLocation(node.data.location));
        case "remote":
          return graph.getAllNodes().filter(byLocation(node.data.data.location));
        case "local":
          return graph.getAllNodes().filter((v) => v.data.kind === "local");
        default:
          return [];
      }
    })().map((v) => v.id)
  );
  matched.add(id);
  return matched;
};
class LocationColorizer {
  constructor(palette) {
    __publicField(this, "palette");
    __publicField(this, "cache", /* @__PURE__ */ new Map());
    __publicField(this, "names", /* @__PURE__ */ new Map());
    this.palette = palette;
  }
  colorize(location) {
    const key = LocationColorizer.locationKey(location);
    let color = this.cache.get(key);
    if (!color) {
      color = this.makeColor();
      this.cache.set(key, color);
    }
    this.names.set(key, this.locationName(location));
    return { background: color, foreground: this.foreground(color) };
  }
  colors() {
    return new Map(
      [...this.names.entries()].map(([k, name]) => [
        k,
        { name, color: this.cache.get(k) }
      ])
    );
  }
  locationName(location) {
    return `${location.type}[${location.parties.join(", ")}]`;
  }
  static locationKey(location) {
    var _a;
    return [
      location.type,
      ...location.parties,
      ...Object.entries((_a = location.parameters) != null ? _a : {}).map(([k, v]) => `${k}=${v}`)
    ].join(":");
  }
  makeColor() {
    const currentColorCount = this.cache.size;
    const position = currentColorCount % this.palette.length;
    const generation = Math.floor(currentColorCount / this.palette.length);
    if (generation === 0) {
      return this.palette[position];
    }
    const hueShifts = [
      // triadic
      120,
      240,
      // tetradic
      90,
      180,
      270
    ];
    const hueShift = hueShifts[generation - 1];
    if (hueShift === void 0) {
      throw new Error("Too many colors");
    }
    return new Color(this.palette[position]).rotate(hueShift).hex();
  }
  foreground(color, darken = 0.2, light = "#ffffff", dark = "#1d1d1d") {
    return new Color(color).darken(darken).isDark() ? light : dark;
  }
}
function colorizeByLocation(colorize) {
  return (node) => {
    switch (node.data.kind) {
      case "function":
        return colorize(node.data.location);
      case "local":
        return { background: "#1d1d1d", foreground: "#ffffff" };
      case "remote":
        return colorize(node.data.data.location);
      case "reveal":
        return { background: "#f04654", foreground: "#ffffff" };
      case "argument":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "return":
        return { background: "#a5aab5", foreground: "#ffffff" };
      case "transform":
        return colorize(node.data.destination);
      default:
        throw new Error(`Unknown shape kind: ${node.data.kind}`);
    }
  };
}
function recolorOnHover({
  partition,
  colorize
}) {
  return (graph) => {
    const highlight = (id) => {
      const g = toPureGraph(graph);
      const { matched, unmatched } = completePartition(g, partition(g, id));
      matched.forEach((k) => {
        const shape = graph.findById(String(k));
        const model = shape.getModel();
        if (isTrusted(model)) {
          const { background, foreground } = colorize(model);
          graph.updateItem(shape, {
            colors: { background, foreground }
          });
        }
      });
      unmatched.forEach((k) => {
        const shape = graph.findById(String(k));
        const model = shape.getModel();
        if (isTrusted(model)) {
          graph.updateItem(shape, {
            colors: { background: "#d3d3d3", foreground: "#ffffff" }
          });
        }
      });
    };
    const reset = () => {
      [...graph.getNodes(), ...graph.getEdges()].forEach((shape) => {
        const model = shape.getModel();
        if (isTrusted(model)) {
          const { background, foreground } = colorize(model);
          graph.updateItem(shape, {
            colors: { background, foreground }
          });
        }
      });
    };
    const onEnter = ({ item }) => {
      if (!item) {
        return;
      }
      highlight(item.getID());
    };
    return {
      enable: () => {
        graph.on("node:mouseenter", onEnter);
        graph.on("node:mouseleave", reset);
      },
      disable: () => {
        graph.off("node:mouseenter", onEnter);
        graph.off("node:mouseleave", reset);
      },
      highlight: (target) => {
        if (target) {
          highlight(target);
        } else {
          reset();
        }
      }
    };
  };
}
function useColorizer(factory) {
  const [colorizer, setColorizer] = useState(factory);
  const [, setColorCount] = useState(0);
  const colorize = useCallback(
    (...args) => {
      const color = colorizer.colorize(...args);
      setColorCount(colorizer.colors().size);
      return color;
    },
    [colorizer]
  );
  return useMemo(
    () => ({
      colorize,
      colors: colorizer.colors.bind(colorizer),
      reset: () => {
        setColorCount(0);
        setColorizer(factory);
      }
    }),
    [colorize, colorizer, factory]
  );
}
function truncate(text, maxLength = 20, placeholder = "...", keep = "start") {
  const trimmed = text.trim();
  if (trimmed.length > maxLength) {
    if (keep === "start") {
      return `${trimmed.slice(0, maxLength)}${placeholder}`;
    } else {
      return `${placeholder}${trimmed.slice(trimmed.length - maxLength)}`;
    }
  }
  return text;
}
function truncateLines(text, {
  maxWidth = 20,
  maxLines = Infinity,
  placeholder = "..."
} = {}) {
  const lines = text.split("\n");
  if (lines.length > maxLines) {
    lines.splice(maxLines, lines.length - maxLines);
    lines[maxLines - 1] = lines[maxLines - 1] + placeholder;
  }
  return lines.map((line) => truncate(line, maxWidth, placeholder)).join("\n");
}
function wrap(text, breakOn, maxWidth = 20) {
  const parts = text.split(breakOn);
  if (!parts.length) {
    return "";
  }
  const lines = [];
  let currentLine = parts.shift();
  if (currentLine === void 0) {
    return "";
  }
  parts.forEach((part) => {
    if ((part + breakOn).length > maxWidth) {
      if (currentLine) {
        lines.push(currentLine);
      }
      lines.push(`${breakOn}${part}`);
    } else if ((currentLine + breakOn + part).length > maxWidth) {
      lines.push(currentLine);
      currentLine = `${breakOn}${part}`;
    } else {
      currentLine += `${breakOn}${part}`;
    }
  });
  if (currentLine) {
    lines.push(currentLine);
  }
  return lines.join("\n");
}
const LOCAL_DATA_NODE = defineShape({
  kind: "local",
  render: ({
    item,
    renderer,
    config: {
      colors: { foreground, background } = {
        foreground: "#ffffff",
        background: "#1d1d1d"
      }
    },
    utils: { reify: reify2 }
  }) => {
    const value = reify2(void 0, item.data);
    let content = "";
    switch (value == null ? void 0 : value.kind) {
      case "dict":
      case "list":
      case "object":
        content = `${value.snapshot}`;
        break;
      case "function":
        content = `${value.name}()`;
        break;
    }
    content = content.trim();
    let label;
    if (item.data.name && content) {
      label = `${item.data.name} = ${content}`;
      if (label.length > 12) {
        label = `${item.data.name}
= ${content}`;
      }
    } else {
      label = content;
    }
    label = truncateLines(label, { maxLines: 3, maxWidth: 15 });
    const rect = renderer.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: background
      }
    });
    const text = renderer.addShape("text", {
      name: "label",
      attrs: {
        text: label,
        x: 0,
        y: 0,
        fontFamily: "Roboto Mono, monospace",
        fontSize: 12,
        lineHeight: 16.8,
        textAlign: "center",
        textBaseline: "middle",
        fill: foreground
      }
    });
    const { width, height, x, y } = text.getBBox();
    rect.attr("width", width + 10);
    rect.attr("height", height + 10);
    rect.attr("x", x - 5);
    rect.attr("y", y - 5);
    return rect;
  }
});
const REMOTE_DATA_NODE = defineShape({
  kind: "remote",
  render: ({ item, renderer, config: { colors }, utils: { colorize } }) => {
    const { background, foreground } = colors || colorize(item.data.location);
    const label = `${item.data.location.type[0]}${item.data.numbering}`;
    const rect = renderer.addShape("circle", {
      name: "background",
      attrs: {
        x: 0,
        y: 0,
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: background
      }
    });
    renderer.addShape("text", {
      name: "label",
      attrs: {
        text: label,
        x: 0,
        y: 0,
        fontFamily: "Inter, sans-serif",
        fontWeight: 700,
        fontSize: 12,
        lineHeight: 16,
        textAlign: "center",
        textBaseline: "middle",
        fill: foreground
      }
    });
    const diameter = 40 + Math.floor(Math.log10(item.data.numbering || 0) / 2) * 5;
    rect.attr("width", diameter);
    rect.attr("height", diameter);
    rect.attr("x", 0);
    rect.attr("y", 0);
    rect.attr("r", diameter / 2);
    return rect;
  }
});
const FUNCTION_NODE = defineShape({
  kind: "function",
  render: ({ item, renderer, config: { colors }, utils: { reify: reify2, colorize } }) => {
    const { background, foreground } = colors || colorize(item.location);
    const label = (() => {
      const parties = item.location.parties.map((d) => d[0].toUpperCase()).join(",");
      if (item.function) {
        const value = reify2("function", item.function);
        if (value) {
          return truncateLines(wrap(`let ${parties} in ${value.name}`, ".", 24), {
            maxWidth: 24,
            maxLines: 2
          });
        }
      }
      return `let ${parties} in (anonymous)`;
    })();
    const rect = renderer.addShape("rect", {
      name: "background",
      attrs: {
        radius: 8,
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: background,
        lineWidth: 2
      }
    });
    const text = renderer.addShape("text", {
      name: "label",
      attrs: {
        text: label,
        x: 0,
        y: 0,
        fontFamily: "Roboto Mono, monospace",
        fontSize: 12,
        fontWeight: 600,
        lineHeight: 14.4,
        letterSpacing: 0.5,
        textAlign: "center",
        textBaseline: "middle",
        fill: foreground
      }
    });
    const { width, height, x, y } = text.getBBox();
    rect.attr("width", width + 30);
    rect.attr("height", height + 15);
    rect.attr("x", x - 15);
    rect.attr("y", y - 7.5);
    return rect;
  }
});
const REVEAL_NODE = defineShape({
  kind: "reveal",
  render: ({
    renderer,
    config: {
      colors: { background, foreground } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const rect = renderer.addShape("rect", {
      name: "background",
      attrs: {
        anchorPoints: [
          [0.5, 0],
          [0.5, 1]
        ],
        stroke: null,
        fill: background
      }
    });
    const text = renderer.addShape("text", {
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
        fill: foreground
      }
    });
    const { width, height, x, y } = text.getBBox();
    rect.attr("width", width + 10);
    rect.attr("height", height + 10);
    rect.attr("x", x - 5);
    rect.attr("y", y - 5);
    return rect;
  }
});
function distance(x1, y1, x2, y2) {
  return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}
function textRotation(x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  let theta = Math.atan2(dy, dx);
  if (dx < 0) {
    theta -= Math.PI;
  }
  if (theta > 70 / 180 * Math.PI) {
    return theta - 1 / 2 * Math.PI;
  }
  if (theta < -70 / 180 * Math.PI) {
    return theta + 1 / 2 * Math.PI;
  }
  return theta;
}
const ARGUMENT_EDGE = defineShape({
  kind: "argument",
  render: ({
    item,
    renderer,
    config: {
      startPoint = { x: 0, y: 0 },
      endPoint = { x: 0, y: 0 },
      colors: { background, foreground } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const shape = renderer.addShape("path", {
      name: "line",
      attrs: {
        stroke: background,
        lineWidth: 1,
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x, endPoint.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (item.name) {
      const label = truncate(item.name, 20);
      const midPoint = shape.getPoint(0.5);
      const rect = renderer.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: background
        }
      });
      const text = renderer.addShape("text", {
        name: "label",
        attrs: {
          text: label,
          x: midPoint.x,
          y: midPoint.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: foreground
        }
      });
      const { width, height, x, y } = text.getBBox();
      rect.attr("width", width + 5);
      rect.attr("height", height + 5);
      const rotation = textRotation(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
      if (width > 30 && width < distance(startPoint.x, startPoint.y, endPoint.x, endPoint.y) - 20) {
        rect.rotateAtPoint(midPoint.x, midPoint.y, rotation);
        text.rotateAtPoint(midPoint.x, midPoint.y, rotation);
      }
      rect.attr("x", x - 2.5);
      rect.attr("y", y - 2.5);
    }
    return shape;
  }
});
const REVEAL_EDGE = defineShape({
  kind: "reveal",
  render: ({
    item,
    renderer,
    config: {
      startPoint = { x: 0, y: 0 },
      endPoint = { x: 0, y: 0 },
      colors: { background, foreground } = {
        background: "#f04654",
        foreground: "#ffffff"
      }
    }
  }) => {
    const shape = renderer.addShape("path", {
      name: "line",
      attrs: {
        stroke: background,
        lineWidth: 1,
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x, endPoint.y]
        ],
        lineDash: [2]
      }
    });
    if (item.name) {
      const label = truncate(item.name, 20);
      const midPoint = shape.getPoint(0.5);
      const rect = renderer.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: background
        }
      });
      const text = renderer.addShape("text", {
        name: "label",
        attrs: {
          text: label,
          x: midPoint.x,
          y: midPoint.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: foreground
        }
      });
      const { width, height, x, y } = text.getBBox();
      rect.attr("width", width + 5);
      rect.attr("height", height + 5);
      const rotation = textRotation(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
      if (width > 30 && width < distance(startPoint.x, startPoint.y, endPoint.x, endPoint.y) - 20) {
        rect.rotateAtPoint(midPoint.x, midPoint.y, rotation);
        text.rotateAtPoint(midPoint.x, midPoint.y, rotation);
      }
      rect.attr("x", x - 2.5);
      rect.attr("y", y - 2.5);
    }
    return shape;
  }
});
const RETURN_EDGE = defineShape({
  kind: "return",
  render: ({
    item,
    renderer,
    config: {
      startPoint = { x: 0, y: 0 },
      endPoint = { x: 0, y: 0 },
      colors: { background, foreground } = {
        background: "#a5aab5",
        foreground: "#ffffff"
      }
    }
  }) => {
    const shape = renderer.addShape("path", {
      name: "line",
      attrs: {
        stroke: background,
        lineWidth: 1,
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x, endPoint.y]
        ],
        endArrow: {
          path: "M 5 -5 L 0 0 L 5 5",
          lineWidth: 1
        }
      }
    });
    if (item.assignment) {
      const label = truncate(item.assignment, 20);
      const midPoint = shape.getPoint(0.5);
      const rect = renderer.addShape("rect", {
        name: "label-background",
        attrs: {
          radius: 0,
          anchorPoints: [
            [0.5, 0],
            [0.5, 1]
          ],
          stroke: null,
          fill: background
        }
      });
      const text = renderer.addShape("text", {
        name: "label",
        attrs: {
          text: label,
          x: midPoint.x,
          y: midPoint.y,
          fontFamily: "Roboto Mono, monospace",
          fontStyle: "italic",
          fontSize: 11,
          textAlign: "center",
          textBaseline: "middle",
          fill: foreground
        }
      });
      const { width, height, x, y } = text.getBBox();
      rect.attr("width", width + 5);
      rect.attr("height", height + 5);
      const rotation = textRotation(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
      if (width > 30 && width < distance(startPoint.x, startPoint.y, endPoint.x, endPoint.y) - 20) {
        rect.rotateAtPoint(midPoint.x, midPoint.y, rotation);
        text.rotateAtPoint(midPoint.x, midPoint.y, rotation);
      }
      rect.attr("x", x - 2.5);
      rect.attr("y", y - 2.5);
    }
    return shape;
  }
});
const TRANSFORM_EDGE = defineShape({
  kind: "transform",
  render: ({
    item,
    renderer,
    config: { startPoint = { x: 0, y: 0 }, endPoint = { x: 0, y: 0 }, colors },
    utils: { colorize }
  }) => {
    const { background } = colors || colorize(item.destination);
    const shape = renderer.addShape("path", {
      name: "line-background",
      attrs: {
        stroke: background,
        lineWidth: 3,
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x, endPoint.y]
        ]
      }
    });
    renderer.addShape("path", {
      name: "line-foreground",
      attrs: {
        stroke: "#ffffff",
        lineWidth: 1.5,
        path: [
          ["M", startPoint.x, startPoint.y],
          ["L", endPoint.x, endPoint.y]
        ]
      }
    });
    return shape;
  }
});
function setupG6() {
  return {
    fromGraph: registerShapes({
      nodes: [LOCAL_DATA_NODE, REMOTE_DATA_NODE, FUNCTION_NODE, REVEAL_NODE],
      edges: [ARGUMENT_EDGE, RETURN_EDGE, TRANSFORM_EDGE, REVEAL_EDGE]
    })
  };
}
function tooltipHeader(root, text) {
  root.append("strong").text(text).style("font-size", "0.9rem");
  root.append("hr").style("margin", "3px 0").style("border", 0).style("border-top", "1px solid #d3d3d3");
}
function attributes(root, items) {
  const container = root.append("div").style("display", "grid").style("gap", ".3rem").style("min-width", "0").style("grid-template-columns", "2fr 8fr").style("grid-auto-flow", "row").style("align-items", "baseline");
  items.forEach(([name, value]) => {
    container.append("span").text(name);
    container.append("code").style("font-weight", 700).style("word-break", "break-all").style("background", "none").text(value);
  });
}
function codeBlock(root, value) {
  root.append("div").style("background", "#f5f5f5").style("margin", "6px 0 0").style("max-height", "10vh").style("overflow", "auto").style("padding", "6px").append("pre").style("background", "none").style("overflow", "auto").style("white-space", "pre").style("word-break", "break-all").text(value);
}
function remoteObjectTooltip({ root }) {
  tooltipHeader(root, (d) => `Remote object #${d.data.numbering || "numbering ?"}`);
  attributes(root, [
    ["Device", (d) => d.data.location.type],
    [
      (d) => d.data.location.parties.length > 1 ? "Parties" : "Party",
      (d) => d.data.location.parties.join(", ")
    ]
  ]);
  const params = root.datum().data.location.parameters || {};
  if (Object.keys(params).length > 0) {
    codeBlock(root, () => YAML.stringify({ properties: params }, { indent: 2 }));
  }
}
function localObjectTooltip({ root, reify: reify2 }) {
  tooltipHeader(root, "Local value");
  const value = reify2(void 0, root.datum().data);
  const node = root.datum();
  switch (value == null ? void 0 : value.kind) {
    case "object":
    case "list":
    case "dict":
      attributes(root.datum(value), [
        ["Name", node.data.name || "?"],
        ["Type", (d) => wrap(d.type, ".", 30)]
      ]);
      codeBlock(root.datum(value), (d) => d.snapshot);
      break;
    case "none":
      attributes(root.datum(value), [
        ["Name", node.data.name || "?"],
        ["Value", "None"]
      ]);
      break;
    case "function":
      attributes(root.datum(value), [
        ["Function", (d) => wrap(d.name, ".", 32)],
        ["Module", (d) => wrap(d.module || "?", ".", 32)],
        ["File", (d) => wrap(d.filename || "?", "/", 32)],
        ["Line", (d) => d.firstlineno || "?"]
      ]);
      codeBlock(root.datum(value), (d) => d.source || "(no source)");
      break;
  }
}
function functionTooltip({ root, reify: reify2 }) {
  tooltipHeader(root, "Code execution");
  attributes(root, [
    ["Device", (d) => `${d.location.type}[${d.location.parties.join(", ")}]`],
    ["Frame #", (d) => d.epoch]
  ]);
  const func = reify2("function", root.datum().function);
  if (!func) {
    return;
  }
  attributes(root.datum(func), [
    ["Function", (d) => wrap(d.name, ".", 32)],
    ["Module", (d) => wrap(d.module || "?", ".", 32)],
    [
      "File",
      (d) => `${wrap(d.filename || "?", "/", 32)}, line ${d.firstlineno || "?"}`
    ]
  ]);
  codeBlock(root.datum(func), (d) => d.source || "(no source, likely a C function)");
}
function tooltip(model, reify2) {
  if (!isTrusted(model)) {
    return "";
  }
  const div = document.createElement("div");
  const root = d3.select(div);
  const { data } = model;
  switch (data.kind) {
    case "remote":
      remoteObjectTooltip({ root: root.datum(data), reify: reify2 });
      break;
    case "local":
      localObjectTooltip({ root: root.datum(data), reify: reify2 });
      break;
    case "function":
      functionTooltip({ root: root.datum(data), reify: reify2 });
      break;
  }
  root.style("box-sizing", "border-box").style("padding", "10px").style("margin", "0").style("display", "flex").style("flex-direction", "column").style("align-items", "stretch").style("gap", ".3rem").style("font-size", "0.8rem").style("color", "#333").style("border-radius", "4px").style("background-color", "#fff").style("min-width", "200px").style("max-width", "25vw").style(
    "box-shadow",
    "0px 1px 2px -2px rgba(0,0,0,0.08), 0px 3px 6px 0px rgba(0,0,0,0.06), 0px 5px 12px 4px rgba(0,0,0,0.03)"
  );
  if (div.childNodes.length === 0) {
    return "";
  }
  return div.outerHTML;
}
const { fromGraph } = setupG6();
const defaultColorizer = () => new LocationColorizer([
  "#79a25c",
  "#de4c8b",
  "#8271df",
  "#3398a6",
  "#c47d3a",
  "#b45dcb",
  "#4c99d8",
  "#df6a72"
]);
function Legend({
  graph,
  colorizer
}) {
  const locationColorizer = useMemo(
    () => recolorOnHover({
      partition: partitionByLocation,
      colorize: colorizeByLocation(colorizer.colorize)
    }),
    [colorizer.colorize]
  );
  const resetColors = useCallback(() => {
    if (!graph.current) {
      return;
    }
    locationColorizer(graph.current).highlight(null);
  }, [graph, locationColorizer]);
  const highlight = useCallback(
    (locationKey) => () => {
      if (!graph.current) {
        return;
      }
      const target = graph.current.getNodes().find((v) => {
        const model = v.getModel();
        if (!isTrusted(model)) {
          return false;
        }
        switch (model.data.kind) {
          case "function":
            return LocationColorizer.locationKey(model.data.location) === locationKey;
          case "remote":
            return LocationColorizer.locationKey(model.data.data.location) === locationKey;
          default:
            return false;
        }
      });
      if (target) {
        locationColorizer(graph.current).highlight(target.getID());
      }
    },
    [graph, locationColorizer]
  );
  const [hovered, setHovered] = useState();
  return /* @__PURE__ */ jsxDEV(
    "div",
    {
      style: {
        display: "grid",
        gridTemplateColumns: "20px 1fr",
        gridAutoRows: "20px",
        alignItems: "center",
        gap: "0.3rem"
      },
      onMouseLeave: (e) => {
        setHovered(void 0);
        resetColors(e);
      },
      children: [...colorizer.colors()].map(([key, { name, color }]) => /* @__PURE__ */ jsxDEV(Fragment, { children: [
        /* @__PURE__ */ jsxDEV(
          "div",
          {
            style: { width: 16, height: 16, margin: 2, backgroundColor: color },
            onMouseEnter: (e) => {
              highlight(key)(e);
              setHovered(key);
            }
          },
          void 0,
          false,
          {
            fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
            lineNumber: 103,
            columnNumber: 11
          },
          this
        ),
        /* @__PURE__ */ jsxDEV(
          "div",
          {
            onMouseEnter: (e) => {
              highlight(key)(e);
              setHovered(key);
            },
            children: /* @__PURE__ */ jsxDEV(
              "span",
              {
                style: {
                  fontFamily: "Inter, sans-serif",
                  fontWeight: hovered === key ? 700 : 400,
                  pointerEvents: "none"
                },
                children: name
              },
              void 0,
              false,
              {
                fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
                lineNumber: 116,
                columnNumber: 13
              },
              this
            )
          },
          void 0,
          false,
          {
            fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
            lineNumber: 110,
            columnNumber: 11
          },
          this
        )
      ] }, key, true, {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 102,
        columnNumber: 9
      }, this))
    },
    void 0,
    false,
    {
      fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
      lineNumber: 88,
      columnNumber: 5
    },
    this
  );
}
function useExecutionGraph() {
  const { reify: reify2 } = useDataProvider();
  const colorizer = useColorizer(defaultColorizer);
  const entityColorizer = useMemo(
    () => recolorOnHover({
      partition: partitionByEntityType,
      colorize: colorizeByLocation(colorizer.colorize)
    }),
    [colorizer.colorize]
  );
  const containerRef = useRef(null);
  const graphRef = useRef();
  const tooltipEnabledRef = useRef(true);
  useEffect(() => {
    if (!containerRef.current) {
      graphRef.current = void 0;
      return;
    }
    const graph = new G6.Graph({
      container: containerRef.current,
      width: containerRef.current.clientWidth,
      height: containerRef.current.clientHeight,
      layout: {
        type: "dagre",
        ranksepFunc: (node) => {
          var _a, _b, _c;
          if (((_a = node.data) == null ? void 0 : _a.kind) === "reveal" || ((_b = node.data) == null ? void 0 : _b.kind) === "remote") {
            return 2.5;
          }
          if (((_c = node.data) == null ? void 0 : _c.kind) === "local") {
            return 5;
          }
          return 10;
        },
        nodesep: 10
      },
      modes: {
        default: [
          { type: "scroll-canvas" },
          { type: "drag-canvas" },
          {
            type: "tooltip",
            formatText: (model) => {
              if (!tooltipEnabledRef.current) {
                return "";
              }
              return tooltip(model, reify2);
            },
            offset: 10
          }
        ],
        highlighting: []
      },
      minZoom: 0.2,
      maxZoom: 3
    });
    graph.on("node:click", ({ item }) => {
      if (item) {
        graph.focusItem(item);
      }
    });
    entityColorizer(graph).enable();
    graphRef.current = graph;
    return () => {
      graph.destroy();
    };
  }, [entityColorizer, reify2]);
  useEffect(() => {
    var _a;
    const outputView = (_a = containerRef.current) == null ? void 0 : _a.closest(".jp-LinkedOutputView");
    const resizeObserver = new ResizeObserver(() => {
      var _a2;
      if (!containerRef.current) {
        return;
      }
      const [height, cssHeight] = (() => {
        if (outputView && outputView.clientHeight !== 0) {
          return [outputView.clientHeight, `${outputView.clientHeight}px`];
        }
        return [
          containerRef.current.clientHeight,
          `${containerRef.current.clientHeight}px`
        ];
      })();
      containerRef.current.style.height = cssHeight;
      (_a2 = graphRef.current) == null ? void 0 : _a2.changeSize(containerRef.current.clientWidth, height);
    });
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }
    if (outputView) {
      resizeObserver.observe(outputView);
    }
    return () => {
      resizeObserver.disconnect();
    };
  }, []);
  return {
    container: containerRef,
    graph: graphRef,
    colorizer,
    tooltipEnabled: tooltipEnabledRef,
    load: (data) => {
      var _a, _b;
      (_a = graphRef.current) == null ? void 0 : _a.data(fromGraph(data, { reify: reify2, colorize: colorizer.colorize }));
      (_b = graphRef.current) == null ? void 0 : _b.render();
    }
  };
}
function ExecutionGraph(data) {
  const { container, load, graph, colorizer, tooltipEnabled } = useExecutionGraph();
  useEffect(() => {
    load(data);
  }, [data, load]);
  return /* @__PURE__ */ jsxDEV("div", { style: { position: "relative" }, children: [
    /* @__PURE__ */ jsxDEV(
      "div",
      {
        style: { width: "100%", height: "80vh", minHeight: "600px" },
        ref: container
      },
      void 0,
      false,
      {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 259,
        columnNumber: 7
      },
      this
    ),
    /* @__PURE__ */ jsxDEV("div", { style: { position: "absolute", top: "1rem", right: "1rem" }, children: /* @__PURE__ */ jsxDEV(Card, { size: "small", style: { fontSize: ".8rem" }, children: [
      /* @__PURE__ */ jsxDEV(ConfigProvider, { theme: { token: { marginLG: 8 } }, children: [
        /* @__PURE__ */ jsxDEV(
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
          },
          void 0,
          false,
          {
            fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
            lineNumber: 266,
            columnNumber: 13
          },
          this
        ),
        /* @__PURE__ */ jsxDEV(Divider, {}, void 0, false, {
          fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
          lineNumber: 278,
          columnNumber: 13
        }, this)
      ] }, void 0, true, {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 265,
        columnNumber: 11
      }, this),
      /* @__PURE__ */ jsxDEV(Legend, { graph, colorizer }, void 0, false, {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 280,
        columnNumber: 11
      }, this),
      /* @__PURE__ */ jsxDEV(ConfigProvider, { theme: { token: { marginLG: 8 } }, children: /* @__PURE__ */ jsxDEV(Divider, {}, void 0, false, {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 282,
        columnNumber: 13
      }, this) }, void 0, false, {
        fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
        lineNumber: 281,
        columnNumber: 11
      }, this),
      /* @__PURE__ */ jsxDEV(
        Form.Item,
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
          colon: false,
          children: /* @__PURE__ */ jsxDEV(
            Switch,
            {
              size: "small",
              defaultChecked: tooltipEnabled.current,
              onChange: (checked) => {
                tooltipEnabled.current = checked;
              }
            },
            void 0,
            false,
            {
              fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
              lineNumber: 296,
              columnNumber: 13
            },
            this
          )
        },
        void 0,
        false,
        {
          fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
          lineNumber: 284,
          columnNumber: 11
        },
        this
      )
    ] }, void 0, true, {
      fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
      lineNumber: 264,
      columnNumber: 9
    }, this) }, void 0, false, {
      fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
      lineNumber: 263,
      columnNumber: 7
    }, this)
  ] }, void 0, true, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/ExecutionGraph/index.tsx",
    lineNumber: 258,
    columnNumber: 5
  }, this);
}
function Visualization({ timeline }) {
  return /* @__PURE__ */ jsxDEV(Alert.ErrorBoundary, { message: /* @__PURE__ */ jsxDEV("strong", { children: "Exception in cell output:" }, void 0, false, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/Visualization.tsx",
    lineNumber: 10,
    columnNumber: 35
  }, this), children: /* @__PURE__ */ jsxDEV(DataProvider, { timeline, children: /* @__PURE__ */ jsxDEV(ExecutionGraph, __spreadValues({}, timeline.graph), void 0, false, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/Visualization.tsx",
    lineNumber: 12,
    columnNumber: 9
  }, this) }, void 0, false, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/Visualization.tsx",
    lineNumber: 11,
    columnNumber: 7
  }, this) }, void 0, false, {
    fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/components/Visualization.tsx",
    lineNumber: 10,
    columnNumber: 5
  }, this);
}
function render({
  elem,
  Component,
  props
}) {
  createRoot(elem).render(
    /* @__PURE__ */ jsxDEV(StrictMode, { children: /* @__PURE__ */ jsxDEV(Component, __spreadValues({}, props), void 0, false, {
      fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/render.tsx",
      lineNumber: 15,
      columnNumber: 7
    }, this) }, void 0, false, {
      fileName: "/Users/wenyu/vector/code/SecretNote/notebook/packages/secretnote-ui/src/render.tsx",
      lineNumber: 14,
      columnNumber: 5
    }, this)
  );
}
export {
  Visualization,
  render
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VzIjpbIi4uLy4uL3NyYy91dGlscy9yZWlmeS50cyIsIi4uLy4uL3NyYy9jb21wb25lbnRzL0RhdGFQcm92aWRlci9jb250ZXh0LnRzIiwiLi4vLi4vc3JjL2NvbXBvbmVudHMvRGF0YVByb3ZpZGVyL2luZGV4LnRzeCIsIi4uLy4uL3NyYy9jb21wb25lbnRzL0RhdGFQcm92aWRlci91dGlscy50cyIsIi4uLy4uL3NyYy9jb21wb25lbnRzL0V4ZWN1dGlvbkdyYXBoL3R5cGVzLnRzIiwiLi4vLi4vc3JjL2NvbXBvbmVudHMvRXhlY3V0aW9uR3JhcGgvdXRpbHMudHMiLCIuLi8uLi9zcmMvY29tcG9uZW50cy9FeGVjdXRpb25HcmFwaC9jb2xvcml6YXRpb24udHMiLCIuLi8uLi9zcmMvdXRpbHMvc3RyaW5nLnRzIiwiLi4vLi4vc3JjL2NvbXBvbmVudHMvRXhlY3V0aW9uR3JhcGgvc2hhcGVzLnRzIiwiLi4vLi4vc3JjL2NvbXBvbmVudHMvRXhlY3V0aW9uR3JhcGgvdG9vbHRpcC50cyIsIi4uLy4uL3NyYy9jb21wb25lbnRzL0V4ZWN1dGlvbkdyYXBoL2luZGV4LnRzeCIsIi4uLy4uL3NyYy9jb21wb25lbnRzL1Zpc3VhbGl6YXRpb24udHN4IiwiLi4vLi4vc3JjL3JlbmRlci50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHR5cGUgeyBSZWZlcmVuY2UsIFJlZmVyZW5jZU1hcCwgVGltZWxpbmUgfSBmcm9tICcuLi8ub3BlbmFwaS1zdHVicyc7XG5cbnR5cGUgVGFnZ2VkVW5pb248VGFnIGV4dGVuZHMgc3RyaW5nPiA9IHsga2luZD86IFRhZyB9O1xuXG5leHBvcnQgdHlwZSBVbmlvbk1lbWJlcjxUIGV4dGVuZHMgVGFnZ2VkVW5pb248c3RyaW5nPiwgSyBleHRlbmRzIFRbJ2tpbmQnXT4gPSBFeHRyYWN0PFxuICBULFxuICB7IGtpbmQ/OiBLIHwgdW5kZWZpbmVkIH1cbj47XG5cbmV4cG9ydCB0eXBlIFJlZmVyZW5jZVJlc29sdmVyPFQgZXh0ZW5kcyBUYWdnZWRVbmlvbjxzdHJpbmc+PiA9IHtcbiAgZ2V0OiAoa2V5OiBzdHJpbmcgfCBudW1iZXIpID0+IFJlaWZpZWQ8VCwgVD4gfCB1bmRlZmluZWQ7XG4gIG9mS2luZDogPEsgZXh0ZW5kcyBOb25OdWxsYWJsZTxUWydraW5kJ10+PihcbiAgICBraW5kOiBLLFxuICAgIGtleTogc3RyaW5nIHwgbnVtYmVyLFxuICApID0+IFJlaWZpZWQ8VW5pb25NZW1iZXI8VCwgSz4sIFQ+IHwgdW5kZWZpbmVkO1xuICBpdGVtczogKCkgPT4gSXRlcmFibGU8W3N0cmluZyB8IG51bWJlciwgUmVpZmllZDxULCBUPl0+O1xuICBpdGVtc09mS2luZDogPEsgZXh0ZW5kcyBOb25OdWxsYWJsZTxUWydraW5kJ10+PihcbiAgICBraW5kOiBLLFxuICApID0+IEl0ZXJhYmxlPFtzdHJpbmcgfCBudW1iZXIsIFJlaWZpZWQ8VW5pb25NZW1iZXI8VCwgSz4sIFQ+XT47XG59O1xuXG50eXBlIFJlZmVyZW5jZUtleXM8VD4gPSB7XG4gIFtLIGluIGtleW9mIFRdOiBUW0tdIGV4dGVuZHMgUmVmZXJlbmNlTWFwIHwgdW5kZWZpbmVkID8gTm9uTnVsbGFibGU8Sz4gOiBuZXZlcjtcbn1ba2V5b2YgVF07XG5cbi8vIGluZmVyIFRfIGRpc3RyaWJ1dGVzIFN0YXRpY1JlY29yZC9EZWZlcnJlZFJlY29yZCBvdmVyIHRoZSB1bmlvbiBtZW1iZXJzIG9mIFRcblxuZXhwb3J0IHR5cGUgU3RhdGljUmVjb3JkPFQ+ID0gVCBleHRlbmRzIGluZmVyIFRfID8gT21pdDxUXywgUmVmZXJlbmNlS2V5czxUXz4+IDogbmV2ZXI7XG5cbmV4cG9ydCB0eXBlIERlZmVycmVkUmVjb3JkPFQsIFUgZXh0ZW5kcyBUYWdnZWRVbmlvbjxzdHJpbmc+PiA9IFQgZXh0ZW5kcyBpbmZlciBUX1xuICA/IFJlY29yZDxSZWZlcmVuY2VLZXlzPFRfPiwgUmVmZXJlbmNlUmVzb2x2ZXI8VT4+XG4gIDogbmV2ZXI7XG5cbmV4cG9ydCB0eXBlIFJlaWZpZWQ8VCwgVSBleHRlbmRzIFRhZ2dlZFVuaW9uPHN0cmluZz4+ID0gU3RhdGljUmVjb3JkPFQ+ICZcbiAgRGVmZXJyZWRSZWNvcmQ8VCwgVT47XG5cbmV4cG9ydCB0eXBlIFNuYXBzaG90VHlwZSA9IE5vbk51bGxhYmxlPFRpbWVsaW5lWyd2YXJpYWJsZXMnXT5bc3RyaW5nXTtcblxuZXhwb3J0IHR5cGUgU25hcHNob3REaXNjcmltaW5hdG9yID0gTm9uTnVsbGFibGU8U25hcHNob3RUeXBlWydraW5kJ10+O1xuXG5leHBvcnQgdHlwZSBTbmFwc2hvdFJlaWZpZXIgPSA8SyBleHRlbmRzIFNuYXBzaG90RGlzY3JpbWluYXRvcj4oXG4gIGtpbmQ6IEsgfCB1bmRlZmluZWQsXG4gIHJlZjogUmVmZXJlbmNlIHwgdW5kZWZpbmVkLFxuKSA9PiBSZWlmaWVkPFVuaW9uTWVtYmVyPFNuYXBzaG90VHlwZSwgSz4sIFNuYXBzaG90VHlwZT4gfCB1bmRlZmluZWQ7XG5cbi8vIEZJWE1FOiBpbXByb3ZlIHRoZXNlIHR5cGVzXG5cbmZ1bmN0aW9uIGlzUmVmZXJlbmNlTGlzdCh2YWx1ZTogdW5rbm93bik6IHZhbHVlIGlzIFJlZmVyZW5jZVtdIHtcbiAgcmV0dXJuIEFycmF5LmlzQXJyYXkodmFsdWUpO1xufVxuXG5mdW5jdGlvbiBpc1JlZmVyZW5jZU1hcCh2YWx1ZTogdW5rbm93bik6IHZhbHVlIGlzIFJlY29yZDxzdHJpbmcsIFJlZmVyZW5jZT4ge1xuICByZXR1cm4gdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAhPT0gbnVsbCAmJiAhT2JqZWN0Lmhhc093bih2YWx1ZSwgJ2tpbmQnKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlaWZ5PEsgZXh0ZW5kcyBTbmFwc2hvdERpc2NyaW1pbmF0b3I+KFxuICByb290S2luZDogSyB8IHVuZGVmaW5lZCxcbiAgcm9vdFJlZjogUmVmZXJlbmNlIHwgdW5kZWZpbmVkLFxuICB2YXJpYWJsZXM6IFJlY29yZDxzdHJpbmcsIFNuYXBzaG90VHlwZT4gfCB1bmRlZmluZWQsXG4pOiBSZWlmaWVkPFVuaW9uTWVtYmVyPFNuYXBzaG90VHlwZSwgSz4sIFNuYXBzaG90VHlwZT4gfCB1bmRlZmluZWQge1xuICBpZiAocm9vdFJlZj8ucmVmID09PSB1bmRlZmluZWQpIHtcbiAgICByZXR1cm4gdW5kZWZpbmVkO1xuICB9XG5cbiAgY29uc3Qgcm9vdCA9IHZhcmlhYmxlcz8uW3Jvb3RSZWYucmVmXTtcblxuICBpZiAocm9vdCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgfVxuXG4gIGlmIChyb290S2luZCAhPT0gdW5kZWZpbmVkICYmIHJvb3Qua2luZCAhPT0gcm9vdEtpbmQpIHtcbiAgICByZXR1cm4gdW5kZWZpbmVkO1xuICB9XG5cbiAgY29uc3Qgc3RhdGljSXRlbXMgPSBPYmplY3QuZnJvbUVudHJpZXMoXG4gICAgT2JqZWN0LmVudHJpZXMocm9vdCkuZmlsdGVyKFxuICAgICAgKFssIHZhbHVlXSkgPT4gIWlzUmVmZXJlbmNlTGlzdCh2YWx1ZSkgJiYgIWlzUmVmZXJlbmNlTWFwKHZhbHVlKSxcbiAgICApLFxuICApIGFzIFN0YXRpY1JlY29yZDxVbmlvbk1lbWJlcjxTbmFwc2hvdFR5cGUsIEs+PjtcblxuICBjb25zdCBkZWZlcnJlZEl0ZW1zID0gT2JqZWN0LmZyb21FbnRyaWVzKFxuICAgIE9iamVjdC5lbnRyaWVzKHJvb3QpXG4gICAgICAuZmlsdGVyKChbLCB2YWx1ZV0pID0+IGlzUmVmZXJlbmNlTWFwKHZhbHVlKSB8fCBpc1JlZmVyZW5jZUxpc3QodmFsdWUpKVxuICAgICAgLm1hcCgoW3Jvb3RLZXksIF9dKSA9PiB7XG4gICAgICAgIGNvbnN0IGxvb2t1cDogUmVmZXJlbmNlTWFwID0gXztcblxuICAgICAgICBsZXQgZ2V0UmVmZXJlbmNlOiAoazogdW5rbm93bikgPT4gUmVmZXJlbmNlIHwgdW5kZWZpbmVkO1xuXG4gICAgICAgIGxldCBpdGVyS2V5czogKCkgPT4gR2VuZXJhdG9yPFxuICAgICAgICAgIHJlYWRvbmx5IFtzdHJpbmcgfCBudW1iZXIsIFJlZmVyZW5jZV0sXG4gICAgICAgICAgdm9pZCxcbiAgICAgICAgICB1bmtub3duXG4gICAgICAgID47XG5cbiAgICAgICAgaWYgKGlzUmVmZXJlbmNlTGlzdChsb29rdXApKSB7XG4gICAgICAgICAgZ2V0UmVmZXJlbmNlID0gKGspID0+IGxvb2t1cFtOdW1iZXIoayldO1xuXG4gICAgICAgICAgaXRlcktleXMgPSBmdW5jdGlvbiogKCkge1xuICAgICAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBsb29rdXAubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgeWllbGQgW2ksIGxvb2t1cFtpXV0gYXMgY29uc3Q7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBnZXRSZWZlcmVuY2UgPSAoaykgPT4gbG9va3VwW1N0cmluZyhrKV07XG5cbiAgICAgICAgICBpdGVyS2V5cyA9IGZ1bmN0aW9uKiAoKSB7XG4gICAgICAgICAgICBmb3IgKGNvbnN0IFtrLCB2XSBvZiBPYmplY3QuZW50cmllcyhsb29rdXApKSB7XG4gICAgICAgICAgICAgIHlpZWxkIFtrLCB2XSBhcyBjb25zdDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9O1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgcmVzb2x2ZXI6IFJlZmVyZW5jZVJlc29sdmVyPFNuYXBzaG90VHlwZT4gPSB7XG4gICAgICAgICAgZ2V0OiAoaXRlbSkgPT4ge1xuICAgICAgICAgICAgY29uc3QgcmVmID0gZ2V0UmVmZXJlbmNlKGl0ZW0pO1xuICAgICAgICAgICAgaWYgKCFyZWYpIHtcbiAgICAgICAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGNvbnN0IHZhbHVlID0gdmFyaWFibGVzPy5bcmVmLnJlZl07XG4gICAgICAgICAgICBpZiAoIXZhbHVlPy5raW5kKSB7XG4gICAgICAgICAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gcmVpZnkodmFsdWUua2luZCwgcmVmLCB2YXJpYWJsZXMpO1xuICAgICAgICAgIH0sXG4gICAgICAgICAgb2ZLaW5kOiAoa2luZCwgaXRlbSkgPT4ge1xuICAgICAgICAgICAgY29uc3QgcmVmID0gZ2V0UmVmZXJlbmNlKGl0ZW0pO1xuICAgICAgICAgICAgaWYgKCFyZWYpIHtcbiAgICAgICAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGNvbnN0IHZhbHVlID0gdmFyaWFibGVzPy5bcmVmLnJlZl07XG4gICAgICAgICAgICBpZiAodmFsdWU/LmtpbmQgIT09IGtpbmQpIHtcbiAgICAgICAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiByZWlmeShraW5kLCByZWYsIHZhcmlhYmxlcyk7XG4gICAgICAgICAgfSxcbiAgICAgICAgICBpdGVtczogZnVuY3Rpb24qICgpIHtcbiAgICAgICAgICAgIGZvciAoY29uc3QgW2tleSwgcmVmXSBvZiBpdGVyS2V5cygpKSB7XG4gICAgICAgICAgICAgIGNvbnN0IHZhbHVlID0gdmFyaWFibGVzPy5bcmVmLnJlZl07XG4gICAgICAgICAgICAgIGlmICghdmFsdWU/LmtpbmQpIHtcbiAgICAgICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICBjb25zdCByZWlmaWVkID0gcmVpZnkodmFsdWUua2luZCwgcmVmLCB2YXJpYWJsZXMpO1xuICAgICAgICAgICAgICBpZiAoIXJlaWZpZWQpIHtcbiAgICAgICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB5aWVsZCBba2V5LCByZWlmaWVkXTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9LFxuICAgICAgICAgIGl0ZW1zT2ZLaW5kOiBmdW5jdGlvbiogKGtleSkge1xuICAgICAgICAgICAgZm9yIChjb25zdCBbc3Via2V5LCByZWZdIG9mIGl0ZXJLZXlzKCkpIHtcbiAgICAgICAgICAgICAgY29uc3QgdmFsdWUgPSB2YXJpYWJsZXM/LltyZWYucmVmXTtcbiAgICAgICAgICAgICAgaWYgKHZhbHVlPy5raW5kICE9PSBrZXkpIHtcbiAgICAgICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICBjb25zdCByZWlmaWVkID0gcmVpZnkoa2V5LCByZWYsIHZhcmlhYmxlcyk7XG4gICAgICAgICAgICAgIGlmICghcmVpZmllZCkge1xuICAgICAgICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIHlpZWxkIFtzdWJrZXksIHJlaWZpZWRdO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sXG4gICAgICAgIH07XG5cbiAgICAgICAgcmV0dXJuIFtyb290S2V5LCByZXNvbHZlcl07XG4gICAgICB9KSxcbiAgKSBhcyBEZWZlcnJlZFJlY29yZDxVbmlvbk1lbWJlcjxTbmFwc2hvdFR5cGUsIEs+LCBTbmFwc2hvdFR5cGU+O1xuXG4gIHJldHVybiB7IC4uLnN0YXRpY0l0ZW1zLCAuLi5kZWZlcnJlZEl0ZW1zIH07XG59XG4iLCJpbXBvcnQgeyBjcmVhdGVDb250ZXh0IH0gZnJvbSAncmVhY3QnO1xuXG5pbXBvcnQgdHlwZSB7IFNuYXBzaG90UmVpZmllciB9IGZyb20gJy4uLy4uL3V0aWxzL3JlaWZ5JztcblxuZXhwb3J0IGNvbnN0IERhdGFQcm92aWRlckNvbnRleHQgPSBjcmVhdGVDb250ZXh0PHsgcmVpZnk6IFNuYXBzaG90UmVpZmllciB9Pih7XG4gIHJlaWZ5OiAoKSA9PiB1bmRlZmluZWQsXG59KTtcbiIsImltcG9ydCB0eXBlIHsgQ29udGV4dFR5cGUgfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyB1c2VNZW1vIH0gZnJvbSAncmVhY3QnO1xuXG5pbXBvcnQgdHlwZSB7IFRpbWVsaW5lIH0gZnJvbSAnLi4vLi4vLm9wZW5hcGktc3R1YnMnO1xuaW1wb3J0IHsgcmVpZnkgfSBmcm9tICcuLi8uLi91dGlscy9yZWlmeSc7XG5cbmltcG9ydCB7IERhdGFQcm92aWRlckNvbnRleHQgfSBmcm9tICcuL2NvbnRleHQnO1xuXG5leHBvcnQgY29uc3QgRGF0YVByb3ZpZGVyID0gKHtcbiAgdGltZWxpbmUsXG4gIGNoaWxkcmVuLFxufTogUmVhY3QuUHJvcHNXaXRoQ2hpbGRyZW48eyB0aW1lbGluZT86IFRpbWVsaW5lIH0+KSA9PiB7XG4gIGNvbnN0IHZhbHVlOiBDb250ZXh0VHlwZTx0eXBlb2YgRGF0YVByb3ZpZGVyQ29udGV4dD4gPSB1c2VNZW1vKFxuICAgICgpID0+ICh7XG4gICAgICByZWlmeTogKGtpbmQsIHJlZikgPT4gcmVpZnkoa2luZCwgcmVmLCB0aW1lbGluZT8udmFyaWFibGVzKSxcbiAgICB9KSxcbiAgICBbdGltZWxpbmU/LnZhcmlhYmxlc10sXG4gICk7XG4gIHJldHVybiAoXG4gICAgPERhdGFQcm92aWRlckNvbnRleHQuUHJvdmlkZXIgdmFsdWU9e3ZhbHVlfT5cbiAgICAgIHtjaGlsZHJlbn1cbiAgICA8L0RhdGFQcm92aWRlckNvbnRleHQuUHJvdmlkZXI+XG4gICk7XG59O1xuIiwiaW1wb3J0IHsgdXNlQ29udGV4dCB9IGZyb20gJ3JlYWN0JztcblxuaW1wb3J0IHsgRGF0YVByb3ZpZGVyQ29udGV4dCB9IGZyb20gJy4vY29udGV4dCc7XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VEYXRhUHJvdmlkZXIoKSB7XG4gIHJldHVybiB1c2VDb250ZXh0KERhdGFQcm92aWRlckNvbnRleHQpO1xufVxuIiwiaW1wb3J0IHR5cGUgKiBhcyBHNiBmcm9tICdAYW50di9nNic7XG5cbmltcG9ydCB0eXBlIHsgTG9naWNhbExvY2F0aW9uLCBUaW1lbGluZSB9IGZyb20gJy4uLy4uLy5vcGVuYXBpLXN0dWJzJztcbmltcG9ydCB0eXBlIHsgU25hcHNob3RSZWlmaWVyIH0gZnJvbSAnLi4vLi4vdXRpbHMvcmVpZnknO1xuaW1wb3J0IHR5cGUgeyBFbGVtZW50T2YgfSBmcm9tICcuLi8uLi91dGlscy90eXBpbmcnO1xuXG5pbXBvcnQgdHlwZSB7IENvbG9yaXplRnVuY3Rpb24gfSBmcm9tICcuL2NvbG9yaXphdGlvbic7XG5cbmV4cG9ydCB0eXBlIEdyYXBoTm9kZVR5cGUgPSBFbGVtZW50T2Y8XG4gIE5vbk51bGxhYmxlPE5vbk51bGxhYmxlPFRpbWVsaW5lWydncmFwaCddPlsnbm9kZXMnXT5cbj47XG5cbmV4cG9ydCB0eXBlIEdyYXBoRWRnZVR5cGUgPSBFbGVtZW50T2Y8XG4gIE5vbk51bGxhYmxlPE5vbk51bGxhYmxlPFRpbWVsaW5lWydncmFwaCddPlsnZWRnZXMnXT5cbj47XG5cbmV4cG9ydCB0eXBlIEdyYXBoRWxlbWVudFR5cGUgPSBHcmFwaE5vZGVUeXBlIHwgR3JhcGhFZGdlVHlwZTtcblxuZXhwb3J0IHR5cGUgR3JhcGhVdGlscyA9IHtcbiAgcmVpZnk6IFNuYXBzaG90UmVpZmllcjtcbiAgY29sb3JpemU6IENvbG9yaXplRnVuY3Rpb248TG9naWNhbExvY2F0aW9uPjtcbn07XG5cbmV4cG9ydCB0eXBlIFRydXN0ZWRNb2RlbDxUIGV4dGVuZHMgR3JhcGhFbGVtZW50VHlwZSA9IEdyYXBoRWxlbWVudFR5cGU+ID1cbiAgRzYuTW9kZWxDb25maWcgJiB7XG4gICAgZGF0YTogVDtcbiAgICBjb2xvcnM/OiB7IGZvcmVncm91bmQ6IHN0cmluZzsgYmFja2dyb3VuZDogc3RyaW5nIH07XG4gICAgX3V0aWxzOiBHcmFwaFV0aWxzO1xuICB9O1xuXG5leHBvcnQgdHlwZSBUcnVzdGVkTm9kZTxUIGV4dGVuZHMgR3JhcGhOb2RlVHlwZSA9IEdyYXBoTm9kZVR5cGU+ID0gRzYuTm9kZUNvbmZpZyAmIHtcbiAgZGF0YTogVDtcbiAgX3V0aWxzOiBHcmFwaFV0aWxzO1xufTtcblxuZXhwb3J0IHR5cGUgVHJ1c3RlZEVkZ2U8VCBleHRlbmRzIEdyYXBoRWRnZVR5cGUgPSBHcmFwaEVkZ2VUeXBlPiA9IEc2LkVkZ2VDb25maWcgJiB7XG4gIGlkOiBzdHJpbmc7XG4gIHNvdXJjZTogc3RyaW5nO1xuICB0YXJnZXQ6IHN0cmluZztcbiAgZGF0YTogVDtcbiAgX3V0aWxzOiBHcmFwaFV0aWxzO1xufTtcblxuZXhwb3J0IGZ1bmN0aW9uIGlzVHJ1c3RlZDxUIGV4dGVuZHMgR3JhcGhOb2RlVHlwZSA9IEdyYXBoTm9kZVR5cGU+KFxuICBkYXRhOiBHNi5Ob2RlQ29uZmlnLFxuKTogZGF0YSBpcyBUcnVzdGVkTm9kZTxUPjtcblxuZXhwb3J0IGZ1bmN0aW9uIGlzVHJ1c3RlZDxUIGV4dGVuZHMgR3JhcGhFZGdlVHlwZSA9IEdyYXBoRWRnZVR5cGU+KFxuICBkYXRhOiBHNi5FZGdlQ29uZmlnLFxuKTogZGF0YSBpcyBUcnVzdGVkRWRnZTxUPjtcblxuZXhwb3J0IGZ1bmN0aW9uIGlzVHJ1c3RlZDxUIGV4dGVuZHMgR3JhcGhFbGVtZW50VHlwZSA9IEdyYXBoRWxlbWVudFR5cGU+KFxuICBkYXRhOiBHNi5Nb2RlbENvbmZpZyxcbik6IGRhdGEgaXMgVHJ1c3RlZE1vZGVsPFQ+O1xuXG5leHBvcnQgZnVuY3Rpb24gaXNUcnVzdGVkKGRhdGE6IHVua25vd24pIHtcbiAgcmV0dXJuIChcbiAgICB0eXBlb2YgZGF0YSA9PT0gJ29iamVjdCcgJiZcbiAgICBkYXRhICE9PSBudWxsICYmXG4gICAgJ2RhdGEnIGluIGRhdGEgJiZcbiAgICB0eXBlb2YgZGF0YVsnZGF0YSddID09PSAnb2JqZWN0JyAmJlxuICAgIGRhdGFbJ2RhdGEnXSAhPT0gbnVsbCAmJlxuICAgICdraW5kJyBpbiBkYXRhWydkYXRhJ10gJiZcbiAgICB0eXBlb2YgZGF0YVsnZGF0YSddWydraW5kJ10gPT09ICdzdHJpbmcnXG4gICk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBpc09mS2luZDxUIGV4dGVuZHMgR3JhcGhFbGVtZW50VHlwZSwgSyBleHRlbmRzIFRbJ2tpbmQnXT4oXG4gIGtpbmQ6IEssXG4gIGl0ZW06IEc2Lk1vZGVsQ29uZmlnLFxuKTogaXRlbSBpcyBUcnVzdGVkTW9kZWw8RXh0cmFjdDxULCB7IGtpbmQ/OiBLIH0+PiB7XG4gIGlmICghaXNUcnVzdGVkPFQ+KGl0ZW0pKSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIGNvbnN0IGRhdGEgPSBpdGVtLmRhdGE7XG4gIGlmIChraW5kICE9PSB1bmRlZmluZWQgJiYgZGF0YS5raW5kICE9PSBraW5kKSB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIHJldHVybiB0cnVlO1xufVxuIiwiaW1wb3J0IHR5cGUgKiBhcyBHNiBmcm9tICdAYW50di9nNic7XG5pbXBvcnQgeyByZWdpc3Rlck5vZGUsIHJlZ2lzdGVyRWRnZSB9IGZyb20gJ0BhbnR2L2c2JztcbmltcG9ydCB0eXBlICogYXMgZ3JhcGhsaWIgZnJvbSAnQGFudHYvZ3JhcGhsaWInO1xuaW1wb3J0IHsgR3JhcGggYXMgUHVyZUdyYXBoIH0gZnJvbSAnQGFudHYvZ3JhcGhsaWInO1xuaW1wb3J0IGlzRXF1YWwgZnJvbSAnbG9kYXNoL2lzRXF1YWwnO1xuXG5pbXBvcnQgdHlwZSB7IEdyYXBoLCBMb2dpY2FsTG9jYXRpb24gfSBmcm9tICcuLi8uLi8ub3BlbmFwaS1zdHVicyc7XG5cbmltcG9ydCB0eXBlIHtcbiAgR3JhcGhVdGlscyxcbiAgR3JhcGhFbGVtZW50VHlwZSxcbiAgVHJ1c3RlZE5vZGUsXG4gIFRydXN0ZWRFZGdlLFxuICBUcnVzdGVkTW9kZWwsXG4gIEdyYXBoTm9kZVR5cGUsXG4gIEdyYXBoRWRnZVR5cGUsXG59IGZyb20gJy4vdHlwZXMnO1xuaW1wb3J0IHsgaXNUcnVzdGVkIH0gZnJvbSAnLi90eXBlcyc7XG5cbnR5cGUgUmVuZGVyaW5nQ29udGV4dDxUIGV4dGVuZHMgR3JhcGhFbGVtZW50VHlwZSwgSz4gPSB7XG4gIGl0ZW06IEV4dHJhY3Q8VCwgeyBraW5kPzogSyB9PjtcbiAgY29uZmlnOiBUcnVzdGVkTW9kZWw8RXh0cmFjdDxULCB7IGtpbmQ/OiBLIH0+PjtcbiAgcmVuZGVyZXI6IEc2LklHcm91cDtcbiAgdXRpbHM6IEdyYXBoVXRpbHM7XG59O1xuXG50eXBlIFNoYXBlRGVmaW5pdGlvbjxUIGV4dGVuZHMgR3JhcGhFbGVtZW50VHlwZSwgSz4gPSB7XG4gIGtpbmQ6IE5vbk51bGxhYmxlPEs+O1xuICByZW5kZXI6IChjdHg6IFJlbmRlcmluZ0NvbnRleHQ8VCwgSz4pID0+IEc2LklTaGFwZTtcbiAgb3B0aW9ucz86IE9taXQ8RzYuU2hhcGVPcHRpb25zLCAnZHJhdyc+O1xufTtcblxudHlwZSBTaGFwZU9wdGlvbnMgPSBHNi5TaGFwZU9wdGlvbnMgJiB7IGtpbmQ6IHN0cmluZyB9O1xuXG5leHBvcnQgZnVuY3Rpb24gZGVmaW5lU2hhcGU8VCBleHRlbmRzIEdyYXBoRWxlbWVudFR5cGUsIEsgZXh0ZW5kcyBUWydraW5kJ10+KHtcbiAga2luZCxcbiAgcmVuZGVyLFxuICBvcHRpb25zLFxufTogU2hhcGVEZWZpbml0aW9uPFQsIEs+KTogU2hhcGVPcHRpb25zIHtcbiAgcmV0dXJuIHtcbiAgICBraW5kLFxuICAgIGRyYXc6IChjb25maWcsIHJlbmRlcmVyKSA9PiB7XG4gICAgICBpZiAoIWlzVHJ1c3RlZDxFeHRyYWN0PFQsIHsga2luZD86IEsgfT4+KGNvbmZpZykpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKFxuICAgICAgICAgIGBVbmV4cGVjdGVkIG1vZGVsIGZvciBzaGFwZSAke2tpbmR9OiAke0pTT04uc3RyaW5naWZ5KGNvbmZpZyl9YCxcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGl0ZW0gPSBjb25maWcuZGF0YTtcbiAgICAgIGNvbnN0IHV0aWxzID0gY29uZmlnLl91dGlscztcbiAgICAgIGNvbnN0IHNoYXBlID0gcmVuZGVyKHsgaXRlbSwgcmVuZGVyZXIsIGNvbmZpZywgdXRpbHMgfSk7XG4gICAgICBjb25maWcuc2l6ZSA9IFtzaGFwZS5hdHRyKCd3aWR0aCcpLCBzaGFwZS5hdHRyKCdoZWlnaHQnKV07XG4gICAgICByZXR1cm4gc2hhcGU7XG4gICAgfSxcbiAgICAuLi5vcHRpb25zLFxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVnaXN0ZXJTaGFwZXMoe1xuICBub2RlcyxcbiAgZWRnZXMsXG59OiB7XG4gIG5vZGVzOiBTaGFwZU9wdGlvbnNbXTtcbiAgZWRnZXM6IFNoYXBlT3B0aW9uc1tdO1xufSkge1xuICBjb25zdCBzaGFwZUlkZW50aWZpZXIgPSAodHlwZTogc3RyaW5nLCBkYXRhOiB7IGtpbmQ/OiBzdHJpbmcgfSkgPT5cbiAgICBgJHt0eXBlfToke2RhdGEua2luZH1gO1xuXG4gIG5vZGVzLmZvckVhY2goKG5vZGUpID0+IHJlZ2lzdGVyTm9kZShzaGFwZUlkZW50aWZpZXIoJ25vZGUnLCBub2RlKSwgbm9kZSkpO1xuICBlZGdlcy5mb3JFYWNoKChlZGdlKSA9PiByZWdpc3RlckVkZ2Uoc2hhcGVJZGVudGlmaWVyKCdlZGdlJywgZWRnZSksIGVkZ2UpKTtcblxuICByZXR1cm4gZnVuY3Rpb24gZnJvbUdyYXBoKGdyYXBoOiBHcmFwaCwgX3V0aWxzOiBHcmFwaFV0aWxzKTogRzYuR3JhcGhEYXRhIHtcbiAgICByZXR1cm4ge1xuICAgICAgbm9kZXM6XG4gICAgICAgIGdyYXBoLm5vZGVzPy5tYXAoXG4gICAgICAgICAgKG5vZGUpID0+XG4gICAgICAgICAgICAoe1xuICAgICAgICAgICAgICBpZDogbm9kZS5pZCxcbiAgICAgICAgICAgICAgdHlwZTogc2hhcGVJZGVudGlmaWVyKCdub2RlJywgbm9kZSksXG4gICAgICAgICAgICAgIGRhdGE6IG5vZGUsXG4gICAgICAgICAgICAgIF91dGlscyxcbiAgICAgICAgICAgIH0pIHNhdGlzZmllcyBUcnVzdGVkTm9kZSxcbiAgICAgICAgKSA/PyBbXSxcbiAgICAgIGVkZ2VzOlxuICAgICAgICBncmFwaC5lZGdlcz8ubWFwKFxuICAgICAgICAgIChlZGdlKSA9PlxuICAgICAgICAgICAgKHtcbiAgICAgICAgICAgICAgaWQ6IGAke2VkZ2Uuc291cmNlfS0ke2VkZ2UudGFyZ2V0fWAsXG4gICAgICAgICAgICAgIHNvdXJjZTogZWRnZS5zb3VyY2UsXG4gICAgICAgICAgICAgIHRhcmdldDogZWRnZS50YXJnZXQsXG4gICAgICAgICAgICAgIHR5cGU6IHNoYXBlSWRlbnRpZmllcignZWRnZScsIGVkZ2UpLFxuICAgICAgICAgICAgICBkYXRhOiBlZGdlLFxuICAgICAgICAgICAgICBfdXRpbHMsXG4gICAgICAgICAgICB9KSBzYXRpc2ZpZXMgVHJ1c3RlZEVkZ2UsXG4gICAgICAgICkgPz8gW10sXG4gICAgfTtcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHRvUHVyZUdyYXBoKGdyYXBoOiBHNi5HcmFwaCkge1xuICBjb25zdCB7IG5vZGVzID0gW10sIGVkZ2VzID0gW10gfSA9IGdyYXBoLnNhdmUoKSBhcyBHNi5HcmFwaERhdGE7XG4gIHJldHVybiBuZXcgUHVyZUdyYXBoKHtcbiAgICBub2Rlczogbm9kZXMuZmlsdGVyKGlzVHJ1c3RlZCkgYXMgVHJ1c3RlZE5vZGVbXSxcbiAgICBlZGdlczogZWRnZXMuZmlsdGVyKGlzVHJ1c3RlZCkgYXMgVHJ1c3RlZEVkZ2VbXSxcbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZWN1cnNpdmU8XG4gIFYgZXh0ZW5kcyBncmFwaGxpYi5QbGFpbk9iamVjdCxcbiAgRSBleHRlbmRzIGdyYXBobGliLlBsYWluT2JqZWN0LFxuPihcbiAgZ3JhcGg6IGdyYXBobGliLkdyYXBoPFYsIEU+LFxuICBvcmlnaW46IGdyYXBobGliLklELFxuICBmaWx0ZXJlcjogKGlkOiBncmFwaGxpYi5JRCkgPT4gZ3JhcGhsaWIuTm9kZTxWPltdLFxuICBzdG9wV2hlbj86ICh2OiBncmFwaGxpYi5Ob2RlPFY+KSA9PiBib29sZWFuLFxuKTogZ3JhcGhsaWIuTm9kZTxWPltdIHtcbiAgY29uc3QgcXVldWU6IGdyYXBobGliLk5vZGU8Vj5bXSA9IFsuLi5maWx0ZXJlci5iaW5kKGdyYXBoKShvcmlnaW4pXTtcbiAgY29uc3QgYWxsOiBncmFwaGxpYi5Ob2RlPFY+W10gPSBbLi4ucXVldWVdO1xuICBjb25zdCBzZWVuID0gbmV3IFNldDx1bmtub3duPihxdWV1ZS5tYXAoKG4pID0+IG4uaWQpKTtcbiAgd2hpbGUgKHF1ZXVlLmxlbmd0aCA+IDApIHtcbiAgICBjb25zdCBub2RlID0gcXVldWUuc2hpZnQoKTtcbiAgICBpZiAoIW5vZGUpIHtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBpZiAoc3RvcFdoZW4gJiYgc3RvcFdoZW4oZ3JhcGguZ2V0Tm9kZShub2RlLmlkKSkpIHtcbiAgICAgIGNvbnRpbnVlO1xuICAgIH1cbiAgICBjb25zdCBzdWNjZXNzb3JzID0gZmlsdGVyZXJcbiAgICAgIC5iaW5kKGdyYXBoKShub2RlLmlkKVxuICAgICAgLmZpbHRlcigobikgPT4gIXNlZW4uaGFzKG4uaWQpKTtcbiAgICBzdWNjZXNzb3JzLmZvckVhY2goKG4pID0+IHtcbiAgICAgIHNlZW4uYWRkKG4uaWQpO1xuICAgICAgcXVldWUucHVzaChuKTtcbiAgICAgIGFsbC5wdXNoKG4pO1xuICAgIH0pO1xuICB9XG4gIHJldHVybiBhbGw7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBjb21wbGV0ZVBhcnRpdGlvbihcbiAgZ3JhcGg6IGdyYXBobGliLkdyYXBoPEdyYXBoTm9kZVR5cGUsIEdyYXBoRWRnZVR5cGU+LFxuICBtYXRjaGVkOiBTZXQ8Z3JhcGhsaWIuSUQ+LFxuKSB7XG4gIFsuLi5tYXRjaGVkXS5mb3JFYWNoKCh2KSA9PlxuICAgIGdyYXBoLmdldFJlbGF0ZWRFZGdlcyh2LCAnYm90aCcpLmZvckVhY2goKGUpID0+IHtcbiAgICAgIGlmIChtYXRjaGVkLmhhcyhlLnNvdXJjZSkgJiYgbWF0Y2hlZC5oYXMoZS50YXJnZXQpKSB7XG4gICAgICAgIG1hdGNoZWQuYWRkKGUuaWQpO1xuICAgICAgfVxuICAgIH0pLFxuICApO1xuICBjb25zdCB1bm1hdGNoZWQgPSBuZXcgU2V0KFtcbiAgICAuLi5ncmFwaFxuICAgICAgLmdldEFsbE5vZGVzKClcbiAgICAgIC5maWx0ZXIoKG4pID0+ICFtYXRjaGVkLmhhcyhuLmlkKSlcbiAgICAgIC5tYXAoKG4pID0+IG4uaWQpLFxuICAgIC4uLmdyYXBoXG4gICAgICAuZ2V0QWxsRWRnZXMoKVxuICAgICAgLmZpbHRlcigoZSkgPT4gIW1hdGNoZWQuaGFzKGUuaWQpKVxuICAgICAgLm1hcCgoZSkgPT4gZS5pZCksXG4gIF0pO1xuICByZXR1cm4geyBtYXRjaGVkLCB1bm1hdGNoZWQgfTtcbn1cblxuZXhwb3J0IHR5cGUgUGFydGl0aW9uRnVuY3Rpb24gPSAoXG4gIGdyYXBoOiBncmFwaGxpYi5HcmFwaDxHcmFwaE5vZGVUeXBlLCBHcmFwaEVkZ2VUeXBlPixcbiAgaWQ6IGdyYXBobGliLklELFxuKSA9PiBTZXQ8Z3JhcGhsaWIuSUQ+O1xuXG5leHBvcnQgY29uc3QgcGFydGl0aW9uQnlFbnRpdHlUeXBlOiBQYXJ0aXRpb25GdW5jdGlvbiA9IChncmFwaCwgaWQpID0+IHtcbiAgY29uc3QgbWF0Y2hlZCA9IG5ldyBTZXQoXG4gICAgKCgpID0+IHtcbiAgICAgIHN3aXRjaCAoZ3JhcGguZ2V0Tm9kZShpZCkuZGF0YS5raW5kKSB7XG4gICAgICAgIGNhc2UgJ2Z1bmN0aW9uJzpcbiAgICAgICAgICByZXR1cm4gZ3JhcGguZ2V0TmVpZ2hib3JzKGlkKTtcbiAgICAgICAgY2FzZSAncmV2ZWFsJzpcbiAgICAgICAgICByZXR1cm4gZ3JhcGguZ2V0TmVpZ2hib3JzKGlkKTtcbiAgICAgICAgY2FzZSAncmVtb3RlJzpcbiAgICAgICAgY2FzZSAnbG9jYWwnOlxuICAgICAgICAgIHJldHVybiBbXG4gICAgICAgICAgICAuLi5yZWN1cnNpdmUoZ3JhcGgsIGlkLCBncmFwaC5nZXRQcmVkZWNlc3NvcnMpLFxuICAgICAgICAgICAgLi4ucmVjdXJzaXZlKGdyYXBoLCBpZCwgZ3JhcGguZ2V0U3VjY2Vzc29ycyksXG4gICAgICAgICAgXTtcbiAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICByZXR1cm4gW107XG4gICAgICB9XG4gICAgICAvLyBJIG1pc3MgUnVzdFxuICAgIH0pKCkubWFwKCh2KSA9PiB2LmlkKSxcbiAgKTtcbiAgbWF0Y2hlZC5hZGQoaWQpO1xuICByZXR1cm4gbWF0Y2hlZDtcbn07XG5cbmV4cG9ydCBjb25zdCBwYXJ0aXRpb25CeUxvY2F0aW9uOiBQYXJ0aXRpb25GdW5jdGlvbiA9IChncmFwaCwgaWQpID0+IHtcbiAgY29uc3QgYnlMb2NhdGlvbjogKFxuICAgIGxvY2F0aW9uOiBMb2dpY2FsTG9jYXRpb24sXG4gICkgPT4gKHY6IGdyYXBobGliLk5vZGU8R3JhcGhOb2RlVHlwZT4pID0+IGJvb2xlYW4gPSAobG9jYXRpb24pID0+IChub2RlKSA9PiB7XG4gICAgc3dpdGNoIChub2RlLmRhdGEua2luZCkge1xuICAgICAgY2FzZSAnZnVuY3Rpb24nOlxuICAgICAgICByZXR1cm4gaXNFcXVhbChub2RlLmRhdGEubG9jYXRpb24sIGxvY2F0aW9uKTtcbiAgICAgIGNhc2UgJ3JlbW90ZSc6XG4gICAgICAgIHJldHVybiBpc0VxdWFsKG5vZGUuZGF0YS5kYXRhLmxvY2F0aW9uLCBsb2NhdGlvbik7XG4gICAgICBjYXNlICdsb2NhbCc6XG4gICAgICAgIHJldHVybiBncmFwaC5nZXRTdWNjZXNzb3JzKG5vZGUuaWQpLnNvbWUoKHYpID0+IGJ5TG9jYXRpb24obG9jYXRpb24pKHYpKTtcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH07XG4gIGNvbnN0IG1hdGNoZWQgPSBuZXcgU2V0KFxuICAgICgoKSA9PiB7XG4gICAgICBjb25zdCBub2RlID0gZ3JhcGguZ2V0Tm9kZShpZCk7XG4gICAgICBzd2l0Y2ggKG5vZGUuZGF0YS5raW5kKSB7XG4gICAgICAgIGNhc2UgJ2Z1bmN0aW9uJzpcbiAgICAgICAgICByZXR1cm4gZ3JhcGguZ2V0QWxsTm9kZXMoKS5maWx0ZXIoYnlMb2NhdGlvbihub2RlLmRhdGEubG9jYXRpb24pKTtcbiAgICAgICAgY2FzZSAncmVtb3RlJzpcbiAgICAgICAgICByZXR1cm4gZ3JhcGguZ2V0QWxsTm9kZXMoKS5maWx0ZXIoYnlMb2NhdGlvbihub2RlLmRhdGEuZGF0YS5sb2NhdGlvbikpO1xuICAgICAgICBjYXNlICdsb2NhbCc6XG4gICAgICAgICAgcmV0dXJuIGdyYXBoLmdldEFsbE5vZGVzKCkuZmlsdGVyKCh2KSA9PiB2LmRhdGEua2luZCA9PT0gJ2xvY2FsJyk7XG4gICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgcmV0dXJuIFtdO1xuICAgICAgfVxuICAgIH0pKCkubWFwKCh2KSA9PiB2LmlkKSxcbiAgKTtcbiAgbWF0Y2hlZC5hZGQoaWQpO1xuICByZXR1cm4gbWF0Y2hlZDtcbn07XG4iLCJpbXBvcnQgdHlwZSAqIGFzIEc2IGZyb20gJ0BhbnR2L2c2JztcbmltcG9ydCB0eXBlICogYXMgZ3JhcGhsaWIgZnJvbSAnQGFudHYvZ3JhcGhsaWInO1xuaW1wb3J0IENvbG9yIGZyb20gJ2NvbG9yJztcbmltcG9ydCB7IHVzZUNhbGxiYWNrLCB1c2VNZW1vLCB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0JztcblxuaW1wb3J0IHR5cGUgeyBMb2dpY2FsTG9jYXRpb24gfSBmcm9tICcuLi8uLi8ub3BlbmFwaS1zdHVicyc7XG5cbmltcG9ydCB0eXBlIHsgVHJ1c3RlZE1vZGVsIH0gZnJvbSAnLi90eXBlcyc7XG5pbXBvcnQgeyBpc1RydXN0ZWQgfSBmcm9tICcuL3R5cGVzJztcbmltcG9ydCB0eXBlIHsgUGFydGl0aW9uRnVuY3Rpb24gfSBmcm9tICcuL3V0aWxzJztcbmltcG9ydCB7IGNvbXBsZXRlUGFydGl0aW9uLCB0b1B1cmVHcmFwaCB9IGZyb20gJy4vdXRpbHMnO1xuXG5leHBvcnQgdHlwZSBDb2xvcml6ZUZ1bmN0aW9uPFQ+ID0gKGl0ZW06IFQpID0+IHtcbiAgYmFja2dyb3VuZDogc3RyaW5nO1xuICBmb3JlZ3JvdW5kOiBzdHJpbmc7XG59O1xuXG5leHBvcnQgaW50ZXJmYWNlIENvbG9yaXplcjxUPiB7XG4gIGNvbG9ycygpOiBNYXA8c3RyaW5nLCB7IG5hbWU6IHN0cmluZzsgY29sb3I6IHN0cmluZyB9PjtcbiAgY29sb3JpemU6IENvbG9yaXplRnVuY3Rpb248VD47XG59XG5cbmV4cG9ydCBjbGFzcyBMb2NhdGlvbkNvbG9yaXplciBpbXBsZW1lbnRzIENvbG9yaXplcjxMb2dpY2FsTG9jYXRpb24+IHtcbiAgcHJpdmF0ZSByZWFkb25seSBwYWxldHRlOiBzdHJpbmdbXTtcblxuICBwcml2YXRlIHJlYWRvbmx5IGNhY2hlID0gbmV3IE1hcDxzdHJpbmcsIHN0cmluZz4oKTtcbiAgcHJpdmF0ZSByZWFkb25seSBuYW1lcyA9IG5ldyBNYXA8c3RyaW5nLCBzdHJpbmc+KCk7XG5cbiAgY29uc3RydWN0b3IocGFsZXR0ZTogc3RyaW5nW10pIHtcbiAgICB0aGlzLnBhbGV0dGUgPSBwYWxldHRlO1xuICB9XG5cbiAgcHVibGljIGNvbG9yaXplKGxvY2F0aW9uOiBMb2dpY2FsTG9jYXRpb24pIHtcbiAgICBjb25zdCBrZXkgPSBMb2NhdGlvbkNvbG9yaXplci5sb2NhdGlvbktleShsb2NhdGlvbik7XG4gICAgbGV0IGNvbG9yID0gdGhpcy5jYWNoZS5nZXQoa2V5KTtcbiAgICBpZiAoIWNvbG9yKSB7XG4gICAgICBjb2xvciA9IHRoaXMubWFrZUNvbG9yKCk7XG4gICAgICB0aGlzLmNhY2hlLnNldChrZXksIGNvbG9yKTtcbiAgICB9XG4gICAgdGhpcy5uYW1lcy5zZXQoa2V5LCB0aGlzLmxvY2F0aW9uTmFtZShsb2NhdGlvbikpO1xuICAgIHJldHVybiB7IGJhY2tncm91bmQ6IGNvbG9yLCBmb3JlZ3JvdW5kOiB0aGlzLmZvcmVncm91bmQoY29sb3IpIH07XG4gIH1cblxuICBwdWJsaWMgY29sb3JzKCkge1xuICAgIHJldHVybiBuZXcgTWFwKFxuICAgICAgWy4uLnRoaXMubmFtZXMuZW50cmllcygpXS5tYXAoKFtrLCBuYW1lXSkgPT4gW1xuICAgICAgICBrLFxuICAgICAgICB7IG5hbWUsIGNvbG9yOiB0aGlzLmNhY2hlLmdldChrKSEgfSxcbiAgICAgIF0pLFxuICAgICk7XG4gIH1cblxuICBwcml2YXRlIGxvY2F0aW9uTmFtZShsb2NhdGlvbjogTG9naWNhbExvY2F0aW9uKSB7XG4gICAgcmV0dXJuIGAke2xvY2F0aW9uLnR5cGV9WyR7bG9jYXRpb24ucGFydGllcy5qb2luKCcsICcpfV1gO1xuICB9XG5cbiAgcHVibGljIHN0YXRpYyBsb2NhdGlvbktleShsb2NhdGlvbjogTG9naWNhbExvY2F0aW9uKSB7XG4gICAgcmV0dXJuIFtcbiAgICAgIGxvY2F0aW9uLnR5cGUsXG4gICAgICAuLi5sb2NhdGlvbi5wYXJ0aWVzLFxuICAgICAgLi4uT2JqZWN0LmVudHJpZXMobG9jYXRpb24ucGFyYW1ldGVycyA/PyB7fSkubWFwKChbaywgdl0pID0+IGAke2t9PSR7dn1gKSxcbiAgICBdLmpvaW4oJzonKTtcbiAgfVxuXG4gIHByb3RlY3RlZCBtYWtlQ29sb3IoKSB7XG4gICAgY29uc3QgY3VycmVudENvbG9yQ291bnQgPSB0aGlzLmNhY2hlLnNpemU7XG4gICAgY29uc3QgcG9zaXRpb24gPSBjdXJyZW50Q29sb3JDb3VudCAlIHRoaXMucGFsZXR0ZS5sZW5ndGg7XG4gICAgY29uc3QgZ2VuZXJhdGlvbiA9IE1hdGguZmxvb3IoY3VycmVudENvbG9yQ291bnQgLyB0aGlzLnBhbGV0dGUubGVuZ3RoKTtcbiAgICBpZiAoZ2VuZXJhdGlvbiA9PT0gMCkge1xuICAgICAgcmV0dXJuIHRoaXMucGFsZXR0ZVtwb3NpdGlvbl07XG4gICAgfVxuICAgIGNvbnN0IGh1ZVNoaWZ0cyA9IFtcbiAgICAgIC8vIHRyaWFkaWNcbiAgICAgIDEyMCwgMjQwLFxuICAgICAgLy8gdGV0cmFkaWNcbiAgICAgIDkwLCAxODAsIDI3MCxcbiAgICBdO1xuICAgIGNvbnN0IGh1ZVNoaWZ0ID0gaHVlU2hpZnRzW2dlbmVyYXRpb24gLSAxXTtcbiAgICBpZiAoaHVlU2hpZnQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdUb28gbWFueSBjb2xvcnMnKTtcbiAgICB9XG4gICAgcmV0dXJuIG5ldyBDb2xvcih0aGlzLnBhbGV0dGVbcG9zaXRpb25dKS5yb3RhdGUoaHVlU2hpZnQpLmhleCgpO1xuICB9XG5cbiAgcHJvdGVjdGVkIGZvcmVncm91bmQoXG4gICAgY29sb3I6IHN0cmluZyxcbiAgICBkYXJrZW4gPSAwLjIsXG4gICAgbGlnaHQgPSAnI2ZmZmZmZicsXG4gICAgZGFyayA9ICcjMWQxZDFkJyxcbiAgKSB7XG4gICAgcmV0dXJuIG5ldyBDb2xvcihjb2xvcikuZGFya2VuKGRhcmtlbikuaXNEYXJrKCkgPyBsaWdodCA6IGRhcms7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGNvbG9yaXplQnlMb2NhdGlvbihjb2xvcml6ZTogQ29sb3JpemVGdW5jdGlvbjxMb2dpY2FsTG9jYXRpb24+KSB7XG4gIHJldHVybiAobm9kZTogVHJ1c3RlZE1vZGVsKSA9PiB7XG4gICAgc3dpdGNoIChub2RlLmRhdGEua2luZCkge1xuICAgICAgY2FzZSAnZnVuY3Rpb24nOlxuICAgICAgICByZXR1cm4gY29sb3JpemUobm9kZS5kYXRhLmxvY2F0aW9uKTtcbiAgICAgIGNhc2UgJ2xvY2FsJzpcbiAgICAgICAgcmV0dXJuIHsgYmFja2dyb3VuZDogJyMxZDFkMWQnLCBmb3JlZ3JvdW5kOiAnI2ZmZmZmZicgfTtcbiAgICAgIGNhc2UgJ3JlbW90ZSc6XG4gICAgICAgIHJldHVybiBjb2xvcml6ZShub2RlLmRhdGEuZGF0YS5sb2NhdGlvbik7XG4gICAgICBjYXNlICdyZXZlYWwnOlxuICAgICAgICByZXR1cm4geyBiYWNrZ3JvdW5kOiAnI2YwNDY1NCcsIGZvcmVncm91bmQ6ICcjZmZmZmZmJyB9O1xuICAgICAgY2FzZSAnYXJndW1lbnQnOlxuICAgICAgICByZXR1cm4geyBiYWNrZ3JvdW5kOiAnI2E1YWFiNScsIGZvcmVncm91bmQ6ICcjZmZmZmZmJyB9O1xuICAgICAgY2FzZSAncmV0dXJuJzpcbiAgICAgICAgcmV0dXJuIHsgYmFja2dyb3VuZDogJyNhNWFhYjUnLCBmb3JlZ3JvdW5kOiAnI2ZmZmZmZicgfTtcbiAgICAgIGNhc2UgJ3RyYW5zZm9ybSc6XG4gICAgICAgIHJldHVybiBjb2xvcml6ZShub2RlLmRhdGEuZGVzdGluYXRpb24pO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBVbmtub3duIHNoYXBlIGtpbmQ6ICR7bm9kZS5kYXRhLmtpbmR9YCk7XG4gICAgfVxuICB9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVjb2xvck9uSG92ZXIoe1xuICBwYXJ0aXRpb24sXG4gIGNvbG9yaXplLFxufToge1xuICBwYXJ0aXRpb246IFBhcnRpdGlvbkZ1bmN0aW9uO1xuICBjb2xvcml6ZTogKG5vZGU6IFRydXN0ZWRNb2RlbCkgPT4geyBiYWNrZ3JvdW5kOiBzdHJpbmc7IGZvcmVncm91bmQ6IHN0cmluZyB9O1xufSkge1xuICByZXR1cm4gKGdyYXBoOiBHNi5HcmFwaCkgPT4ge1xuICAgIGNvbnN0IGhpZ2hsaWdodCA9IChpZDogZ3JhcGhsaWIuSUQpID0+IHtcbiAgICAgIGNvbnN0IGcgPSB0b1B1cmVHcmFwaChncmFwaCk7XG4gICAgICBjb25zdCB7IG1hdGNoZWQsIHVubWF0Y2hlZCB9ID0gY29tcGxldGVQYXJ0aXRpb24oZywgcGFydGl0aW9uKGcsIGlkKSk7XG5cbiAgICAgIG1hdGNoZWQuZm9yRWFjaCgoaykgPT4ge1xuICAgICAgICBjb25zdCBzaGFwZSA9IGdyYXBoLmZpbmRCeUlkKFN0cmluZyhrKSk7XG4gICAgICAgIGNvbnN0IG1vZGVsID0gc2hhcGUuZ2V0TW9kZWwoKTtcbiAgICAgICAgaWYgKGlzVHJ1c3RlZChtb2RlbCkpIHtcbiAgICAgICAgICBjb25zdCB7IGJhY2tncm91bmQsIGZvcmVncm91bmQgfSA9IGNvbG9yaXplKG1vZGVsKTtcbiAgICAgICAgICBncmFwaC51cGRhdGVJdGVtKHNoYXBlLCB7XG4gICAgICAgICAgICBjb2xvcnM6IHsgYmFja2dyb3VuZCwgZm9yZWdyb3VuZCB9LFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgdW5tYXRjaGVkLmZvckVhY2goKGspID0+IHtcbiAgICAgICAgY29uc3Qgc2hhcGUgPSBncmFwaC5maW5kQnlJZChTdHJpbmcoaykpO1xuICAgICAgICBjb25zdCBtb2RlbCA9IHNoYXBlLmdldE1vZGVsKCk7XG4gICAgICAgIGlmIChpc1RydXN0ZWQobW9kZWwpKSB7XG4gICAgICAgICAgZ3JhcGgudXBkYXRlSXRlbShzaGFwZSwge1xuICAgICAgICAgICAgY29sb3JzOiB7IGJhY2tncm91bmQ6ICcjZDNkM2QzJywgZm9yZWdyb3VuZDogJyNmZmZmZmYnIH0sXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH07XG5cbiAgICBjb25zdCByZXNldCA9ICgpID0+IHtcbiAgICAgIFsuLi5ncmFwaC5nZXROb2RlcygpLCAuLi5ncmFwaC5nZXRFZGdlcygpXS5mb3JFYWNoKChzaGFwZSkgPT4ge1xuICAgICAgICBjb25zdCBtb2RlbCA9IHNoYXBlLmdldE1vZGVsKCk7XG4gICAgICAgIGlmIChpc1RydXN0ZWQobW9kZWwpKSB7XG4gICAgICAgICAgY29uc3QgeyBiYWNrZ3JvdW5kLCBmb3JlZ3JvdW5kIH0gPSBjb2xvcml6ZShtb2RlbCk7XG4gICAgICAgICAgZ3JhcGgudXBkYXRlSXRlbShzaGFwZSwge1xuICAgICAgICAgICAgY29sb3JzOiB7IGJhY2tncm91bmQsIGZvcmVncm91bmQgfSxcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfTtcblxuICAgIGNvbnN0IG9uRW50ZXIgPSAoeyBpdGVtIH06IHsgaXRlbTogRzYuSXRlbSB8IG51bGwgfSkgPT4ge1xuICAgICAgaWYgKCFpdGVtKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGhpZ2hsaWdodChpdGVtLmdldElEKCkpO1xuICAgIH07XG5cbiAgICByZXR1cm4ge1xuICAgICAgZW5hYmxlOiAoKSA9PiB7XG4gICAgICAgIGdyYXBoLm9uKCdub2RlOm1vdXNlZW50ZXInLCBvbkVudGVyKTtcbiAgICAgICAgZ3JhcGgub24oJ25vZGU6bW91c2VsZWF2ZScsIHJlc2V0KTtcbiAgICAgIH0sXG4gICAgICBkaXNhYmxlOiAoKSA9PiB7XG4gICAgICAgIGdyYXBoLm9mZignbm9kZTptb3VzZWVudGVyJywgb25FbnRlcik7XG4gICAgICAgIGdyYXBoLm9mZignbm9kZTptb3VzZWxlYXZlJywgcmVzZXQpO1xuICAgICAgfSxcbiAgICAgIGhpZ2hsaWdodDogKHRhcmdldDogZ3JhcGhsaWIuSUQgfCBudWxsKSA9PiB7XG4gICAgICAgIGlmICh0YXJnZXQpIHtcbiAgICAgICAgICBoaWdobGlnaHQodGFyZ2V0KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXNldCgpO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgIH07XG4gIH07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VDb2xvcml6ZXI8VD4oXG4gIGZhY3Rvcnk6ICgpID0+IENvbG9yaXplcjxUPixcbik6IENvbG9yaXplcjxUPiAmIHsgcmVzZXQ6ICgpID0+IHZvaWQgfSB7XG4gIGNvbnN0IFtjb2xvcml6ZXIsIHNldENvbG9yaXplcl0gPSB1c2VTdGF0ZShmYWN0b3J5KTtcbiAgY29uc3QgWywgc2V0Q29sb3JDb3VudF0gPSB1c2VTdGF0ZSgwKTtcblxuICBjb25zdCBjb2xvcml6ZSA9IHVzZUNhbGxiYWNrPENvbG9yaXplRnVuY3Rpb248VD4+KFxuICAgICguLi5hcmdzKSA9PiB7XG4gICAgICBjb25zdCBjb2xvciA9IGNvbG9yaXplci5jb2xvcml6ZSguLi5hcmdzKTtcbiAgICAgIHNldENvbG9yQ291bnQoY29sb3JpemVyLmNvbG9ycygpLnNpemUpO1xuICAgICAgcmV0dXJuIGNvbG9yO1xuICAgIH0sXG4gICAgW2NvbG9yaXplcl0sXG4gICk7XG5cbiAgcmV0dXJuIHVzZU1lbW8oXG4gICAgKCkgPT4gKHtcbiAgICAgIGNvbG9yaXplLFxuICAgICAgY29sb3JzOiBjb2xvcml6ZXIuY29sb3JzLmJpbmQoY29sb3JpemVyKSxcbiAgICAgIHJlc2V0OiAoKSA9PiB7XG4gICAgICAgIHNldENvbG9yQ291bnQoMCk7XG4gICAgICAgIHNldENvbG9yaXplcihmYWN0b3J5KTtcbiAgICAgIH0sXG4gICAgfSksXG4gICAgW2NvbG9yaXplLCBjb2xvcml6ZXIsIGZhY3RvcnldLFxuICApO1xufVxuIiwiZXhwb3J0IGZ1bmN0aW9uIHRydW5jYXRlKFxuICB0ZXh0OiBzdHJpbmcsXG4gIG1heExlbmd0aCA9IDIwLFxuICBwbGFjZWhvbGRlciA9ICcuLi4nLFxuICBrZWVwOiAnc3RhcnQnIHwgJ2VuZCcgPSAnc3RhcnQnLFxuKSB7XG4gIGNvbnN0IHRyaW1tZWQgPSB0ZXh0LnRyaW0oKTtcbiAgaWYgKHRyaW1tZWQubGVuZ3RoID4gbWF4TGVuZ3RoKSB7XG4gICAgaWYgKGtlZXAgPT09ICdzdGFydCcpIHtcbiAgICAgIHJldHVybiBgJHt0cmltbWVkLnNsaWNlKDAsIG1heExlbmd0aCl9JHtwbGFjZWhvbGRlcn1gO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gYCR7cGxhY2Vob2xkZXJ9JHt0cmltbWVkLnNsaWNlKHRyaW1tZWQubGVuZ3RoIC0gbWF4TGVuZ3RoKX1gO1xuICAgIH1cbiAgfVxuICByZXR1cm4gdGV4dDtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHRydW5jYXRlTGluZXMoXG4gIHRleHQ6IHN0cmluZyxcbiAge1xuICAgIG1heFdpZHRoID0gMjAsXG4gICAgbWF4TGluZXMgPSBJbmZpbml0eSxcbiAgICBwbGFjZWhvbGRlciA9ICcuLi4nLFxuICB9OiB7IG1heFdpZHRoPzogbnVtYmVyOyBtYXhMaW5lcz86IG51bWJlcjsgcGxhY2Vob2xkZXI/OiBzdHJpbmcgfSA9IHt9LFxuKSB7XG4gIGNvbnN0IGxpbmVzID0gdGV4dC5zcGxpdCgnXFxuJyk7XG4gIGlmIChsaW5lcy5sZW5ndGggPiBtYXhMaW5lcykge1xuICAgIGxpbmVzLnNwbGljZShtYXhMaW5lcywgbGluZXMubGVuZ3RoIC0gbWF4TGluZXMpO1xuICAgIGxpbmVzW21heExpbmVzIC0gMV0gPSBsaW5lc1ttYXhMaW5lcyAtIDFdICsgcGxhY2Vob2xkZXI7XG4gIH1cbiAgcmV0dXJuIGxpbmVzLm1hcCgobGluZSkgPT4gdHJ1bmNhdGUobGluZSwgbWF4V2lkdGgsIHBsYWNlaG9sZGVyKSkuam9pbignXFxuJyk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB3cmFwKHRleHQ6IHN0cmluZywgYnJlYWtPbjogc3RyaW5nLCBtYXhXaWR0aCA9IDIwKTogc3RyaW5nIHtcbiAgY29uc3QgcGFydHMgPSB0ZXh0LnNwbGl0KGJyZWFrT24pO1xuXG4gIGlmICghcGFydHMubGVuZ3RoKSB7XG4gICAgcmV0dXJuICcnO1xuICB9XG5cbiAgY29uc3QgbGluZXM6IHN0cmluZ1tdID0gW107XG5cbiAgbGV0IGN1cnJlbnRMaW5lOiBzdHJpbmcgPSBwYXJ0cy5zaGlmdCgpITtcbiAgaWYgKGN1cnJlbnRMaW5lID09PSB1bmRlZmluZWQpIHtcbiAgICByZXR1cm4gJyc7XG4gIH1cblxuICBwYXJ0cy5mb3JFYWNoKChwYXJ0KSA9PiB7XG4gICAgaWYgKChwYXJ0ICsgYnJlYWtPbikubGVuZ3RoID4gbWF4V2lkdGgpIHtcbiAgICAgIGlmIChjdXJyZW50TGluZSkge1xuICAgICAgICBsaW5lcy5wdXNoKGN1cnJlbnRMaW5lKTtcbiAgICAgIH1cbiAgICAgIGxpbmVzLnB1c2goYCR7YnJlYWtPbn0ke3BhcnR9YCk7XG4gICAgfSBlbHNlIGlmICgoY3VycmVudExpbmUgKyBicmVha09uICsgcGFydCkubGVuZ3RoID4gbWF4V2lkdGgpIHtcbiAgICAgIGxpbmVzLnB1c2goY3VycmVudExpbmUpO1xuICAgICAgY3VycmVudExpbmUgPSBgJHticmVha09ufSR7cGFydH1gO1xuICAgIH0gZWxzZSB7XG4gICAgICBjdXJyZW50TGluZSArPSBgJHticmVha09ufSR7cGFydH1gO1xuICAgIH1cbiAgfSk7XG5cbiAgaWYgKGN1cnJlbnRMaW5lKSB7XG4gICAgbGluZXMucHVzaChjdXJyZW50TGluZSk7XG4gIH1cblxuICByZXR1cm4gbGluZXMuam9pbignXFxuJyk7XG59XG4iLCJpbXBvcnQgdHlwZSB7XG4gIEFyZ3VtZW50RWRnZSxcbiAgUmV0dXJuRWRnZSxcbiAgUmV2ZWFsRWRnZSxcbiAgVHJhbnNmb3JtRWRnZSxcbn0gZnJvbSAnLi4vLi4vLm9wZW5hcGktc3R1YnMnO1xuaW1wb3J0IHsgdHJ1bmNhdGUsIHRydW5jYXRlTGluZXMsIHdyYXAgfSBmcm9tICcuLi8uLi91dGlscy9zdHJpbmcnO1xuXG5pbXBvcnQgeyBkZWZpbmVTaGFwZSwgcmVnaXN0ZXJTaGFwZXMgfSBmcm9tICcuL3V0aWxzJztcblxuZGVjbGFyZSBtb2R1bGUgJ0BhbnR2L2c2JyB7XG4gIGludGVyZmFjZSBJU2hhcGUge1xuICAgIGdldFBvaW50KHJhdGlvOiBudW1iZXIpOiB7XG4gICAgICB4OiBudW1iZXI7XG4gICAgICB5OiBudW1iZXI7XG4gICAgfTtcbiAgfVxufVxuXG5jb25zdCBMT0NBTF9EQVRBX05PREUgPSBkZWZpbmVTaGFwZSh7XG4gIGtpbmQ6ICdsb2NhbCcsXG4gIHJlbmRlcjogKHtcbiAgICBpdGVtLFxuICAgIHJlbmRlcmVyLFxuICAgIGNvbmZpZzoge1xuICAgICAgY29sb3JzOiB7IGZvcmVncm91bmQsIGJhY2tncm91bmQgfSA9IHtcbiAgICAgICAgZm9yZWdyb3VuZDogJyNmZmZmZmYnLFxuICAgICAgICBiYWNrZ3JvdW5kOiAnIzFkMWQxZCcsXG4gICAgICB9LFxuICAgIH0sXG4gICAgdXRpbHM6IHsgcmVpZnkgfSxcbiAgfSkgPT4ge1xuICAgIGNvbnN0IHZhbHVlID0gcmVpZnkodW5kZWZpbmVkLCBpdGVtLmRhdGEpO1xuXG4gICAgbGV0IGNvbnRlbnQ6IHN0cmluZyA9ICcnO1xuXG4gICAgc3dpdGNoICh2YWx1ZT8ua2luZCkge1xuICAgICAgY2FzZSAnZGljdCc6XG4gICAgICBjYXNlICdsaXN0JzpcbiAgICAgIGNhc2UgJ29iamVjdCc6XG4gICAgICAgIGNvbnRlbnQgPSBgJHt2YWx1ZS5zbmFwc2hvdH1gO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2Z1bmN0aW9uJzpcbiAgICAgICAgY29udGVudCA9IGAke3ZhbHVlLm5hbWV9KClgO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cblxuICAgIGNvbnRlbnQgPSBjb250ZW50LnRyaW0oKTtcblxuICAgIGxldCBsYWJlbDogc3RyaW5nO1xuXG4gICAgaWYgKGl0ZW0uZGF0YS5uYW1lICYmIGNvbnRlbnQpIHtcbiAgICAgIGxhYmVsID0gYCR7aXRlbS5kYXRhLm5hbWV9ID0gJHtjb250ZW50fWA7XG4gICAgICBpZiAobGFiZWwubGVuZ3RoID4gMTIpIHtcbiAgICAgICAgbGFiZWwgPSBgJHtpdGVtLmRhdGEubmFtZX1cXG49ICR7Y29udGVudH1gO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBsYWJlbCA9IGNvbnRlbnQ7XG4gICAgfVxuXG4gICAgbGFiZWwgPSB0cnVuY2F0ZUxpbmVzKGxhYmVsLCB7IG1heExpbmVzOiAzLCBtYXhXaWR0aDogMTUgfSk7XG5cbiAgICBjb25zdCByZWN0ID0gcmVuZGVyZXIuYWRkU2hhcGUoJ3JlY3QnLCB7XG4gICAgICBuYW1lOiAnYmFja2dyb3VuZCcsXG4gICAgICBhdHRyczoge1xuICAgICAgICBhbmNob3JQb2ludHM6IFtcbiAgICAgICAgICBbMC41LCAwXSxcbiAgICAgICAgICBbMC41LCAxXSxcbiAgICAgICAgXSxcbiAgICAgICAgc3Ryb2tlOiBudWxsLFxuICAgICAgICBmaWxsOiBiYWNrZ3JvdW5kLFxuICAgICAgfSxcbiAgICB9KTtcblxuICAgIGNvbnN0IHRleHQgPSByZW5kZXJlci5hZGRTaGFwZSgndGV4dCcsIHtcbiAgICAgIG5hbWU6ICdsYWJlbCcsXG4gICAgICBhdHRyczoge1xuICAgICAgICB0ZXh0OiBsYWJlbCxcbiAgICAgICAgeDogMCxcbiAgICAgICAgeTogMCxcbiAgICAgICAgZm9udEZhbWlseTogJ1JvYm90byBNb25vLCBtb25vc3BhY2UnLFxuICAgICAgICBmb250U2l6ZTogMTIsXG4gICAgICAgIGxpbmVIZWlnaHQ6IDE2LjgsXG4gICAgICAgIHRleHRBbGlnbjogJ2NlbnRlcicsXG4gICAgICAgIHRleHRCYXNlbGluZTogJ21pZGRsZScsXG4gICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICB9LFxuICAgIH0pO1xuXG4gICAgY29uc3QgeyB3aWR0aCwgaGVpZ2h0LCB4LCB5IH0gPSB0ZXh0LmdldEJCb3goKTtcblxuICAgIHJlY3QuYXR0cignd2lkdGgnLCB3aWR0aCArIDEwKTtcbiAgICByZWN0LmF0dHIoJ2hlaWdodCcsIGhlaWdodCArIDEwKTtcbiAgICByZWN0LmF0dHIoJ3gnLCB4IC0gNSk7XG4gICAgcmVjdC5hdHRyKCd5JywgeSAtIDUpO1xuXG4gICAgcmV0dXJuIHJlY3Q7XG4gIH0sXG59KTtcblxuY29uc3QgUkVNT1RFX0RBVEFfTk9ERSA9IGRlZmluZVNoYXBlKHtcbiAga2luZDogJ3JlbW90ZScsXG4gIHJlbmRlcjogKHsgaXRlbSwgcmVuZGVyZXIsIGNvbmZpZzogeyBjb2xvcnMgfSwgdXRpbHM6IHsgY29sb3JpemUgfSB9KSA9PiB7XG4gICAgY29uc3QgeyBiYWNrZ3JvdW5kLCBmb3JlZ3JvdW5kIH0gPSBjb2xvcnMgfHwgY29sb3JpemUoaXRlbS5kYXRhLmxvY2F0aW9uKTtcbiAgICBjb25zdCBsYWJlbCA9IGAke2l0ZW0uZGF0YS5sb2NhdGlvbi50eXBlWzBdfSR7aXRlbS5kYXRhLm51bWJlcmluZ31gO1xuXG4gICAgY29uc3QgcmVjdCA9IHJlbmRlcmVyLmFkZFNoYXBlKCdjaXJjbGUnLCB7XG4gICAgICBuYW1lOiAnYmFja2dyb3VuZCcsXG4gICAgICBhdHRyczoge1xuICAgICAgICB4OiAwLFxuICAgICAgICB5OiAwLFxuICAgICAgICBhbmNob3JQb2ludHM6IFtcbiAgICAgICAgICBbMC41LCAwXSxcbiAgICAgICAgICBbMC41LCAxXSxcbiAgICAgICAgXSxcbiAgICAgICAgc3Ryb2tlOiBudWxsLFxuICAgICAgICBmaWxsOiBiYWNrZ3JvdW5kLFxuICAgICAgfSxcbiAgICB9KTtcblxuICAgIHJlbmRlcmVyLmFkZFNoYXBlKCd0ZXh0Jywge1xuICAgICAgbmFtZTogJ2xhYmVsJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIHRleHQ6IGxhYmVsLFxuICAgICAgICB4OiAwLFxuICAgICAgICB5OiAwLFxuICAgICAgICBmb250RmFtaWx5OiAnSW50ZXIsIHNhbnMtc2VyaWYnLFxuICAgICAgICBmb250V2VpZ2h0OiA3MDAsXG4gICAgICAgIGZvbnRTaXplOiAxMixcbiAgICAgICAgbGluZUhlaWdodDogMTYsXG4gICAgICAgIHRleHRBbGlnbjogJ2NlbnRlcicsXG4gICAgICAgIHRleHRCYXNlbGluZTogJ21pZGRsZScsXG4gICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICB9LFxuICAgIH0pO1xuXG4gICAgY29uc3QgZGlhbWV0ZXIgPSA0MCArIE1hdGguZmxvb3IoTWF0aC5sb2cxMChpdGVtLmRhdGEubnVtYmVyaW5nIHx8IDApIC8gMikgKiA1O1xuXG4gICAgcmVjdC5hdHRyKCd3aWR0aCcsIGRpYW1ldGVyKTtcbiAgICByZWN0LmF0dHIoJ2hlaWdodCcsIGRpYW1ldGVyKTtcbiAgICByZWN0LmF0dHIoJ3gnLCAwKTtcbiAgICByZWN0LmF0dHIoJ3knLCAwKTtcbiAgICByZWN0LmF0dHIoJ3InLCBkaWFtZXRlciAvIDIpO1xuXG4gICAgcmV0dXJuIHJlY3Q7XG4gIH0sXG59KTtcblxuY29uc3QgRlVOQ1RJT05fTk9ERSA9IGRlZmluZVNoYXBlKHtcbiAga2luZDogJ2Z1bmN0aW9uJyxcbiAgcmVuZGVyOiAoeyBpdGVtLCByZW5kZXJlciwgY29uZmlnOiB7IGNvbG9ycyB9LCB1dGlsczogeyByZWlmeSwgY29sb3JpemUgfSB9KSA9PiB7XG4gICAgY29uc3QgeyBiYWNrZ3JvdW5kLCBmb3JlZ3JvdW5kIH0gPSBjb2xvcnMgfHwgY29sb3JpemUoaXRlbS5sb2NhdGlvbik7XG5cbiAgICBjb25zdCBsYWJlbCA9ICgoKSA9PiB7XG4gICAgICBjb25zdCBwYXJ0aWVzID0gaXRlbS5sb2NhdGlvbi5wYXJ0aWVzLm1hcCgoZCkgPT4gZFswXS50b1VwcGVyQ2FzZSgpKS5qb2luKCcsJyk7XG4gICAgICBpZiAoaXRlbS5mdW5jdGlvbikge1xuICAgICAgICBjb25zdCB2YWx1ZSA9IHJlaWZ5KCdmdW5jdGlvbicsIGl0ZW0uZnVuY3Rpb24pO1xuICAgICAgICBpZiAodmFsdWUpIHtcbiAgICAgICAgICByZXR1cm4gdHJ1bmNhdGVMaW5lcyh3cmFwKGBsZXQgJHtwYXJ0aWVzfSBpbiAke3ZhbHVlLm5hbWV9YCwgJy4nLCAyNCksIHtcbiAgICAgICAgICAgIG1heFdpZHRoOiAyNCxcbiAgICAgICAgICAgIG1heExpbmVzOiAyLFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gYGxldCAke3BhcnRpZXN9IGluIChhbm9ueW1vdXMpYDtcbiAgICB9KSgpO1xuXG4gICAgY29uc3QgcmVjdCA9IHJlbmRlcmVyLmFkZFNoYXBlKCdyZWN0Jywge1xuICAgICAgbmFtZTogJ2JhY2tncm91bmQnLFxuICAgICAgYXR0cnM6IHtcbiAgICAgICAgcmFkaXVzOiA4LFxuICAgICAgICBhbmNob3JQb2ludHM6IFtcbiAgICAgICAgICBbMC41LCAwXSxcbiAgICAgICAgICBbMC41LCAxXSxcbiAgICAgICAgXSxcbiAgICAgICAgc3Ryb2tlOiBudWxsLFxuICAgICAgICBmaWxsOiBiYWNrZ3JvdW5kLFxuICAgICAgICBsaW5lV2lkdGg6IDIsXG4gICAgICB9LFxuICAgIH0pO1xuXG4gICAgY29uc3QgdGV4dCA9IHJlbmRlcmVyLmFkZFNoYXBlKCd0ZXh0Jywge1xuICAgICAgbmFtZTogJ2xhYmVsJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIHRleHQ6IGxhYmVsLFxuICAgICAgICB4OiAwLFxuICAgICAgICB5OiAwLFxuICAgICAgICBmb250RmFtaWx5OiAnUm9ib3RvIE1vbm8sIG1vbm9zcGFjZScsXG4gICAgICAgIGZvbnRTaXplOiAxMixcbiAgICAgICAgZm9udFdlaWdodDogNjAwLFxuICAgICAgICBsaW5lSGVpZ2h0OiAxNC40LFxuICAgICAgICBsZXR0ZXJTcGFjaW5nOiAwLjUsXG4gICAgICAgIHRleHRBbGlnbjogJ2NlbnRlcicsXG4gICAgICAgIHRleHRCYXNlbGluZTogJ21pZGRsZScsXG4gICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICB9LFxuICAgIH0pO1xuXG4gICAgY29uc3QgeyB3aWR0aCwgaGVpZ2h0LCB4LCB5IH0gPSB0ZXh0LmdldEJCb3goKTtcblxuICAgIHJlY3QuYXR0cignd2lkdGgnLCB3aWR0aCArIDMwKTtcbiAgICByZWN0LmF0dHIoJ2hlaWdodCcsIGhlaWdodCArIDE1KTtcbiAgICByZWN0LmF0dHIoJ3gnLCB4IC0gMTUpO1xuICAgIHJlY3QuYXR0cigneScsIHkgLSA3LjUpO1xuXG4gICAgcmV0dXJuIHJlY3Q7XG4gIH0sXG59KTtcblxuY29uc3QgUkVWRUFMX05PREUgPSBkZWZpbmVTaGFwZSh7XG4gIGtpbmQ6ICdyZXZlYWwnLFxuICByZW5kZXI6ICh7XG4gICAgcmVuZGVyZXIsXG4gICAgY29uZmlnOiB7XG4gICAgICBjb2xvcnM6IHsgYmFja2dyb3VuZCwgZm9yZWdyb3VuZCB9ID0ge1xuICAgICAgICBiYWNrZ3JvdW5kOiAnI2YwNDY1NCcsXG4gICAgICAgIGZvcmVncm91bmQ6ICcjZmZmZmZmJyxcbiAgICAgIH0sXG4gICAgfSxcbiAgfSkgPT4ge1xuICAgIGNvbnN0IHJlY3QgPSByZW5kZXJlci5hZGRTaGFwZSgncmVjdCcsIHtcbiAgICAgIG5hbWU6ICdiYWNrZ3JvdW5kJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIGFuY2hvclBvaW50czogW1xuICAgICAgICAgIFswLjUsIDBdLFxuICAgICAgICAgIFswLjUsIDFdLFxuICAgICAgICBdLFxuICAgICAgICBzdHJva2U6IG51bGwsXG4gICAgICAgIGZpbGw6IGJhY2tncm91bmQsXG4gICAgICB9LFxuICAgIH0pO1xuICAgIGNvbnN0IHRleHQgPSByZW5kZXJlci5hZGRTaGFwZSgndGV4dCcsIHtcbiAgICAgIG5hbWU6ICdsYWJlbCcsXG4gICAgICBhdHRyczoge1xuICAgICAgICB0ZXh0OiAncmV2ZWFsJyxcbiAgICAgICAgeDogMCxcbiAgICAgICAgeTogMCxcbiAgICAgICAgZm9udEZhbWlseTogJ0ludGVyLCBzYW5zLXNlcmlmJyxcbiAgICAgICAgZm9udFNpemU6IDEyLFxuICAgICAgICBmb250V2VpZ2h0OiA1MDAsXG4gICAgICAgIGxpbmVIZWlnaHQ6IDE2LjgsXG4gICAgICAgIHRleHRBbGlnbjogJ2NlbnRlcicsXG4gICAgICAgIHRleHRCYXNlbGluZTogJ21pZGRsZScsXG4gICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICB9LFxuICAgIH0pO1xuXG4gICAgY29uc3QgeyB3aWR0aCwgaGVpZ2h0LCB4LCB5IH0gPSB0ZXh0LmdldEJCb3goKTtcblxuICAgIHJlY3QuYXR0cignd2lkdGgnLCB3aWR0aCArIDEwKTtcbiAgICByZWN0LmF0dHIoJ2hlaWdodCcsIGhlaWdodCArIDEwKTtcbiAgICByZWN0LmF0dHIoJ3gnLCB4IC0gNSk7XG4gICAgcmVjdC5hdHRyKCd5JywgeSAtIDUpO1xuXG4gICAgcmV0dXJuIHJlY3Q7XG4gIH0sXG59KTtcblxuZnVuY3Rpb24gZGlzdGFuY2UoeDE6IG51bWJlciwgeTE6IG51bWJlciwgeDI6IG51bWJlciwgeTI6IG51bWJlcik6IG51bWJlciB7XG4gIHJldHVybiBNYXRoLnNxcnQoTWF0aC5wb3coeDIgLSB4MSwgMikgKyBNYXRoLnBvdyh5MiAtIHkxLCAyKSk7XG59XG5cbi8vIFRoYW5rIHlvdSBHUFQgKGFuZCBEZXNtb3MpXG5mdW5jdGlvbiB0ZXh0Um90YXRpb24oeDE6IG51bWJlciwgeTE6IG51bWJlciwgeDI6IG51bWJlciwgeTI6IG51bWJlcik6IG51bWJlciB7XG4gIGNvbnN0IGR4ID0geDIgLSB4MTtcbiAgY29uc3QgZHkgPSB5MiAtIHkxO1xuICBsZXQgdGhldGEgPSBNYXRoLmF0YW4yKGR5LCBkeCk7XG4gIGlmIChkeCA8IDApIHtcbiAgICB0aGV0YSAtPSBNYXRoLlBJO1xuICB9XG4gIGlmICh0aGV0YSA+ICg3MCAvIDE4MCkgKiBNYXRoLlBJKSB7XG4gICAgcmV0dXJuIHRoZXRhIC0gKDEgLyAyKSAqIE1hdGguUEk7XG4gIH1cbiAgaWYgKHRoZXRhIDwgKC03MCAvIDE4MCkgKiBNYXRoLlBJKSB7XG4gICAgcmV0dXJuIHRoZXRhICsgKDEgLyAyKSAqIE1hdGguUEk7XG4gIH1cbiAgcmV0dXJuIHRoZXRhO1xufVxuXG5jb25zdCBBUkdVTUVOVF9FREdFID0gZGVmaW5lU2hhcGU8QXJndW1lbnRFZGdlLCAnYXJndW1lbnQnPih7XG4gIGtpbmQ6ICdhcmd1bWVudCcsXG4gIHJlbmRlcjogKHtcbiAgICBpdGVtLFxuICAgIHJlbmRlcmVyLFxuICAgIGNvbmZpZzoge1xuICAgICAgc3RhcnRQb2ludCA9IHsgeDogMCwgeTogMCB9LFxuICAgICAgZW5kUG9pbnQgPSB7IHg6IDAsIHk6IDAgfSxcbiAgICAgIGNvbG9yczogeyBiYWNrZ3JvdW5kLCBmb3JlZ3JvdW5kIH0gPSB7XG4gICAgICAgIGJhY2tncm91bmQ6ICcjYTVhYWI1JyxcbiAgICAgICAgZm9yZWdyb3VuZDogJyNmZmZmZmYnLFxuICAgICAgfSxcbiAgICB9LFxuICB9KSA9PiB7XG4gICAgY29uc3Qgc2hhcGUgPSByZW5kZXJlci5hZGRTaGFwZSgncGF0aCcsIHtcbiAgICAgIG5hbWU6ICdsaW5lJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIHN0cm9rZTogYmFja2dyb3VuZCxcbiAgICAgICAgbGluZVdpZHRoOiAxLFxuICAgICAgICBwYXRoOiBbXG4gICAgICAgICAgWydNJywgc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnldLFxuICAgICAgICAgIFsnTCcsIGVuZFBvaW50LngsIGVuZFBvaW50LnldLFxuICAgICAgICBdLFxuICAgICAgICBlbmRBcnJvdzoge1xuICAgICAgICAgIHBhdGg6ICdNIDUgLTUgTCAwIDAgTCA1IDUnLFxuICAgICAgICAgIGxpbmVXaWR0aDogMSxcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSk7XG4gICAgaWYgKGl0ZW0ubmFtZSkge1xuICAgICAgY29uc3QgbGFiZWwgPSB0cnVuY2F0ZShpdGVtLm5hbWUsIDIwKTtcbiAgICAgIGNvbnN0IG1pZFBvaW50ID0gc2hhcGUuZ2V0UG9pbnQoMC41KTtcbiAgICAgIGNvbnN0IHJlY3QgPSByZW5kZXJlci5hZGRTaGFwZSgncmVjdCcsIHtcbiAgICAgICAgbmFtZTogJ2xhYmVsLWJhY2tncm91bmQnLFxuICAgICAgICBhdHRyczoge1xuICAgICAgICAgIHJhZGl1czogMCxcbiAgICAgICAgICBhbmNob3JQb2ludHM6IFtcbiAgICAgICAgICAgIFswLjUsIDBdLFxuICAgICAgICAgICAgWzAuNSwgMV0sXG4gICAgICAgICAgXSxcbiAgICAgICAgICBzdHJva2U6IG51bGwsXG4gICAgICAgICAgZmlsbDogYmFja2dyb3VuZCxcbiAgICAgICAgfSxcbiAgICAgIH0pO1xuICAgICAgY29uc3QgdGV4dCA9IHJlbmRlcmVyLmFkZFNoYXBlKCd0ZXh0Jywge1xuICAgICAgICBuYW1lOiAnbGFiZWwnLFxuICAgICAgICBhdHRyczoge1xuICAgICAgICAgIHRleHQ6IGxhYmVsLFxuICAgICAgICAgIHg6IG1pZFBvaW50LngsXG4gICAgICAgICAgeTogbWlkUG9pbnQueSxcbiAgICAgICAgICBmb250RmFtaWx5OiAnUm9ib3RvIE1vbm8sIG1vbm9zcGFjZScsXG4gICAgICAgICAgZm9udFN0eWxlOiAnaXRhbGljJyxcbiAgICAgICAgICBmb250U2l6ZTogMTEsXG4gICAgICAgICAgdGV4dEFsaWduOiAnY2VudGVyJyxcbiAgICAgICAgICB0ZXh0QmFzZWxpbmU6ICdtaWRkbGUnLFxuICAgICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICAgIH0sXG4gICAgICB9KTtcbiAgICAgIGNvbnN0IHsgd2lkdGgsIGhlaWdodCwgeCwgeSB9ID0gdGV4dC5nZXRCQm94KCk7XG4gICAgICByZWN0LmF0dHIoJ3dpZHRoJywgd2lkdGggKyA1KTtcbiAgICAgIHJlY3QuYXR0cignaGVpZ2h0JywgaGVpZ2h0ICsgNSk7XG4gICAgICBjb25zdCByb3RhdGlvbiA9IHRleHRSb3RhdGlvbihzdGFydFBvaW50LngsIHN0YXJ0UG9pbnQueSwgZW5kUG9pbnQueCwgZW5kUG9pbnQueSk7XG4gICAgICBpZiAoXG4gICAgICAgIHdpZHRoID4gMzAgJiZcbiAgICAgICAgd2lkdGggPCBkaXN0YW5jZShzdGFydFBvaW50LngsIHN0YXJ0UG9pbnQueSwgZW5kUG9pbnQueCwgZW5kUG9pbnQueSkgLSAyMFxuICAgICAgKSB7XG4gICAgICAgIHJlY3Qucm90YXRlQXRQb2ludChtaWRQb2ludC54LCBtaWRQb2ludC55LCByb3RhdGlvbik7XG4gICAgICAgIHRleHQucm90YXRlQXRQb2ludChtaWRQb2ludC54LCBtaWRQb2ludC55LCByb3RhdGlvbik7XG4gICAgICB9XG4gICAgICByZWN0LmF0dHIoJ3gnLCB4IC0gMi41KTtcbiAgICAgIHJlY3QuYXR0cigneScsIHkgLSAyLjUpO1xuICAgIH1cbiAgICByZXR1cm4gc2hhcGU7XG4gIH0sXG59KTtcblxuY29uc3QgUkVWRUFMX0VER0UgPSBkZWZpbmVTaGFwZTxSZXZlYWxFZGdlLCAncmV2ZWFsJz4oe1xuICBraW5kOiAncmV2ZWFsJyxcbiAgcmVuZGVyOiAoe1xuICAgIGl0ZW0sXG4gICAgcmVuZGVyZXIsXG4gICAgY29uZmlnOiB7XG4gICAgICBzdGFydFBvaW50ID0geyB4OiAwLCB5OiAwIH0sXG4gICAgICBlbmRQb2ludCA9IHsgeDogMCwgeTogMCB9LFxuICAgICAgY29sb3JzOiB7IGJhY2tncm91bmQsIGZvcmVncm91bmQgfSA9IHtcbiAgICAgICAgYmFja2dyb3VuZDogJyNmMDQ2NTQnLFxuICAgICAgICBmb3JlZ3JvdW5kOiAnI2ZmZmZmZicsXG4gICAgICB9LFxuICAgIH0sXG4gIH0pID0+IHtcbiAgICBjb25zdCBzaGFwZSA9IHJlbmRlcmVyLmFkZFNoYXBlKCdwYXRoJywge1xuICAgICAgbmFtZTogJ2xpbmUnLFxuICAgICAgYXR0cnM6IHtcbiAgICAgICAgc3Ryb2tlOiBiYWNrZ3JvdW5kLFxuICAgICAgICBsaW5lV2lkdGg6IDEsXG4gICAgICAgIHBhdGg6IFtcbiAgICAgICAgICBbJ00nLCBzdGFydFBvaW50LngsIHN0YXJ0UG9pbnQueV0sXG4gICAgICAgICAgWydMJywgZW5kUG9pbnQueCwgZW5kUG9pbnQueV0sXG4gICAgICAgIF0sXG4gICAgICAgIGxpbmVEYXNoOiBbMl0sXG4gICAgICB9LFxuICAgIH0pO1xuICAgIGlmIChpdGVtLm5hbWUpIHtcbiAgICAgIGNvbnN0IGxhYmVsID0gdHJ1bmNhdGUoaXRlbS5uYW1lLCAyMCk7XG4gICAgICBjb25zdCBtaWRQb2ludCA9IHNoYXBlLmdldFBvaW50KDAuNSk7XG4gICAgICBjb25zdCByZWN0ID0gcmVuZGVyZXIuYWRkU2hhcGUoJ3JlY3QnLCB7XG4gICAgICAgIG5hbWU6ICdsYWJlbC1iYWNrZ3JvdW5kJyxcbiAgICAgICAgYXR0cnM6IHtcbiAgICAgICAgICByYWRpdXM6IDAsXG4gICAgICAgICAgYW5jaG9yUG9pbnRzOiBbXG4gICAgICAgICAgICBbMC41LCAwXSxcbiAgICAgICAgICAgIFswLjUsIDFdLFxuICAgICAgICAgIF0sXG4gICAgICAgICAgc3Ryb2tlOiBudWxsLFxuICAgICAgICAgIGZpbGw6IGJhY2tncm91bmQsXG4gICAgICAgIH0sXG4gICAgICB9KTtcbiAgICAgIGNvbnN0IHRleHQgPSByZW5kZXJlci5hZGRTaGFwZSgndGV4dCcsIHtcbiAgICAgICAgbmFtZTogJ2xhYmVsJyxcbiAgICAgICAgYXR0cnM6IHtcbiAgICAgICAgICB0ZXh0OiBsYWJlbCxcbiAgICAgICAgICB4OiBtaWRQb2ludC54LFxuICAgICAgICAgIHk6IG1pZFBvaW50LnksXG4gICAgICAgICAgZm9udEZhbWlseTogJ1JvYm90byBNb25vLCBtb25vc3BhY2UnLFxuICAgICAgICAgIGZvbnRTdHlsZTogJ2l0YWxpYycsXG4gICAgICAgICAgZm9udFNpemU6IDExLFxuICAgICAgICAgIHRleHRBbGlnbjogJ2NlbnRlcicsXG4gICAgICAgICAgdGV4dEJhc2VsaW5lOiAnbWlkZGxlJyxcbiAgICAgICAgICBmaWxsOiBmb3JlZ3JvdW5kLFxuICAgICAgICB9LFxuICAgICAgfSk7XG4gICAgICBjb25zdCB7IHdpZHRoLCBoZWlnaHQsIHgsIHkgfSA9IHRleHQuZ2V0QkJveCgpO1xuICAgICAgcmVjdC5hdHRyKCd3aWR0aCcsIHdpZHRoICsgNSk7XG4gICAgICByZWN0LmF0dHIoJ2hlaWdodCcsIGhlaWdodCArIDUpO1xuICAgICAgY29uc3Qgcm90YXRpb24gPSB0ZXh0Um90YXRpb24oc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnksIGVuZFBvaW50LngsIGVuZFBvaW50LnkpO1xuICAgICAgaWYgKFxuICAgICAgICB3aWR0aCA+IDMwICYmXG4gICAgICAgIHdpZHRoIDwgZGlzdGFuY2Uoc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnksIGVuZFBvaW50LngsIGVuZFBvaW50LnkpIC0gMjBcbiAgICAgICkge1xuICAgICAgICByZWN0LnJvdGF0ZUF0UG9pbnQobWlkUG9pbnQueCwgbWlkUG9pbnQueSwgcm90YXRpb24pO1xuICAgICAgICB0ZXh0LnJvdGF0ZUF0UG9pbnQobWlkUG9pbnQueCwgbWlkUG9pbnQueSwgcm90YXRpb24pO1xuICAgICAgfVxuICAgICAgcmVjdC5hdHRyKCd4JywgeCAtIDIuNSk7XG4gICAgICByZWN0LmF0dHIoJ3knLCB5IC0gMi41KTtcbiAgICB9XG4gICAgcmV0dXJuIHNoYXBlO1xuICB9LFxufSk7XG5cbmNvbnN0IFJFVFVSTl9FREdFID0gZGVmaW5lU2hhcGU8UmV0dXJuRWRnZSwgJ3JldHVybic+KHtcbiAga2luZDogJ3JldHVybicsXG4gIHJlbmRlcjogKHtcbiAgICBpdGVtLFxuICAgIHJlbmRlcmVyLFxuICAgIGNvbmZpZzoge1xuICAgICAgc3RhcnRQb2ludCA9IHsgeDogMCwgeTogMCB9LFxuICAgICAgZW5kUG9pbnQgPSB7IHg6IDAsIHk6IDAgfSxcbiAgICAgIGNvbG9yczogeyBiYWNrZ3JvdW5kLCBmb3JlZ3JvdW5kIH0gPSB7XG4gICAgICAgIGJhY2tncm91bmQ6ICcjYTVhYWI1JyxcbiAgICAgICAgZm9yZWdyb3VuZDogJyNmZmZmZmYnLFxuICAgICAgfSxcbiAgICB9LFxuICB9KSA9PiB7XG4gICAgY29uc3Qgc2hhcGUgPSByZW5kZXJlci5hZGRTaGFwZSgncGF0aCcsIHtcbiAgICAgIG5hbWU6ICdsaW5lJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIHN0cm9rZTogYmFja2dyb3VuZCxcbiAgICAgICAgbGluZVdpZHRoOiAxLFxuICAgICAgICBwYXRoOiBbXG4gICAgICAgICAgWydNJywgc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnldLFxuICAgICAgICAgIFsnTCcsIGVuZFBvaW50LngsIGVuZFBvaW50LnldLFxuICAgICAgICBdLFxuICAgICAgICBlbmRBcnJvdzoge1xuICAgICAgICAgIHBhdGg6ICdNIDUgLTUgTCAwIDAgTCA1IDUnLFxuICAgICAgICAgIGxpbmVXaWR0aDogMSxcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSk7XG4gICAgaWYgKGl0ZW0uYXNzaWdubWVudCkge1xuICAgICAgY29uc3QgbGFiZWwgPSB0cnVuY2F0ZShpdGVtLmFzc2lnbm1lbnQsIDIwKTtcbiAgICAgIGNvbnN0IG1pZFBvaW50ID0gc2hhcGUuZ2V0UG9pbnQoMC41KTtcbiAgICAgIGNvbnN0IHJlY3QgPSByZW5kZXJlci5hZGRTaGFwZSgncmVjdCcsIHtcbiAgICAgICAgbmFtZTogJ2xhYmVsLWJhY2tncm91bmQnLFxuICAgICAgICBhdHRyczoge1xuICAgICAgICAgIHJhZGl1czogMCxcbiAgICAgICAgICBhbmNob3JQb2ludHM6IFtcbiAgICAgICAgICAgIFswLjUsIDBdLFxuICAgICAgICAgICAgWzAuNSwgMV0sXG4gICAgICAgICAgXSxcbiAgICAgICAgICBzdHJva2U6IG51bGwsXG4gICAgICAgICAgZmlsbDogYmFja2dyb3VuZCxcbiAgICAgICAgfSxcbiAgICAgIH0pO1xuICAgICAgY29uc3QgdGV4dCA9IHJlbmRlcmVyLmFkZFNoYXBlKCd0ZXh0Jywge1xuICAgICAgICBuYW1lOiAnbGFiZWwnLFxuICAgICAgICBhdHRyczoge1xuICAgICAgICAgIHRleHQ6IGxhYmVsLFxuICAgICAgICAgIHg6IG1pZFBvaW50LngsXG4gICAgICAgICAgeTogbWlkUG9pbnQueSxcbiAgICAgICAgICBmb250RmFtaWx5OiAnUm9ib3RvIE1vbm8sIG1vbm9zcGFjZScsXG4gICAgICAgICAgZm9udFN0eWxlOiAnaXRhbGljJyxcbiAgICAgICAgICBmb250U2l6ZTogMTEsXG4gICAgICAgICAgdGV4dEFsaWduOiAnY2VudGVyJyxcbiAgICAgICAgICB0ZXh0QmFzZWxpbmU6ICdtaWRkbGUnLFxuICAgICAgICAgIGZpbGw6IGZvcmVncm91bmQsXG4gICAgICAgIH0sXG4gICAgICB9KTtcbiAgICAgIGNvbnN0IHsgd2lkdGgsIGhlaWdodCwgeCwgeSB9ID0gdGV4dC5nZXRCQm94KCk7XG4gICAgICByZWN0LmF0dHIoJ3dpZHRoJywgd2lkdGggKyA1KTtcbiAgICAgIHJlY3QuYXR0cignaGVpZ2h0JywgaGVpZ2h0ICsgNSk7XG4gICAgICBjb25zdCByb3RhdGlvbiA9IHRleHRSb3RhdGlvbihzdGFydFBvaW50LngsIHN0YXJ0UG9pbnQueSwgZW5kUG9pbnQueCwgZW5kUG9pbnQueSk7XG4gICAgICBpZiAoXG4gICAgICAgIHdpZHRoID4gMzAgJiZcbiAgICAgICAgd2lkdGggPCBkaXN0YW5jZShzdGFydFBvaW50LngsIHN0YXJ0UG9pbnQueSwgZW5kUG9pbnQueCwgZW5kUG9pbnQueSkgLSAyMFxuICAgICAgKSB7XG4gICAgICAgIHJlY3Qucm90YXRlQXRQb2ludChtaWRQb2ludC54LCBtaWRQb2ludC55LCByb3RhdGlvbik7XG4gICAgICAgIHRleHQucm90YXRlQXRQb2ludChtaWRQb2ludC54LCBtaWRQb2ludC55LCByb3RhdGlvbik7XG4gICAgICB9XG4gICAgICByZWN0LmF0dHIoJ3gnLCB4IC0gMi41KTtcbiAgICAgIHJlY3QuYXR0cigneScsIHkgLSAyLjUpO1xuICAgIH1cbiAgICByZXR1cm4gc2hhcGU7XG4gIH0sXG59KTtcblxuY29uc3QgVFJBTlNGT1JNX0VER0UgPSBkZWZpbmVTaGFwZTxUcmFuc2Zvcm1FZGdlLCAndHJhbnNmb3JtJz4oe1xuICBraW5kOiAndHJhbnNmb3JtJyxcbiAgcmVuZGVyOiAoe1xuICAgIGl0ZW0sXG4gICAgcmVuZGVyZXIsXG4gICAgY29uZmlnOiB7IHN0YXJ0UG9pbnQgPSB7IHg6IDAsIHk6IDAgfSwgZW5kUG9pbnQgPSB7IHg6IDAsIHk6IDAgfSwgY29sb3JzIH0sXG4gICAgdXRpbHM6IHsgY29sb3JpemUgfSxcbiAgfSkgPT4ge1xuICAgIGNvbnN0IHsgYmFja2dyb3VuZCB9ID0gY29sb3JzIHx8IGNvbG9yaXplKGl0ZW0uZGVzdGluYXRpb24pO1xuICAgIGNvbnN0IHNoYXBlID0gcmVuZGVyZXIuYWRkU2hhcGUoJ3BhdGgnLCB7XG4gICAgICBuYW1lOiAnbGluZS1iYWNrZ3JvdW5kJyxcbiAgICAgIGF0dHJzOiB7XG4gICAgICAgIHN0cm9rZTogYmFja2dyb3VuZCxcbiAgICAgICAgbGluZVdpZHRoOiAzLFxuICAgICAgICBwYXRoOiBbXG4gICAgICAgICAgWydNJywgc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnldLFxuICAgICAgICAgIFsnTCcsIGVuZFBvaW50LngsIGVuZFBvaW50LnldLFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICB9KTtcbiAgICByZW5kZXJlci5hZGRTaGFwZSgncGF0aCcsIHtcbiAgICAgIG5hbWU6ICdsaW5lLWZvcmVncm91bmQnLFxuICAgICAgYXR0cnM6IHtcbiAgICAgICAgc3Ryb2tlOiAnI2ZmZmZmZicsXG4gICAgICAgIGxpbmVXaWR0aDogMS41LFxuICAgICAgICBwYXRoOiBbXG4gICAgICAgICAgWydNJywgc3RhcnRQb2ludC54LCBzdGFydFBvaW50LnldLFxuICAgICAgICAgIFsnTCcsIGVuZFBvaW50LngsIGVuZFBvaW50LnldLFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICB9KTtcbiAgICByZXR1cm4gc2hhcGU7XG4gIH0sXG59KTtcblxuZXhwb3J0IGZ1bmN0aW9uIHNldHVwRzYoKSB7XG4gIHJldHVybiB7XG4gICAgZnJvbUdyYXBoOiByZWdpc3RlclNoYXBlcyh7XG4gICAgICBub2RlczogW0xPQ0FMX0RBVEFfTk9ERSwgUkVNT1RFX0RBVEFfTk9ERSwgRlVOQ1RJT05fTk9ERSwgUkVWRUFMX05PREVdLFxuICAgICAgZWRnZXM6IFtBUkdVTUVOVF9FREdFLCBSRVRVUk5fRURHRSwgVFJBTlNGT1JNX0VER0UsIFJFVkVBTF9FREdFXSxcbiAgICB9KSxcbiAgfTtcbn1cbiIsImltcG9ydCB0eXBlICogYXMgRzYgZnJvbSAnQGFudHYvZzYnO1xuaW1wb3J0ICogYXMgZDMgZnJvbSAnZDMnO1xuaW1wb3J0IFlBTUwgZnJvbSAneWFtbCc7XG5cbmltcG9ydCB0eXBlIHtcbiAgUmVtb3RlT2JqZWN0Tm9kZSxcbiAgTG9jYWxPYmplY3ROb2RlLFxuICBGdW5jdGlvbk5vZGUsXG59IGZyb20gJy4uLy4uLy5vcGVuYXBpLXN0dWJzJztcbmltcG9ydCB0eXBlIHsgU25hcHNob3RSZWlmaWVyIH0gZnJvbSAnLi4vLi4vdXRpbHMvcmVpZnknO1xuaW1wb3J0IHsgd3JhcCB9IGZyb20gJy4uLy4uL3V0aWxzL3N0cmluZyc7XG5cbmltcG9ydCB7IGlzVHJ1c3RlZCB9IGZyb20gJy4vdHlwZXMnO1xuXG50eXBlIFNlbGVjdGlvbjxULCBFIGV4dGVuZHMgZDMuQmFzZVR5cGUgPSBIVE1MRGl2RWxlbWVudD4gPSBkMy5TZWxlY3Rpb248XG4gIEUsXG4gIFQsXG4gIG51bGwsXG4gIHVuZGVmaW5lZFxuPjtcblxudHlwZSBUb29sdGlwUHJvcHM8VCwgRSBleHRlbmRzIGQzLkJhc2VUeXBlID0gSFRNTERpdkVsZW1lbnQ+ID0ge1xuICByb290OiBTZWxlY3Rpb248VCwgRT47XG4gIHJlaWZ5OiBTbmFwc2hvdFJlaWZpZXI7XG59O1xuXG5mdW5jdGlvbiB0b29sdGlwSGVhZGVyPFQ+KFxuICByb290OiBUb29sdGlwUHJvcHM8VD5bJ3Jvb3QnXSxcbiAgdGV4dDogc3RyaW5nIHwgZDMuVmFsdWVGbjxIVE1MRWxlbWVudCwgVCwgc3RyaW5nPixcbikge1xuICByb290LmFwcGVuZCgnc3Ryb25nJykudGV4dCh0ZXh0KS5zdHlsZSgnZm9udC1zaXplJywgJzAuOXJlbScpO1xuICByb290XG4gICAgLmFwcGVuZCgnaHInKVxuICAgIC5zdHlsZSgnbWFyZ2luJywgJzNweCAwJylcbiAgICAuc3R5bGUoJ2JvcmRlcicsIDApXG4gICAgLnN0eWxlKCdib3JkZXItdG9wJywgJzFweCBzb2xpZCAjZDNkM2QzJyk7XG59XG5cbmZ1bmN0aW9uIGF0dHJpYnV0ZXM8VD4oXG4gIHJvb3Q6IFRvb2x0aXBQcm9wczxUPlsncm9vdCddLFxuICBpdGVtczogW1xuICAgIHN0cmluZyB8IGQzLlZhbHVlRm48SFRNTEVsZW1lbnQsIFQsIHN0cmluZyB8IG51bWJlciB8IGJvb2xlYW4+LFxuICAgIHN0cmluZyB8IGQzLlZhbHVlRm48SFRNTEVsZW1lbnQsIFQsIHN0cmluZyB8IG51bWJlciB8IGJvb2xlYW4+LFxuICBdW10sXG4pIHtcbiAgY29uc3QgY29udGFpbmVyID0gcm9vdFxuICAgIC5hcHBlbmQoJ2RpdicpXG4gICAgLnN0eWxlKCdkaXNwbGF5JywgJ2dyaWQnKVxuICAgIC5zdHlsZSgnZ2FwJywgJy4zcmVtJylcbiAgICAuc3R5bGUoJ21pbi13aWR0aCcsICcwJylcbiAgICAuc3R5bGUoJ2dyaWQtdGVtcGxhdGUtY29sdW1ucycsICcyZnIgOGZyJylcbiAgICAuc3R5bGUoJ2dyaWQtYXV0by1mbG93JywgJ3JvdycpXG4gICAgLnN0eWxlKCdhbGlnbi1pdGVtcycsICdiYXNlbGluZScpO1xuICBpdGVtcy5mb3JFYWNoKChbbmFtZSwgdmFsdWVdKSA9PiB7XG4gICAgY29udGFpbmVyLmFwcGVuZCgnc3BhbicpLnRleHQobmFtZSk7XG4gICAgY29udGFpbmVyXG4gICAgICAuYXBwZW5kKCdjb2RlJylcbiAgICAgIC5zdHlsZSgnZm9udC13ZWlnaHQnLCA3MDApXG4gICAgICAuc3R5bGUoJ3dvcmQtYnJlYWsnLCAnYnJlYWstYWxsJylcbiAgICAgIC5zdHlsZSgnYmFja2dyb3VuZCcsICdub25lJylcbiAgICAgIC50ZXh0KHZhbHVlKTtcbiAgfSk7XG59XG5cbmZ1bmN0aW9uIGNvZGVCbG9jazxUPihcbiAgcm9vdDogVG9vbHRpcFByb3BzPFQ+Wydyb290J10sXG4gIHZhbHVlOiBzdHJpbmcgfCBkMy5WYWx1ZUZuPEhUTUxFbGVtZW50LCBULCBzdHJpbmcgfCBudW1iZXIgfCBib29sZWFuPixcbikge1xuICByb290XG4gICAgLmFwcGVuZCgnZGl2JylcbiAgICAuc3R5bGUoJ2JhY2tncm91bmQnLCAnI2Y1ZjVmNScpXG4gICAgLnN0eWxlKCdtYXJnaW4nLCAnNnB4IDAgMCcpXG4gICAgLnN0eWxlKCdtYXgtaGVpZ2h0JywgJzEwdmgnKVxuICAgIC5zdHlsZSgnb3ZlcmZsb3cnLCAnYXV0bycpXG4gICAgLnN0eWxlKCdwYWRkaW5nJywgJzZweCcpXG4gICAgLmFwcGVuZCgncHJlJylcbiAgICAuc3R5bGUoJ2JhY2tncm91bmQnLCAnbm9uZScpXG4gICAgLnN0eWxlKCdvdmVyZmxvdycsICdhdXRvJylcbiAgICAuc3R5bGUoJ3doaXRlLXNwYWNlJywgJ3ByZScpXG4gICAgLnN0eWxlKCd3b3JkLWJyZWFrJywgJ2JyZWFrLWFsbCcpXG4gICAgLnRleHQodmFsdWUpO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVtb3RlT2JqZWN0VG9vbHRpcCh7IHJvb3QgfTogVG9vbHRpcFByb3BzPFJlbW90ZU9iamVjdE5vZGU+KSB7XG4gIHRvb2x0aXBIZWFkZXIocm9vdCwgKGQpID0+IGBSZW1vdGUgb2JqZWN0ICMke2QuZGF0YS5udW1iZXJpbmcgfHwgJ251bWJlcmluZyA/J31gKTtcbiAgYXR0cmlidXRlcyhyb290LCBbXG4gICAgWydEZXZpY2UnLCAoZCkgPT4gZC5kYXRhLmxvY2F0aW9uLnR5cGVdLFxuICAgIFtcbiAgICAgIChkKSA9PiAoZC5kYXRhLmxvY2F0aW9uLnBhcnRpZXMubGVuZ3RoID4gMSA/ICdQYXJ0aWVzJyA6ICdQYXJ0eScpLFxuICAgICAgKGQpID0+IGQuZGF0YS5sb2NhdGlvbi5wYXJ0aWVzLmpvaW4oJywgJyksXG4gICAgXSxcbiAgXSk7XG4gIGNvbnN0IHBhcmFtcyA9IHJvb3QuZGF0dW0oKS5kYXRhLmxvY2F0aW9uLnBhcmFtZXRlcnMgfHwge307XG4gIGlmIChPYmplY3Qua2V5cyhwYXJhbXMpLmxlbmd0aCA+IDApIHtcbiAgICBjb2RlQmxvY2socm9vdCwgKCkgPT4gWUFNTC5zdHJpbmdpZnkoeyBwcm9wZXJ0aWVzOiBwYXJhbXMgfSwgeyBpbmRlbnQ6IDIgfSkpO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2NhbE9iamVjdFRvb2x0aXAoeyByb290LCByZWlmeSB9OiBUb29sdGlwUHJvcHM8TG9jYWxPYmplY3ROb2RlPikge1xuICB0b29sdGlwSGVhZGVyKHJvb3QsICdMb2NhbCB2YWx1ZScpO1xuXG4gIGNvbnN0IHZhbHVlID0gcmVpZnkodW5kZWZpbmVkLCByb290LmRhdHVtKCkuZGF0YSk7XG4gIGNvbnN0IG5vZGUgPSByb290LmRhdHVtKCk7XG5cbiAgc3dpdGNoICh2YWx1ZT8ua2luZCkge1xuICAgIGNhc2UgJ29iamVjdCc6XG4gICAgY2FzZSAnbGlzdCc6XG4gICAgY2FzZSAnZGljdCc6XG4gICAgICBhdHRyaWJ1dGVzKHJvb3QuZGF0dW0odmFsdWUpLCBbXG4gICAgICAgIFsnTmFtZScsIG5vZGUuZGF0YS5uYW1lIHx8ICc/J10sXG4gICAgICAgIFsnVHlwZScsIChkKSA9PiB3cmFwKGQudHlwZSwgJy4nLCAzMCldLFxuICAgICAgXSk7XG4gICAgICBjb2RlQmxvY2socm9vdC5kYXR1bSh2YWx1ZSksIChkKSA9PiBkLnNuYXBzaG90KTtcbiAgICAgIGJyZWFrO1xuICAgIGNhc2UgJ25vbmUnOlxuICAgICAgYXR0cmlidXRlcyhyb290LmRhdHVtKHZhbHVlKSwgW1xuICAgICAgICBbJ05hbWUnLCBub2RlLmRhdGEubmFtZSB8fCAnPyddLFxuICAgICAgICBbJ1ZhbHVlJywgJ05vbmUnXSxcbiAgICAgIF0pO1xuICAgICAgYnJlYWs7XG4gICAgY2FzZSAnZnVuY3Rpb24nOlxuICAgICAgYXR0cmlidXRlcyhyb290LmRhdHVtKHZhbHVlKSwgW1xuICAgICAgICBbJ0Z1bmN0aW9uJywgKGQpID0+IHdyYXAoZC5uYW1lLCAnLicsIDMyKV0sXG4gICAgICAgIFsnTW9kdWxlJywgKGQpID0+IHdyYXAoZC5tb2R1bGUgfHwgJz8nLCAnLicsIDMyKV0sXG4gICAgICAgIFsnRmlsZScsIChkKSA9PiB3cmFwKGQuZmlsZW5hbWUgfHwgJz8nLCAnLycsIDMyKV0sXG4gICAgICAgIFsnTGluZScsIChkKSA9PiBkLmZpcnN0bGluZW5vIHx8ICc/J10sXG4gICAgICBdKTtcbiAgICAgIGNvZGVCbG9jayhyb290LmRhdHVtKHZhbHVlKSwgKGQpID0+IGQuc291cmNlIHx8ICcobm8gc291cmNlKScpO1xuICAgICAgYnJlYWs7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGZ1bmN0aW9uVG9vbHRpcCh7IHJvb3QsIHJlaWZ5IH06IFRvb2x0aXBQcm9wczxGdW5jdGlvbk5vZGU+KSB7XG4gIHRvb2x0aXBIZWFkZXIocm9vdCwgJ0NvZGUgZXhlY3V0aW9uJyk7XG5cbiAgYXR0cmlidXRlcyhyb290LCBbXG4gICAgWydEZXZpY2UnLCAoZCkgPT4gYCR7ZC5sb2NhdGlvbi50eXBlfVske2QubG9jYXRpb24ucGFydGllcy5qb2luKCcsICcpfV1gXSxcbiAgICBbJ0ZyYW1lICMnLCAoZCkgPT4gZC5lcG9jaF0sXG4gIF0pO1xuXG4gIGNvbnN0IGZ1bmMgPSByZWlmeSgnZnVuY3Rpb24nLCByb290LmRhdHVtKCkuZnVuY3Rpb24pO1xuXG4gIGlmICghZnVuYykge1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGF0dHJpYnV0ZXMocm9vdC5kYXR1bShmdW5jKSwgW1xuICAgIFsnRnVuY3Rpb24nLCAoZCkgPT4gd3JhcChkLm5hbWUsICcuJywgMzIpXSxcbiAgICBbJ01vZHVsZScsIChkKSA9PiB3cmFwKGQubW9kdWxlIHx8ICc/JywgJy4nLCAzMildLFxuICAgIFtcbiAgICAgICdGaWxlJyxcbiAgICAgIChkKSA9PiBgJHt3cmFwKGQuZmlsZW5hbWUgfHwgJz8nLCAnLycsIDMyKX0sIGxpbmUgJHtkLmZpcnN0bGluZW5vIHx8ICc/J31gLFxuICAgIF0sXG4gIF0pO1xuXG4gIGNvZGVCbG9jayhyb290LmRhdHVtKGZ1bmMpLCAoZCkgPT4gZC5zb3VyY2UgfHwgJyhubyBzb3VyY2UsIGxpa2VseSBhIEMgZnVuY3Rpb24pJyk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB0b29sdGlwKG1vZGVsOiBHNi5Nb2RlbENvbmZpZywgcmVpZnk6IFNuYXBzaG90UmVpZmllcik6IHN0cmluZyB7XG4gIGlmICghaXNUcnVzdGVkKG1vZGVsKSkge1xuICAgIHJldHVybiAnJztcbiAgfVxuICBjb25zdCBkaXYgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgY29uc3Qgcm9vdCA9IGQzLnNlbGVjdChkaXYpO1xuICBjb25zdCB7IGRhdGEgfSA9IG1vZGVsO1xuICBzd2l0Y2ggKGRhdGEua2luZCkge1xuICAgIGNhc2UgJ3JlbW90ZSc6XG4gICAgICByZW1vdGVPYmplY3RUb29sdGlwKHsgcm9vdDogcm9vdC5kYXR1bShkYXRhKSwgcmVpZnkgfSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlICdsb2NhbCc6XG4gICAgICBsb2NhbE9iamVjdFRvb2x0aXAoeyByb290OiByb290LmRhdHVtKGRhdGEpLCByZWlmeSB9KTtcbiAgICAgIGJyZWFrO1xuICAgIGNhc2UgJ2Z1bmN0aW9uJzpcbiAgICAgIGZ1bmN0aW9uVG9vbHRpcCh7IHJvb3Q6IHJvb3QuZGF0dW0oZGF0YSksIHJlaWZ5IH0pO1xuICAgICAgYnJlYWs7XG4gICAgZGVmYXVsdDpcbiAgICAgIGJyZWFrO1xuICB9XG4gIHJvb3RcbiAgICAuc3R5bGUoJ2JveC1zaXppbmcnLCAnYm9yZGVyLWJveCcpXG4gICAgLnN0eWxlKCdwYWRkaW5nJywgJzEwcHgnKVxuICAgIC5zdHlsZSgnbWFyZ2luJywgJzAnKVxuICAgIC5zdHlsZSgnZGlzcGxheScsICdmbGV4JylcbiAgICAuc3R5bGUoJ2ZsZXgtZGlyZWN0aW9uJywgJ2NvbHVtbicpXG4gICAgLnN0eWxlKCdhbGlnbi1pdGVtcycsICdzdHJldGNoJylcbiAgICAuc3R5bGUoJ2dhcCcsICcuM3JlbScpXG4gICAgLnN0eWxlKCdmb250LXNpemUnLCAnMC44cmVtJylcbiAgICAuc3R5bGUoJ2NvbG9yJywgJyMzMzMnKVxuICAgIC5zdHlsZSgnYm9yZGVyLXJhZGl1cycsICc0cHgnKVxuICAgIC5zdHlsZSgnYmFja2dyb3VuZC1jb2xvcicsICcjZmZmJylcbiAgICAuc3R5bGUoJ21pbi13aWR0aCcsICcyMDBweCcpXG4gICAgLnN0eWxlKCdtYXgtd2lkdGgnLCAnMjV2dycpXG4gICAgLnN0eWxlKFxuICAgICAgJ2JveC1zaGFkb3cnLFxuICAgICAgJzBweCAxcHggMnB4IC0ycHggcmdiYSgwLDAsMCwwLjA4KSwgMHB4IDNweCA2cHggMHB4IHJnYmEoMCwwLDAsMC4wNiksIDBweCA1cHggMTJweCA0cHggcmdiYSgwLDAsMCwwLjAzKScsXG4gICAgKTtcbiAgaWYgKGRpdi5jaGlsZE5vZGVzLmxlbmd0aCA9PT0gMCkge1xuICAgIHJldHVybiAnJztcbiAgfVxuICByZXR1cm4gZGl2Lm91dGVySFRNTDtcbn1cbiIsImltcG9ydCAqIGFzIEc2IGZyb20gJ0BhbnR2L2c2JztcbmltcG9ydCB7IENhcmQsIENvbmZpZ1Byb3ZpZGVyLCBEaXZpZGVyLCBGb3JtLCBTd2l0Y2ggfSBmcm9tICdhbnRkJztcbmltcG9ydCB0eXBlIHsgTW91c2VFdmVudEhhbmRsZXIsIE11dGFibGVSZWZPYmplY3QgfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBGcmFnbWVudCwgdXNlQ2FsbGJhY2ssIHVzZUVmZmVjdCwgdXNlTWVtbywgdXNlUmVmLCB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0JztcblxuaW1wb3J0IHR5cGUgeyBHcmFwaCBhcyBHcmFwaFByb3BzLCBMb2dpY2FsTG9jYXRpb24gfSBmcm9tICcuLi8uLi8ub3BlbmFwaS1zdHVicyc7XG5pbXBvcnQgeyB1c2VEYXRhUHJvdmlkZXIgfSBmcm9tICcuLi9EYXRhUHJvdmlkZXIvdXRpbHMnO1xuXG5pbXBvcnQgdHlwZSB7IENvbG9yaXplciB9IGZyb20gJy4vY29sb3JpemF0aW9uJztcbmltcG9ydCB7IGNvbG9yaXplQnlMb2NhdGlvbiwgcmVjb2xvck9uSG92ZXIsIHVzZUNvbG9yaXplciB9IGZyb20gJy4vY29sb3JpemF0aW9uJztcbmltcG9ydCB7IExvY2F0aW9uQ29sb3JpemVyIH0gZnJvbSAnLi9jb2xvcml6YXRpb24nO1xuaW1wb3J0IHsgc2V0dXBHNiB9IGZyb20gJy4vc2hhcGVzJztcbmltcG9ydCB7IHRvb2x0aXAgfSBmcm9tICcuL3Rvb2x0aXAnO1xuaW1wb3J0IHsgaXNUcnVzdGVkLCB0eXBlIEdyYXBoTm9kZVR5cGUgfSBmcm9tICcuL3R5cGVzJztcbmltcG9ydCB7IHBhcnRpdGlvbkJ5RW50aXR5VHlwZSwgcGFydGl0aW9uQnlMb2NhdGlvbiB9IGZyb20gJy4vdXRpbHMnO1xuXG50eXBlIEdyYXBoUmVmID0gTXV0YWJsZVJlZk9iamVjdDxHNi5HcmFwaCB8IHVuZGVmaW5lZD47XG5cbmNvbnN0IHsgZnJvbUdyYXBoIH0gPSBzZXR1cEc2KCk7XG5cbmNvbnN0IGRlZmF1bHRDb2xvcml6ZXIgPSAoKSA9PlxuICBuZXcgTG9jYXRpb25Db2xvcml6ZXIoW1xuICAgICcjNzlhMjVjJyxcbiAgICAnI2RlNGM4YicsXG4gICAgJyM4MjcxZGYnLFxuICAgICcjMzM5OGE2JyxcbiAgICAnI2M0N2QzYScsXG4gICAgJyNiNDVkY2InLFxuICAgICcjNGM5OWQ4JyxcbiAgICAnI2RmNmE3MicsXG4gIF0pO1xuXG5mdW5jdGlvbiBMZWdlbmQoe1xuICBncmFwaCxcbiAgY29sb3JpemVyLFxufToge1xuICBncmFwaDogR3JhcGhSZWY7XG4gIGNvbG9yaXplcjogQ29sb3JpemVyPExvZ2ljYWxMb2NhdGlvbj47XG59KSB7XG4gIGNvbnN0IGxvY2F0aW9uQ29sb3JpemVyID0gdXNlTWVtbyhcbiAgICAoKSA9PlxuICAgICAgcmVjb2xvck9uSG92ZXIoe1xuICAgICAgICBwYXJ0aXRpb246IHBhcnRpdGlvbkJ5TG9jYXRpb24sXG4gICAgICAgIGNvbG9yaXplOiBjb2xvcml6ZUJ5TG9jYXRpb24oY29sb3JpemVyLmNvbG9yaXplKSxcbiAgICAgIH0pLFxuICAgIFtjb2xvcml6ZXIuY29sb3JpemVdLFxuICApO1xuXG4gIGNvbnN0IHJlc2V0Q29sb3JzID0gdXNlQ2FsbGJhY2s8TW91c2VFdmVudEhhbmRsZXI+KCgpID0+IHtcbiAgICBpZiAoIWdyYXBoLmN1cnJlbnQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgbG9jYXRpb25Db2xvcml6ZXIoZ3JhcGguY3VycmVudCkuaGlnaGxpZ2h0KG51bGwpO1xuICB9LCBbZ3JhcGgsIGxvY2F0aW9uQ29sb3JpemVyXSk7XG5cbiAgY29uc3QgaGlnaGxpZ2h0ID0gdXNlQ2FsbGJhY2soXG4gICAgKGxvY2F0aW9uS2V5OiBzdHJpbmcpOiBNb3VzZUV2ZW50SGFuZGxlciA9PlxuICAgICAgKCkgPT4ge1xuICAgICAgICBpZiAoIWdyYXBoLmN1cnJlbnQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZ3JhcGguY3VycmVudC5nZXROb2RlcygpLmZpbmQoKHYpID0+IHtcbiAgICAgICAgICBjb25zdCBtb2RlbCA9IHYuZ2V0TW9kZWwoKTtcbiAgICAgICAgICBpZiAoIWlzVHJ1c3RlZDxHcmFwaE5vZGVUeXBlPihtb2RlbCkpIHtcbiAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgICB9XG4gICAgICAgICAgc3dpdGNoIChtb2RlbC5kYXRhLmtpbmQpIHtcbiAgICAgICAgICAgIGNhc2UgJ2Z1bmN0aW9uJzpcbiAgICAgICAgICAgICAgcmV0dXJuIExvY2F0aW9uQ29sb3JpemVyLmxvY2F0aW9uS2V5KG1vZGVsLmRhdGEubG9jYXRpb24pID09PSBsb2NhdGlvbktleTtcbiAgICAgICAgICAgIGNhc2UgJ3JlbW90ZSc6XG4gICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgTG9jYXRpb25Db2xvcml6ZXIubG9jYXRpb25LZXkobW9kZWwuZGF0YS5kYXRhLmxvY2F0aW9uKSA9PT0gbG9jYXRpb25LZXlcbiAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgICBpZiAodGFyZ2V0KSB7XG4gICAgICAgICAgbG9jYXRpb25Db2xvcml6ZXIoZ3JhcGguY3VycmVudCkuaGlnaGxpZ2h0KHRhcmdldC5nZXRJRCgpKTtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICBbZ3JhcGgsIGxvY2F0aW9uQ29sb3JpemVyXSxcbiAgKTtcblxuICBjb25zdCBbaG92ZXJlZCwgc2V0SG92ZXJlZF0gPSB1c2VTdGF0ZTxzdHJpbmc+KCk7XG5cbiAgcmV0dXJuIChcbiAgICA8ZGl2XG4gICAgICBzdHlsZT17e1xuICAgICAgICBkaXNwbGF5OiAnZ3JpZCcsXG4gICAgICAgIGdyaWRUZW1wbGF0ZUNvbHVtbnM6ICcyMHB4IDFmcicsXG4gICAgICAgIGdyaWRBdXRvUm93czogJzIwcHgnLFxuICAgICAgICBhbGlnbkl0ZW1zOiAnY2VudGVyJyxcbiAgICAgICAgZ2FwOiAnMC4zcmVtJyxcbiAgICAgIH19XG4gICAgICBvbk1vdXNlTGVhdmU9eyhlKSA9PiB7XG4gICAgICAgIHNldEhvdmVyZWQodW5kZWZpbmVkKTtcbiAgICAgICAgcmVzZXRDb2xvcnMoZSk7XG4gICAgICB9fVxuICAgID5cbiAgICAgIHtbLi4uY29sb3JpemVyLmNvbG9ycygpXS5tYXAoKFtrZXksIHsgbmFtZSwgY29sb3IgfV0pID0+IChcbiAgICAgICAgPEZyYWdtZW50IGtleT17a2V5fT5cbiAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICBzdHlsZT17eyB3aWR0aDogMTYsIGhlaWdodDogMTYsIG1hcmdpbjogMiwgYmFja2dyb3VuZENvbG9yOiBjb2xvciB9fVxuICAgICAgICAgICAgb25Nb3VzZUVudGVyPXsoZSkgPT4ge1xuICAgICAgICAgICAgICBoaWdobGlnaHQoa2V5KShlKTtcbiAgICAgICAgICAgICAgc2V0SG92ZXJlZChrZXkpO1xuICAgICAgICAgICAgfX1cbiAgICAgICAgICAvPlxuICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgIG9uTW91c2VFbnRlcj17KGUpID0+IHtcbiAgICAgICAgICAgICAgaGlnaGxpZ2h0KGtleSkoZSk7XG4gICAgICAgICAgICAgIHNldEhvdmVyZWQoa2V5KTtcbiAgICAgICAgICAgIH19XG4gICAgICAgICAgPlxuICAgICAgICAgICAgPHNwYW5cbiAgICAgICAgICAgICAgc3R5bGU9e3tcbiAgICAgICAgICAgICAgICBmb250RmFtaWx5OiAnSW50ZXIsIHNhbnMtc2VyaWYnLFxuICAgICAgICAgICAgICAgIGZvbnRXZWlnaHQ6IGhvdmVyZWQgPT09IGtleSA/IDcwMCA6IDQwMCxcbiAgICAgICAgICAgICAgICBwb2ludGVyRXZlbnRzOiAnbm9uZScsXG4gICAgICAgICAgICAgIH19XG4gICAgICAgICAgICA+XG4gICAgICAgICAgICAgIHtuYW1lfVxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L0ZyYWdtZW50PlxuICAgICAgKSl9XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbmZ1bmN0aW9uIHVzZUV4ZWN1dGlvbkdyYXBoKCkge1xuICBjb25zdCB7IHJlaWZ5IH0gPSB1c2VEYXRhUHJvdmlkZXIoKTtcblxuICBjb25zdCBjb2xvcml6ZXIgPSB1c2VDb2xvcml6ZXIoZGVmYXVsdENvbG9yaXplcik7XG5cbiAgY29uc3QgZW50aXR5Q29sb3JpemVyID0gdXNlTWVtbyhcbiAgICAoKSA9PlxuICAgICAgcmVjb2xvck9uSG92ZXIoe1xuICAgICAgICBwYXJ0aXRpb246IHBhcnRpdGlvbkJ5RW50aXR5VHlwZSxcbiAgICAgICAgY29sb3JpemU6IGNvbG9yaXplQnlMb2NhdGlvbihjb2xvcml6ZXIuY29sb3JpemUpLFxuICAgICAgfSksXG4gICAgW2NvbG9yaXplci5jb2xvcml6ZV0sXG4gICk7XG5cbiAgY29uc3QgY29udGFpbmVyUmVmID0gdXNlUmVmPEhUTUxEaXZFbGVtZW50PihudWxsKTtcbiAgY29uc3QgZ3JhcGhSZWYgPSB1c2VSZWY8RzYuR3JhcGg+KCk7XG4gIGNvbnN0IHRvb2x0aXBFbmFibGVkUmVmID0gdXNlUmVmKHRydWUpO1xuXG4gIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgaWYgKCFjb250YWluZXJSZWYuY3VycmVudCkge1xuICAgICAgZ3JhcGhSZWYuY3VycmVudCA9IHVuZGVmaW5lZDtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBncmFwaCA9IG5ldyBHNi5HcmFwaCh7XG4gICAgICBjb250YWluZXI6IGNvbnRhaW5lclJlZi5jdXJyZW50LFxuICAgICAgd2lkdGg6IGNvbnRhaW5lclJlZi5jdXJyZW50LmNsaWVudFdpZHRoLFxuICAgICAgaGVpZ2h0OiBjb250YWluZXJSZWYuY3VycmVudC5jbGllbnRIZWlnaHQsXG4gICAgICBsYXlvdXQ6IHtcbiAgICAgICAgdHlwZTogJ2RhZ3JlJyxcbiAgICAgICAgcmFua3NlcEZ1bmM6IChub2RlOiB7IGRhdGE6IEdyYXBoTm9kZVR5cGUgfSkgPT4ge1xuICAgICAgICAgIGlmIChub2RlLmRhdGE/LmtpbmQgPT09ICdyZXZlYWwnIHx8IG5vZGUuZGF0YT8ua2luZCA9PT0gJ3JlbW90ZScpIHtcbiAgICAgICAgICAgIHJldHVybiAyLjU7XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChub2RlLmRhdGE/LmtpbmQgPT09ICdsb2NhbCcpIHtcbiAgICAgICAgICAgIHJldHVybiA1O1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gMTA7XG4gICAgICAgIH0sXG4gICAgICAgIG5vZGVzZXA6IDEwLFxuICAgICAgfSxcbiAgICAgIG1vZGVzOiB7XG4gICAgICAgIGRlZmF1bHQ6IFtcbiAgICAgICAgICB7IHR5cGU6ICdzY3JvbGwtY2FudmFzJyB9LFxuICAgICAgICAgIHsgdHlwZTogJ2RyYWctY2FudmFzJyB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHR5cGU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGZvcm1hdFRleHQ6IChtb2RlbCkgPT4ge1xuICAgICAgICAgICAgICBpZiAoIXRvb2x0aXBFbmFibGVkUmVmLmN1cnJlbnQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgcmV0dXJuIHRvb2x0aXAobW9kZWwsIHJlaWZ5KTtcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBvZmZzZXQ6IDEwLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICAgIGhpZ2hsaWdodGluZzogW10sXG4gICAgICB9LFxuICAgICAgbWluWm9vbTogMC4yLFxuICAgICAgbWF4Wm9vbTogMyxcbiAgICB9KTtcblxuICAgIGdyYXBoLm9uKCdub2RlOmNsaWNrJywgKHsgaXRlbSB9KSA9PiB7XG4gICAgICBpZiAoaXRlbSkge1xuICAgICAgICBncmFwaC5mb2N1c0l0ZW0oaXRlbSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBlbnRpdHlDb2xvcml6ZXIoZ3JhcGgpLmVuYWJsZSgpO1xuXG4gICAgZ3JhcGhSZWYuY3VycmVudCA9IGdyYXBoO1xuXG4gICAgcmV0dXJuICgpID0+IHtcbiAgICAgIGdyYXBoLmRlc3Ryb3koKTtcbiAgICB9O1xuICB9LCBbZW50aXR5Q29sb3JpemVyLCByZWlmeV0pO1xuXG4gIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgY29uc3Qgb3V0cHV0VmlldyA9IGNvbnRhaW5lclJlZi5jdXJyZW50Py5jbG9zZXN0KCcuanAtTGlua2VkT3V0cHV0VmlldycpO1xuICAgIGNvbnN0IHJlc2l6ZU9ic2VydmVyID0gbmV3IFJlc2l6ZU9ic2VydmVyKCgpID0+IHtcbiAgICAgIGlmICghY29udGFpbmVyUmVmLmN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgW2hlaWdodCwgY3NzSGVpZ2h0XSA9ICgoKSA9PiB7XG4gICAgICAgIGlmIChvdXRwdXRWaWV3ICYmIG91dHB1dFZpZXcuY2xpZW50SGVpZ2h0ICE9PSAwKSB7XG4gICAgICAgICAgcmV0dXJuIFtvdXRwdXRWaWV3LmNsaWVudEhlaWdodCwgYCR7b3V0cHV0Vmlldy5jbGllbnRIZWlnaHR9cHhgXTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gW1xuICAgICAgICAgIGNvbnRhaW5lclJlZi5jdXJyZW50LmNsaWVudEhlaWdodCxcbiAgICAgICAgICBgJHtjb250YWluZXJSZWYuY3VycmVudC5jbGllbnRIZWlnaHR9cHhgLFxuICAgICAgICBdO1xuICAgICAgfSkoKTtcbiAgICAgIGNvbnRhaW5lclJlZi5jdXJyZW50LnN0eWxlLmhlaWdodCA9IGNzc0hlaWdodDtcbiAgICAgIGdyYXBoUmVmLmN1cnJlbnQ/LmNoYW5nZVNpemUoY29udGFpbmVyUmVmLmN1cnJlbnQuY2xpZW50V2lkdGgsIGhlaWdodCk7XG4gICAgfSk7XG4gICAgaWYgKGNvbnRhaW5lclJlZi5jdXJyZW50KSB7XG4gICAgICByZXNpemVPYnNlcnZlci5vYnNlcnZlKGNvbnRhaW5lclJlZi5jdXJyZW50KTtcbiAgICB9XG4gICAgaWYgKG91dHB1dFZpZXcpIHtcbiAgICAgIHJlc2l6ZU9ic2VydmVyLm9ic2VydmUob3V0cHV0Vmlldyk7XG4gICAgfVxuICAgIHJldHVybiAoKSA9PiB7XG4gICAgICByZXNpemVPYnNlcnZlci5kaXNjb25uZWN0KCk7XG4gICAgfTtcbiAgfSwgW10pO1xuXG4gIHJldHVybiB7XG4gICAgY29udGFpbmVyOiBjb250YWluZXJSZWYsXG4gICAgZ3JhcGg6IGdyYXBoUmVmLFxuICAgIGNvbG9yaXplcixcbiAgICB0b29sdGlwRW5hYmxlZDogdG9vbHRpcEVuYWJsZWRSZWYsXG4gICAgbG9hZDogKGRhdGE6IEdyYXBoUHJvcHMpID0+IHtcbiAgICAgIGdyYXBoUmVmLmN1cnJlbnQ/LmRhdGEoZnJvbUdyYXBoKGRhdGEsIHsgcmVpZnksIGNvbG9yaXplOiBjb2xvcml6ZXIuY29sb3JpemUgfSkpO1xuICAgICAgZ3JhcGhSZWYuY3VycmVudD8ucmVuZGVyKCk7XG4gICAgfSxcbiAgfTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIEV4ZWN1dGlvbkdyYXBoKGRhdGE6IEdyYXBoUHJvcHMpIHtcbiAgY29uc3QgeyBjb250YWluZXIsIGxvYWQsIGdyYXBoLCBjb2xvcml6ZXIsIHRvb2x0aXBFbmFibGVkIH0gPSB1c2VFeGVjdXRpb25HcmFwaCgpO1xuXG4gIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgbG9hZChkYXRhKTtcbiAgfSwgW2RhdGEsIGxvYWRdKTtcblxuICByZXR1cm4gKFxuICAgIDxkaXYgc3R5bGU9e3sgcG9zaXRpb246ICdyZWxhdGl2ZScgfX0+XG4gICAgICA8ZGl2XG4gICAgICAgIHN0eWxlPXt7IHdpZHRoOiAnMTAwJScsIGhlaWdodDogJzgwdmgnLCBtaW5IZWlnaHQ6ICc2MDBweCcgfX1cbiAgICAgICAgcmVmPXtjb250YWluZXJ9XG4gICAgICAvPlxuICAgICAgPGRpdiBzdHlsZT17eyBwb3NpdGlvbjogJ2Fic29sdXRlJywgdG9wOiAnMXJlbScsIHJpZ2h0OiAnMXJlbScgfX0+XG4gICAgICAgIDxDYXJkIHNpemU9XCJzbWFsbFwiIHN0eWxlPXt7IGZvbnRTaXplOiAnLjhyZW0nIH19PlxuICAgICAgICAgIDxDb25maWdQcm92aWRlciB0aGVtZT17eyB0b2tlbjogeyBtYXJnaW5MRzogOCB9IH19PlxuICAgICAgICAgICAgPHNwYW5cbiAgICAgICAgICAgICAgc3R5bGU9e3tcbiAgICAgICAgICAgICAgICBmb250V2VpZ2h0OiA3MDAsXG4gICAgICAgICAgICAgICAgYmFja2dyb3VuZENvbG9yOiAnI2YwNDY1NCcsXG4gICAgICAgICAgICAgICAgY29sb3I6ICcjZmZmZmZmJyxcbiAgICAgICAgICAgICAgICBkaXNwbGF5OiAnaW5saW5lLWJsb2NrJyxcbiAgICAgICAgICAgICAgICBwYWRkaW5nOiAnMC4ycmVtIDAuNXJlbScsXG4gICAgICAgICAgICAgICAgYm9yZGVyUmFkaXVzOiAnMC4ycmVtJyxcbiAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgREVWRUxPUEVSIFBSRVZJRVdcbiAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICAgIDxEaXZpZGVyIC8+XG4gICAgICAgICAgPC9Db25maWdQcm92aWRlcj5cbiAgICAgICAgICA8TGVnZW5kIGdyYXBoPXtncmFwaH0gY29sb3JpemVyPXtjb2xvcml6ZXJ9IC8+XG4gICAgICAgICAgPENvbmZpZ1Byb3ZpZGVyIHRoZW1lPXt7IHRva2VuOiB7IG1hcmdpbkxHOiA4IH0gfX0+XG4gICAgICAgICAgICA8RGl2aWRlciAvPlxuICAgICAgICAgIDwvQ29uZmlnUHJvdmlkZXI+XG4gICAgICAgICAgPEZvcm0uSXRlbVxuICAgICAgICAgICAgbmFtZT1cInRvb2x0aXBFbmFibGVkXCJcbiAgICAgICAgICAgIGxhYmVsPVwiVG9vbHRpcFwiXG4gICAgICAgICAgICBzdHlsZT17e1xuICAgICAgICAgICAgICBtYXJnaW46IDAsXG4gICAgICAgICAgICAgIGhlaWdodDogMjAsXG4gICAgICAgICAgICAgIGRpc3BsYXk6ICdmbGV4JyxcbiAgICAgICAgICAgICAgYWxpZ25JdGVtczogJ2NlbnRlcicsXG4gICAgICAgICAgICAgIGZvbnRTaXplOiAnLjhyZW0nLFxuICAgICAgICAgICAgfX1cbiAgICAgICAgICAgIGNvbG9uPXtmYWxzZX1cbiAgICAgICAgICA+XG4gICAgICAgICAgICA8U3dpdGNoXG4gICAgICAgICAgICAgIHNpemU9XCJzbWFsbFwiXG4gICAgICAgICAgICAgIGRlZmF1bHRDaGVja2VkPXt0b29sdGlwRW5hYmxlZC5jdXJyZW50fVxuICAgICAgICAgICAgICBvbkNoYW5nZT17KGNoZWNrZWQpID0+IHtcbiAgICAgICAgICAgICAgICB0b29sdGlwRW5hYmxlZC5jdXJyZW50ID0gY2hlY2tlZDtcbiAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgPC9Gb3JtLkl0ZW0+XG4gICAgICAgIDwvQ2FyZD5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICApO1xufVxuIiwiaW1wb3J0IHsgQWxlcnQgfSBmcm9tICdhbnRkJztcblxuaW1wb3J0IHR5cGUgeyBWaXN1YWxpemF0aW9uIGFzIFZpc3VhbGl6YXRpb25Qcm9wcyB9IGZyb20gJy4uLy5vcGVuYXBpLXN0dWJzJztcblxuaW1wb3J0IHsgRGF0YVByb3ZpZGVyIH0gZnJvbSAnLi9EYXRhUHJvdmlkZXInO1xuaW1wb3J0IHsgRXhlY3V0aW9uR3JhcGggfSBmcm9tICcuL0V4ZWN1dGlvbkdyYXBoJztcblxuZXhwb3J0IGZ1bmN0aW9uIFZpc3VhbGl6YXRpb24oeyB0aW1lbGluZSB9OiBWaXN1YWxpemF0aW9uUHJvcHMpIHtcbiAgcmV0dXJuIChcbiAgICA8QWxlcnQuRXJyb3JCb3VuZGFyeSBtZXNzYWdlPXs8c3Ryb25nPkV4Y2VwdGlvbiBpbiBjZWxsIG91dHB1dDo8L3N0cm9uZz59PlxuICAgICAgPERhdGFQcm92aWRlciB0aW1lbGluZT17dGltZWxpbmV9PlxuICAgICAgICA8RXhlY3V0aW9uR3JhcGggey4uLnRpbWVsaW5lLmdyYXBofSAvPlxuICAgICAgPC9EYXRhUHJvdmlkZXI+XG4gICAgPC9BbGVydC5FcnJvckJvdW5kYXJ5PlxuICApO1xufVxuIiwiaW1wb3J0IHsgU3RyaWN0TW9kZSB9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IGNyZWF0ZVJvb3QgfSBmcm9tICdyZWFjdC1kb20vY2xpZW50JztcblxuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlcih7XG4gIGVsZW0sXG4gIENvbXBvbmVudCxcbiAgcHJvcHMsXG59OiB7XG4gIGVsZW06IEhUTUxFbGVtZW50O1xuICBDb21wb25lbnQ6IFJlYWN0LkZDO1xuICBwcm9wcz86IFJlY29yZDxzdHJpbmcsIHVua25vd24+O1xufSkge1xuICBjcmVhdGVSb290KGVsZW0pLnJlbmRlcihcbiAgICA8U3RyaWN0TW9kZT5cbiAgICAgIDxDb21wb25lbnQgey4uLnByb3BzfSAvPlxuICAgIDwvU3RyaWN0TW9kZT4sXG4gICk7XG59XG4iXSwibmFtZXMiOlsidGhpcyIsInJlbmRlciIsImZyb21HcmFwaCIsIlB1cmVHcmFwaCIsInJlaWZ5IiwiX2EiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUErQ0EsU0FBUyxnQkFBZ0IsT0FBc0M7QUFDdEQsU0FBQSxNQUFNLFFBQVEsS0FBSztBQUM1QjtBQUVBLFNBQVMsZUFBZSxPQUFvRDtBQUNuRSxTQUFBLE9BQU8sVUFBVSxZQUFZLFVBQVUsUUFBUSxDQUFDLE9BQU8sT0FBTyxPQUFPLE1BQU07QUFDcEY7QUFFZ0IsU0FBQSxNQUNkLFVBQ0EsU0FDQSxXQUNpRTtBQUM3RCxPQUFBLG1DQUFTLFNBQVEsUUFBVztBQUN2QixXQUFBO0FBQUEsRUFDVDtBQUVNLFFBQUEsT0FBTyx1Q0FBWSxRQUFRO0FBRWpDLE1BQUksU0FBUyxRQUFX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
