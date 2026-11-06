/* Living Mark home.js — the living mark, rotating word, rebus manifesto,
   brand builder, work tilt, flip cards, process line, halftone portrait
   and the testimonial deck. */
(function () {
  "use strict";
  const { $, $$, reduce, fine, burst } = window.UV;
  const TAU = Math.PI * 2;

  /* ---------------------------------------------------------------- Living mark
     One shape, many identities. 240 points on a circle; each identity is a
     radius function r(theta). The mark eases between them and never sits
     perfectly still, because a brand is a living system. */
  const words = $$(".rot__w");
  let wordI = 0;
  function nextWord() {
    if (!words.length) return;
    const cur = words[wordI]; wordI = (wordI + 1) % words.length; const nx = words[wordI];
    cur.classList.remove("is-on"); cur.classList.add("is-out"); setTimeout(() => cur.classList.remove("is-out"), 650);
    nx.classList.add("is-on");
  }
  (function () {
    const box = $("#mark"); if (!box) return;
    const path = $("#markPath"), shade = $("#markShade"), label = $("#markName");
    const N = 240, abs = Math.abs, pow = Math.pow, cos = Math.cos, sin = Math.sin;
    const SHAPES = [
      ["Circle", () => 1],
      ["Signature", (a) => 0.46 + 0.54 * pow(abs(cos(4 * a)), 6)],
      ["Bloom", (a) => 0.58 + 0.42 * pow(abs(cos(2 * a)), 0.5)],
      ["Squircle", (a) => pow(pow(abs(cos(a)), 4) + pow(abs(sin(a)), 4), -0.25) / 1.1892],
      ["Spark", (a) => 1 / pow(pow(abs(cos(a)), 0.6) + pow(abs(sin(a)), 0.6), 1 / 0.6)],
      ["Sun", (a) => 0.84 + 0.16 * Math.tanh(5 * cos(12 * a))],
      ["Blob", (a, t) => 0.8 + 0.1 * sin(3 * a + t) + 0.06 * sin(5 * a - 1.3 * t) + 0.04 * sin(2 * a + 0.7 * t)],
    ];
    const cur = new Float32Array(N).fill(1);
    let si = 0, rot = 0, t = 0, running = false, lean = 0, leanT = 0, scale = 1, scaleT = 1, timer;
    const target = (a) => SHAPES[si][1](a, t);
    function d() {
      let s = "";
      for (let i = 0; i < N; i++) {
        const a = (i / N) * TAU, r = 100 * scale * cur[i];
        s += (i ? "L" : "M") + (r * cos(a + rot)).toFixed(1) + " " + (r * sin(a + rot)).toFixed(1);
      }
      return s + "Z";
    }
    function frame() {
      if (!running) return;
      t += 0.016; rot += 0.0018 + lean * 0.01; lean += (leanT - lean) * 0.06; scale += (scaleT - scale) * 0.08;
      for (let i = 0; i < N; i++) {
        const a = (i / N) * TAU;
        const wob = reduce ? 0 : 0.012 * sin(3 * a + t * 1.3) + 0.008 * sin(5 * a - t);
        cur[i] += (target(a) + wob - cur[i]) * 0.085;
      }
      const dd = d(); path.setAttribute("d", dd); shade.setAttribute("d", dd);
      requestAnimationFrame(frame);
    }
    function go(n) {
      si = (n + SHAPES.length) % SHAPES.length; label.textContent = SHAPES[si][0];
      nextWord();
    }
    const auto = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => go(si + 1), 2900); };
    box.addEventListener("click", (e) => { go(si + 1); auto(); burst(e.clientX, e.clientY, 14); });
    box.addEventListener("mouseenter", () => { scaleT = 1.05; leanT = 1; });
    box.addEventListener("mouseleave", () => { scaleT = 1; leanT = 0; });
    if (reduce) { for (let i = 0; i < N; i++) cur[i] = SHAPES[1][1]((i / N) * TAU); si = 1; label.textContent = SHAPES[1][0]; const dd = d(); path.setAttribute("d", dd); shade.setAttribute("d", dd); return; }
    new IntersectionObserver(([e]) => { if (e.isIntersecting && !running) { running = true; requestAnimationFrame(frame); auto(); } else if (!e.isIntersecting) { running = false; clearInterval(timer); } }).observe(box);
  })();

  /* ---------------------------------------------------------------- Rebus manifesto */
  (function () {
    const t = $(".manifesto__t"); if (!t) return;
    const ws = $$(".mw, .rb", t);
    $$(".rb", t).forEach((r) => r.addEventListener("click", () => r.classList.toggle("is-open")));
    if (reduce) { ws.forEach((w) => w.classList.add("is-lit")); return; }
    let q = false;
    const run = () => {
      q = false;
      const r = t.getBoundingClientRect(), p = Math.min(1, Math.max(0, (innerHeight * 0.82 - r.top) / (r.height + innerHeight * 0.25)));
      const n = Math.round(p * ws.length * 1.15);
      ws.forEach((w, i) => w.classList.toggle("is-lit", i < n));
    };
    addEventListener("scroll", () => { if (!q) { q = true; requestAnimationFrame(run); } }, { passive: true }); run();
  })();

  /* ---------------------------------------------------------------- Brand builder */
  (function () {
    const out = $("#bbOut"); if (!out) return;
    const P = window.BRAND_BUILDER, nameIn = $("#bbName");
    let g = "sun", tagI = 0;
    const pers = () => ($("input[name=bbP]:checked") || {}).value || "warm";
    function render(pop) {
      const p = P[pers()], name = nameIn.value.trim() || "Your brand";
      out.dataset.font = pers();
      out.style.setProperty("--b1", p.c1); out.style.setProperty("--b2", p.c2); out.style.setProperty("--bink", p.ink); out.style.setProperty("--bpaper", p.paper);
      $$("#bbWord, .bb__w2", out).forEach((el) => (el.textContent = name));
      const tag = p.tags[tagI % p.tags.length].replace("{n}", name);
      $$("#bbTag, .bb__tag2", out).forEach((el) => (el.textContent = tag));
      $$(".bb__mark use", out).forEach((u) => u.setAttribute("href", "#g-" + g));
      $$(".bb__mark .g", out).forEach((s) => s.setAttribute("class", "g g--" + g));
      const mail = $(".mk--card small", out); mail && (mail.textContent = "hello@" + (name.toLowerCase().replace(/[^a-z0-9]/g, "") || "brand") + ".com.au");
      $("#bbPal").innerHTML = [[p.c1, "Primary"], [p.c2, "Accent"], [p.ink, "Ink"], [p.paper, "Paper"]].map(([c, n]) => `<li><i style="background:${c}"></i><span>${n} ${c}</span></li>`).join("");
      $$(".bb__g").forEach((b) => b.classList.toggle("is-on", b.dataset.g === g));
      if (pop) { out.classList.remove("is-pop"); void out.offsetWidth; out.classList.add("is-pop"); }
    }
    nameIn.addEventListener("input", () => render(false));
    $$("input[name=bbP]").forEach((r) => r.addEventListener("change", () => { tagI = 0; render(true); }));
    $$(".bb__g").forEach((b) => b.addEventListener("click", () => { g = b.dataset.g; render(true); }));
    $("#bbShuffle").addEventListener("click", (e) => {
      const keys = Object.keys(P), gs = $$(".bb__g").map((b) => b.dataset.g);
      const k = keys[Math.floor(Math.random() * keys.length)]; $(`input[name=bbP][value=${k}]`).checked = true;
      g = gs[Math.floor(Math.random() * gs.length)]; tagI = Math.floor(Math.random() * 3);
      render(true); const r = e.currentTarget.getBoundingClientRect(); burst(r.left + r.width / 2, r.top + r.height / 2, 14);
    });
    render(false);
  })();

  /* ---------------------------------------------------------------- Work tilt */
  if (fine && !reduce) $$(".wk__img").forEach((el) => {
    el.addEventListener("mousemove", (e) => { const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5; el.style.transform = `perspective(1000px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`; });
    el.addEventListener("mouseleave", () => (el.style.transform = ""));
  });

  /* ---------------------------------------------------------------- Flip cards */
  $$(".flip").forEach((f) => {
    f.addEventListener("click", (e) => { if (e.target.closest("a")) return; f.classList.toggle("is-flipped"); });
    f.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); f.classList.toggle("is-flipped"); } });
  });

  /* ---------------------------------------------------------------- Process line draws as you scroll */
  (function () {
    const track = $(".process__track"), line = $("#prLine"); if (!track || !line) return;
    if (reduce) { line.style.setProperty("--draw", 0); return; }
    let q = false;
    const run = () => { q = false; const r = track.getBoundingClientRect(), p = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.2))); line.style.setProperty("--draw", (1 - p).toFixed(3)); };
    addEventListener("scroll", () => { if (!q) { q = true; requestAnimationFrame(run); } }, { passive: true }); run();
  })();

  /* ---------------------------------------------------------------- Halftone portrait
     The photo is redrawn as red riso dots on ink. Dots swell around the cursor. */
  (function () {
    const fig = $(".about__img"), cv = $("#halftone"); if (!fig || !cv) return;
    const img = $("img", fig), ctx = cv.getContext("2d");
    let cols, rows, step, lum = null, mx = -999, my = -999, raf = 0, W = 0, H = 0;
    function sample() {
      W = fig.clientWidth; H = Math.round(W * 1.25); if (!W) return false;
      const dpr = Math.min(2, devicePixelRatio || 1);
      cv.width = W * dpr; cv.height = H * dpr; cv.style.height = H + "px"; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      step = W < 420 ? 6 : 8; cols = Math.ceil(W / step); rows = Math.ceil(H / step);
      const off = document.createElement("canvas"); off.width = cols; off.height = rows; const o = off.getContext("2d");
      const ir = img.naturalWidth / img.naturalHeight, cr = cols / rows;
      let sw = img.naturalWidth, sh = img.naturalHeight, sx = 0, sy = 0;
      if (ir > cr) { sw = sh * cr; sx = (img.naturalWidth - sw) / 2; } else { sh = sw / cr; sy = (img.naturalHeight - sh) * 0.15; }
      o.drawImage(img, sx, sy, sw, sh, 0, 0, cols, rows);
      try { const d = o.getImageData(0, 0, cols, rows).data; lum = new Float32Array(cols * rows); for (let i = 0; i < cols * rows; i++) lum[i] = (0.2126 * d[i * 4] + 0.7152 * d[i * 4 + 1] + 0.0722 * d[i * 4 + 2]) / 255; }
      catch (e) { return false; }
      // stretch contrast between the 3rd and 99th percentile, then push mid-tones down
      const sorted = Array.from(lum).sort((a, b) => a - b), lo = sorted[Math.floor(sorted.length * 0.03)], hi = sorted[Math.floor(sorted.length * 0.99)];
      for (let i = 0; i < lum.length; i++) lum[i] = Math.pow(Math.min(1, Math.max(0, (lum[i] - lo) / (hi - lo || 1))), 1.9);
      return true;
    }
    function draw() {
      raf = 0; if (!lum) return;
      ctx.fillStyle = "#161211"; ctx.fillRect(0, 0, W, H); ctx.fillStyle = "#F83232";
      for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
        const cx = x * step + step / 2 + (y % 2 ? step / 2 : 0), cy = y * step + step / 2;
        let r = (0.08 + lum[y * cols + x] * 0.92) * step * 0.6;
        const dx = cx - mx, dy = cy - my, dist = dx * dx + dy * dy;
        if (dist < 14000) r *= 1 + 0.9 * (1 - dist / 14000);
        if (r < 0.35) continue;
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.fill();
      }
    }
    const init = () => { if (sample()) { draw(); fig.classList.add("is-ht"); } };
    img.complete && img.naturalWidth ? init() : img.addEventListener("load", init);
    addEventListener("resize", () => { clearTimeout(init.t); init.t = setTimeout(init, 200); });
    if (fine && !reduce) {
      fig.addEventListener("mousemove", (e) => { const r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; raf || (raf = requestAnimationFrame(draw)); });
      fig.addEventListener("mouseleave", () => { mx = my = -999; raf || (raf = requestAnimationFrame(draw)); });
    }
  })();

  /* ---------------------------------------------------------------- Testimonial deck */
  (function () {
    const deck = $("#deck"); if (!deck) return;
    const cards = $$(".card", deck); let order = cards.map((_, i) => i), busy = false;
    const paint = () => { order.forEach((ci, pos) => cards[ci].style.setProperty("--o", pos)); $("#deckCount").textContent = `${order[0] + 1} / ${cards.length}`; };
    const next = () => {
      if (busy) return; busy = true;
      const top = cards[order[0]]; top.classList.add("is-leaving");
      setTimeout(() => { order.push(order.shift()); top.classList.remove("is-leaving"); paint(); busy = false; }, reduce ? 0 : 420);
    };
    cards.forEach((c) => c.addEventListener("click", next));
    $("#deckNext").addEventListener("click", next);
    paint();
  })();
})();
