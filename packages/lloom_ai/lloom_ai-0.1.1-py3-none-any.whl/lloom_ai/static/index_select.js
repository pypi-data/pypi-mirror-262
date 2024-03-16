var ae = Object.defineProperty;
var de = (e, t, n) => t in e ? ae(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var M = (e, t, n) => (de(e, typeof t != "symbol" ? t + "" : t, n), n);
function j() {
}
function ie(e) {
  return e();
}
function Q() {
  return /* @__PURE__ */ Object.create(null);
}
function C(e) {
  e.forEach(ie);
}
function fe(e) {
  return typeof e == "function";
}
function he(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function _e(e) {
  return Object.keys(e).length === 0;
}
function o(e, t) {
  e.appendChild(t);
}
function A(e, t, n) {
  e.insertBefore(t, n || null);
}
function y(e) {
  e.parentNode && e.parentNode.removeChild(e);
}
function se(e, t) {
  for (let n = 0; n < e.length; n += 1)
    e[n] && e[n].d(t);
}
function h(e) {
  return document.createElement(e);
}
function m(e) {
  return document.createTextNode(e);
}
function S() {
  return m(" ");
}
function pe() {
  return m("");
}
function W(e, t, n, l) {
  return e.addEventListener(t, n, l), () => e.removeEventListener(t, n, l);
}
function r(e, t, n) {
  n == null ? e.removeAttribute(t) : e.getAttribute(t) !== n && e.setAttribute(t, n);
}
function me(e) {
  return Array.from(e.childNodes);
}
function T(e, t) {
  t = "" + t, e.data !== t && (e.data = /** @type {string} */
  t);
}
let D;
function N(e) {
  D = e;
}
const k = [], X = [];
let w = [];
const Y = [], ge = /* @__PURE__ */ Promise.resolve();
let U = !1;
function ve() {
  U || (U = !0, ge.then(oe));
}
function q(e) {
  w.push(e);
}
const R = /* @__PURE__ */ new Set();
let $ = 0;
function oe() {
  if ($ !== 0)
    return;
  const e = D;
  do {
    try {
      for (; $ < k.length; ) {
        const t = k[$];
        $++, N(t), be(t.$$);
      }
    } catch (t) {
      throw k.length = 0, $ = 0, t;
    }
    for (N(null), k.length = 0, $ = 0; X.length; )
      X.pop()();
    for (let t = 0; t < w.length; t += 1) {
      const n = w[t];
      R.has(n) || (R.add(n), n());
    }
    w.length = 0;
  } while (k.length);
  for (; Y.length; )
    Y.pop()();
  U = !1, R.clear(), N(e);
}
function be(e) {
  if (e.fragment !== null) {
    e.update(), C(e.before_update);
    const t = e.dirty;
    e.dirty = [-1], e.fragment && e.fragment.p(e.ctx, t), e.after_update.forEach(q);
  }
}
function $e(e) {
  const t = [], n = [];
  w.forEach((l) => e.indexOf(l) === -1 ? t.push(l) : n.push(l)), n.forEach((l) => l()), w = t;
}
const ke = /* @__PURE__ */ new Set();
function we(e, t) {
  e && e.i && (ke.delete(e), e.i(t));
}
function P(e) {
  return (e == null ? void 0 : e.length) !== void 0 ? e : Array.from(e);
}
function ye(e, t, n) {
  const { fragment: l, after_update: c } = e.$$;
  l && l.m(t, n), q(() => {
    const f = e.$$.on_mount.map(ie).filter(fe);
    e.$$.on_destroy ? e.$$.on_destroy.push(...f) : C(f), e.$$.on_mount = [];
  }), c.forEach(q);
}
function ze(e, t) {
  const n = e.$$;
  n.fragment !== null && ($e(n.after_update), C(n.on_destroy), n.fragment && n.fragment.d(t), n.on_destroy = n.fragment = null, n.ctx = []);
}
function Ee(e, t) {
  e.$$.dirty[0] === -1 && (k.push(e), ve(), e.$$.dirty.fill(0)), e.$$.dirty[t / 31 | 0] |= 1 << t % 31;
}
function Oe(e, t, n, l, c, f, i = null, u = [-1]) {
  const d = D;
  N(e);
  const s = e.$$ = {
    fragment: null,
    ctx: [],
    // state
    props: f,
    update: j,
    not_equal: c,
    bound: Q(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(t.context || (d ? d.$$.context : [])),
    // everything else
    callbacks: Q(),
    dirty: u,
    skip_bound: !1,
    root: t.target || d.$$.root
  };
  i && i(s.root);
  let g = !1;
  if (s.ctx = n ? n(e, t.props || {}, (_, z, ...v) => {
    const b = v.length ? v[0] : z;
    return s.ctx && c(s.ctx[_], s.ctx[_] = b) && (!s.skip_bound && s.bound[_] && s.bound[_](b), g && Ee(e, _)), z;
  }) : [], s.update(), g = !0, C(s.before_update), s.fragment = l ? l(s.ctx) : !1, t.target) {
    if (t.hydrate) {
      const _ = me(t.target);
      s.fragment && s.fragment.l(_), _.forEach(y);
    } else
      s.fragment && s.fragment.c();
    t.intro && we(e.$$.fragment), ye(e, t.target, t.anchor), oe();
  }
  N(d);
}
class Se {
  constructor() {
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    M(this, "$$");
    /**
     * ### PRIVATE API
     *
     * Do not use, may change at any time
     *
     * @type {any}
     */
    M(this, "$$set");
  }
  /** @returns {void} */
  $destroy() {
    ze(this, 1), this.$destroy = j;
  }
  /**
   * @template {Extract<keyof Events, string>} K
   * @param {K} type
   * @param {((e: Events[K]) => void) | null | undefined} callback
   * @returns {() => void}
   */
  $on(t, n) {
    if (!fe(n))
      return j;
    const l = this.$$.callbacks[t] || (this.$$.callbacks[t] = []);
    return l.push(n), () => {
      const c = l.indexOf(n);
      c !== -1 && l.splice(c, 1);
    };
  }
  /**
   * @param {Partial<Props>} props
   * @returns {void}
   */
  $set(t) {
    this.$$set && !_e(t) && (this.$$.skip_bound = !0, this.$$set(t), this.$$.skip_bound = !1);
  }
}
const Ne = "4";
typeof window < "u" && (window.__svelte || (window.__svelte = { v: /* @__PURE__ */ new Set() })).v.add(Ne);
function Z(e, t, n) {
  const l = e.slice();
  return l[6] = t[n][0], l[7] = t[n][1], l[8] = t, l[9] = n, l;
}
function ee(e, t, n) {
  const l = e.slice();
  return l[10] = t[n], l;
}
function te(e) {
  let t, n = P(Object.entries(
    /*concepts*/
    e[0]
  )), l = [];
  for (let c = 0; c < n.length; c += 1)
    l[c] = ce(Z(e, n, c));
  return {
    c() {
      for (let c = 0; c < l.length; c += 1)
        l[c].c();
      t = pe();
    },
    m(c, f) {
      for (let i = 0; i < l.length; i += 1)
        l[i] && l[i].m(c, f);
      A(c, t, f);
    },
    p(c, f) {
      if (f & /*Object, concepts, handleCheck*/
      3) {
        n = P(Object.entries(
          /*concepts*/
          c[0]
        ));
        let i;
        for (i = 0; i < n.length; i += 1) {
          const u = Z(c, n, i);
          l[i] ? l[i].p(u, f) : (l[i] = ce(u), l[i].c(), l[i].m(t.parentNode, t));
        }
        for (; i < l.length; i += 1)
          l[i].d(1);
        l.length = n.length;
      }
    },
    d(c) {
      c && y(t), se(l, c);
    }
  };
}
function ne(e) {
  let t, n = P(
    /*c*/
    e[7].examples
  ), l = [];
  for (let c = 0; c < n.length; c += 1)
    l[c] = le(ee(e, n, c));
  return {
    c() {
      t = h("ul");
      for (let c = 0; c < l.length; c += 1)
        l[c].c();
      r(t, "class", "svelte-ezd55v");
    },
    m(c, f) {
      A(c, t, f);
      for (let i = 0; i < l.length; i += 1)
        l[i] && l[i].m(t, null);
    },
    p(c, f) {
      if (f & /*Object, concepts*/
      1) {
        n = P(
          /*c*/
          c[7].examples
        );
        let i;
        for (i = 0; i < n.length; i += 1) {
          const u = ee(c, n, i);
          l[i] ? l[i].p(u, f) : (l[i] = le(u), l[i].c(), l[i].m(t, null));
        }
        for (; i < l.length; i += 1)
          l[i].d(1);
        l.length = n.length;
      }
    },
    d(c) {
      c && y(t), se(l, c);
    }
  };
}
function le(e) {
  let t, n, l = (
    /*example*/
    e[10] + ""
  ), c, f;
  return {
    c() {
      t = h("li"), n = m('"'), c = m(l), f = m('"'), r(t, "class", "examples svelte-ezd55v");
    },
    m(i, u) {
      A(i, t, u), o(t, n), o(t, c), o(t, f);
    },
    p(i, u) {
      u & /*concepts*/
      1 && l !== (l = /*example*/
      i[10] + "") && T(c, l);
    },
    d(i) {
      i && y(t);
    }
  };
}
function ce(e) {
  let t, n, l, c, f, i, u, d, s, g = (
    /*i*/
    e[9] + 1 + ""
  ), _, z, v = (
    /*c*/
    e[7].name + ""
  ), b, J, F, L, B, I = (
    /*c*/
    e[7].prompt + ""
  ), V, G, E, H, x, K;
  function re() {
    e[3].call(
      c,
      /*each_value*/
      e[8],
      /*i*/
      e[9]
    );
  }
  function ue() {
    return (
      /*change_handler*/
      e[4](
        /*c_id*/
        e[6]
      )
    );
  }
  let a = (
    /*c*/
    e[7].examples && ne(e)
  );
  return {
    c() {
      t = h("div"), n = h("div"), l = h("div"), c = h("input"), u = S(), d = h("label"), s = h("b"), _ = m(g), z = m(": "), b = m(v), F = S(), L = h("div"), B = h("p"), V = m(I), G = S(), E = h("div"), a && a.c(), H = S(), r(c, "type", "checkbox"), r(c, "id", f = /*c_id*/
      e[6]), r(c, "name", i = /*c*/
      e[7].name), r(c, "class", "svelte-ezd55v"), r(d, "for", J = /*c_id*/
      e[6]), r(d, "class", "svelte-ezd55v"), r(l, "class", "left svelte-ezd55v"), r(B, "class", "svelte-ezd55v"), r(L, "class", "mid svelte-ezd55v"), r(E, "class", "right svelte-ezd55v"), r(n, "class", "concept-detail svelte-ezd55v"), r(t, "class", "concept-card");
    },
    m(O, p) {
      A(O, t, p), o(t, n), o(n, l), o(l, c), c.checked = /*c*/
      e[7].active, o(l, u), o(l, d), o(d, s), o(s, _), o(s, z), o(s, b), o(n, F), o(n, L), o(L, B), o(B, V), o(n, G), o(n, E), a && a.m(E, null), o(t, H), x || (K = [
        W(c, "change", re),
        W(c, "change", ue)
      ], x = !0);
    },
    p(O, p) {
      e = O, p & /*concepts*/
      1 && f !== (f = /*c_id*/
      e[6]) && r(c, "id", f), p & /*concepts*/
      1 && i !== (i = /*c*/
      e[7].name) && r(c, "name", i), p & /*Object, concepts*/
      1 && (c.checked = /*c*/
      e[7].active), p & /*concepts*/
      1 && v !== (v = /*c*/
      e[7].name + "") && T(b, v), p & /*concepts*/
      1 && J !== (J = /*c_id*/
      e[6]) && r(d, "for", J), p & /*concepts*/
      1 && I !== (I = /*c*/
      e[7].prompt + "") && T(V, I), /*c*/
      e[7].examples ? a ? a.p(e, p) : (a = ne(e), a.c(), a.m(E, null)) : a && (a.d(1), a = null);
    },
    d(O) {
      O && y(t), a && a.d(), x = !1, C(K);
    }
  };
}
function je(e) {
  let t, n, l, c = (
    /*concepts*/
    e[0] && te(e)
  );
  return {
    c() {
      t = h("div"), n = h("p"), n.textContent = "Select concepts to score", l = S(), c && c.c(), r(n, "class", "header svelte-ezd55v");
    },
    m(f, i) {
      A(f, t, i), o(t, n), o(t, l), c && c.m(t, null);
    },
    p(f, [i]) {
      /*concepts*/
      f[0] ? c ? c.p(f, i) : (c = te(f), c.c(), c.m(t, null)) : c && (c.d(1), c = null);
    },
    i: j,
    o: j,
    d(f) {
      f && y(t), c && c.d();
    }
  };
}
function Ce(e, t, n) {
  let { model: l } = t, c, f = l.get("data");
  f && (c = JSON.parse(f));
  function i(s) {
    s = s.c_id;
    let g = JSON.stringify(c);
    l.set("data", g), l.save_changes();
  }
  function u(s, g) {
    s[g][1].active = this.checked, n(0, c);
  }
  const d = (s) => i({ c_id: s });
  return e.$$set = (s) => {
    "model" in s && n(2, l = s.model);
  }, [c, i, l, u, d];
}
class Ae extends Se {
  constructor(t) {
    super(), Oe(this, t, Ce, je, he, { model: 2 });
  }
}
function Le({ model: e, el: t }) {
  let n = new Ae({ target: t, props: { model: e } });
  return () => n.$destroy();
}
export {
  Le as render
};
