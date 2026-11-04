/* =========================================================================
   core.js — shared by every page.
   Smooth scroll, UV torch engine, hidden-note hunt, nav, menu, cursor,
   reveal, counters, FAQ, email copy and form handling.
   Page scripts (home.js, pages.js, book.js, blog.js) load after this and
   may render content first; init runs on DOMContentLoaded.
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

  const UV = (window.UV = { S, $, $$, esc, reduce, fine, G, onFrame: [], torch: { x: -999, y: -999, tx: -999, ty: -999, user: false, lastTouch: 0 } });

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (typeof Lenis !== "undefined" && !reduce) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    if (G) { lenis.on("scroll", ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  UV.lenis = lenis;
  UV.goTo = (el, offset = -24) => { if (!el) return; lenis ? lenis.scrollTo(el, { offset: el.id === "top" ? 0 : offset, duration: 1.3 }) : el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); };
  UV.lock = (on) => { document.body.classList.toggle("locked", on); lenis && (on ? lenis.stop() : lenis.start()); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]'); if (!a) return;
    const id = a.getAttribute("href"); if (id === "#") return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); UV.goTo(el); history.replaceState(null, "", id);
  });

  /* ---------- Toast + sparkle burst ---------- */
  UV.toast = (msg, ms = 2400) => { const t = $("#toast"); if (!t) return; t.textContent = msg; t.classList.add("is-on"); clearTimeout(UV.toast.t); UV.toast.t = setTimeout(() => t.classList.remove("is-on"), ms); };
  UV.burst = (x, y, n = 18) => {
    if (!G || reduce) return;
    for (let i = 0; i < n; i++) {
      const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      s.innerHTML = '<use href="#spark"/>';
      Object.assign(s.style, { position: "fixed", left: 0, top: 0, width: "22px", height: "22px", color: i % 3 ? "#B596FF" : "#ECE8F4", zIndex: 9991, pointerEvents: "none", filter: "drop-shadow(0 0 6px #7844E9)" });
      document.body.appendChild(s);
      const a = (i / n) * Math.PI * 2, d = 90 + Math.random() * 160;
      gsap.fromTo(s, { x: x - 11, y: y - 11, scale: 0 }, { x: x - 11 + Math.cos(a) * d, y: y - 11 + Math.sin(a) * d, scale: 0.4 + Math.random(), rotate: 180, duration: 1.1, ease: "power3.out" });
      gsap.to(s, { opacity: 0, delay: 0.7, duration: 0.5, onComplete: () => s.remove() });
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

  /* ---------- FAQ accordion (call again after rendering new items) ---------- */
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
    const f = (v) => pre + v.toFixed(dec) + suf;
    if (reduce) { el.textContent = f(to); return; }
    (function step(now) { const p = Math.min(1, (now - t0) / 1500), k = 1 - Math.pow(1 - p, 4); el.textContent = f(to * k); if (p < 1) requestAnimationFrame(step); })(t0);
  };

  /* ---------- Shared contact helpers ---------- */
  function fillShared() {
    const soc = (S.socials || []).map((s) => `<a class="social" href="${esc(s.href)}" target="_blank" rel="noopener">${esc(s.label)} ↗</a>`).join("");
    $$("[data-socials]").forEach((el) => (el.innerHTML = soc));
    $$("[data-email-text]").forEach((el) => (el.textContent = S.email || ""));
    $$("a[data-email-link]").forEach((el) => (el.href = "mailto:" + (S.email || "")));
    $$("[data-availability]").forEach((el) => (el.textContent = S.availability || ""));
    $$("[data-reply]").forEach((el) => (el.textContent = S.replyTime || ""));
    $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
    $$("[data-copy-email]").forEach((b) => b.addEventListener("click", async (e) => {
      try { await navigator.clipboard.writeText(S.email); UV.toast("✦ Email copied. Talk soon."); } catch { location.href = "mailto:" + S.email; }
      const r = e.currentTarget.getBoundingClientRect(); UV.burst(r.right - 30, r.top + r.height / 2, 12);
    }));
  }

  /* ---------- Forms: Formspree when configured, otherwise mailto ---------- */
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
  UV.validate = (form) => {
    let ok = true;
    $$("[required]", form).forEach((f) => { const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)); f.closest(".field")?.classList.toggle("is-error", bad); if (bad) ok = false; });
    if (!ok) UV.toast("A couple of fields need a look.");
    return ok;
  };
  function bindForms() {
    $$("form.js-form").forEach((form) => form.addEventListener("submit", async (e) => {
      e.preventDefault(); if (!UV.validate(form)) return;
      const d = new FormData(form), needs = d.getAll("needs").join(", ");
      const lines = [];
      for (const [k, v] of d.entries()) if (k !== "_gotcha" && k !== "needs" && v) lines.push(`${k[0].toUpperCase() + k.slice(1)}: ${v}`);
      if (needs) lines.push("Needs: " + needs);
      await UV.sendForm(form, { subject: (form.dataset.subject || "Website enquiry") + " from " + (d.get("name") || "a visitor"), lines, onDone: () => {
        form.classList.add("is-sent"); const b = $(".btn", form)?.getBoundingClientRect(); b && UV.burst(b.left + b.width / 2, b.top, 18);
      } });
    }));
  }

  /* ---------- Init (after page scripts have rendered) ---------- */
  function init() {
    fillShared(); bindForms(); UV.bindFaq();

    /* Reveal + counters */
    const rio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); rio.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    $$(".reveal").forEach((el) => rio.observe(el));
    const cio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { cio.unobserve(e.target); UV.countUp(e.target); } }), { threshold: 0.5 });
    $$("[data-count]").forEach((el) => cio.observe(el));

    /* Nav: hide on scroll down, progress, scroll-spy for same-page links */
    const nav = $("#nav"), prog = $("#progress"); let lastY = 0;
    addEventListener("scroll", () => {
      const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
      nav && nav.classList.toggle("is-hidden", y > lastY && y > 500 && !document.body.classList.contains("locked"));
      lastY = y; prog && (prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`);
    }, { passive: true });
    const spyLinks = $$('.nav__links a[href^="#"]');
    if (spyLinks.length) {
      const spy = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) spyLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + e.target.id)); }), { rootMargin: "-45% 0px -50% 0px" });
      $$("main section[id]").forEach((s) => spy.observe(s));
    }

    /* Loader (home page only) + intro */
    const intro = () => {
      const lines = $$(".hero__title .line > span, .phero__title .line > span");
      if (G && !reduce) gsap.to(lines, { y: 0, duration: 1.2, ease: "power4.out", stagger: 0.1 });
      else lines.forEach((s) => (s.style.transform = "none"));
      $$(".hero .fade, .phero .fade").forEach((el, i) => setTimeout(() => el.classList.add("is-in"), (reduce ? 0 : 260) + i * 100));
    };
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

    /* Cursor + magnetic */
    if (fine && !reduce && $("#cursor")) {
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

    torchEngine();
    if (G) addEventListener("load", () => ScrollTrigger.refresh());
  }

  /* ---------- UV torch engine ---------- */
  function torchEngine() {
    const torch = UV.torch, visibleUV = new Set();
    const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting ? visibleUV.add(e.target) : visibleUV.delete(e.target)), { rootMargin: "200px" });
    $$(".uv").forEach((el) => io.observe(el));
    const notes = $$("[data-note]"), dwell = new Map(); let found = 0;
    const foundT = $("#foundT"); foundT && (foundT.textContent = notes.length);
    if (!notes.length && $("#hudCount")) $("#hudCount").hidden = true;

    function markFound(n) {
      if (n.classList.contains("found")) return;
      n.classList.add("found"); found++;
      $("#foundN").textContent = found;
      const hud = $("#hud"); hud.classList.remove("pulse"); void hud.offsetWidth; hud.classList.add("pulse");
      if (found === notes.length) { UV.toast(`✦ All ${notes.length} notes found. You'd make a great analyst.`, 4200); const r = $("#hudCount").getBoundingClientRect(); UV.burst(r.left + 40, r.top, 30); }
      else UV.toast(`✦ Hidden note ${found}/${notes.length} found`);
    }

    if (fine) {
      addEventListener("mousemove", (e) => { torch.tx = e.clientX; torch.ty = e.clientY; torch.user = true; }, { passive: true });
      document.addEventListener("mouseleave", () => { torch.tx = torch.ty = -999; });
    } else {
      const t = (e) => { const p = e.touches[0]; if (!p) return; torch.tx = p.clientX; torch.ty = p.clientY - 70; torch.lastTouch = performance.now(); torch.user = true; };
      addEventListener("touchstart", t, { passive: true }); addEventListener("touchmove", t, { passive: true });
    }
    const hero = $(".hero, .phero"); let heroVisible = !!hero;
    hero && new IntersectionObserver(([e]) => (heroVisible = e.isIntersecting), { threshold: 0.2 }).observe(hero);

    const reveal = $("#revealAll");
    reveal && reveal.addEventListener("click", (e) => {
      const on = document.body.classList.toggle("uv-all");
      e.currentTarget.setAttribute("aria-pressed", on); e.currentTarget.textContent = on ? "Hide ink" : "Reveal all";
      document.dispatchEvent(new CustomEvent("uv:revealall", { detail: on }));
    });
    $("#hudCount")?.addEventListener("click", () => UV.toast(found === notes.length ? "✦ All notes found. Legend." : `✦ ${notes.length - found} hidden notes left on this page. Keep shining.`));

    if (reduce) { document.body.classList.add("uv-all"); return; }
    let last = performance.now();
    (function frame(now) {
      const dt = Math.min(64, now - last); last = now;
      if (!fine && hero && heroVisible && now - torch.lastTouch > 2500) {
        const r = hero.getBoundingClientRect(), t = now / 1000;
        torch.tx = r.left + r.width * (0.5 + 0.38 * Math.sin(t * 0.7)); torch.ty = r.top + r.height * (0.45 + 0.3 * Math.sin(t * 1.1 + 1));
      }
      const k = fine ? 0.35 : 0.12;
      torch.x += (torch.tx - torch.x) * k; torch.y += (torch.ty - torch.y) * k;
      root.style.setProperty("--mx", torch.x.toFixed(1) + "px"); root.style.setProperty("--my", torch.y.toFixed(1) + "px");
      const items = [...visibleUV].map((el) => [el, el.getBoundingClientRect()]);
      items.forEach(([el, r]) => { el.style.setProperty("--x", (torch.x - r.left).toFixed(1) + "px"); el.style.setProperty("--y", (torch.y - r.top).toFixed(1) + "px"); });
      if (torch.user || !fine) notes.forEach((n) => {
        if (n.classList.contains("found") || !visibleUV.has(n)) return;
        const r = n.getBoundingClientRect(), d = Math.hypot(torch.x - (r.left + r.width / 2), torch.y - (r.top + r.height / 2));
        const v = d < Math.max(110, r.width / 2) ? (dwell.get(n) || 0) + dt : 0;
        dwell.set(n, v); if (v > 450) markFound(n);
      });
      UV.onFrame.forEach((fn) => fn(dt, torch));
      requestAnimationFrame(frame);
    })(last);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
