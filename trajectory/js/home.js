/* =========================================================================
   Trajectory home.js — interactive hero chart, scroll-driven case study
   chart, growth lab model and process pipeline.
   ========================================================================= */
(function () {
  "use strict";
  const { S, $, $$, reduce, G } = window.UV;
  const NS = "http://www.w3.org/2000/svg";
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");
  const smooth = (p) => { let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`; for (let i = 1; i < p.length; i++) { const [x0, y0] = p[i - 1], [x1, y1] = p[i], c = (x0 + x1) / 2; d += ` C${c.toFixed(1)},${y0.toFixed(1)} ${c.toFixed(1)},${y1.toFixed(1)} ${x1.toFixed(1)},${y1.toFixed(1)}`; } return d; };
  const scale = (s, W, H, px, py, min, max) => { const mn = min ?? Math.min(...s), mx = max ?? Math.max(...s), r = mx - mn || 1; return s.map((v, i) => [px + (i / (s.length - 1)) * (W - 2 * px), H - py - ((v - mn) / r) * (H - 2 * py)]); };

  /* ---------- 1. Interactive hero chart ---------- */
  (function hero() {
    const svg = $("#hcSvg"); if (!svg) return;
    const W = 720, H = 300, months = ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"];
    const SERIES = {   // DEMO data for the illustration
      leads: { label: "Organic enquiries / month", data: [42, 48, 45, 57, 66, 72, 85, 93, 108, 121, 134, 143], fmt: (v) => Math.round(v), unit: " enquiries" },
      roas: { label: "Blended ROAS", data: [1.4, 1.6, 1.7, 2.0, 2.3, 2.5, 2.8, 3.0, 3.1, 3.3, 3.5, 3.6], fmt: (v) => v.toFixed(1) + "x", unit: "" },
      rev: { label: "Revenue attributed / month", data: [38, 41, 40, 47, 55, 61, 70, 78, 86, 95, 104, 112], fmt: (v) => "$" + Math.round(v) + "k", unit: "" },
    };
    svg.innerHTML = `<defs><linearGradient id="hcGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6A2CFF" stop-opacity=".32"/><stop offset="1" stop-color="#6A2CFF" stop-opacity="0"/></linearGradient></defs>
      ${[0.2, 0.4, 0.6, 0.8].map((f) => `<line x1="0" x2="${W}" y1="${H * f}" y2="${H * f}" class="ch-grid"/>`).join("")}
      <path class="hc-area"/><path class="ch-line" id="hcLine"/><g id="hcDots"></g>
      <line class="hc-x" id="hcX" y1="0" y2="${H}" x1="-10" x2="-10"/><circle r="7" class="ch-head" id="hcHead"/>`;
    const area = $(".hc-area", svg), line = $("#hcLine"), dots = $("#hcDots"), head = $("#hcHead"), xl = $("#hcX"), tip = $("#hcTip");
    let key = "leads", pts = [], drawn = false;
    const d0 = (p) => smooth(p);
    function geom(k) { return scale(SERIES[k].data, W, H, 14, 26); }
    function setHeader(k, i) {
      const s = SERIES[k], v = s.data[i ?? s.data.length - 1], growth = Math.round((s.data[s.data.length - 1] / s.data[0] - 1) * 100);
      $("#hcLabel").textContent = s.label; $("#hcValue").textContent = s.fmt(v);
      $("#hcDelta").textContent = i == null ? `▲ ${growth}%` : months[i];
    }
    function render(k, animate) {
      const next = geom(k), from = pts.length ? pts : next.map(([x]) => [x, H]);
      const paint = (p) => { const d = d0(p); line.setAttribute("d", d); area.setAttribute("d", `${d} L${p[p.length - 1][0]},${H} L${p[0][0]},${H}Z`); head.setAttribute("cx", p[p.length - 1][0]); head.setAttribute("cy", p[p.length - 1][1]); dots.innerHTML = p.slice(0, -1).map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.2" class="ch-dot"/>`).join(""); };
      if (!animate || reduce || !G) { pts = next; paint(next); }
      else { const o = { t: 0 }; gsap.to(o, { t: 1, duration: 0.8, ease: "power3.inOut", onUpdate: () => { pts = from.map(([x, y], i) => [x, y + (next[i][1] - y) * o.t]); paint(pts); } }); }
      setHeader(k);
    }
    render(key, true); drawn = true;
    $$(".tabs button").forEach((b) => b.addEventListener("click", () => { $$(".tabs button").forEach((x) => x.setAttribute("aria-selected", x === b)); key = b.dataset.series; render(key, true); }));
    const plot = $(".hc__plot");
    plot.addEventListener("pointermove", (e) => {
      const r = plot.getBoundingClientRect(), x = ((e.clientX - r.left) / r.width) * W;
      let i = 0, best = 1e9; pts.forEach(([px], j) => { const d = Math.abs(px - x); if (d < best) { best = d; i = j; } });
      const [px, py] = pts[i];
      xl.setAttribute("x1", px); xl.setAttribute("x2", px); head.setAttribute("cx", px); head.setAttribute("cy", py);
      tip.hidden = false; tip.style.left = (px / W) * 100 + "%"; tip.style.top = (py / H) * 100 + "%";
      const s = SERIES[key]; tip.innerHTML = `${months[i]} · ${s.fmt(s.data[i])}${i ? `<b>${s.data[i] >= s.data[i - 1] ? "▲" : "▼"} ${Math.abs(Math.round((s.data[i] / s.data[i - 1] - 1) * 100))}%</b>` : ""}`;
      setHeader(key, i);
    });
    plot.addEventListener("pointerleave", () => { tip.hidden = true; xl.setAttribute("x1", -10); xl.setAttribute("x2", -10); const l = pts[pts.length - 1]; head.setAttribute("cx", l[0]); head.setAttribute("cy", l[1]); setHeader(key); });
  })();

  /* ---------- 2. Scrollytelling case study chart ---------- */
  (function story() {
    const svg = $("#stSvg"); if (!svg || !S.caseStudies) return;
    const W = 600, H = 300, C = S.caseStudies, steps = $$(".story__step");
    svg.innerHTML = `<defs><linearGradient id="stGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C4B3FF" stop-opacity=".35"/><stop offset="1" stop-color="#C4B3FF" stop-opacity="0"/></linearGradient></defs>
      ${[0.25, 0.5, 0.75].map((f) => `<line x1="0" x2="${W}" y1="${H * f}" y2="${H * f}" class="st-grid"/>`).join("")}<path class="st-area"/><path class="st-line"/><circle r="8" class="st-head"/>`;
    const area = $(".st-area", svg), line = $(".st-line", svg), head = $(".st-head", svg);
    $("#stDots").innerHTML = C.map(() => "<i></i>").join("");
    const dots = $$("#stDots i");
    const geo = C.map((c) => scale(c.series, W, H, 12, 22));
    let cur = geo[0].map((p) => [...p]), active = -1;
    const paint = (p) => { const d = smooth(p); line.setAttribute("d", d); area.setAttribute("d", `${d} L${p[p.length - 1][0]},${H} L${p[0][0]},${H}Z`); head.setAttribute("cx", p[p.length - 1][0]); head.setAttribute("cy", p[p.length - 1][1]); };
    const kfmt = (k) => (k.value > 0 && k.suffix === "%" ? "+" : "") + k.value.toFixed(k.decimals || 0) + k.suffix;
    function go(i) {
      if (i === active) return; active = i;
      steps.forEach((s, j) => s.classList.toggle("is-on", j === i)); dots.forEach((d, j) => d.classList.toggle("is-on", j <= i));
      const k = C[i].kpis[0]; $("#stLabel").textContent = `Case ${String(i + 1).padStart(2, "0")} · ${C[i].industry}`; $("#stBig").textContent = kfmt(k); $("#stSub").textContent = k.label;
      const from = cur.map((p) => [...p]), to = geo[i];
      if (reduce || !G) { cur = to.map((p) => [...p]); paint(cur); return; }
      const o = { t: 0 }; gsap.to(o, { t: 1, duration: 0.9, ease: "power3.inOut", overwrite: true, onUpdate: () => { cur = from.map(([x, y], j) => [x, y + (to[j][1] - y) * o.t]); paint(cur); } });
    }
    paint(cur); go(0);
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) go(+e.target.dataset.step); }), { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach((s) => io.observe(s));
  })();

  /* ---------- 3. Growth lab ---------- */
  (function lab() {
    const I = { v: $("#iV"), c: $("#iC"), a: $("#iA"), l: $("#iL") }; if (!I.v) return;
    const svg = $("#labSvg"), W = 520, H = 220;
    svg.innerHTML = `<defs><linearGradient id="labGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C4B3FF" stop-opacity=".45"/><stop offset="1" stop-color="#C4B3FF" stop-opacity="0"/></linearGradient></defs><path class="lab-b"/><path class="lab-l1"/><path class="lab-l2"/>`;
    const pB = $(".lab-b", svg), l1 = $(".lab-l1", svg), l2 = $(".lab-l2", svg);
    const shown = { y: 0 }; let raf;
    function update() {
      Object.values(I).forEach((inp) => inp.style.setProperty("--p", ((inp.value - inp.min) / (inp.max - inp.min)) * 100 + "%"));
      const v = +I.v.value, cr = +I.c.value / 100, a = +I.a.value, lift = +I.l.value / 100;
      $("#oV").textContent = v.toLocaleString("en-AU"); $("#oC").textContent = (+I.c.value).toFixed(1) + "%"; $("#oA").textContent = money(a); $("#oL").textContent = "+" + I.l.value + "%";
      const now = v * cr * a, ramp = (m) => Math.min(1, m / 4);    // lift ramps in over the first 4 months
      const base = Array.from({ length: 13 }, () => now), opt = Array.from({ length: 13 }, (_, m) => now * (1 + lift * ramp(m)));
      const lo = now * 0.8, hi = Math.max(...opt) * 1.06, P = (arr) => arr.map((val, m) => [8 + (m / 12) * (W - 16), H - 10 - ((val - lo) / (hi - lo)) * (H - 24)]);
      const pb = P(base), po = P(opt), db = smooth(pb), dop = smooth(po);
      l1.setAttribute("d", db); l2.setAttribute("d", dop); pB.setAttribute("d", `${dop} L${pb[12][0]},${pb[12][1]} ${[...pb].reverse().map(([x, y]) => `L${x},${y}`).join(" ")}Z`);
      const extra = opt.slice(1).reduce((t, v) => t + v - now, 0); $("#rM").textContent = "+" + money(opt[12] - now) + " / month at full lift";
      cancelAnimationFrame(raf); const from = shown.y, t0 = performance.now();
      (function step(t) { const p = Math.min(1, (t - t0) / 500), e = 1 - Math.pow(1 - p, 3); shown.y = from + (extra - from) * e; $("#rY").textContent = money(shown.y); if (p < 1) raf = requestAnimationFrame(step); })(t0);
    }
    Object.values(I).forEach((inp) => inp.addEventListener("input", update)); update();
  })();

  /* ---------- 4. Process pipeline fill ---------- */
  if (G && !reduce && $(".pipe")) ScrollTrigger.create({ trigger: ".pipe", start: "top 75%", end: "bottom 55%", scrub: true, onUpdate: (s) => $("#pipeFill") && $("#pipeFill").parentElement.style.setProperty("--p", s.progress.toFixed(3)) });
  else $("#pipeFill") && $("#pipeFill").parentElement.style.setProperty("--p", 1);
})();
