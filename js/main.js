/* =========================================================================
   main.js — rendering, motion and interaction.
   Content comes from js/content.js; you rarely need to touch this file.
   ========================================================================= */
(function () {
  "use strict";

  const S = window.SITE || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const G = typeof gsap !== "undefined";
  if (G && typeof ScrollTrigger !== "undefined") gsap.registerPlugin(ScrollTrigger);

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const STAR = '<svg class="i-star" aria-hidden="true"><use href="#star"/></svg>';
  function fmt(n, o = {}) {
    let { decimals = 0, prefix = "", suffix = "", abbr = false } = o;
    let v = Math.abs(n), unit = "";
    if (abbr) {
      if (v >= 1e6) { v /= 1e6; unit = "M"; decimals = 1; }
      else if (v >= 1e3) { v /= 1e3; unit = "k"; decimals = v >= 100 ? 0 : 1; }
    }
    const body = v.toLocaleString("en-AU", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    return (n < 0 ? "-" : "") + prefix + body + unit + suffix;
  }
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");

  /* ------------------------------------------------------------------ */
  /* 1. Smooth scroll                                                    */
  /* ------------------------------------------------------------------ */
  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduce) {
    lenis = new Lenis({ lerp: 0.11, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  const goTo = (el) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: -20, duration: 1.4 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href");
    if (id === "#") return;
    const el = id === "#top" ? document.body : $(id); if (!el) return;
    e.preventDefault(); closeMenu(); closeModal(); goTo(el);
  });

  /* ------------------------------------------------------------------ */
  /* 2. Render content                                                   */
  /* ------------------------------------------------------------------ */
  const ICON = {
    seo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>',
    paid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M3 18l6-6 4 4 8-9"/><path d="M15 7h6v6"/></svg>',
    analytics: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="3" y="12" width="4" height="9"/><rect x="10" y="6" width="4" height="15"/><rect x="17" y="2" width="4" height="19"/></svg>',
    cro: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="miter"><path d="M3 4h18l-7 9v6l-4 2v-8z"/></svg>',
    email: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><rect x="3" y="5" width="18" height="14"/><path d="M3 6l9 7 9-7"/></svg>',
    social: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="6" cy="12" r="3"/><circle cx="18" cy="5" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 10.6l6.8-4.2M8.6 13.4l6.8 4.2"/></svg>'
  };
  const SPARK = {
    seo: [3, 4, 4, 6, 8, 7, 11, 13, 14, 18, 21, 25], paid: [10, 12, 9, 14, 16, 15, 19, 21, 24, 23, 27, 30],
    analytics: [8, 6, 9, 7, 11, 10, 13, 12, 15, 14, 17, 19], cro: [11, 12, 11, 14, 16, 15, 19, 21, 23, 24, 26, 27],
    email: [6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31], social: [2, 3, 3, 5, 6, 8, 9, 12, 13, 16, 19, 22]
  };

  function pts(series, W, H, padX, padY) {
    const max = Math.max(...series), min = Math.min(...series), r = max - min || 1;
    return series.map((v, i) => [padX + (i / (series.length - 1)) * (W - padX * 2), H - padY - ((v - min) / r) * (H - padY * 2)]);
  }
  function smooth(p) {
    let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`;
    for (let i = 1; i < p.length; i++) { const [x0, y0] = p[i - 1], [x1, y1] = p[i], cx = (x0 + x1) / 2; d += ` C${cx.toFixed(1)},${y0.toFixed(1)} ${cx.toFixed(1)},${y1.toFixed(1)} ${x1.toFixed(1)},${y1.toFixed(1)}`; }
    return d;
  }
  function spark(series) {
    const W = 240, H = 90, p = pts(series, W, H, 6, 12), d = smooth(p), l = p[p.length - 1];
    const bars = p.map(([x, y]) => `<rect x="${(x - 5).toFixed(1)}" y="${y.toFixed(1)}" width="10" height="${(H - y).toFixed(1)}" fill="#0B0B0B" opacity=".08"/>`).join("");
    return `<svg class="svc__spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">${bars}<path d="${d}" fill="none" stroke="#F83232" stroke-width="3.5" stroke-linecap="round"/><rect x="${l[0] - 6}" y="${l[1] - 6}" width="12" height="12" fill="#F83232" stroke="#0B0B0B" stroke-width="2" transform="rotate(45 ${l[0]} ${l[1]})"/></svg>`;
  }
  function cover(series, id) {
    const W = 720, H = 360, p = pts(series, W, H, 50, 56), d = smooth(p), l = p[p.length - 1];
    const grid = Array.from({ length: 9 }, (_, i) => `<line x1="0" y1="${i * 45}" x2="${W}" y2="${i * 45}" stroke="#0B0B0B" stroke-opacity=".09"/>`).join("") +
      Array.from({ length: 17 }, (_, i) => `<line x1="${i * 45}" y1="0" x2="${i * 45}" y2="${H}" stroke="#0B0B0B" stroke-opacity=".09"/>`).join("");
    const bars = p.map(([x, y], i) => `<rect x="${(x - 14).toFixed(1)}" y="${(y + 18).toFixed(1)}" width="28" height="${(H - y - 18).toFixed(1)}" fill="${i === p.length - 1 ? "#F83232" : "url(#" + id + "h)"}" stroke="#0B0B0B" stroke-width="2"/>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs><pattern id="${id}h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#F5F4F0"/><line x1="0" y1="0" x2="0" y2="8" stroke="#0B0B0B" stroke-width="2.4"/></pattern></defs>
      <rect width="${W}" height="${H}" fill="#E4E1DA"/>${grid}${bars}
      <path d="${d}" transform="translate(5 5)" fill="none" stroke="#0B0B0B" stroke-width="7" stroke-linecap="round"/>
      <path d="${d}" fill="none" stroke="#F83232" stroke-width="7" stroke-linecap="round"/>
      <g transform="translate(${l[0]} ${l[1]})"><circle r="15" fill="#F83232" stroke="#0B0B0B" stroke-width="3"/></g>
    </svg>`;
  }

  function render() {
    // Receipt
    const rl = $("#receiptLines");
    if (rl && S.receipt) {
      rl.innerHTML = S.receipt.lines.map((l) => `<li><span>${esc(l.label)}</span><b class="${l.value < 0 ? "neg" : ""}" data-count="${l.value}" data-decimals="${l.decimals || 0}" data-prefix="${esc(l.prefix || "")}" data-suffix="${esc(l.suffix || "")}" ${l.abbr ? "data-abbr" : ""} data-manual>0</b></li>`).join("");
      $("#receiptTotalLabel").textContent = S.receipt.total.label;
      $("#receiptTotal").textContent = S.receipt.total.value;
    }
    // Tapes
    const tape = (arr) => { const one = arr.map((t) => `<span>${esc(t)} ${STAR}</span>`).join(""); return one + one; };
    if (S.tapeA) $("#tapeA").innerHTML = tape(S.tapeA);
    if (S.tapeB) $("#tapeB").innerHTML = tape(S.tapeB);
    // Manifesto
    const mf = $("#manifesto");
    if (mf && S.manifesto) {
      const parts = S.manifesto.split(/(\[[^\]]+\])/g).filter(Boolean);
      mf.innerHTML = parts.map((part) => {
        const hi = part.startsWith("[");
        const words = (hi ? part.slice(1, -1) : part).split(/\s+/).filter(Boolean);
        const html = words.map((w) => `<span class="w">${esc(w)}</span>`).join(" ");
        return hi ? `<span class="hiw">${html}</span>` : html;
      }).join(" ");
    }
    // Numbers
    if (S.numbers) $("#numbers").innerHTML = S.numbers.map((n) => `<div class="num reveal"><strong><span data-count="${n.value}" data-decimals="${n.decimals || 0}" data-prefix="${esc(n.prefix || "")}">0</span><i>${esc(n.suffix || "")}</i></strong><span>${esc(n.label)}</span></div>`).join("");
    // Services
    if (S.services) $("#servicesGrid").innerHTML = S.services.map((s, i) => `
      <article class="svc reveal">
        <div class="svc__top"><span class="svc__icon">${ICON[s.id] || ICON.seo}</span><span class="svc__n">0${i + 1}</span></div>
        <h3>${esc(s.title)}</h3><p>${esc(s.blurb)}</p>
        <div class="svc__tags">${(s.tags || []).map((t) => `<span>${esc(t)}</span>`).join("")}</div>
        ${spark(SPARK[s.id] || SPARK.seo)}
      </article>`).join("");
    // Cases
    const track = $("#workTrack");
    if (track && S.caseStudies) {
      track.innerHTML = S.caseStudies.map((c, i) => `
        <article class="case" data-case="${i}" data-cursor="Open" tabindex="0" role="button" aria-label="Open case study: ${esc(c.title)}">
          <div class="case__media">${cover(c.series, "c" + i)}${c.image ? `<img src="${esc(c.image)}" alt="" loading="lazy" onerror="this.remove()">` : ""}
            <div class="case__tags"><span>${esc(c.industry)}</span><span>${esc(c.year)}</span></div></div>
          <div class="case__body">
            <span class="case__client">${esc(c.client)}</span>
            <h3>${esc(c.title)}</h3>
            <p class="case__summary">${esc(c.summary)}</p>
            <div class="case__kpis">${c.kpis.map((k) => `<div><strong class="${k.value < 0 ? "neg" : ""}" data-count="${k.value}" data-decimals="${k.decimals || 0}" data-suffix="${esc(k.suffix || "")}">0</strong><small>${esc(k.label)}</small></div>`).join("")}</div>
            <span class="case__more">Read the case study <b aria-hidden="true">→</b></span>
          </div>
        </article>`).join("") + `
        <div class="case case--end"><div>${STAR}<h3>Your chart goes here.</h3><p>Tell me what you're trying to grow and I'll show you how I'd measure it.</p><a href="#contact" class="btn btn--ink" data-magnetic>Start a project →</a></div></div>`;
      $("#workTotal").textContent = String(S.caseStudies.length).padStart(2, "0");
    }
    // Loop
    if (S.process) {
      $("#loopList").innerHTML = S.process.map((p, i) => `<li data-step="${i}"><b>0${i + 1}</b><strong>${esc(p.title)}</strong><p>${esc(p.text)}</p></li>`).join("");
      $("#ringNodes").innerHTML = S.process.map((p, i) => {
        const a = (i * 360 / S.process.length - 90) * Math.PI / 180;
        return `<div class="node" style="left:${(50 + Math.cos(a) * 42.5).toFixed(2)}%;top:${(50 + Math.sin(a) * 42.5).toFixed(2)}%"><span>0${i + 1}</span></div>`;
      }).join("");
    }
    // Stack
    if (S.stack) $("#stackRows").innerHTML = S.stack.map((row, i) => { const one = row.map((t) => `<span class="tool"><svg><use href="#star"/></svg>${esc(t)}</span>`).join(""); return `<div class="stack__row${i % 2 ? " stack__row--rev" : ""}">${one}${one}</div>`; }).join("");
    // Experience
    if (S.experience) $("#ledger").innerHTML = S.experience.map((e) => `<li class="reveal"><span class="ledger__period">${esc(e.period)}</span><div><h3>${esc(e.role)}</h3><span class="ledger__org">${esc(e.org)}</span></div><p>${esc(e.text)}</p></li>`).join("");
    if (S.education) $("#education").innerHTML = S.education.map((e) => `<li><small>${esc(e.period)}</small><strong>${esc(e.title)}</strong><span>${esc(e.org)}</span></li>`).join("");
    if (S.certifications) $("#certs").innerHTML = S.certifications.map((c) => `<li>${esc(c)}</li>`).join("");
    // Quotes
    if (S.testimonials) $("#quotes").innerHTML = S.testimonials.map((t) => `<blockquote class="quote reveal"><p>${esc(t.quote)}</p><footer><span class="quote__av">${esc(t.name.split(" ").map((w) => w[0]).join("").slice(0, 2))}</span><div><strong>${esc(t.name)}</strong><small>${esc(t.org)}</small></div></footer></blockquote>`).join("");
    // Posts
    if (S.insights) $("#posts").innerHTML = S.insights.map((p) => `<a class="post reveal" href="${esc(p.href || "#")}" data-cursor="Read"><span class="post__tag">${esc(p.tag)}</span><h3>${esc(p.title)}</h3><div class="post__foot"><span>${p.minutes} min read</span><b>→</b></div></a>`).join("");
    // FAQ
    if (S.faq) {
      $("#faqList").innerHTML = S.faq.map((f, i) => `<div class="faq__item reveal"><button class="faq__q" aria-expanded="false" aria-controls="fa${i}"><span>${esc(f.q)}</span><svg aria-hidden="true"><use href="#star"/></svg></button><div class="faq__a" id="fa${i}" role="region"><div><p>${esc(f.a)}</p></div></div></div>`).join("");
      const ld = document.createElement("script"); ld.type = "application/ld+json";
      ld.textContent = JSON.stringify({ "@context": "https://schema.org", "@type": "FAQPage", mainEntity: S.faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) });
      document.head.appendChild(ld);
    }
    // Contact
    const soc = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener">${esc(s.label)} ↗</a>`).join("");
    $("#socials").innerHTML = soc; $("#mobileSocials").innerHTML = soc;
    if (S.email) $("#emailText").textContent = S.email;
    if (S.availability) $("#availability").textContent = S.availability;
    $("#year").textContent = new Date().getFullYear();
  }
  render();

  /* ------------------------------------------------------------------ */
  /* 3. Hero: split headline into letters + cursor-reactive weight       */
  /* ------------------------------------------------------------------ */
  $$(".hero__title .vf").forEach((el) => { el.innerHTML = [...el.textContent].map((c) => `<span class="ch">${esc(c)}</span>`).join(""); });
  const chars = $$(".hero__title .ch");
  if (fine && !reduce && chars.length) {
    const state = chars.map(() => ({ w: 900, d: 78 }));
    let mx = -9999, my = -9999, active = false, raf = null;
    const hero = $("#hero");
    hero.addEventListener("mousemove", (e) => { mx = e.clientX; my = e.clientY; if (!raf) raf = requestAnimationFrame(tick); });
    hero.addEventListener("mouseleave", () => { mx = my = -9999; if (!raf) raf = requestAnimationFrame(tick); });
    function tick() {
      raf = null; let moving = false;
      chars.forEach((c, i) => {
        const r = c.getBoundingClientRect();
        const dist = Math.hypot(mx - (r.left + r.width / 2), my - (r.top + r.height / 2));
        const k = Math.max(0, 1 - dist / 300), e = k * k * (3 - 2 * k);
        const tw = 900 - e * 720, td = 78 + e * 22, s = state[i];
        s.w += (tw - s.w) * 0.22; s.d += (td - s.d) * 0.22;
        if (Math.abs(tw - s.w) > 0.5 || Math.abs(td - s.d) > 0.1) moving = true;
        c.style.setProperty("--w", s.w.toFixed(0)); c.style.setProperty("--d", s.d.toFixed(1));
      });
      if (moving) raf = requestAnimationFrame(tick);
    }
  }

  /* ------------------------------------------------------------------ */
  /* 4. Counters                                                         */
  /* ------------------------------------------------------------------ */
  function countUp(el, dur = 1500) {
    const target = parseFloat(el.dataset.count);
    const o = { decimals: +(el.dataset.decimals || 0), prefix: el.dataset.prefix || "", suffix: el.dataset.suffix || "", abbr: "abbr" in el.dataset };
    if (reduce) { el.textContent = fmt(target, o); return; }
    const t0 = performance.now();
    const step = (now) => { const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 4); el.textContent = fmt(target * e, p < 1 && o.abbr ? { ...o } : o); if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target, o); };
    requestAnimationFrame(step);
  }
  const cio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { cio.unobserve(e.target); countUp(e.target); } }), { threshold: 0.4 });
  $$("[data-count]:not([data-manual])").forEach((el) => cio.observe(el));

  /* ------------------------------------------------------------------ */
  /* 5. Loader + intro                                                   */
  /* ------------------------------------------------------------------ */
  function intro() {
    const stickers = $$(".sticker");
    if (G && !reduce) {
      const tl = gsap.timeline({ defaults: { ease: "power4.out" } });
      tl.to(".hl .ch", { y: 0, opacity: 1, duration: 1.0, stagger: 0.025 })
        .to(".hl__block", { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power3.inOut" }, 0.45)
        .from(".masthead", { y: -14, opacity: 0, duration: 0.6 }, 0.1)
        .from(".receipt", { y: -220, rotate: 16, opacity: 0, duration: 1.1, ease: "back.out(1.4)" }, 0.5)
        .fromTo(stickers, { opacity: 0, "--s": 0 }, { opacity: 1, "--s": 1, duration: 0.7, ease: "back.out(2.2)", stagger: 0.12 }, 0.9)
        .from(".hero__foot > *", { y: 24, opacity: 0, duration: 0.7, stagger: 0.08 }, 0.7);
    } else {
      $$(".hl .ch").forEach((c) => { c.style.transform = "none"; c.style.opacity = 1; });
      $$(".hl__block").forEach((b) => (b.style.clipPath = "none"));
      stickers.forEach((s) => (s.style.opacity = 1));
    }
    setTimeout(() => $$("#receiptLines [data-count]").forEach((el, i) => setTimeout(() => countUp(el, 1300), i * 140)), reduce ? 0 : 900);
  }
  const loader = $("#loader");
  if (loader && !reduce) {
    const pct = $("#loaderPct"), bar = $("#loaderBar"), t0 = performance.now(), dur = 1250;
    const tick = (now) => {
      const p = Math.min(1, (now - t0) / dur), n = Math.round((1 - Math.pow(1 - p, 3)) * 100);
      pct.textContent = String(n).padStart(3, "0"); bar.style.width = n + "%";
      if (p < 1) requestAnimationFrame(tick);
      else { loader.classList.add("is-done"); setTimeout(intro, 250); setTimeout(() => loader.remove(), 1100); }
    };
    requestAnimationFrame(tick);
  } else { loader && loader.remove(); intro(); }

  /* ------------------------------------------------------------------ */
  /* 6. Nav, progress, active section, menu                              */
  /* ------------------------------------------------------------------ */
  const nav = $("#nav"), prog = $("#progress");
  let lastY = 0;
  addEventListener("scroll", () => {
    const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    nav.classList.toggle("is-hidden", y > lastY && y > 500 && !document.body.classList.contains("locked"));
    lastY = y; prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
  }, { passive: true });
  const links = $$(".nav__links a");
  const spy = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) links.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + e.target.id)); }), { rootMargin: "-45% 0px -50% 0px" });
  $$("main section[id]").forEach((s) => spy.observe(s));

  const burger = $("#burger"), menu = $("#mobileMenu");
  const lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  function closeMenu() { if (!menu.classList.contains("is-open")) return; menu.classList.remove("is-open"); burger.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); menu.setAttribute("aria-hidden", "true"); lock(false); }
  burger.addEventListener("click", () => {
    if (menu.classList.contains("is-open")) return closeMenu();
    menu.classList.add("is-open"); burger.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); menu.setAttribute("aria-hidden", "false"); lock(true);
  });

  /* ------------------------------------------------------------------ */
  /* 7. Melbourne clock                                                  */
  /* ------------------------------------------------------------------ */
  const tf = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", hour: "2-digit", minute: "2-digit", hour12: false });
  const df = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", day: "2-digit", month: "2-digit", year: "numeric" });
  const clock = () => {
    const now = new Date(), t = tf.format(now);
    $("#clockText").textContent = "MEL " + t;
    $("#mastClock").textContent = "Melbourne " + t;
    $("#receiptMeta").textContent = `#${(S.receipt && S.receipt.id) || "MS"} · ${df.format(now)} ${t}`;
  };
  clock(); setInterval(clock, 15000);

  /* ------------------------------------------------------------------ */
  /* 8. Cursor + magnetic buttons                                        */
  /* ------------------------------------------------------------------ */
  const cur = $("#cursor"), curLabel = $("#cursorLabel");
  if (fine && !reduce) {
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y;
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
    (function loop() { cx += (x - cx) * 0.28; cy += (y - cy) * 0.28; cur.style.transform = `translate(${cx}px, ${cy}px)`; requestAnimationFrame(loop); })();
    const RED = '[data-theme="red"], .btn--red, .hl__block, .sticker--pill, .post__tag, .quote:nth-child(3n+1), .case__tags span:last-child';
    document.addEventListener("mouseover", (e) => {
      const t = e.target;
      const hov = t.closest("a, button, [data-drag], [data-cursor], input, select, textarea, label, .svc, .tool, .ledger li");
      cur.classList.toggle("is-hover", !!hov);
      const lab = t.closest("[data-cursor]")?.dataset.cursor || (t.closest("[data-drag]") ? "Drag me" : t.closest("#heroBurst") ? "Pop!" : "");
      curLabel.textContent = lab; cur.classList.toggle("has-label", !!lab);
      cur.classList.toggle("on-red", !!t.closest(RED));
    });
    document.addEventListener("mouseleave", () => (cur.style.opacity = 0));
    document.addEventListener("mouseenter", () => (cur.style.opacity = 1));

    $$("[data-magnetic]").forEach((el) => {
      el.addEventListener("mousemove", (e) => { const r = el.getBoundingClientRect(); el.style.translate = `${(e.clientX - r.left - r.width / 2) * 0.25}px ${(e.clientY - r.top - r.height / 2) * 0.35}px`; });
      el.addEventListener("mouseleave", () => { el.style.transition = "translate .5s cubic-bezier(.34,1.56,.64,1), transform .25s, box-shadow .25s, background .2s, color .2s"; el.style.translate = "0 0"; setTimeout(() => (el.style.transition = ""), 500); });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 9. Draggable stickers                                               */
  /* ------------------------------------------------------------------ */
  $$("[data-drag]").forEach((el) => {
    let sx = 0, sy = 0, ox = 0, oy = 0, id = null;
    el.addEventListener("pointerdown", (e) => {
      id = e.pointerId; el.setPointerCapture(id); el.classList.add("is-dragging");
      sx = e.clientX; sy = e.clientY; ox = parseFloat(el.style.getPropertyValue("--dx")) || 0; oy = parseFloat(el.style.getPropertyValue("--dy")) || 0;
    });
    el.addEventListener("pointermove", (e) => {
      if (e.pointerId !== id) return;
      el.style.setProperty("--dx", ox + e.clientX - sx + "px"); el.style.setProperty("--dy", oy + e.clientY - sy + "px");
    });
    const end = (e) => {
      if (e.pointerId !== id) return; id = null; el.classList.remove("is-dragging");
      el.style.setProperty("--r", (Math.random() * 20 - 10).toFixed(1) + "deg");
    };
    el.addEventListener("pointerup", end); el.addEventListener("pointercancel", end);
  });

  /* ------------------------------------------------------------------ */
  /* 10. Starburst pop                                                   */
  /* ------------------------------------------------------------------ */
  function pop(x, y, n = 16) {
    if (reduce || !G) return;
    for (let i = 0; i < n; i++) {
      const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      s.setAttribute("class", "burst-bit"); s.innerHTML = '<use href="#star"/>';
      if (i % 3 === 0) s.style.color = "#0B0B0B";
      document.body.appendChild(s);
      const a = (i / n) * Math.PI * 2 + Math.random() * 0.4, d = 120 + Math.random() * 180, sc = 0.5 + Math.random() * 1.2;
      gsap.set(s, { x: x - 14, y: y - 14, scale: 0 });
      gsap.to(s, { x: x - 14 + Math.cos(a) * d, y: y - 14 + Math.sin(a) * d + 60, scale: sc, rotate: Math.random() * 540 - 270, duration: 1 + Math.random() * 0.5, ease: "power3.out" });
      gsap.to(s, { opacity: 0, duration: 0.4, delay: 0.8 + Math.random() * 0.4, onComplete: () => s.remove() });
    }
  }
  $("#heroBurst").addEventListener("click", (e) => {
    const r = e.currentTarget.getBoundingClientRect(); pop(r.left + r.width / 2, r.top + r.height / 2, 22);
    if (G) gsap.fromTo(e.currentTarget, { scale: 1.5 }, { scale: 1, duration: 0.8, ease: "elastic.out(1, .35)" });
  });
  $$(".contact__star, .numbers__star").forEach((s) => s.addEventListener("click", (e) => pop(e.clientX, e.clientY, 14)));

  /* ------------------------------------------------------------------ */
  /* 11. Reveal                                                          */
  /* ------------------------------------------------------------------ */
  const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });
  $$(".reveal, .h2").forEach((el) => rio.observe(el));

  /* ------------------------------------------------------------------ */
  /* 12. Scroll-driven sections                                          */
  /* ------------------------------------------------------------------ */
  const words = $$("#manifesto .w"), hiws = $$("#manifesto .hiw");
  const steps = $$("#loopList li"), nodes = $$(".node"), nodesWrap = $("#ringNodes");
  let curStep = -1;
  function setStep(i) {
    if (i === curStep || !S.process) return; curStep = i;
    const n = S.process.length;
    steps.forEach((li, k) => li.classList.toggle("is-on", k === i));
    nodes.forEach((nd, k) => { nd.classList.toggle("is-on", k === i); nd.classList.toggle("is-done", k < i); nd.querySelector("span").style.transform = `rotate(${i * 360 / n}deg)`; });
    nodesWrap.style.transform = `rotate(${-i * 360 / n}deg)`;
    $("#ringN").textContent = String(i + 1).padStart(2, "0");
    $("#ringT").textContent = S.process[i].title;
    if (G && !reduce) gsap.fromTo(".ring__center", { scale: 0.9 }, { scale: 1, duration: 0.6, ease: "back.out(3)" });
  }

  if (G && !reduce) {
    ScrollTrigger.create({ trigger: "#manifesto", start: "top 82%", end: "bottom 45%", scrub: true,
      onUpdate: (st) => { const on = Math.round(st.progress * words.length); words.forEach((w, k) => w.classList.toggle("on", k < on)); hiws.forEach((h) => h.classList.toggle("on", h.lastElementChild.classList.contains("on"))); } });

    const mm = gsap.matchMedia();
    mm.add("(min-width: 761px)", () => {
      const track = $("#workTrack"), pin = $("#workPin"), cards = $$(".case[data-case]");
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      const tw = gsap.to(track, { x: () => -dist(), ease: "none",
        scrollTrigger: { trigger: pin, start: "top 70px", end: () => "+=" + dist(), pin: true, scrub: 0.7, invalidateOnRefresh: true, anticipatePin: 1,
          onUpdate: (st) => { const i = Math.min(cards.length - 1, Math.floor(st.progress * cards.length)); $("#workIdx").textContent = String(i + 1).padStart(2, "0"); $("#workBar").style.width = Math.max(8, st.progress * 100) + "%"; } } });
      return () => tw.scrollTrigger && tw.scrollTrigger.kill();
    });
    mm.add("(min-width: 1025px)", () => {
      setStep(0);
      const st = ScrollTrigger.create({ trigger: "#loopPin", start: "top top", end: "+=220%", pin: true, scrub: true,
        onUpdate: (s) => { $("#ringProg").style.strokeDashoffset = (1 - s.progress).toFixed(4); setStep(Math.min(S.process.length - 1, Math.floor(s.progress * S.process.length * 0.999))); } });
      return () => { st.kill(); };
    });
    addEventListener("load", () => ScrollTrigger.refresh());
  } else {
    words.forEach((w) => w.classList.add("on")); hiws.forEach((h) => h.classList.add("on"));
    setStep(0); $("#ringProg").style.strokeDashoffset = 0;
  }

  /* ------------------------------------------------------------------ */
  /* 13. Growth calculator                                               */
  /* ------------------------------------------------------------------ */
  (function calc() {
    const c = Object.assign({ visitors: 20000, conversion: 1.5, value: 120, lift: 30 }, S.calculator);
    const I = { v: $("#iVisitors"), c: $("#iConversion"), a: $("#iValue"), l: $("#iLift") };
    I.v.value = c.visitors; I.c.value = c.conversion; I.a.value = c.value; I.l.value = c.lift;
    const shown = { year: 0, now: 0, nw: 0, month: 0, conv: 0 };
    let anim = null;
    function fill(inp) { inp.style.setProperty("--p", ((inp.value - inp.min) / (inp.max - inp.min) * 100) + "%"); }
    function update() {
      Object.values(I).forEach(fill);
      const v = +I.v.value, cr = +I.c.value / 100, a = +I.a.value, l = +I.l.value / 100;
      $("#oVisitors").textContent = v.toLocaleString("en-AU");
      $("#oConversion").textContent = (+I.c.value).toFixed(1) + "%";
      $("#oValue").textContent = money(a);
      $("#oLift").textContent = "+" + I.l.value + "%";
      const now = v * cr * a, nw = v * cr * (1 + l) * a;
      const target = { year: (nw - now) * 12, now, nw, month: nw - now, conv: v * cr * l };
      $("#bNow").style.width = (now / nw * 100).toFixed(1) + "%"; $("#bNew").style.width = "100%";
      cancelAnimationFrame(anim);
      const from = { ...shown }, t0 = performance.now();
      const step = (t) => {
        const p = Math.min(1, (t - t0) / 500), e = 1 - Math.pow(1 - p, 3);
        for (const k in target) shown[k] = from[k] + (target[k] - from[k]) * e;
        $("#rYear").textContent = money(shown.year); $("#rNow").textContent = money(shown.now) + "/mo"; $("#rNew").textContent = money(shown.nw) + "/mo";
        $("#rMonth").textContent = money(shown.month); $("#rConv").textContent = Math.round(shown.conv).toLocaleString("en-AU");
        if (p < 1) anim = requestAnimationFrame(step);
      };
      anim = requestAnimationFrame(step);
    }
    Object.values(I).forEach((inp) => inp.addEventListener("input", update));
    update();
  })();

  /* ------------------------------------------------------------------ */
  /* 14. FAQ                                                             */
  /* ------------------------------------------------------------------ */
  $$(".faq__item").forEach((item, i) => {
    const q = $(".faq__q", item);
    q.addEventListener("click", () => {
      const open = !item.classList.contains("is-open");
      $$(".faq__item").forEach((o) => { o.classList.remove("is-open"); $(".faq__q", o).setAttribute("aria-expanded", "false"); });
      if (open) { item.classList.add("is-open"); q.setAttribute("aria-expanded", "true"); }
    });
    if (i === 0) { item.classList.add("is-open"); q.setAttribute("aria-expanded", "true"); }
  });

  /* ------------------------------------------------------------------ */
  /* 15. Case study modal                                                */
  /* ------------------------------------------------------------------ */
  const modal = $("#modal"), body = $("#modalBody");
  let lastFocus = null;
  function openCase(i) {
    const c = S.caseStudies[i]; if (!c) return;
    lastFocus = document.activeElement;
    body.innerHTML = `
      <div class="modal__media">${cover(c.series, "m" + i)}${c.image ? `<img src="${esc(c.image)}" alt="" onerror="this.remove()">` : ""}</div>
      <div class="modal__content">
        <div><span class="case__client">${esc(c.client)} · ${esc(c.industry)} · ${esc(c.year)}</span><h2 id="modalTitle">${esc(c.title)}</h2></div>
        <div class="case__kpis">${c.kpis.map((k) => `<div><strong class="${k.value < 0 ? "neg" : ""}">${fmt(k.value, { decimals: k.decimals || 0, suffix: k.suffix || "" })}</strong><small>${esc(k.label)}</small></div>`).join("")}</div>
        <div class="modal__sec"><h4>The problem</h4><p>${esc(c.problem)}</p></div>
        <div class="modal__sec"><h4>The approach</h4><p>${esc(c.approach)}</p></div>
        <div class="modal__sec"><h4>The result</h4><p>${esc(c.result)}</p></div>
        <div class="modal__tags">${(c.services || []).map((s) => `<span>${esc(s)}</span>`).join("")}</div>
        <div><a href="#contact" class="btn btn--red">Get results like these →</a></div>
      </div>`;
    modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false"); lock(true);
    $(".modal__close").focus();
  }
  function closeModal() { if (!modal.classList.contains("is-open")) return; modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); lock(false); lastFocus && lastFocus.focus(); }
  document.addEventListener("click", (e) => {
    const card = e.target.closest(".case[data-case]");
    if (card && !e.target.closest("a")) return openCase(+card.dataset.case);
    if (e.target.closest("[data-close]")) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeModal(); closeMenu(); }
    if ((e.key === "Enter" || e.key === " ") && e.target.matches(".case[data-case]")) { e.preventDefault(); openCase(+e.target.dataset.case); }
  });

  /* ------------------------------------------------------------------ */
  /* 16. Email copy + toast                                              */
  /* ------------------------------------------------------------------ */
  const toast = (msg) => { const t = $("#toast"); t.textContent = msg; t.classList.add("is-on"); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove("is-on"), 2200); };
  $("#emailBtn").addEventListener("click", async (e) => {
    try { await navigator.clipboard.writeText(S.email); toast("✱ Email copied. Talk soon."); }
    catch { location.href = "mailto:" + S.email; }
    const r = e.currentTarget.getBoundingClientRect(); pop(r.right - 30, r.top + r.height / 2, 12);
  });

  /* ------------------------------------------------------------------ */
  /* 17. Contact form                                                    */
  /* ------------------------------------------------------------------ */
  const form = $("#contactForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    let ok = true;
    $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); f.closest(".field").classList.toggle("is-error", bad); if (bad) ok = false; });
    if (!ok) { toast("A couple of fields need a look."); return; }
    const d = new FormData(form), note = $("#formNote");
    const needs = d.getAll("needs").join(", ") || "—";
    if (/YOUR_FORM_ID/.test(form.action)) {
      const msg = `Name: ${d.get("name")}\nEmail: ${d.get("email")}\nNeeds: ${needs}\nBudget: ${d.get("budget") || "Not sure"}\n\n${d.get("message")}`;
      location.href = `mailto:${S.email}?subject=${encodeURIComponent("Project enquiry from " + d.get("name"))}&body=${encodeURIComponent(msg)}`;
      form.classList.add("is-sent"); note.textContent = "Opening your email app…"; return;
    }
    note.textContent = "Sending…";
    try {
      const res = await fetch(form.action, { method: "POST", body: d, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error();
      form.classList.add("is-sent"); note.textContent = "Got it. Reply within one business day."; form.reset();
      const b = $(".form .btn").getBoundingClientRect(); pop(b.left + b.width / 2, b.top, 20);
    } catch { note.textContent = "Something broke. Email me at " + S.email; }
  });
})();
