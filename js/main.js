/* =========================================================================
   main.js — mastha portfolio. Rendering, UV torch engine and motion.
   Content lives in js/content.js.
   ========================================================================= */
(function () {
  "use strict";

  const S = window.SITE || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const root = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const G = typeof gsap !== "undefined";
  if (G && typeof ScrollTrigger !== "undefined") gsap.registerPlugin(ScrollTrigger);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");
  const SPARK = '<svg aria-hidden="true"><use href="#spark"/></svg>';
  const PLUS = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>';

  /* ------------------------------------------------------------------ */
  /* Smooth scroll                                                       */
  /* ------------------------------------------------------------------ */
  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduce) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  const goTo = (el) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: el.id === "top" ? 0 : -24, duration: 1.4 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href"); if (id === "#") return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); closeModal(); goTo(el);
  });

  /* ------------------------------------------------------------------ */
  /* Charts                                                              */
  /* ------------------------------------------------------------------ */
  let uid = 0;
  function lineChart(series, { W = 400, H = 160, pad = 10, grid = true, dots = true } = {}) {
    const id = "lc" + uid++;
    const max = Math.max(...series), min = Math.min(...series), r = max - min || 1;
    const p = series.map((v, i) => [pad + (i / (series.length - 1)) * (W - pad * 2), H - pad - ((v - min) / r) * (H - pad * 2.4)]);
    let d = `M${p[0][0]},${p[0][1]}`;
    for (let i = 1; i < p.length; i++) { const [x0, y0] = p[i - 1], [x1, y1] = p[i], c = (x0 + x1) / 2; d += ` C${c},${y0} ${c},${y1} ${x1},${y1}`; }
    const l = p[p.length - 1];
    const g = grid ? [.25, .5, .75].map((f) => `<line x1="0" x2="${W}" y1="${H * f}" y2="${H * f}" stroke="rgba(236,232,244,.06)" stroke-dasharray="3 5"/>`).join("") : "";
    const pts = dots ? p.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2" fill="#B596FF" opacity=".5"/>`).join("") : "";
    return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="${id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7844E9" stop-opacity=".45"/><stop offset="1" stop-color="#7844E9" stop-opacity="0"/></linearGradient></defs>${g}
      <path d="${d} L${l[0]},${H} L${p[0][0]},${H}Z" fill="url(#${id})"/>
      <path d="${d}" fill="none" stroke="#B596FF" stroke-width="2.4" stroke-linecap="round" filter="url(#uvglow)"/>${pts}
      <circle cx="${l[0]}" cy="${l[1]}" r="4.5" fill="#DCCBFF"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/></circle></svg>`;
  }
  function cover(seed) {
    const rnd = (n) => { const x = Math.sin(seed * 99 + n * 7.13) * 10000; return x - Math.floor(x); };
    let s = "";
    for (let i = 0; i < 9; i++) s += `<circle cx="${280 + rnd(i) * 60}" cy="${90 + rnd(i + 3) * 40}" r="${20 + i * 22}" fill="none" stroke="rgba(181,150,255,${(0.5 - i * 0.05).toFixed(2)})" stroke-width="1"/>`;
    for (let i = 0; i < 14; i++) { const h = 20 + rnd(i + 20) * 90 + i * 4; s += `<rect x="${20 + i * 17}" y="${180 - h}" width="9" height="${h}" rx="2" fill="url(#cg${seed})" opacity="${0.35 + i * 0.045}"/>`; }
    return `<svg viewBox="0 0 400 225" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="cg${seed}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#B596FF"/><stop offset="1" stop-color="#2A1566"/></linearGradient><radialGradient id="cr${seed}" cx=".75" cy=".3" r=".7"><stop offset="0" stop-color="#7844E9" stop-opacity=".45"/><stop offset="1" stop-color="#7844E9" stop-opacity="0"/></radialGradient></defs><rect width="400" height="225" fill="url(#cr${seed})"/>${s}</svg>`;
  }

  /* ------------------------------------------------------------------ */
  /* Render                                                              */
  /* ------------------------------------------------------------------ */
  function render() {
    if (S.clients) { const one = S.clients.map((c) => `<span>${esc(c)} ${SPARK}</span>`).join(""); $("#clients").innerHTML = one + one; }

    if (S.stats) $("#stats").innerHTML = S.stats.map((s) => `
      <div class="stat reveal"><strong><span data-count="${s.value}" data-decimals="${s.decimals || 0}" data-prefix="${esc(s.prefix || "")}">0</span><i>${esc(s.suffix || "")}</i></strong><span>${esc(s.label)}</span>${lineChart(s.spark, { W: 200, H: 38, pad: 4, grid: false, dots: false })}</div>`).join("");

    if (S.services) $("#services-list").innerHTML = S.services.map((s, i) => `
      <li class="svc__item reveal${i === 0 ? " is-open" : ""}">
        <button class="svc__head" aria-expanded="${i === 0}" aria-controls="svc${i}">
          <span class="svc__n">0${i + 1}</span><span class="svc__title">${esc(s.title)}</span><span class="svc__short">${esc(s.short)}</span><span class="svc__plus">${PLUS}</span>
        </button>
        <div class="svc__body" id="svc${i}"><div><div class="svc__inner"><p>${esc(s.text)}</p><ul>${s.deliver.map((d) => `<li>${esc(d)}</li>`).join("")}</ul></div></div></div>
      </li>`).join("");

    if (S.caseStudies) $("#files").innerHTML = S.caseStudies.map((c, i) => `
      <article class="file" style="--i:${i}" data-case="${i}" data-cursor="Open file" tabindex="0" role="button" aria-label="Open case file: ${esc(c.title)}">
        <div class="file__main">
          <div class="file__tab"><span>Case file <b>${esc(c.file)}</b></span><span class="file__class">Classified</span></div>
          <h3>${esc(c.title)}</h3>
          <p class="file__meta">${esc(c.client)} · ${esc(c.industry)} · ${esc(c.year)}</p>
          <p>${esc(c.summary)}</p>
          <div class="file__tags">${c.tags.map((t) => `<span>${esc(t)}</span>`).join("")}</div>
          <span class="file__open">Open full report <i>→</i></span>
        </div>
        <div class="file__data">
          <span class="stamp">Declassified</span>
          <div class="file__chart">${lineChart(c.series)}</div>
          <div class="kpis">${c.kpis.map((k, j) => `<div class="kpi"><span class="redact" style="--d:${j * 0.12}s"><span class="redact__bar"></span><b class="uv">${esc(k.v)}</b></span><small>${esc(k.l)}</small></div>`).join("")}</div>
        </div>
      </article>`).join("");

    if (S.process) $("#steps").innerHTML = S.process.map((p, i) => `<li class="step reveal" data-step="${i}"><b>0${i + 1}</b><strong>${esc(p.title)}</strong><p>${esc(p.text)}</p></li>`).join("");

    if (S.stack) $("#stack").innerHTML = S.stack.map((g) => `<div class="tool-card reveal"><h3>${esc(g.group)}</h3><ul>${g.tools.map((t) => `<li>${esc(t)}</li>`).join("")}</ul></div>`).join("");

    if (S.experience) $("#timeline").innerHTML = S.experience.map((e) => `<li class="job reveal"><span class="job__period">${esc(e.period)}</span><h3>${esc(e.role)}</h3><span class="job__org">${esc(e.org)}</span><p>${esc(e.text)}</p><div class="job__tags">${(e.tags || []).map((t) => `<span>${esc(t)}</span>`).join("")}</div></li>`).join("");
    if (S.education) $("#education").innerHTML = S.education.map((e) => `<li><small>${esc(e.period)}</small><strong>${esc(e.title)}</strong><span>${esc(e.org)}</span></li>`).join("");
    if (S.certifications) $("#certs").innerHTML = S.certifications.map((c) => `<li>${esc(c)}</li>`).join("");

    if (S.testimonials) {
      $("#quoteSlides").innerHTML = S.testimonials.map((t, i) => `<blockquote class="qs${i === 0 ? " is-on" : ""}"><p>${esc(t.quote)}</p><footer><span class="qs__av">${esc(t.name.split(" ").map((w) => w[0]).join("").slice(0, 2))}</span><div><strong>${esc(t.name)}</strong><small>${esc(t.role)}</small></div></footer></blockquote>`).join("");
      $("#qDots").innerHTML = S.testimonials.map((_, i) => `<button aria-label="Testimonial ${i + 1}" class="${i === 0 ? "is-on" : ""}"></button>`).join("");
    }

    if (S.insights) $("#posts").innerHTML = S.insights.map((p, i) => `<a class="post reveal" href="${esc(p.href || "#")}" data-cursor="Read"><div class="post__cover">${cover(i + 1)}</div><div class="post__body"><div class="post__meta"><b>${esc(p.tag)}</b><span>${esc(p.date)} · ${p.minutes} min</span></div><h3>${esc(p.title)}</h3><span class="post__more">Read article →</span></div></a>`).join("");

    if (S.faq) {
      $("#faqList").innerHTML = S.faq.map((f, i) => `<div class="faq__item reveal${i === 0 ? " is-open" : ""}"><button class="faq__q" aria-expanded="${i === 0}" aria-controls="fq${i}"><span>${esc(f.q)}</span>${SPARK}</button><div class="faq__a" id="fq${i}" role="region"><div><p>${esc(f.a)}</p></div></div></div>`).join("");
      const ld = document.createElement("script"); ld.type = "application/ld+json";
      ld.textContent = JSON.stringify({ "@context": "https://schema.org", "@type": "FAQPage", mainEntity: S.faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) });
      document.head.appendChild(ld);
    }

    const soc = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener">${esc(s.label)} ↗</a>`).join("");
    $("#socials").innerHTML = soc; $("#menuSocials").innerHTML = soc;
    if (S.email) $("#emailText").textContent = S.email;
    if (S.availability) $("#availability").textContent = S.availability;
    if (S.replyTime) $("#replyTime").textContent = S.replyTime;
    if (S.bookingUrl) $("#bookBtn").href = S.bookingUrl;
    $("#year").textContent = new Date().getFullYear();
  }
  render();

  /* ------------------------------------------------------------------ */
  /* Toast + sparkle burst                                               */
  /* ------------------------------------------------------------------ */
  const toast = (msg, ms = 2400) => { const t = $("#toast"); t.textContent = msg; t.classList.add("is-on"); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove("is-on"), ms); };
  function burst(x, y, n = 18) {
    if (!G || reduce) return;
    for (let i = 0; i < n; i++) {
      const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      s.innerHTML = '<use href="#spark"/>';
      Object.assign(s.style, { position: "fixed", left: 0, top: 0, width: "22px", height: "22px", color: i % 3 ? "#B596FF" : "#ECE8F4", zIndex: 9991, pointerEvents: "none", filter: "drop-shadow(0 0 6px #7844E9)" });
      document.body.appendChild(s);
      const a = (i / n) * Math.PI * 2, d = 90 + Math.random() * 160;
      gsap.fromTo(s, { x: x - 11, y: y - 11, scale: 0, rotate: 0 }, { x: x - 11 + Math.cos(a) * d, y: y - 11 + Math.sin(a) * d, scale: 0.4 + Math.random(), rotate: 180, duration: 1.1, ease: "power3.out" });
      gsap.to(s, { opacity: 0, delay: 0.7, duration: 0.5, onComplete: () => s.remove() });
    }
  }

  /* ------------------------------------------------------------------ */
  /* UV torch engine                                                     */
  /* ------------------------------------------------------------------ */
  const torch = { x: -999, y: -999, tx: -999, ty: -999, user: false, lastTouch: 0 };
  const visibleUV = new Set();
  const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting ? visibleUV.add(e.target) : visibleUV.delete(e.target)), { rootMargin: "200px" });
  $$(".uv").forEach((el) => io.observe(el));
  const notes = $$("[data-note]"), dwell = new Map();
  let found = 0;
  $("#foundT").textContent = notes.length;

  function markFound(n) {
    if (n.classList.contains("found")) return;
    n.classList.add("found"); found++;
    $("#foundN").textContent = found;
    const hud = $("#hud"); hud.classList.remove("pulse"); void hud.offsetWidth; hud.classList.add("pulse");
    if (found === notes.length) {
      toast("✦ All 7 notes found. You'd make a great analyst. Let's talk.", 4200);
      const r = $("#hudCount").getBoundingClientRect(); burst(r.left + 40, r.top, 30);
    } else toast(`✦ Hidden note ${found}/${notes.length} found`);
  }

  if (fine) {
    addEventListener("mousemove", (e) => { torch.tx = e.clientX; torch.ty = e.clientY; torch.user = true; }, { passive: true });
    document.addEventListener("mouseleave", () => { torch.tx = torch.ty = -999; });
  } else {
    const t = (e) => { const p = e.touches[0]; if (!p) return; torch.tx = p.clientX; torch.ty = p.clientY - 70; torch.lastTouch = performance.now(); torch.user = true; };
    addEventListener("touchstart", t, { passive: true });
    addEventListener("touchmove", t, { passive: true });
  }
  const hero = $("#top");
  let heroVisible = true;
  new IntersectionObserver(([e]) => (heroVisible = e.isIntersecting), { threshold: 0.2 }).observe(hero);

  let last = performance.now();
  function frame(now) {
    const dt = Math.min(64, now - last); last = now;
    // touch devices: wander through the hero when the finger isn't on screen
    if (!fine && heroVisible && now - torch.lastTouch > 2500) {
      const r = hero.getBoundingClientRect(), t = now / 1000;
      torch.tx = r.left + r.width * (0.5 + 0.38 * Math.sin(t * 0.7)); torch.ty = r.top + r.height * (0.45 + 0.3 * Math.sin(t * 1.1 + 1));
    }
    const k = fine ? 0.35 : 0.12;
    torch.x += (torch.tx - torch.x) * k; torch.y += (torch.ty - torch.y) * k;
    root.style.setProperty("--mx", torch.x.toFixed(1) + "px"); root.style.setProperty("--my", torch.y.toFixed(1) + "px");

    // read all rects first, then write (avoids layout thrash)
    const items = [...visibleUV].map((el) => [el, el.getBoundingClientRect()]);
    items.forEach(([el, r]) => { el.style.setProperty("--x", (torch.x - r.left).toFixed(1) + "px"); el.style.setProperty("--y", (torch.y - r.top).toFixed(1) + "px"); });

    // note hunt
    if (torch.user || !fine) notes.forEach((n) => {
      if (n.classList.contains("found") || !visibleUV.has(n)) return;
      const r = n.getBoundingClientRect(), d = Math.hypot(torch.x - (r.left + r.width / 2), torch.y - (r.top + r.height / 2));
      const v = d < Math.max(110, r.width / 2) ? (dwell.get(n) || 0) + dt : 0;
      dwell.set(n, v); if (v > 450) markFound(n);
    });

    // declassify case files when the torch rests on the numbers
    if (fine) $$(".file:not(.declassified)").forEach((f) => {
      const k2 = f.querySelector(".kpis").getBoundingClientRect();
      const inside = torch.x > k2.left - 30 && torch.x < k2.right + 30 && torch.y > k2.top - 30 && torch.y < k2.bottom + 30;
      const v = inside ? (dwell.get(f) || 0) + dt : 0; dwell.set(f, v);
      if (v > 380) declassify(f);
    });
    requestAnimationFrame(frame);
  }
  if (!reduce) requestAnimationFrame(frame);
  else document.body.classList.add("uv-all");

  function declassify(f) { if (f.classList.contains("declassified")) return; f.classList.add("declassified"); f.querySelector(".file__class").textContent = "Declassified"; }
  if (!fine) {
    const fio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { setTimeout(() => declassify(e.target), 700); fio.unobserve(e.target); } }), { threshold: 0.55 });
    $$(".file").forEach((f) => fio.observe(f));
  }

  $("#revealAll").addEventListener("click", (e) => {
    const on = document.body.classList.toggle("uv-all");
    e.currentTarget.setAttribute("aria-pressed", on); e.currentTarget.textContent = on ? "Hide ink" : "Reveal all";
    if (on) $$(".file").forEach(declassify);
  });
  $("#hudCount").addEventListener("click", () => toast(found === notes.length ? "✦ All notes found. Legend." : `✦ ${notes.length - found} hidden notes left. Keep shining.`));

  /* ------------------------------------------------------------------ */
  /* Loader + intro                                                      */
  /* ------------------------------------------------------------------ */
  function intro() {
    if (G && !reduce) gsap.to(".hero__title .line > span", { y: 0, duration: 1.2, ease: "power4.out", stagger: 0.1 });
    else $$(".hero__title .line > span").forEach((s) => (s.style.transform = "none"));
    $$(".hero .fade").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), (reduce ? 0 : 300) + i * 110));
  }
  const loader = $("#loader");
  if (loader && !reduce) {
    const lit = $(".loader__lit"), pct = $("#loaderPct"), t0 = performance.now(), dur = 1500;
    (function tick(now) {
      const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 2);
      lit.style.setProperty("--lx", (-15 + e * 130) + "%"); pct.textContent = String(Math.round(e * 100)).padStart(2, "0");
      if (p < 1) requestAnimationFrame(tick);
      else { lit.style.webkitMaskImage = lit.style.maskImage = "none"; setTimeout(() => { loader.classList.add("is-done"); intro(); }, 260); setTimeout(() => loader.remove(), 1200); }
    })(t0);
  } else { loader && loader.remove(); intro(); }

  /* ------------------------------------------------------------------ */
  /* Nav, progress, menu                                                 */
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

  const burger = $("#burger"), menu = $("#menu");
  const lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  function closeMenu() { if (!menu.classList.contains("is-open")) return; menu.classList.remove("is-open"); burger.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); menu.setAttribute("aria-hidden", "true"); lock(false); }
  burger.addEventListener("click", () => {
    if (menu.classList.contains("is-open")) return closeMenu();
    menu.classList.add("is-open"); burger.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); menu.setAttribute("aria-hidden", "false"); lock(true);
  });

  /* ------------------------------------------------------------------ */
  /* Cursor + magnetic buttons                                           */
  /* ------------------------------------------------------------------ */
  if (fine && !reduce) {
    const cur = $("#cursor"), lab = $("#cursorLabel"), dot = $(".cursor__dot"), ring = $(".cursor__ring");
    let x = -100, y = -100, rx = -100, ry = -100;
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
    (function loop() { rx += (x - rx) * 0.2; ry += (y - ry) * 0.2; dot.style.transform = `translate(${x}px,${y}px)`; ring.style.translate = `${rx}px ${ry}px`; lab.style.transform = `translate(${rx}px,${ry}px)`; requestAnimationFrame(loop); })();
    document.addEventListener("mouseover", (e) => {
      const t = e.target;
      cur.classList.toggle("is-hover", !!t.closest("a, button, input, select, textarea, label, [data-cursor]"));
      const l = t.closest("[data-cursor]")?.dataset.cursor || ""; lab.textContent = l; cur.classList.toggle("has-label", !!l);
    });
    $$("[data-magnetic]").forEach((el) => {
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
        el.style.translate = `${(mx - r.width / 2) * 0.2}px ${(my - r.height / 2) * 0.3}px`;
        el.style.setProperty("--bx", mx + "px"); el.style.setProperty("--by", my + "px");
      });
      el.addEventListener("mouseleave", () => { el.style.transition = "translate .5s cubic-bezier(.34,1.56,.64,1), background .25s, box-shadow .3s"; el.style.translate = "0 0"; setTimeout(() => (el.style.transition = ""), 500); });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Reveal + counters                                                   */
  /* ------------------------------------------------------------------ */
  const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$(".reveal").forEach((el) => rio.observe(el));
  const cio = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, dec = +el.dataset.decimals || 0, pre = el.dataset.prefix || "", t0 = performance.now();
    const f = (v) => pre + v.toFixed(dec);
    if (reduce) { el.textContent = f(to); return; }
    (function step(now) { const p = Math.min(1, (now - t0) / 1500), k = 1 - Math.pow(1 - p, 4); el.textContent = f(to * k); if (p < 1) requestAnimationFrame(step); })(t0);
  }), { threshold: 0.5 });
  $$("[data-count]").forEach((el) => cio.observe(el));

  /* ------------------------------------------------------------------ */
  /* Statement: light up word by word                                    */
  /* ------------------------------------------------------------------ */
  const st = $("#statement");
  [...st.childNodes].forEach((n) => {
    if (n.nodeType === 3) { const frag = document.createDocumentFragment(); n.textContent.split(/(\s+)/).forEach((w) => { if (!w) return; if (/^\s+$/.test(w)) frag.append(w); else { const s = document.createElement("span"); s.className = "w"; s.textContent = w; frag.append(s); } }); n.replaceWith(frag); }
    else if (n.nodeType === 1) n.classList.add("w");
  });
  const words = $$(".w", st);
  if (G && !reduce) ScrollTrigger.create({ trigger: st, start: "top 80%", end: "bottom 45%", scrub: true, onUpdate: (s) => { const on = Math.round(s.progress * words.length); words.forEach((w, i) => w.classList.toggle("on", i < on)); } });
  else words.forEach((w) => w.classList.add("on"));

  /* ------------------------------------------------------------------ */
  /* Case files: stacking depth                                          */
  /* ------------------------------------------------------------------ */
  if (G && !reduce) {
    const mm = gsap.matchMedia();
    mm.add("(min-width: 1025px)", () => {
      const files = $$(".file");
      files.slice(0, -1).forEach((f, i) => {
        gsap.to(f, { scale: 0.95, filter: "brightness(.7)", ease: "none", scrollTrigger: { trigger: files[i + 1], start: "top 70%", end: "top 130px", scrub: true } });
      });
    });
    addEventListener("load", () => ScrollTrigger.refresh());
  }

  /* ------------------------------------------------------------------ */
  /* Services accordion                                                  */
  /* ------------------------------------------------------------------ */
  $$(".svc__item").forEach((it) => {
    const b = $(".svc__head", it);
    b.addEventListener("click", () => { const open = !it.classList.contains("is-open"); it.classList.toggle("is-open", open); b.setAttribute("aria-expanded", open); });
  });

  /* ------------------------------------------------------------------ */
  /* Growth lab                                                          */
  /* ------------------------------------------------------------------ */
  (function lab() {
    const c = Object.assign({ visitors: 20000, conversion: 1.5, value: 120, lift: 30 }, S.calculator);
    const I = { v: $("#iVisitors"), c: $("#iConversion"), a: $("#iValue"), l: $("#iLift") };
    I.v.value = c.visitors; I.c.value = c.conversion; I.a.value = c.value; I.l.value = c.lift;
    const chart = $("#labChart"); chart.innerHTML = Array.from({ length: 12 }, (_, i) => `<i class="${i < 4 ? "base" : ""}"></i>`).join("");
    const bars = $$("i", chart), shown = { y: 0, now: 0, nw: 0, cv: 0 }; let raf;
    function update() {
      Object.values(I).forEach((inp) => inp.style.setProperty("--p", ((inp.value - inp.min) / (inp.max - inp.min) * 100) + "%"));
      const v = +I.v.value, cr = +I.c.value / 100, a = +I.a.value, l = +I.l.value / 100;
      $("#oVisitors").textContent = v.toLocaleString("en-AU"); $("#oConversion").textContent = (+I.c.value).toFixed(1) + "%";
      $("#oValue").textContent = money(a); $("#oLift").textContent = "+" + I.l.value + "%";
      const now = v * cr * a, nw = now * (1 + l), tgt = { y: (nw - now) * 12, now, nw, cv: v * cr * l };
      bars.forEach((b, i) => { const ramp = i < 4 ? 0 : Math.min(1, (i - 3) / 5); b.style.height = ((now + (nw - now) * ramp) / nw * 100).toFixed(1) + "%"; });
      cancelAnimationFrame(raf); const from = { ...shown }, t0 = performance.now();
      (function step(t) {
        const p = Math.min(1, (t - t0) / 500), e = 1 - Math.pow(1 - p, 3);
        for (const k in tgt) shown[k] = from[k] + (tgt[k] - from[k]) * e;
        $("#rYear").textContent = money(shown.y); $("#rNow").textContent = money(shown.now) + "/mo"; $("#rNew").textContent = money(shown.nw) + "/mo"; $("#rConv").textContent = Math.round(shown.cv).toLocaleString("en-AU");
        if (p < 1) raf = requestAnimationFrame(step);
      })(t0);
    }
    Object.values(I).forEach((inp) => inp.addEventListener("input", update)); update();
  })();

  /* ------------------------------------------------------------------ */
  /* Terminal process                                                    */
  /* ------------------------------------------------------------------ */
  (function terminal() {
    const body = $("#termBody"), steps = $$(".step"), P = S.process || [];
    const setStep = (i) => steps.forEach((s, k) => s.classList.toggle("is-on", k === i));
    const full = () => P.map((p) => `<span class="p">$</span> ${esc(p.cmd)}\n<span class="ok">✓</span> ${esc(p.out)}\n`).join("\n");
    if (reduce) { body.innerHTML = full() + '\n<span class="p">$</span> <span class="c"></span>'; setStep(P.length - 1); return; }
    let started = false;
    new IntersectionObserver(([e], o) => { if (e.isIntersecting && !started) { started = true; o.disconnect(); run(); } }, { threshold: 0.4 }).observe($("#term"));
    async function run() {
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      let html = "";
      for (let i = 0; i < P.length; i++) {
        setStep(i);
        html += '<span class="p">$</span> ';
        for (const ch of P[i].cmd) { html += esc(ch); body.innerHTML = html + '<span class="c"></span>'; await wait(22); }
        await wait(260); html += `\n<span class="ok">✓</span> ${esc(P[i].out)}\n\n`; body.innerHTML = html + '<span class="c"></span>'; await wait(700);
      }
      body.innerHTML = html + '<span class="p">$</span> <span class="c"></span>';
    }
  })();

  /* ------------------------------------------------------------------ */
  /* Testimonials                                                        */
  /* ------------------------------------------------------------------ */
  (function quotes() {
    const slides = $$(".qs"), dots = $$("#qDots button"); if (!slides.length) return;
    let i = 0, timer;
    const show = (n) => { i = (n + slides.length) % slides.length; slides.forEach((s, k) => s.classList.toggle("is-on", k === i)); dots.forEach((d, k) => d.classList.toggle("is-on", k === i)); };
    const auto = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => show(i + 1), 6500); };
    $("#qPrev").addEventListener("click", () => { show(i - 1); auto(); });
    $("#qNext").addEventListener("click", () => { show(i + 1); auto(); });
    dots.forEach((d, k) => d.addEventListener("click", () => { show(k); auto(); }));
    const stage = $(".quote-stage"); stage.addEventListener("mouseenter", () => clearInterval(timer)); stage.addEventListener("mouseleave", auto);
    auto();
  })();

  /* ------------------------------------------------------------------ */
  /* FAQ                                                                 */
  /* ------------------------------------------------------------------ */
  $$(".faq__item").forEach((it) => {
    const q = $(".faq__q", it);
    q.addEventListener("click", () => {
      const open = !it.classList.contains("is-open");
      $$(".faq__item").forEach((o) => { o.classList.remove("is-open"); $(".faq__q", o).setAttribute("aria-expanded", "false"); });
      if (open) { it.classList.add("is-open"); q.setAttribute("aria-expanded", "true"); }
    });
  });

  /* ------------------------------------------------------------------ */
  /* Case file modal                                                     */
  /* ------------------------------------------------------------------ */
  const modal = $("#modal"), mbody = $("#modalBody"); let lastFocus = null;
  function openCase(i) {
    const c = S.caseStudies[i]; if (!c) return; lastFocus = document.activeElement;
    mbody.innerHTML = `<div class="modal__chart">${lineChart(c.series, { W: 800, H: 200 })}</div>
      <div class="modal__content">
        <div><span class="mono muted">Case file ${esc(c.file)} · ${esc(c.client)} · ${esc(c.industry)} · ${esc(c.year)} · ${esc(c.duration)}</span><h2 id="modalTitle">${esc(c.title)}</h2></div>
        <div class="modal__kpis">${c.kpis.map((k) => `<div><strong>${esc(k.v)}</strong><small>${esc(k.l)}</small></div>`).join("")}</div>
        <div class="modal__sec"><h4>The problem</h4><p>${esc(c.problem)}</p></div>
        <div class="modal__sec"><h4>The approach</h4><p>${esc(c.approach)}</p></div>
        <div class="modal__sec"><h4>The result</h4><p>${esc(c.result)}</p></div>
        <div><a href="#contact" class="btn btn--violet">Get results like these →</a></div>
      </div>`;
    modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false"); lock(true); $(".modal__close").focus();
    declassify($$(".file")[i]);
  }
  function closeModal() { if (!modal.classList.contains("is-open")) return; modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); lock(false); lastFocus && lastFocus.focus(); }
  document.addEventListener("click", (e) => {
    const f = e.target.closest(".file[data-case]"); if (f) return openCase(+f.dataset.case);
    if (e.target.closest("[data-close]")) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeModal(); closeMenu(); }
    if ((e.key === "Enter" || e.key === " ") && e.target.matches(".file[data-case]")) { e.preventDefault(); openCase(+e.target.dataset.case); }
  });

  /* ------------------------------------------------------------------ */
  /* Contact                                                             */
  /* ------------------------------------------------------------------ */
  $("#emailBtn").addEventListener("click", async (e) => {
    try { await navigator.clipboard.writeText(S.email); toast("✦ Email copied. Talk soon."); } catch { location.href = "mailto:" + S.email; }
    const r = e.currentTarget.getBoundingClientRect(); burst(r.right - 30, r.top + r.height / 2, 12);
  });
  const form = $("#contactForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); let ok = true;
    $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); f.closest(".field").classList.toggle("is-error", bad); if (bad) ok = false; });
    if (!ok) { toast("A couple of fields need a look."); return; }
    const d = new FormData(form), note = $("#formNote"), needs = d.getAll("needs").join(", ") || "—";
    if (/YOUR_FORM_ID/.test(form.action)) {
      const msg = `Name: ${d.get("name")}\nEmail: ${d.get("email")}\nCompany: ${d.get("company") || "—"}\nNeeds: ${needs}\nBudget: ${d.get("budget") || "Not sure"}\n\n${d.get("message")}`;
      location.href = `mailto:${S.email}?subject=${encodeURIComponent("Project enquiry from " + d.get("name"))}&body=${encodeURIComponent(msg)}`;
      form.classList.add("is-sent"); note.textContent = "Opening your email app…"; return;
    }
    note.textContent = "Sending…";
    try {
      const res = await fetch(form.action, { method: "POST", body: d, headers: { Accept: "application/json" } }); if (!res.ok) throw new Error();
      form.classList.add("is-sent"); note.textContent = "Got it. Reply within one business day."; form.reset();
      const b = $(".form .btn").getBoundingClientRect(); burst(b.left + b.width / 2, b.top, 20);
    } catch { note.textContent = "Something broke. Email me at " + S.email; }
  });
})();
