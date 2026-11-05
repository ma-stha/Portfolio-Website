/* Studio home.js — work index, quotes, growth model. */
(function () {
  "use strict";
  const { $, $$, reduce } = window.UV;
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");

  /* Work index accordion */
  $$(".wk").forEach((row) => {
    const b = $(".wk__head", row);
    b.addEventListener("click", () => {
      const open = !row.classList.contains("is-open");
      $$(".wk").forEach((r) => { r.classList.remove("is-open"); $(".wk__head", r).setAttribute("aria-expanded", "false"); });
      if (open) { row.classList.add("is-open"); b.setAttribute("aria-expanded", "true"); }
      $("#preview")?.classList.remove("is-on");
    });
  });

  /* Quotes */
  (function () {
    const items = $$(".qt__item"); if (!items.length) return;
    let i = 0, t;
    const show = (n) => { i = (n + items.length) % items.length; items.forEach((it, k) => it.classList.toggle("is-on", k === i)); $("#qCount").textContent = `${i + 1} / ${items.length}`; };
    const auto = () => { clearInterval(t); if (!reduce) t = setInterval(() => show(i + 1), 7000); };
    $("#qPrev").addEventListener("click", () => { show(i - 1); auto(); });
    $("#qNext").addEventListener("click", () => { show(i + 1); auto(); });
    auto();
  })();

  /* Growth model */
  (function () {
    const I = { v: $("#iV"), c: $("#iC"), a: $("#iA"), l: $("#iL") }; if (!I.v) return;
    const svg = $("#labSvg"), W = 520, H = 160;
    svg.innerHTML = '<path class="lab-b"/><path class="lab-l1"/><path class="lab-l2"/>';
    const pB = $(".lab-b", svg), l1 = $(".lab-l1", svg), l2 = $(".lab-l2", svg);
    let shown = 0, raf;
    function update() {
      Object.values(I).forEach((inp) => inp.style.setProperty("--p", ((inp.value - inp.min) / (inp.max - inp.min)) * 100 + "%"));
      const v = +I.v.value, cr = +I.c.value / 100, a = +I.a.value, lift = +I.l.value / 100;
      $("#oV").textContent = v.toLocaleString("en-AU"); $("#oC").textContent = (+I.c.value).toFixed(1) + "%"; $("#oA").textContent = money(a); $("#oL").textContent = "+" + I.l.value + "%";
      const now = v * cr * a, ramp = (m) => Math.min(1, m / 4);
      const opt = Array.from({ length: 13 }, (_, m) => now * (1 + lift * ramp(m)));
      const lo = now * 0.9, hi = Math.max(...opt) * 1.04;
      const P = (val, m) => [(m / 12) * W, H - ((val - lo) / (hi - lo)) * H];
      const pb = opt.map((_, m) => P(now, m)), po = opt.map((val, m) => P(val, m));
      const d = (pts) => "M" + pts.map((p) => p.map((n) => n.toFixed(1)).join(",")).join(" L");
      l1.setAttribute("d", d(pb)); l2.setAttribute("d", d(po));
      pB.setAttribute("d", d(po) + " L" + [...pb].reverse().map((p) => p.map((n) => n.toFixed(1)).join(",")).join(" L") + "Z");
      const extra = opt.slice(1).reduce((t, val) => t + val - now, 0);
      $("#rM").textContent = `That is ${money(opt[12] - now)} more each month once the lift is fully in place, from ${money(now)} today.`;
      cancelAnimationFrame(raf); const from = shown, t0 = performance.now();
      (function step(t) { const p = Math.min(1, (t - t0) / 450), e = 1 - Math.pow(1 - p, 3); shown = from + (extra - from) * e; $("#rY").textContent = money(shown); if (p < 1) raf = requestAnimationFrame(step); })(t0);
    }
    Object.values(I).forEach((inp) => inp.addEventListener("input", update)); update();
  })();
})();
