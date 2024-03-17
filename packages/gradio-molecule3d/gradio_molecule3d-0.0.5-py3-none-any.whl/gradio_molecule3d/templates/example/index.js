const {
  SvelteComponent: f,
  append: u,
  attr: d,
  detach: o,
  element: y,
  init: g,
  insert: v,
  noop: r,
  safe_not_equal: c,
  set_data: m,
  text: b,
  toggle_class: _
} = window.__gradio__svelte__internal;
function A(t) {
  let e, n = (Array.isArray(
    /*value*/
    t[0]
  ) ? (
    /*value*/
    t[0].join(", ")
  ) : (
    /*value*/
    t[0]
  )) + "", s;
  return {
    c() {
      e = y("div"), s = b(n), d(e, "class", "svelte-1hgn91n"), _(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), _(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), _(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    m(l, a) {
      v(l, e, a), u(e, s);
    },
    p(l, [a]) {
      a & /*value*/
      1 && n !== (n = (Array.isArray(
        /*value*/
        l[0]
      ) ? (
        /*value*/
        l[0].join(", ")
      ) : (
        /*value*/
        l[0]
      )) + "") && m(s, n), a & /*type*/
      2 && _(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), a & /*type*/
      2 && _(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), a & /*selected*/
      4 && _(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: r,
    o: r,
    d(l) {
      l && o(e);
    }
  };
}
function h(t, e, n) {
  let { value: s } = e, { type: l } = e, { selected: a = !1 } = e;
  return t.$$set = (i) => {
    "value" in i && n(0, s = i.value), "type" in i && n(1, l = i.type), "selected" in i && n(2, a = i.selected);
  }, [s, l, a];
}
class j extends f {
  constructor(e) {
    super(), g(this, e, h, A, c, { value: 0, type: 1, selected: 2 });
  }
}
export {
  j as default
};
