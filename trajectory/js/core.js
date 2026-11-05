/* =========================================================================
   Trajectory core.js — shared by every page.
   Exposes window.UV (the shared helper API that pages.js, book.js and
   blog.js expect), plus smooth scroll, nav, menu, cursor, section spine,
   reveal, counters, FAQ and forms.
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
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  UV.goTo = (el, offset = -90) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: el.id === "top" ? 0 : offset, duration: 1.2 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  UV.lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href"); if (id === "#") return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); UV.goTo(el); history.replaceState(null, "", id);
  });

  UV.toast = (msg, ms = 2400) => { const t = $("#toast"); if (!t) return; t.textContent = msg; t.classList.add("is-on"); clearTimeout(UV.toast.t); UV.toast.t = setTimeout(() => t.classList.remove("is-on"), ms); };
  UV.burst = (x, y, n = 14) => {
    if (reduce || !G) return;
    for (let i = 0; i < n; i++) {
      const d = document.createElement("i");
      Object.assign(d.style, { position: "fixed", left: 0, top: 0, width: "9px", height: "9px", borderRadius: "50%", background: i % 3 ? "#6A2CFF" : "#D7FF3E", zIndex: 9991, pointerEvents: "none" });
      document.body.appendChild(d);
      const a = (i / n) * Math.PI * 2, r = 70 + Math.random() * 110;
      gsap.fromTo(d, { x: x - 4, y: y - 4, scale: 0 }, { x: x - 4 + Math.cos(a) * r, y: y - 4 + Math.sin(a) * r, scale: 0.6 + Math.random(), duration: 0.9, ease: "power3.out" });
      gsap.to(d, { opacity: 0, delay: 0.55, duration: 0.4, onComplete: () => d.remove() });
    }
  };

  const burger = $("#burger"), menu = $("#menu");
  function closeMenu() { if (!menu || !menu.classList.contains("is-open")) return; menu.classList.remove("is-open"); burger.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); menu.setAttribute("aria-hidden", "true"); UV.lock(false); }
  UV.closeMenu = closeMenu;
  burger && burger.addEventListener("click", () => {
    if (menu.classList.contains("is-open")) return closeMenu();
    menu.classList.add("is-open"); burger.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); menu.setAttribute("aria-hidden", "false"); UV.lock(true);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });

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
    (function step(now) { const p = Math.min(1, (now - t0) / 1400), k = 1 - Math.pow(1 - p, 4); el.textContent = f(to * k); if (p < 1) requestAnimationFrame(step); })(t0);
  };

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
    $$("[data-availability]").forEach((el) => (el.textContent = S.availability || "Available"));
    $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
    $$("[data-copy-email]").forEach((b) => b.addEventListener("click", async (e) => {
      e.preventDefault();
      try { await navigator.clipboard.writeText(S.email); UV.toast("Email copied. Talk soon."); } catch { location.href = "mailto:" + S.email; }
      const r = e.currentTarget.getBoundingClientRect(); UV.burst(r.left + r.width / 2, r.top + r.height / 2);
    }));
    $$("form.js-form").forEach((form) => form.addEventListener("submit", async (e) => {
      e.preventDefault(); if (!UV.validate(form)) return;
      const d = new FormData(form), lines = [];
      for (const [k, v] of d.entries()) if (k !== "_gotcha" && k !== "needs" && v) lines.push(`${k[0].toUpperCase() + k.slice(1)}: ${v}`);
      const needs = d.getAll("needs").join(", "); if (needs) lines.push("Needs: " + needs);
      await UV.sendForm(form, { subject: (form.dataset.subject || "Website enquiry") + " from " + (d.get("name") || d.get("email") || "a visitor"), lines, onDone: () => {
        form.classList.add("is-sent"); const b = $(".btn", form)?.getBoundingClientRect(); b && UV.burst(b.left + b.width / 2, b.top);
      } });
    }));
  }

  function spine() {
    const nav = $("#spine"), secs = $$("[data-spine]").filter((s) => s.offsetHeight > 0);
    if (!nav || secs.length < 3) return;
    secs.forEach((s, i) => { if (!s.id) s.id = "s-" + i; });
    nav.innerHTML = '<span class="spine__fill"></span>' + secs.map((s) => `<a href="#${s.id}"><i></i><span>${esc(s.dataset.spine)}</span></a>`).join("");
    const links = $$("a", nav), fill = $(".spine__fill", nav);
    const update = () => {
      const mid = innerHeight * 0.45; let cur = 0;
      secs.forEach((s, i) => { if (s.getBoundingClientRect().top < mid) cur = i; });
      links.forEach((a, i) => { a.classList.toggle("is-on", i === cur); a.classList.toggle("is-past", i < cur); });
      const a = links[cur]; fill.style.height = a ? (a.offsetTop + a.offsetHeight / 2 - 6) + "px" : 0;
    };
    addEventListener("scroll", update, { passive: true }); update();
  }

  function init() {
    fillShared(); UV.bindFaq(); spine();
    const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.14, rootMargin: "0px 0px -6% 0px" });
    $$(".rv").forEach((el) => rio.observe(el));
    const cio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { cio.unobserve(e.target); UV.countUp(e.target); } }), { threshold: 0.5 });
    $$("[data-count]").forEach((el) => cio.observe(el));

    const nav = $("#nav"), prog = $("#progress"); let lastY = 0;
    addEventListener("scroll", () => {
      const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
      nav.classList.toggle("is-hidden", y > lastY && y > 520 && !document.body.classList.contains("locked"));
      lastY = y; prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
    }, { passive: true });

    const tf = new Intl.DateTimeFormat("en-AU", { timeZone: "Australia/Melbourne", hour: "2-digit", minute: "2-digit", hour12: false });
    const ck = () => $$("[data-mel-clock]").forEach((el) => (el.textContent = "Melbourne " + tf.format(new Date())));
    ck(); setInterval(ck, 15000);

    const lines = $$(".display .tl > span");
    if (G && !reduce) gsap.to(lines, { y: 0, duration: 1.1, ease: "power4.out", stagger: 0.1, delay: 0.05 });
    else lines.forEach((s) => (s.style.transform = "none"));
    $$(".fade").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), (reduce ? 0 : 250) + i * 90));

    const cur = $("#cursor");
    if (cur && fine && !reduce) {
      const lab = $("#cursorLabel"); let x = -50, y = -50, cx = x, cy = y;
      addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
      (function loop() { cx += (x - cx) * 0.25; cy += (y - cy) * 0.25; cur.style.transform = `translate(${cx}px, ${cy}px)`; requestAnimationFrame(loop); })();
      document.addEventListener("mouseover", (e) => {
        const t = e.target, chart = t.closest("#heroChart");
        cur.classList.toggle("is-hidden", !!chart);
        cur.classList.toggle("is-hover", !chart && !!t.closest("a, button, input, select, textarea, label, [data-cursor]"));
        const l = chart ? "" : (t.closest("[data-cursor]")?.dataset.cursor || ""); lab.textContent = l; cur.classList.toggle("has-label", !!l);
      });
      document.addEventListener("mouseleave", () => (cur.style.opacity = 0));
      document.addEventListener("mouseenter", () => (cur.style.opacity = 1));
      $$("[data-magnetic]").forEach((el) => {
        el.addEventListener("mousemove", (e) => { const r = el.getBoundingClientRect(); el.style.translate = `${(e.clientX - r.left - r.width / 2) * 0.18}px ${(e.clientY - r.top - r.height / 2) * 0.3}px`; });
        el.addEventListener("mouseleave", () => { el.style.transition = "translate .5s cubic-bezier(.34,1.56,.64,1), background .25s, box-shadow .3s"; el.style.translate = "0 0"; setTimeout(() => (el.style.transition = ""), 500); });
      });
    }
    if (G) addEventListener("load", () => ScrollTrigger.refresh());
  }
  document.addEventListener("DOMContentLoaded", init);
})();
