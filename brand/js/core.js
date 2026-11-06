/* =========================================================================
   Living Mark core.js — shared by every page.
   window.UV is the helper API that pages.js, book.js and blog.js expect.
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
  const UV = (window.UV = { S, $, $$, esc, reduce, fine, G });

  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduce) {
    lenis = new Lenis({ lerp: 0.12, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  UV.goTo = (el, offset = -80) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: el.id === "top" ? 0 : offset, duration: 1.1 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  UV.lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href"); if (id === "#") return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); UV.goTo(el); history.replaceState(null, "", id);
  });

  UV.toast = (msg, ms = 2200) => { const t = $("#toast"); if (!t) return; t.textContent = msg; t.classList.add("is-on"); clearTimeout(UV.toast.t); UV.toast.t = setTimeout(() => t.classList.remove("is-on"), ms); };
  UV.burst = (x, y, n = 16) => {   // the glyph confetti: brand icons fly out from a point
    if (reduce) return;
    const names = ["star", "spark", "bloom", "heart", "sun", "eye", "bubble", "arch"];
    for (let i = 0; i < n; i++) {
      const el = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      el.setAttribute("viewBox", "0 0 100 100"); el.setAttribute("class", "burst-g");
      el.innerHTML = `<use href="#g-${names[i % names.length]}"/>`;
      el.style.left = x - 13 + "px"; el.style.top = y - 13 + "px";
      if (i % 3 === 1) el.style.color = "#161211";
      document.body.appendChild(el);
      const a = (i / n) * Math.PI * 2 + Math.random() * 0.5, d = 90 + Math.random() * 140;
      el.animate([{ transform: "translate(0,0) scale(.3) rotate(0)", opacity: 1 }, { transform: `translate(${Math.cos(a) * d}px, ${Math.sin(a) * d + 40}px) scale(${0.7 + Math.random()}) rotate(${Math.random() * 540 - 270}deg)`, opacity: 0 }],
        { duration: 1100 + Math.random() * 500, easing: "cubic-bezier(.2,.8,.2,1)", fill: "forwards" }).onfinish = () => el.remove();
    }
  };

  const burger = $("#burger"), menu = $("#menu");
  function closeMenu() { if (!menu || !menu.classList.contains("is-open")) return; menu.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); burger.textContent = "Menu"; menu.setAttribute("aria-hidden", "true"); UV.lock(false); UV.headerTheme && UV.headerTheme(); }
  UV.closeMenu = closeMenu;
  burger && burger.addEventListener("click", () => {
    if (menu.classList.contains("is-open")) return closeMenu();
    menu.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); burger.textContent = "Close"; menu.setAttribute("aria-hidden", "false"); UV.lock(true); UV.headerTheme && UV.headerTheme();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
    if ((e.key === "g" || e.key === "G") && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) toggleGrid();
  });
  function toggleGrid() { const on = document.body.classList.toggle("show-grid"); const b = $("#gridToggle"); b && (b.textContent = on ? "Hide grid (G)" : "Show grid (G)"); }
  $("#gridToggle")?.addEventListener("click", toggleGrid);

  UV.bindFaq = (scope = document) => $$(".faq__item:not([data-bound])", scope).forEach((it) => {
    it.dataset.bound = 1; const q = $(".faq__q", it), list = it.parentElement;
    q.addEventListener("click", () => {
      const open = !it.classList.contains("is-open");
      $$(".faq__item", list).forEach((o) => { o.classList.remove("is-open"); $(".faq__q", o).setAttribute("aria-expanded", "false"); });
      if (open) { it.classList.add("is-open"); q.setAttribute("aria-expanded", "true"); }
    });
  });

  UV.countUp = (el) => {
    const to = +el.dataset.count, dec = +el.dataset.decimals || 0, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "", t0 = performance.now();
    const f = (v) => pre + v.toFixed(dec) + suf;
    if (reduce) { el.textContent = f(to); return; }
    (function step(now) { const p = Math.min(1, (now - t0) / 1600), k = 1 - Math.pow(1 - p, 4); el.textContent = f(to * k); if (p < 1) requestAnimationFrame(step); })(t0);
  };

  UV.validate = (form) => {
    let ok = true;
    $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); (f.closest(".field") || f).classList.toggle("is-error", bad); if (bad) ok = false; });
    if (!ok) UV.toast("Please check the highlighted fields.");
    return ok;
  };
  UV.sendForm = async (form, { subject, lines, onDone }) => {
    const note = $("[data-form-note]", form);
    if (/YOUR_FORM_ID/.test(form.action)) {
      location.href = `mailto:${S.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
      note && (note.textContent = "Opening your email app…"); onDone && onDone(); return true;
    }
    note && (note.textContent = "Sending…");
    try {
      const res = await fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error();
      note && (note.textContent = "Received. Reply within one business day."); onDone && onDone(); return true;
    } catch { note && (note.textContent = "Something went wrong. Email " + S.email); return false; }
  };

  /* Fit a single line of text to its container width */
  function fit() {
    $$("[data-fit]").forEach((el) => {
      el.style.fontSize = "100px"; el.style.width = "max-content";
      const sw = el.getBoundingClientRect().width; el.style.width = "";
      const w = el.parentElement.clientWidth;
      if (sw) el.style.fontSize = ((100 * w) / sw * 0.998).toFixed(2) + "px";
    });
  }

  /* Floating preview for rows with <template> */
  function previews() {
    const pv = $("#preview"); if (!pv || !fine) return;
    let x = 0, y = 0, cx = 0, cy = 0, on = false, raf;
    const loop = () => { cx += (x - cx) * 0.18; cy += (y - cy) * 0.18; pv.style.translate = `${cx + 24}px ${cy - pv.offsetHeight / 2}px`; if (on) raf = requestAnimationFrame(loop); };
    $$("[data-preview]").forEach((el) => {
      const tpl = el.querySelector("template"); if (!tpl) return;
      el.addEventListener("mouseenter", (e) => { pv.innerHTML = tpl.innerHTML; x = cx = e.clientX; y = cy = e.clientY; on = true; pv.classList.add("is-on"); cancelAnimationFrame(raf); loop(); });
      el.addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; if (x > innerWidth - 400) x -= 400; });
      el.addEventListener("mouseleave", () => { on = false; pv.classList.remove("is-on"); });
    });
  }

  function fillShared() {
    const soc = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join("");
    $$("[data-socials]").forEach((el) => (el.innerHTML = soc));
    $$("[data-email-text]").forEach((el) => (el.textContent = S.email || ""));
    $$("[data-availability]").forEach((el) => (el.textContent = S.availability || "Available"));
    $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
    $$("[data-copy-email]").forEach((b) => b.addEventListener("click", async (e) => {
      e.preventDefault();
      try { await navigator.clipboard.writeText(S.email); UV.toast("Email address copied."); } catch { location.href = "mailto:" + S.email; }
    }));
    $$("form.js-form").forEach((form) => form.addEventListener("submit", async (e) => {
      e.preventDefault(); if (!UV.validate(form)) return;
      const d = new FormData(form), lines = [];
      for (const [k, v] of d.entries()) if (k !== "_gotcha" && k !== "needs" && v) lines.push(`${k[0].toUpperCase() + k.slice(1)}: ${v}`);
      const needs = d.getAll("needs").join(", "); if (needs) lines.push("Interested in: " + needs);
      await UV.sendForm(form, { subject: (form.dataset.subject || "Website enquiry") + " from " + (d.get("name") || d.get("email") || "a visitor"), lines, onDone: () => { form.classList.add("is-sent"); const r = form.querySelector("[type=submit]").getBoundingClientRect(); UV.burst(r.left + r.width / 2, r.top + r.height / 2, 18); } });
    }));
  }


  /* Every coloured block gets a theme so the header and cursor can follow it */
  function themes() {
    $$(".ph, .art__head").forEach((el) => el.dataset.theme || (el.dataset.theme = "red"));
    $$(".cta, .ft").forEach((el) => el.dataset.theme || (el.dataset.theme = "dark"));
  }
  function themeAt(x, y) {
    const els = document.elementsFromPoint(x, y);
    for (const el of els) { if (el.closest("#nav, #cursor")) continue; if (el.closest(".menu.is-open")) return "dark"; const t = el.closest("[data-theme]"); if (t) return t.dataset.theme; }
    return "light";
  }
  function headerTheme() {
    const hd = $("#nav"); if (!hd) return;
    let q = false;
    const run = () => { q = false; const t = document.body.classList.contains("locked") ? "dark" : themeAt(innerWidth / 2, hd.offsetHeight + 2); hd.classList.toggle("is-red", t === "red"); hd.classList.toggle("is-dark", t === "dark"); hd.classList.toggle("is-blush", t === "blush"); };
    addEventListener("scroll", () => { if (!q) { q = true; requestAnimationFrame(run); } }, { passive: true });
    addEventListener("resize", run); run(); UV.headerTheme = run;
  }

  /* Custom cursor: a dot that grows into a label over anything clickable */
  function cursor() {
    const c = $("#cursor"), lab = $("#cursorLabel"); if (!c || !fine || reduce) return;
    document.documentElement.classList.add("has-cursor"); document.body.classList.add("has-cursor");
    let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y, tick = 0;
    c.classList.add("is-hidden");
    const loop = () => {
      cx += (x - cx) * 0.24; cy += (y - cy) * 0.24;
      c.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      if (++tick % 6 === 0) { const t = themeAt(x, y); c.classList.toggle("on-dark", t === "dark"); c.classList.toggle("on-red", t === "red"); }
      requestAnimationFrame(loop);
    };
    let seen = false;
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; if (!seen) { seen = true; cx = x; cy = y; } if (!e.target.closest("input, textarea, select")) c.classList.remove("is-hidden"); }, { passive: true });
    document.addEventListener("mouseleave", () => c.classList.add("is-hidden"));
    document.addEventListener("mouseover", (e) => {
      const l = e.target.closest("[data-cursor]"), a = e.target.closest("a, button, label, summary, [role=button]");
      const inField = e.target.closest("input, textarea, select");
      if (inField && !l) c.classList.add("is-hidden");
      if (l) { lab.textContent = l.dataset.cursor; c.classList.add("is-label"); c.classList.remove("is-link"); }
      else { c.classList.remove("is-label"); c.classList.toggle("is-link", !!a); }
    });
    loop();
  }

  function init() {
    themes(); fillShared(); UV.bindFaq(); fit(); previews();
    addEventListener("resize", fit); document.fonts && document.fonts.ready.then(fit);

    const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });
    $$(".rv").forEach((el) => rio.observe(el));
    const cio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { cio.unobserve(e.target); UV.countUp(e.target); } }), { threshold: 0.6 });
    $$("[data-count]").forEach((el) => cio.observe(el));

    const hd = $("#nav"); let lastY = 0;
    addEventListener("scroll", () => {
      const y = scrollY;
      hd.classList.toggle("is-scrolled", y > 10);
      hd.classList.toggle("is-hidden", y > lastY && y > 400 && !document.body.classList.contains("locked"));
      lastY = y;
    }, { passive: true });

    const tf = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", hour: "2-digit", minute: "2-digit", hour12: false });
    const ck = () => $$("[data-mel-clock]").forEach((el) => (el.textContent = tf.format(new Date())));
    ck(); setInterval(ck, 15000);

    const lines = $$(".hero .ln > span, .ph .ln > span, .contact .ln > span");
    const intro = lines.filter((l) => !l.closest(".contact"));
    if (G && !reduce) {
      gsap.to(intro, { y: 0, duration: 1.15, ease: "expo.out", stagger: 0.08, delay: 0.05 });
      const c = lines.filter((l) => l.closest(".contact"));
      c.forEach((l) => ScrollTrigger.create({ trigger: l.closest(".contact"), start: "top 75%", once: true, onEnter: () => gsap.to(l, { y: 0, duration: 1.2, ease: "expo.out" }) }));
    } else lines.forEach((l) => (l.style.transform = "none"));
    $$(".in").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), (reduce ? 0 : 350) + i * 90));
    headerTheme(); cursor();
    if (G) addEventListener("load", () => ScrollTrigger.refresh());
  }
  document.addEventListener("DOMContentLoaded", init);
})();

/* Pattern bands drift sideways as you scroll (alternate rows go opposite ways). */
(function () {
  "use strict";
  const rows = Array.from(document.querySelectorAll(".band__row"));
  if (!rows.length || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let q = false;
  const run = () => {
    q = false;
    rows.forEach((r, i) => {
      const third = r.scrollWidth / 3; if (!third) return;
      const x = (scrollY * 0.22) % third;
      r.style.transform = `translate3d(${i % 2 ? x - third : -x}px, 0, 0)`;
    });
  };
  addEventListener("scroll", () => { if (!q) { q = true; requestAnimationFrame(run); } }, { passive: true });
  run();
})();
