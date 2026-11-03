/* =========================================================================
   main.js — behaviour, rendering and motion for the portfolio.
   Content lives in js/content.js; you should rarely need to edit this file.
   ========================================================================= */
(function () {
  "use strict";

  const S = window.SITE || {};
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = typeof gsap !== "undefined";
  if (hasGsap && typeof ScrollTrigger !== "undefined") gsap.registerPlugin(ScrollTrigger);

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (n, { decimals = 0, prefix = "", suffix = "", abbr = false } = {}) => {
    let v = n;
    let suf = suffix;
    if (abbr) {
      if (Math.abs(v) >= 1e6) { v = v / 1e6; suf = "M" + suffix; }
      else if (Math.abs(v) >= 1e3) { v = v / 1e3; suf = "k" + suffix; }
      decimals = Number.isInteger(v) ? 0 : 1;
    }
    const body = Math.abs(v).toLocaleString("en-AU", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    return (n < 0 ? "-" : "") + prefix + body + suf;
  };

  /* ---------------------------------------------------------------------
     1. Smooth scroll (Lenis) + GSAP ticker
  --------------------------------------------------------------------- */
  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduceMotion) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (hasGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  const scrollTo = (target) => {
    const el = typeof target === "string" ? $(target) : target;
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: -70, duration: 1.4 });
    else el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute("href");
    if (id.length < 2) { e.preventDefault(); scrollTo(document.body); return; }
    const el = $(id);
    if (!el) return;
    e.preventDefault();
    closeMenu();
    scrollTo(el);
    history.replaceState(null, "", id);
  });

  /* ---------------------------------------------------------------------
     2. Loader
  --------------------------------------------------------------------- */
  const loader = $("#loader");
  const startIntro = () => {
    document.body.classList.add("is-ready");
    if (hasGsap && !reduceMotion) {
      gsap.to(".hero__title .word", { y: 0, opacity: 1, duration: 1.2, ease: "power4.out", stagger: 0.08, delay: 0.1 });
    } else {
      $$(".hero__title .word").forEach((w) => { w.style.transform = "none"; w.style.opacity = 1; });
    }
    $$(".hero .reveal-up").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), 350 + i * 120));
  };
  if (loader && !reduceMotion) {
    const pct = $("#loaderPct"), bar = $("#loaderBar");
    const start = performance.now(), dur = 1300;
    const tick = (now) => {
      const p = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - p, 3);
      const n = Math.round(eased * 100);
      pct.textContent = String(n).padStart(2, "0");
      bar.style.width = n + "%";
      if (p < 1) requestAnimationFrame(tick);
      else { loader.classList.add("is-done"); setTimeout(startIntro, 150); setTimeout(() => loader.remove(), 1200); }
    };
    requestAnimationFrame(tick);
  } else { loader && loader.remove(); startIntro(); }

  /* ---------------------------------------------------------------------
     3. Navigation: scrolled state, hide on scroll down, active link, menu
  --------------------------------------------------------------------- */
  const nav = $("#nav"), progress = $("#progress");
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    nav.classList.toggle("is-scrolled", y > 40);
    nav.classList.toggle("is-hidden", y > lastY && y > 400 && !document.body.classList.contains("menu-open"));
    lastY = y;
    const h = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const sections = $$("main section[id]");
  const navLinks = $$(".nav__links a");
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      navLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  sections.forEach((s) => spy.observe(s));

  const burger = $("#burger"), menu = $("#mobileMenu");
  function closeMenu() {
    if (!menu.classList.contains("is-open")) return;
    menu.classList.remove("is-open"); burger.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false"); menu.setAttribute("aria-hidden", "true");
    document.body.classList.remove("menu-open"); lenis && lenis.start();
  }
  burger.addEventListener("click", () => {
    const open = !menu.classList.contains("is-open");
    if (!open) return closeMenu();
    menu.classList.add("is-open"); burger.classList.add("is-open");
    burger.setAttribute("aria-expanded", "true"); menu.setAttribute("aria-hidden", "false");
    document.body.classList.add("menu-open"); lenis && lenis.stop();
  });

  /* ---------------------------------------------------------------------
     4. Melbourne clock
  --------------------------------------------------------------------- */
  const clockEls = [$("#clockText"), $("#dashTime")];
  const melb = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false });
  const tickClock = () => {
    const t = melb.format(new Date());
    if (clockEls[0]) clockEls[0].textContent = "MEL " + t.slice(0, 5);
    if (clockEls[1]) clockEls[1].textContent = t + " AEDT";
  };
  tickClock(); setInterval(tickClock, 1000);
  $("#year") && ($("#year").textContent = new Date().getFullYear());

  /* ---------------------------------------------------------------------
     5. Custom cursor + magnetic buttons
  --------------------------------------------------------------------- */
  const cursor = $("#cursor");
  if (cursor && finePointer && !reduceMotion) {
    let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
    addEventListener("mousemove", (e) => { mx = e.clientX; my = e.clientY; }, { passive: true });
    const dot = $(".cursor__dot", cursor), ring = $(".cursor__ring", cursor), label = $(".cursor__label", cursor);
    const loop = () => {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%,-50%)`;
      ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%,-50%) scale(${cursor.classList.contains("is-drag") ? 2.6 : cursor.classList.contains("is-hover") ? 1.8 : 1})`;
      label.style.transform = `translate(${rx}px, ${ry}px) translate(-50%,-50%)`;
      requestAnimationFrame(loop);
    };
    ring.style.transition = "background .3s, border-color .3s";
    loop();
    document.addEventListener("mouseover", (e) => {
      const t = e.target.closest("[data-cursor], a, button, .case, .testimonials__rail");
      cursor.classList.toggle("is-hover", !!t && !t.classList.contains("testimonials__rail") && !t.classList.contains("case"));
      const drag = t && (t.classList.contains("case") || t.classList.contains("testimonials__rail"));
      cursor.classList.toggle("is-drag", !!drag);
      label.textContent = drag ? (t.classList.contains("case") ? "Open" : "Drag") : "";
    });
    document.addEventListener("mouseleave", () => (cursor.style.opacity = 0));
    document.addEventListener("mouseenter", () => (cursor.style.opacity = 1));

    const magnet = (el) => {
      const strength = 0.35;
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
      });
      el.addEventListener("mouseleave", () => { el.style.transition = "transform .6s cubic-bezier(.22,1,.36,1)"; el.style.transform = ""; setTimeout(() => (el.style.transition = ""), 600); });
    };
    const bindMagnets = () => $$("[data-magnetic]:not([data-bound])").forEach((el) => { el.dataset.bound = 1; magnet(el); });
    bindMagnets();
    document.addEventListener("rendered", bindMagnets);
  }

  /* ---------------------------------------------------------------------
     6. Hero signal canvas
  --------------------------------------------------------------------- */
  (function signal() {
    const c = $("#signalCanvas");
    if (!c || reduceMotion) return;
    const ctx = c.getContext("2d");
    let w, h, dpr, t = 0, px = 0.5, py = 0.5, tx = 0.5, ty = 0.5;
    const resize = () => { dpr = Math.min(devicePixelRatio || 1, 2); w = c.clientWidth; h = c.clientHeight; c.width = w * dpr; c.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    resize(); addEventListener("resize", resize);
    addEventListener("mousemove", (e) => { tx = e.clientX / innerWidth; ty = e.clientY / innerHeight; }, { passive: true });
    const LINES = 7;
    let visible = true;
    new IntersectionObserver(([en]) => (visible = en.isIntersecting)).observe(c);
    const draw = () => {
      requestAnimationFrame(draw);
      if (!visible) return;
      t += 0.006; px += (tx - px) * 0.04; py += (ty - py) * 0.04;
      ctx.clearRect(0, 0, w, h);
      const cx = w * (0.62 + (px - 0.5) * 0.08), cy = h * (0.45 + (py - 0.5) * 0.1);
      const glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * 0.5);
      glow.addColorStop(0, "rgba(255,176,32,0.10)"); glow.addColorStop(0.5, "rgba(255,122,26,0.03)"); glow.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = glow; ctx.fillRect(0, 0, w, h);
      for (let i = 0; i < LINES; i++) {
        const k = i / (LINES - 1);
        const amp = 28 + k * 70 + (py - 0.5) * 40;
        const baseY = h * (0.35 + k * 0.45);
        ctx.beginPath();
        for (let x = 0; x <= w; x += 6) {
          const nx = x / w;
          const y = baseY + Math.sin(nx * 6 + t * 2 + i * 0.9) * amp * 0.5 + Math.sin(nx * 13 - t * 3.2 + i) * amp * 0.25 + Math.cos(nx * 2.2 + t + (px - 0.5) * 4) * amp * 0.6;
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        const alpha = 0.05 + (1 - Math.abs(k - 0.5) * 2) * 0.16;
        ctx.strokeStyle = i % 3 === 1 ? `rgba(127,214,255,${alpha})` : `rgba(255,176,32,${alpha})`;
        ctx.lineWidth = 1 + k * 0.6; ctx.stroke();
      }
      // scanning data points
      for (let i = 0; i < 24; i++) {
        const nx = ((t * 0.07 + i / 24) % 1), x = nx * w;
        const y = h * (0.35 + (i % 7) / 6 * 0.45) + Math.sin(nx * 6 + t * 2 + (i % 7) * 0.9) * 20;
        const a = Math.sin(nx * Math.PI);
        ctx.fillStyle = `rgba(255,176,32,${0.35 * a})`; ctx.beginPath(); ctx.arc(x, y, 1.6, 0, Math.PI * 2); ctx.fill();
      }
    };
    draw();
  })();

  /* ---------------------------------------------------------------------
     7. Charts (SVG helpers)
  --------------------------------------------------------------------- */
  const NS = "http://www.w3.org/2000/svg";
  const linePath = (series, W, H, pad = 8) => {
    const max = Math.max(...series), min = Math.min(...series), rng = max - min || 1;
    const pts = series.map((v, i) => [pad + (i / (series.length - 1)) * (W - pad * 2), H - pad - ((v - min) / rng) * (H - pad * 2)]);
    let d = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], cx = (x0 + x1) / 2;
      d += ` C${cx},${y0} ${cx},${y1} ${x1},${y1}`;
    }
    return { d, pts };
  };
  const chartSVG = (series, { W = 320, H = 120, id = "c" + Math.random().toString(36).slice(2, 7), bars = true, grid = true, color = "#FFB020" } = {}) => {
    const { d, pts } = linePath(series, W, H, 10);
    const last = pts[pts.length - 1];
    const gridLines = grid ? [0.25, 0.5, 0.75].map((f) => `<line x1="0" y1="${H * f}" x2="${W}" y2="${H * f}" stroke="rgba(236,233,225,.07)" stroke-width="1"/>`).join("") : "";
    const barEls = bars ? pts.map(([x, y]) => `<rect x="${x - 4}" y="${y}" width="8" height="${H - 10 - y}" rx="2" fill="${color}" opacity=".12"/>`).join("") : "";
    return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" xmlns="${NS}">
      <defs><linearGradient id="${id}-f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${color}" stop-opacity=".35"/><stop offset="1" stop-color="${color}" stop-opacity="0"/></linearGradient></defs>
      ${gridLines}${barEls}
      <path d="${d} L${last[0]},${H} L${pts[0][0]},${H} Z" fill="url(#${id}-f)"/>
      <path d="${d}" fill="none" stroke="${color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="chart-line" pathLength="1"/>
      <circle cx="${last[0]}" cy="${last[1]}" r="4" fill="${color}"><animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/></circle>
      <circle cx="${last[0]}" cy="${last[1]}" r="10" fill="${color}" opacity=".18"><animate attributeName="r" values="8;16;8" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".25;0;.25" dur="2s" repeatCount="indefinite"/></circle>
    </svg>`;
  };
  // Cover artwork for case studies without a photo
  const coverSVG = (series, id) => {
    const W = 640, H = 360;
    const { d, pts } = linePath(series, W, H * 0.9, 40);
    const cols = Array.from({ length: 12 }, (_, i) => `<line x1="${(i / 12) * W}" y1="0" x2="${(i / 12) * W}" y2="${H}" stroke="rgba(236,233,225,.05)"/>`).join("");
    const bars = pts.map(([x, y], i) => `<rect x="${x - 10}" y="${y + 20}" width="20" height="${H - y - 20}" rx="4" fill="url(#${id}-b)" opacity="${0.25 + (i / pts.length) * 0.5}"/>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" xmlns="${NS}">
      <defs>
        <linearGradient id="${id}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#171A22"/><stop offset="1" stop-color="#0B0D12"/></linearGradient>
        <linearGradient id="${id}-b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB020"/><stop offset="1" stop-color="#FF7A1A" stop-opacity=".1"/></linearGradient>
        <radialGradient id="${id}-g" cx=".8" cy=".2" r=".8"><stop offset="0" stop-color="#FFB020" stop-opacity=".25"/><stop offset="1" stop-color="#FFB020" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="${W}" height="${H}" fill="url(#${id}-bg)"/><rect width="${W}" height="${H}" fill="url(#${id}-g)"/>${cols}${bars}
      <path d="${d}" transform="translate(0,20)" fill="none" stroke="#ECE9E1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>
      <circle cx="${pts[pts.length - 1][0]}" cy="${pts[pts.length - 1][1] + 20}" r="7" fill="#FFB020"/>
    </svg>`;
  };

  /* ---------------------------------------------------------------------
     8. Count-up numbers
  --------------------------------------------------------------------- */
  const counters = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target; counters.unobserve(el);
      const target = parseFloat(el.dataset.count), opts = { decimals: +(el.dataset.decimals || 0), prefix: el.dataset.prefix || "", suffix: el.dataset.suffix || "", abbr: "abbr" in el.dataset };
      if (reduceMotion) { el.textContent = fmt(target, opts); return; }
      const start = performance.now(), dur = 1600;
      const step = (now) => {
        const p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt(target * e, opts);
        if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target, opts);
      };
      requestAnimationFrame(step);
    });
  }, { threshold: 0.5 });
  const observeCounters = () => $$("[data-count]:not([data-observed])").forEach((el) => { el.dataset.observed = 1; counters.observe(el); });

  /* ---------------------------------------------------------------------
     9. Render content
  --------------------------------------------------------------------- */
  const ICONS = {
    seo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M8 11h6M11 8v6"/></svg>',
    paid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
    analytics: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/></svg>',
    cro: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16l-6 8v6l-4 2v-8z"/></svg>',
    email: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    social: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><path d="M7 7l3 3M17 7l-3 3M7 17l3-3M17 17l-3-3"/></svg>'
  };
  const ART = {
    seo: () => chartSVG([3, 5, 4, 7, 9, 8, 12, 15, 14, 18, 22, 26], { bars: false, grid: false, color: "#D9680E" }),
    paid: () => chartSVG([10, 12, 9, 14, 16, 15, 19, 21, 24, 23, 27, 30], { grid: false, color: "#D9680E" }),
    analytics: () => chartSVG([8, 6, 9, 7, 11, 10, 13, 12, 15, 14, 17, 19], { bars: true, grid: false, color: "#5B8DEF" }),
    cro: () => chartSVG([1.1, 1.2, 1.1, 1.4, 1.6, 1.5, 1.9, 2.1, 2.3, 2.4, 2.6, 2.7], { bars: false, grid: false, color: "#D9680E" }),
    email: () => chartSVG([6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31], { bars: false, grid: false, color: "#D9680E" }),
    social: () => chartSVG([2, 3, 3, 5, 6, 8, 9, 12, 13, 16, 19, 22], { bars: true, grid: false, color: "#5B8DEF" })
  };

  function render() {
    // Ticker
    const tk = $("#ticker");
    if (tk && S.ticker) { const items = S.ticker.map((t) => `<span>${esc(t)}</span>`).join(""); tk.innerHTML = items + items; }

    // Numbers
    const nums = $("#numbers");
    if (nums && S.numbers) nums.innerHTML = S.numbers.map((n) => `
      <div class="number reveal-up"><strong data-count="${n.value}" data-decimals="${n.decimals || 0}" data-prefix="${esc(n.prefix || "")}" data-suffix="${esc(n.suffix || "")}">0</strong><span>${esc(n.label)}</span></div>`).join("");

    // Services
    const sg = $("#services-grid");
    if (sg && S.services) sg.innerHTML = S.services.map((s, i) => `
      <article class="svc ${s.size === "wide" ? "svc--wide" : ""} reveal-up" data-cursor="hover">
        <span class="svc__n">0${i + 1}</span>
        <div class="svc__icon">${ICONS[s.id] || ICONS.seo}</div>
        <h3>${esc(s.title)}</h3><p>${esc(s.blurb)}</p>
        <div class="svc__tags">${(s.tags || []).map((t) => `<span>${esc(t)}</span>`).join("")}</div>
        <div class="svc__art">${(ART[s.id] || ART.seo)()}</div>
      </article>`).join("");

    // Case studies
    const track = $("#workTrack");
    if (track && S.caseStudies) {
      track.innerHTML = S.caseStudies.map((c, i) => `
        <article class="case reveal-up" data-case="${i}" tabindex="0" role="button" aria-label="Open case study: ${esc(c.title)}">
          <div class="case__media">
            ${coverSVG(c.series, "cv" + i)}
            ${c.image ? `<img src="${esc(c.image)}" alt="" loading="lazy" onerror="this.remove()">` : ""}
            <div class="case__meta"><span>${esc(c.industry)}</span><span>${esc(c.year)}</span></div>
          </div>
          <div class="case__body">
            <span class="case__client">${esc(c.client)}</span>
            <h3>${esc(c.title)}</h3>
            <p class="case__summary">${esc(c.summary)}</p>
            <div class="case__kpis">${c.kpis.map((k) => `<div><strong class="${k.value < 0 ? "neg" : ""}" data-count="${k.value}" data-decimals="${k.decimals || 0}" data-suffix="${esc(k.suffix || "")}">0</strong><small>${esc(k.label)}</small></div>`).join("")}</div>
          </div>
          <span class="case__open" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 16 16"><path d="M3 13L13 3M6 3h7v7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </article>`).join("") + `
        <div class="case case--end reveal-up"><div><p class="eyebrow">Your project</p><h3>The next chart could be <em style="font-family:var(--font-display);font-style:italic;font-weight:400;color:var(--amber)">yours.</em></h3><p>Tell me what you're trying to grow and I'll show you how I'd measure it.</p><a href="#contact" class="btn btn--amber" data-magnetic data-cursor="hover">Start a conversation</a></div></div>`;
    }

    // Process
    const steps = $("#steps");
    if (steps && S.process) steps.insertAdjacentHTML("beforeend", S.process.map((p) => `
      <li class="step reveal-up"><span class="step__n">${esc(p.n)}</span><h3>${esc(p.title)}</h3><p>${esc(p.text)}</p></li>`).join(""));

    // Stack
    const rows = $("#stackRows");
    if (rows && S.stack) rows.innerHTML = S.stack.map((row, i) => { const items = row.map((t) => `<span class="tool"><i></i>${esc(t)}</span>`).join(""); return `<div class="stack__row ${i % 2 ? "stack__row--rev" : ""}">${items}${items}</div>`; }).join("");

    // Experience / education / certs
    const tl = $("#timeline");
    if (tl && S.experience) tl.innerHTML = S.experience.map((e) => `
      <li class="exp reveal-up"><span class="exp__period">${esc(e.period)}</span><h3>${esc(e.role)}</h3><span class="exp__org">${esc(e.org)}</span><p>${esc(e.text)}</p></li>`).join("");
    const edu = $("#education");
    if (edu && S.education) edu.innerHTML = S.education.map((e) => `<li><small>${esc(e.period)}</small><strong>${esc(e.title)}</strong><span>${esc(e.org)}</span></li>`).join("");
    const certs = $("#certs");
    if (certs && S.certifications) certs.innerHTML = S.certifications.map((c) => `<li>${esc(c)}</li>`).join("");

    // Testimonials
    const rail = $("#testimonials-rail");
    if (rail && S.testimonials) rail.innerHTML = S.testimonials.map((t) => `
      <blockquote class="quote reveal-up"><p>${esc(t.quote)}</p><footer><span class="quote__avatar">${esc((t.name || "?").split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase())}</span><div><strong>${esc(t.name)}</strong><span>${esc(t.org)}</span></div></footer></blockquote>`).join("");

    // Insights
    const ig = $("#insights-grid");
    if (ig && S.insights) ig.innerHTML = S.insights.map((p) => `
      <a class="post reveal-up" href="${esc(p.href || "#")}" data-cursor="hover"><span class="post__tag">${esc(p.tag)}</span><h3>${esc(p.title)}</h3><div class="post__foot"><span class="mono">${p.minutes} min read</span><span class="link-arrow">Read</span></div></a>`).join("");

    // FAQ
    const fl = $("#faq-list");
    if (fl && S.faq) {
      fl.innerHTML = S.faq.map((f, i) => `
        <div class="faq__item reveal-up"><button class="faq__q" aria-expanded="false" aria-controls="faq-a-${i}"><span>${esc(f.q)}</span><i></i></button><div class="faq__a" id="faq-a-${i}"><div><p>${esc(f.a)}</p></div></div></div>`).join("");
      const ld = document.createElement("script"); ld.type = "application/ld+json";
      ld.textContent = JSON.stringify({ "@context": "https://schema.org", "@type": "FAQPage", mainEntity: S.faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) });
      document.head.appendChild(ld);
    }

    // Socials / contact
    const socialHTML = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener" data-cursor="hover"><b>${esc(s.short)}</b>${esc(s.label)}</a>`).join("");
    $("#socials") && ($("#socials").innerHTML = socialHTML);
    $("#mobileSocials") && ($("#mobileSocials").innerHTML = socialHTML);
    const em = $("#contactEmail");
    if (em && S.email) { em.textContent = S.email; em.href = "mailto:" + S.email; }
    $("#availability") && S.availability && ($("#availability").textContent = S.availability);

    // Footer marquee
    const fm = $("#footerMarquee");
    if (fm) { const item = `<span>Manjil <em>Shrestha</em> — Digital Marketing Expert in Melbourne —&nbsp;</span>`; fm.innerHTML = item + item; }

    // Dashboard chart
    const dc = $("#dashChart");
    if (dc) dc.outerHTML = chartSVG([14, 16, 15, 19, 22, 24, 28, 31, 30, 34, 36, 38], { id: "dash" }).replace("<svg ", '<svg id="dashChart" ');

    document.dispatchEvent(new Event("rendered"));
  }
  render();

  /* ---------------------------------------------------------------------
     10. Reveal on scroll
  --------------------------------------------------------------------- */
  const revealer = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); revealer.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$(".reveal-up").forEach((el) => { if (!el.closest(".hero")) revealer.observe(el); });
  observeCounters();

  /* ---------------------------------------------------------------------
     11. Horizontal case-study scroll (desktop) + process line (GSAP)
  --------------------------------------------------------------------- */
  if (hasGsap && !reduceMotion) {
    const mm = gsap.matchMedia();
    mm.add("(min-width: 821px)", () => {
      const track = $("#workTrack"), pin = $("#workPin");
      if (!track || !pin) return;
      const getX = () => -(track.scrollWidth - innerWidth);
      const tween = gsap.to(track, {
        x: getX, ease: "none",
        scrollTrigger: { trigger: pin, start: "top 90px", end: () => "+=" + (track.scrollWidth - innerWidth + 200), pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1 }
      });
      // reveal cards as they enter horizontally
      $$(".case", track).forEach((card) => {
        ScrollTrigger.create({ trigger: card, containerAnimation: tween, start: "left 95%", onEnter: () => card.classList.add("is-in"), once: true });
      });
      return () => tween.scrollTrigger && tween.scrollTrigger.kill();
    });

    const stepsEl = $("#steps"), stepItems = $$(".step");
    if (stepsEl && stepItems.length) {
      ScrollTrigger.create({
        trigger: stepsEl, start: "top 70%", end: "bottom 50%", scrub: true,
        onUpdate: (self) => {
          stepsEl.style.setProperty("--p", self.progress.toFixed(3));
          stepItems.forEach((s, i) => s.classList.toggle("is-on", self.progress >= i / stepItems.length + 0.02));
        }
      });
    }

    // subtle parallax on the dashboard card
    const dash = $(".dash");
    if (dash && finePointer) {
      $("#hero").addEventListener("mousemove", (e) => {
        const r = dash.getBoundingClientRect();
        const x = (e.clientX - (r.left + r.width / 2)) / r.width, y = (e.clientY - (r.top + r.height / 2)) / r.height;
        gsap.to(dash, { rotateY: x * 6, rotateX: -y * 6, transformPerspective: 900, duration: 0.8, ease: "power2.out" });
      });
      $("#hero").addEventListener("mouseleave", () => gsap.to(dash, { rotateY: 0, rotateX: 0, duration: 1, ease: "power3.out" }));
    }
    addEventListener("load", () => ScrollTrigger.refresh());
  } else {
    $$(".step").forEach((s) => s.classList.add("is-on"));
    $("#steps") && $("#steps").style.setProperty("--p", 1);
  }

  /* ---------------------------------------------------------------------
     12. Testimonials controls
  --------------------------------------------------------------------- */
  (function () {
    const rail = $("#testimonials-rail");
    if (!rail) return;
    const step = () => (rail.querySelector(".quote")?.getBoundingClientRect().width || 400) + 20;
    $("#tPrev")?.addEventListener("click", () => rail.scrollBy({ left: -step(), behavior: "smooth" }));
    $("#tNext")?.addEventListener("click", () => rail.scrollBy({ left: step(), behavior: "smooth" }));
    let down = false, sx = 0, sl = 0;
    rail.addEventListener("pointerdown", (e) => { down = true; sx = e.clientX; sl = rail.scrollLeft; rail.style.scrollSnapType = "none"; });
    addEventListener("pointerup", () => { if (down) { down = false; rail.style.scrollSnapType = ""; } });
    rail.addEventListener("pointermove", (e) => { if (down) rail.scrollLeft = sl - (e.clientX - sx); });
  })();

  /* ---------------------------------------------------------------------
     13. FAQ accordion
  --------------------------------------------------------------------- */
  $$(".faq__item").forEach((item) => {
    const btn = $(".faq__q", item);
    btn.addEventListener("click", () => {
      const open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open);
      $$(".faq__item").forEach((o) => { if (o !== item) { o.classList.remove("is-open"); $(".faq__q", o).setAttribute("aria-expanded", "false"); } });
    });
  });
  const first = $(".faq__item"); if (first) { first.classList.add("is-open"); $(".faq__q", first).setAttribute("aria-expanded", "true"); }

  /* ---------------------------------------------------------------------
     14. Case study modal
  --------------------------------------------------------------------- */
  const modal = $("#modal"), modalBody = $("#modalBody");
  let lastFocus = null;
  const openCase = (i) => {
    const c = S.caseStudies[i]; if (!c) return;
    lastFocus = document.activeElement;
    modalBody.innerHTML = `
      <div class="modal__media">${coverSVG(c.series, "md" + i)}${c.image ? `<img src="${esc(c.image)}" alt="" onerror="this.remove()">` : ""}</div>
      <div class="modal__content">
        <div><span class="case__client">${esc(c.client)} · ${esc(c.industry)} · ${esc(c.year)}</span><h2 id="modalTitle" style="margin-top:10px">${esc(c.title)}</h2></div>
        <div class="modal__kpis">${c.kpis.map((k) => `<div><strong class="${k.value < 0 ? "neg" : ""}">${fmt(k.value, { decimals: k.decimals || 0, suffix: k.suffix || "" })}</strong><small>${esc(k.label)}</small></div>`).join("")}</div>
        <div class="modal__section"><h4>The problem</h4><p>${esc(c.problem)}</p></div>
        <div class="modal__section"><h4>The approach</h4><p>${esc(c.approach)}</p></div>
        <div class="modal__section"><h4>The result</h4><p>${esc(c.result)}</p></div>
        <div class="modal__tags">${(c.services || []).map((s) => `<span>${esc(s)}</span>`).join("")}</div>
        <div><a href="#contact" class="btn btn--amber" data-close data-cursor="hover">Get results like these</a></div>
      </div>`;
    modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("menu-open"); lenis && lenis.stop();
    $(".modal__close").focus();
  };
  const closeModal = () => {
    if (!modal.classList.contains("is-open")) return;
    modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("menu-open"); lenis && lenis.start();
    lastFocus && lastFocus.focus();
  };
  document.addEventListener("click", (e) => {
    const card = e.target.closest(".case[data-case]");
    if (card && !e.target.closest("a")) return openCase(+card.dataset.case);
    if (e.target.closest("[data-close]")) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeModal(); closeMenu(); }
    if ((e.key === "Enter" || e.key === " ") && e.target.matches(".case[data-case]")) { e.preventDefault(); openCase(+e.target.dataset.case); }
  });

  /* ---------------------------------------------------------------------
     15. Contact form (Formspree, with mailto fallback until configured)
  --------------------------------------------------------------------- */
  const form = $("#contactForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      let ok = true;
      $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); f.closest(".field").classList.toggle("is-error", bad); if (bad) ok = false; });
      if (!ok) return;
      const note = $("#formNote"), data = new FormData(form);
      const configured = !/YOUR_FORM_ID/.test(form.action);
      if (!configured) {
        const body = encodeURIComponent(`Name: ${data.get("name")}\nEmail: ${data.get("email")}\nCompany: ${data.get("company")}\nBudget: ${data.get("budget")}\n\n${data.get("message")}`);
        location.href = `mailto:${S.email}?subject=${encodeURIComponent("Project enquiry from " + data.get("name"))}&body=${body}`;
        form.classList.add("is-sent"); note.textContent = "Opening your email app…"; return;
      }
      note.textContent = "Sending…";
      try {
        const res = await fetch(form.action, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error();
        form.classList.add("is-sent"); note.textContent = "Thanks. I'll be in touch within one business day."; form.reset();
      } catch { note.textContent = "Something went wrong. Email me directly at " + S.email; }
    });
  }
})();
