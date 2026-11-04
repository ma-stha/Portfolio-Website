/* =========================================================================
   core.js — shared behaviour for the inner pages (services, book, contact,
   blog, articles). The home page keeps its own main.js.
   Exposes window.UV, a small helper API used by pages.js, book.js and
   blog.js (the name is historical; it is just the site toolkit).
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

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduce) {
    lenis = new Lenis({ lerp: 0.11, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  UV.goTo = (el, offset = -24) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: el.id === "top" ? 0 : offset, duration: 1.3 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  UV.lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href"); if (id === "#") return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); UV.goTo(el); history.replaceState(null, "", id);
  });

  /* ---------- Toast + starburst particles ---------- */
  UV.toast = (msg, ms = 2400) => { const t = $("#toast"); if (!t) return; t.textContent = msg; t.classList.add("is-on"); clearTimeout(UV.toast.t); UV.toast.t = setTimeout(() => t.classList.remove("is-on"), ms); };
  UV.burst = (x, y, n = 16) => {
    if (reduce || !G) return;
    for (let i = 0; i < n; i++) {
      const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      s.setAttribute("class", "burst-bit"); s.innerHTML = '<use href="#star"/>';
      if (i % 3 === 0) s.style.color = "#0B0B0B";
      document.body.appendChild(s);
      const a = (i / n) * Math.PI * 2 + Math.random() * 0.4, d = 110 + Math.random() * 170;
      gsap.set(s, { x: x - 14, y: y - 14, scale: 0 });
      gsap.to(s, { x: x - 14 + Math.cos(a) * d, y: y - 14 + Math.sin(a) * d + 60, scale: 0.5 + Math.random() * 1.1, rotate: Math.random() * 540 - 270, duration: 1 + Math.random() * 0.5, ease: "power3.out" });
      gsap.to(s, { opacity: 0, duration: 0.4, delay: 0.8 + Math.random() * 0.4, onComplete: () => s.remove() });
    }
  };

  /* ---------- Menu ---------- */
  const burger = $("#burger"), menu = $("#menu");
  function closeMenu() { if (!menu || !menu.classList.contains("is-open")) return; menu.classList.remove("is-open"); burger.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); menu.setAttribute("aria-hidden", "true"); UV.lock(false); }
  UV.closeMenu = closeMenu;
  burger && burger.addEventListener("click", () => {
    if (menu.classList.contains("is-open")) return closeMenu();
    menu.classList.add("is-open"); burger.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); menu.setAttribute("aria-hidden", "false"); UV.lock(true);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });

  /* ---------- FAQ ---------- */
  UV.bindFaq = (scope = document) => $$(".faq__item:not([data-bound])", scope).forEach((it) => {
    it.dataset.bound = 1; const q = $(".faq__q", it), list = it.parentElement;
    q.addEventListener("click", () => {
      const open = !it.classList.contains("is-open");
      $$(".faq__item", list).forEach((o) => { o.classList.remove("is-open"); $(".faq__q", o).setAttribute("aria-expanded", "false"); });
      if (open) { it.classList.add("is-open"); q.setAttribute("aria-expanded", "true"); }
    });
  });

  /* ---------- Count-up ---------- */
  UV.countUp = (el) => {
    const to = +el.dataset.count, dec = +el.dataset.decimals || 0, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "", t0 = performance.now();
    const f = (v) => (v < 0 ? "-" : "") + pre + Math.abs(v).toFixed(dec) + suf;
    if (reduce) { el.textContent = f(to); return; }
    (function step(now) { const p = Math.min(1, (now - t0) / 1400), k = 1 - Math.pow(1 - p, 4); el.textContent = f(to * k); if (p < 1) requestAnimationFrame(step); })(t0);
  };

  /* ---------- Forms ---------- */
  UV.validate = (form) => {
    let ok = true;
    $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); (f.closest(".field") || f).classList.toggle("is-error", bad); if (bad) ok = false; });
    if (!ok) UV.toast("A couple of fields need a look.");
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
      note && (note.textContent = "Got it. Reply within one business day."); onDone && onDone(); return true;
    } catch { note && (note.textContent = "Something broke. Email me at " + S.email); return false; }
  };

  function fillShared() {
    const soc = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener">${esc(s.label)} ↗</a>`).join("");
    $$("[data-socials]").forEach((el) => (el.innerHTML = soc));
    $$("[data-email-text]").forEach((el) => (el.textContent = S.email || ""));
    $$("[data-availability]").forEach((el) => (el.textContent = S.availability || ""));
    $$("[data-reply]").forEach((el) => (el.textContent = S.replyTime || ""));
    $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
    $$("[data-copy-email]").forEach((b) => b.addEventListener("click", async (e) => {
      try { await navigator.clipboard.writeText(S.email); UV.toast("✱ Email copied. Talk soon."); } catch { location.href = "mailto:" + S.email; }
      const r = e.currentTarget.getBoundingClientRect(); UV.burst(r.right - 30, r.top + r.height / 2, 12);
    }));
    $$("form.js-form").forEach((form) => form.addEventListener("submit", async (e) => {
      e.preventDefault(); if (!UV.validate(form)) return;
      const d = new FormData(form), lines = [];
      for (const [k, v] of d.entries()) if (k !== "_gotcha" && k !== "needs" && v) lines.push(`${k[0].toUpperCase() + k.slice(1)}: ${v}`);
      const needs = d.getAll("needs").join(", "); if (needs) lines.push("Needs: " + needs);
      await UV.sendForm(form, { subject: (form.dataset.subject || "Website enquiry") + " from " + (d.get("name") || d.get("email") || "a visitor"), lines, onDone: () => {
        form.classList.add("is-sent"); const b = $(".btn", form)?.getBoundingClientRect(); b && UV.burst(b.left + b.width / 2, b.top, 16);
      } });
    }));
  }

  /* ---------- Init ---------- */
  function init() {
    fillShared(); UV.bindFaq();

    const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });
    $$(".reveal, .h2").forEach((el) => rio.observe(el));
    const cio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { cio.unobserve(e.target); UV.countUp(e.target); } }), { threshold: 0.5 });
    $$("[data-count]").forEach((el) => cio.observe(el));

    /* Nav: hide on scroll down + progress bar */
    const nav = $("#nav"), prog = $("#progress"); let lastY = 0;
    addEventListener("scroll", () => {
      const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
      nav && nav.classList.toggle("is-hidden", y > lastY && y > 500 && !document.body.classList.contains("locked"));
      lastY = y; prog && (prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`);
    }, { passive: true });

    /* Melbourne clock in nav */
    const tf = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", hour: "2-digit", minute: "2-digit", hour12: false });
    const ck = () => $$("[data-mel-clock]").forEach((el) => (el.textContent = "MEL " + tf.format(new Date())));
    ck(); setInterval(ck, 15000);

    /* Intro: page title lines slide up, stickers pop in */
    const lines = $$(".phero__title .line > span"), stickers = $$(".sticker");
    if (G && !reduce) {
      gsap.to(lines, { y: 0, duration: 1.1, ease: "power4.out", stagger: 0.09, delay: 0.1 });
      gsap.to(".phero__title .blk", { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power3.inOut", delay: 0.45 });
      gsap.fromTo(stickers, { opacity: 0, "--s": 0 }, { opacity: 1, "--s": 1, duration: 0.7, ease: "back.out(2.2)", stagger: 0.12, delay: 0.7 });
    } else {
      lines.forEach((s) => (s.style.transform = "none")); $$(".phero__title .blk").forEach((b) => (b.style.clipPath = "none")); stickers.forEach((s) => (s.style.opacity = 1));
    }
    $$(".phero .fade").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), (reduce ? 0 : 280) + i * 90));

    /* Draggable stickers */
    $$("[data-drag]").forEach((el) => {
      let sx = 0, sy = 0, ox = 0, oy = 0, id = null;
      el.addEventListener("pointerdown", (e) => { id = e.pointerId; el.setPointerCapture(id); el.classList.add("is-dragging"); sx = e.clientX; sy = e.clientY; ox = parseFloat(el.style.getPropertyValue("--dx")) || 0; oy = parseFloat(el.style.getPropertyValue("--dy")) || 0; });
      el.addEventListener("pointermove", (e) => { if (e.pointerId !== id) return; el.style.setProperty("--dx", ox + e.clientX - sx + "px"); el.style.setProperty("--dy", oy + e.clientY - sy + "px"); });
      const end = (e) => { if (e.pointerId !== id) return; id = null; el.classList.remove("is-dragging"); el.style.setProperty("--r", (Math.random() * 20 - 10).toFixed(1) + "deg"); };
      el.addEventListener("pointerup", end); el.addEventListener("pointercancel", end);
    });
    $$("[data-pop]").forEach((el) => el.addEventListener("click", (e) => { const r = el.getBoundingClientRect(); UV.burst(r.left + r.width / 2, r.top + r.height / 2, 18); }));

    /* Starburst cursor + magnetic buttons */
    const cur = $("#cursor");
    if (cur && fine && !reduce) {
      const lab = $("#cursorLabel"); let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y;
      addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
      (function loop() { cx += (x - cx) * 0.28; cy += (y - cy) * 0.28; cur.style.transform = `translate(${cx}px, ${cy}px)`; requestAnimationFrame(loop); })();
      const RED = '.band--red, .btn--red, .blk, .sticker--pill, .tag--red, .plan--hot, .cta-band, .cal__days .is-sel, .slot.is-sel, .filter.is-on';
      document.addEventListener("mouseover", (e) => {
        const t = e.target;
        cur.classList.toggle("is-hover", !!t.closest("a, button, [data-drag], [data-cursor], input, select, textarea, label"));
        const l = t.closest("[data-cursor]")?.dataset.cursor || (t.closest("[data-drag]") ? "Drag me" : "");
        lab.textContent = l; cur.classList.toggle("has-label", !!l);
        cur.classList.toggle("on-red", !!t.closest(RED));
      });
      document.addEventListener("mouseleave", () => (cur.style.opacity = 0));
      document.addEventListener("mouseenter", () => (cur.style.opacity = 1));
      $$("[data-magnetic]").forEach((el) => {
        el.addEventListener("mousemove", (e) => { const r = el.getBoundingClientRect(); el.style.translate = `${(e.clientX - r.left - r.width / 2) * 0.22}px ${(e.clientY - r.top - r.height / 2) * 0.32}px`; });
        el.addEventListener("mouseleave", () => { el.style.transition = "translate .5s cubic-bezier(.34,1.56,.64,1), transform .25s, box-shadow .25s, background .2s, color .2s"; el.style.translate = "0 0"; setTimeout(() => (el.style.transition = ""), 500); });
      });
    }
    if (G) addEventListener("load", () => ScrollTrigger.refresh());
  }
  document.addEventListener("DOMContentLoaded", init);
})();
