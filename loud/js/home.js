/* LOUD home.js — the name chart, kinetic manifesto, horizontal receipts,
   moving service rows, quotes and the growth model. */
(function () {
  "use strict";
  const { $, $$, reduce, fine, G } = window.UV;
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");
  const ST = G && typeof ScrollTrigger !== "undefined";

  /* ---------------------------------------------------------------- Name chart
     Six bars spell MANJIL and rise like a growth chart. Bars near the cursor
     grow; on touch screens a slow wave runs through them instead. */
  (function () {
    const box = $("#namechart"); if (!box) return;
    const bars = $$(".nb", box), poly = $("#ncPoly"), dot = $("#ncDot"), tag = $("#ncTag");
    const base = bars.map((b) => +b.dataset.base);
    const n = bars.length, h = base.map(() => (reduce ? 1 : 0)).map((k, i) => k * base[i]), boost = base.map(() => 0);
    let ready = reduce, px = null, W = 0, H = 0, cols = [], running = false, t0 = performance.now();
    const sumBase = base.reduce((a, b) => a + b, 0);

    function measure() {
      const r = box.getBoundingClientRect(); W = r.width; H = r.height;
      cols = bars.map((b) => { const q = b.getBoundingClientRect(); return [q.left - r.left + q.width / 2, q.width]; });
    }
    function draw() {
      bars.forEach((b, i) => b.style.setProperty("--h", h[i].toFixed(4)));
      const pts = cols.map(([x], i) => [x, H - h[i] * H]);
      poly.setAttribute("points", pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join(" "));
      const last = pts[n - 1] || [0, 0];
      dot.setAttribute("cx", last[0].toFixed(1)); dot.setAttribute("cy", last[1].toFixed(1));
      tag.style.top = last[1].toFixed(1) + "px";
      tag.textContent = "▲ +" + Math.round((h.reduce((a, b) => a + b, 0) / sumBase) * 212) + "%";
      let peak = -1, best = 0.15; boost.forEach((v, i) => { if (v > best) { best = v; peak = i; } });
      bars.forEach((b, i) => b.classList.toggle("is-peak", i === peak));
    }
    function frame(now) {
      if (!running) return;
      const wave = !fine && ready ? (Math.sin((now - t0) / 1400) * 0.5 + 0.5) * W : null;
      const p = px ?? wave;
      let moving = false;
      for (let i = 0; i < n; i++) {
        const [cx, cw] = cols[i] || [0, 1];
        boost[i] = p == null ? 0 : Math.exp(-Math.pow((cx - p) / (cw * 1.15), 2));
        const target = ready ? base[i] * 0.84 + boost[i] * 0.16 * (1.6 - base[i] * 0.6) : h[i];
        const d = target - h[i]; h[i] += d * 0.1; if (Math.abs(d) > 0.0005) moving = true;
      }
      draw();
      if (moving || p != null || !ready) requestAnimationFrame(frame); else running = false;
    }
    const kick = () => { if (!running) { running = true; requestAnimationFrame(frame); } };

    measure(); draw();
    addEventListener("resize", () => { measure(); draw(); kick(); });
    document.fonts && document.fonts.ready.then(() => { measure(); draw(); });
    if (reduce) { bars.forEach((b, i) => { h[i] = base[i] * 0.84; }); draw(); return; }

    // intro: bars shoot up one after another
    const introTargets = base.map((b) => b * 0.84);
    (function intro(now) {
      const t = (now - t0 - 250) / 1100;
      for (let i = 0; i < n; i++) { const k = Math.min(1, Math.max(0, t - i * 0.1)); const e = 1 - Math.pow(1 - k, 4) * Math.cos(k * 4.5); h[i] = introTargets[i] * Math.min(1.08, e); }
      draw();
      if (t < 1.6) requestAnimationFrame(intro); else { ready = true; kick(); }
    })(t0);

    const hero = box.closest(".hero");
    if (fine) {
      hero.addEventListener("mousemove", (e) => { const r = box.getBoundingClientRect(); px = e.clientX - r.left; kick(); });
      hero.addEventListener("mouseleave", () => { px = null; kick(); });
    }
    new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) kick(); else running = false; })).observe(box);
  })();

  /* ---------------------------------------------------------------- Manifesto */
  (function () {
    const k = $(".kin"); if (!k || !ST || reduce) return;
    k.classList.add("is-live");
    const strike = $(".kin__strike", k), old = $(".kin__w--old span", k);
    const late = [$(".kin__l--2", k), $(".kin__w--new", k), $(".kin__note", k)];
    gsap.set(late, { opacity: 0, y: 60 });
    const tl = gsap.timeline({ scrollTrigger: { trigger: k, start: "top top", end: "+=140%", pin: true, scrub: 0.6, anticipatePin: 1 } });
    tl.to(strike, { "--s": 1, duration: 1, ease: "power2.inOut" })
      .to(old, { opacity: 0.35, duration: 0.5 }, "<0.5")
      .to(late, { opacity: 1, y: 0, duration: 0.8, stagger: 0.25, ease: "power3.out" }, ">-0.1")
      .to({}, { duration: 0.4 });
  })();

  /* ---------------------------------------------------------------- Receipts (horizontal) */
  (function () {
    const sec = $(".results"), track = $("#resTrack"); if (!sec || !track || !ST || reduce) return;
    const mm = gsap.matchMedia();
    mm.add("(min-width: 761px)", () => {
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      const tw = gsap.to(track, { x: () => -dist(), ease: "none", scrollTrigger: { trigger: sec, start: "top top", end: () => "+=" + dist(), pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1 } });
      $$(".res__big", track).slice(1).forEach((b) => gsap.from(b, { yPercent: 30, opacity: 0.2, ease: "power2.out", scrollTrigger: { trigger: b.closest(".res"), containerAnimation: tw, start: "left 90%", end: "left 40%", scrub: true } }));
      return () => gsap.set(track, { clearProps: "transform" });
    });
  })();

  /* ---------------------------------------------------------------- Service rows drift */
  (function () {
    if (!ST || reduce) return;
    const mm = gsap.matchMedia();
    mm.add("(min-width: 761px)", () => {
      $$(".srow").forEach((row) => {
        const d = +getComputedStyle(row).getPropertyValue("--d") || 1, w = $(".srow__w", row);
        gsap.fromTo(w, { x: -50 * d }, { x: 50 * d, ease: "none", scrollTrigger: { trigger: row, start: "top bottom", end: "bottom top", scrub: true } });
      });
    });
  })();

  /* ---------------------------------------------------------------- Method cards: tilt as they stack */
  (function () {
    if (!ST || reduce) return;
    const cards = $$(".mt");
    cards.forEach((c, i) => {
      if (i === cards.length - 1) return;
      gsap.to(c, { scale: 0.94, ease: "none", scrollTrigger: { trigger: cards[i + 1], start: "top 85%", end: "top 30%", scrub: true } });
    });
  })();

  /* ---------------------------------------------------------------- Quotes */
  (function () {
    const items = $$(".qt__item"); if (!items.length) return;
    let i = 0, t;
    const show = (n) => { i = (n + items.length) % items.length; items.forEach((it, k) => it.classList.toggle("is-on", k === i)); $("#qCount").textContent = `${i + 1} / ${items.length}`; };
    const auto = () => { clearInterval(t); if (!reduce) t = setInterval(() => show(i + 1), 7000); };
    $("#qPrev").addEventListener("click", () => { show(i - 1); auto(); });
    $("#qNext").addEventListener("click", () => { show(i + 1); auto(); });
    auto();
  })();

  /* ---------------------------------------------------------------- Growth model */
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
      const d = (pts) => "M" + pts.map((p) => p.map((q) => q.toFixed(1)).join(",")).join(" L");
      l1.setAttribute("d", d(pb)); l2.setAttribute("d", d(po));
      pB.setAttribute("d", d(po) + " L" + [...pb].reverse().map((p) => p.map((q) => q.toFixed(1)).join(",")).join(" L") + "Z");
      const extra = opt.slice(1).reduce((t, val) => t + val - now, 0);
      $("#rM").textContent = `That is ${money(opt[12] - now)} more each month once the lift is fully in place, from ${money(now)} today.`;
      cancelAnimationFrame(raf); const from = shown, t1 = performance.now();
      (function step(t) { const p = Math.min(1, (t - t1) / 450), e = 1 - Math.pow(1 - p, 3); shown = from + (extra - from) * e; $("#rY").textContent = money(shown); if (p < 1) raf = requestAnimationFrame(step); })(t1);
    }
    Object.values(I).forEach((inp) => inp.addEventListener("input", update)); update();
  })();
})();
