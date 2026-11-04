/* =========================================================================
   home.js — homepage sections. Needs core.js and content.js loaded first.
   ========================================================================= */
(function () {
  "use strict";
  const { S, $, $$, esc, reduce, fine, G } = window.UV;
  const money = (n) => "$" + Math.round(n).toLocaleString("en-AU");
  const SPARK = '<svg aria-hidden="true"><use href="#spark"/></svg>';
  const PLUS = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>';

  /* ---------- Charts ---------- */
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

  /* ---------- Render ---------- */
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

  /* ---------- Case files: declassify under the torch ---------- */
  function declassify(f) { if (!f || f.classList.contains("declassified")) return; f.classList.add("declassified"); f.querySelector(".file__class").textContent = "Declassified"; }
  const dwell = new Map();
  if (fine) UV.onFrame.push((dt, torch) => {
    $$(".file:not(.declassified)").forEach((f) => {
      const k = f.querySelector(".kpis").getBoundingClientRect();
      const inside = torch.x > k.left - 30 && torch.x < k.right + 30 && torch.y > k.top - 30 && torch.y < k.bottom + 30;
      const v = inside ? (dwell.get(f) || 0) + dt : 0; dwell.set(f, v);
      if (v > 380) declassify(f);
    });
  });
  else {
    const fio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { setTimeout(() => declassify(e.target), 700); fio.unobserve(e.target); } }), { threshold: 0.55 });
    $$(".file").forEach((f) => fio.observe(f));
  }
  document.addEventListener("uv:revealall", (e) => { if (e.detail) $$(".file").forEach(declassify); });

  /* ---------- Statement word-by-word ---------- */
  const st = $("#statement");
  [...st.childNodes].forEach((n) => {
    if (n.nodeType === 3) { const frag = document.createDocumentFragment(); n.textContent.split(/(\s+)/).forEach((w) => { if (!w) return; if (/^\s+$/.test(w)) frag.append(w); else { const s = document.createElement("span"); s.className = "w"; s.textContent = w; frag.append(s); } }); n.replaceWith(frag); }
    else if (n.nodeType === 1) n.classList.add("w");
  });
  const words = $$(".w", st);
  if (G && !reduce) ScrollTrigger.create({ trigger: st, start: "top 80%", end: "bottom 45%", scrub: true, onUpdate: (s) => { const on = Math.round(s.progress * words.length); words.forEach((w, i) => w.classList.toggle("on", i < on)); } });
  else words.forEach((w) => w.classList.add("on"));

  /* ---------- Case files stacking depth ---------- */
  if (G && !reduce) gsap.matchMedia().add("(min-width: 1025px)", () => {
    const files = $$(".file");
    files.slice(0, -1).forEach((f, i) => gsap.to(f, { scale: 0.95, filter: "brightness(.7)", ease: "none", scrollTrigger: { trigger: files[i + 1], start: "top 70%", end: "top 130px", scrub: true } }));
  });

  /* ---------- Services accordion ---------- */
  $$(".svc__item").forEach((it) => { const b = $(".svc__head", it); b.addEventListener("click", () => { const open = !it.classList.contains("is-open"); it.classList.toggle("is-open", open); b.setAttribute("aria-expanded", open); }); });

  /* ---------- Growth lab ---------- */
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

  /* ---------- Terminal ---------- */
  (function terminal() {
    const body = $("#termBody"), steps = $$(".step"), P = S.process || [];
    const setStep = (i) => steps.forEach((s, k) => s.classList.toggle("is-on", k === i));
    if (reduce) { body.innerHTML = P.map((p) => `<span class="p">$</span> ${esc(p.cmd)}\n<span class="ok">✓</span> ${esc(p.out)}\n`).join("\n") + '\n<span class="p">$</span> <span class="c"></span>'; setStep(P.length - 1); return; }
    let started = false;
    new IntersectionObserver(([e], o) => { if (e.isIntersecting && !started) { started = true; o.disconnect(); run(); } }, { threshold: 0.4 }).observe($("#term"));
    async function run() {
      const wait = (ms) => new Promise((r) => setTimeout(r, ms)); let html = "";
      for (let i = 0; i < P.length; i++) {
        setStep(i); html += '<span class="p">$</span> ';
        for (const ch of P[i].cmd) { html += esc(ch); body.innerHTML = html + '<span class="c"></span>'; await wait(22); }
        await wait(260); html += `\n<span class="ok">✓</span> ${esc(P[i].out)}\n\n`; body.innerHTML = html + '<span class="c"></span>'; await wait(700);
      }
      body.innerHTML = html + '<span class="p">$</span> <span class="c"></span>';
    }
  })();

  /* ---------- Testimonials ---------- */
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

  /* ---------- Case file modal ---------- */
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
        <div><a href="book/" class="btn btn--violet">Get results like these →</a></div>
      </div>`;
    modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false"); UV.lock(true); $(".modal__close").focus();
    declassify($$(".file")[i]);
  }
  function closeModal() { if (!modal.classList.contains("is-open")) return; modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); UV.lock(false); lastFocus && lastFocus.focus(); }
  document.addEventListener("click", (e) => {
    const f = e.target.closest(".file[data-case]"); if (f) return openCase(+f.dataset.case);
    if (e.target.closest("[data-close]") || e.target.closest('a[href^="#"]')) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
    if ((e.key === "Enter" || e.key === " ") && e.target.matches(".file[data-case]")) { e.preventDefault(); openCase(+e.target.dataset.case); }
  });
})();
