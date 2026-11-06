/* pages.js — small behaviours for the services and contact pages. */
(function () {
  "use strict";
  const { $, $$ } = window.UV;

  /* Services: highlight the side index while scrolling */
  const idx = $$(".svcx__index a[href^='#']");
  if (idx.length) {
    const spy = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) idx.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + e.target.id));
    }), { rootMargin: "-40% 0px -55% 0px" });
    $$(".svcx__item").forEach((s) => spy.observe(s));
  }

  /* Contact: live Melbourne clock and availability status */
  const clock = $("#mClock");
  if (clock) {
    const tz = "Australia/Melbourne";
    const tf = new Intl.DateTimeFormat("en-AU", { timeZone: tz, hour: "2-digit", minute: "2-digit", hour12: false });
    const zf = new Intl.DateTimeFormat("en-AU", { timeZone: tz, timeZoneName: "short" });
    const df = new Intl.DateTimeFormat("en-US", { timeZone: tz, weekday: "short", hour: "numeric", hourCycle: "h23" });
    const tick = () => {
      const now = new Date(), parts = Object.fromEntries(df.formatToParts(now).map((p) => [p.type, p.value]));
      const h = +parts.hour, day = parts.weekday, weekend = day === "Sat" || day === "Sun";
      clock.innerHTML = `${tf.format(now)}<small>${(zf.formatToParts(now).find((p) => p.type === "timeZoneName") || {}).value || ""}</small>`;
      const status = weekend ? "Weekend in Melbourne. I'll reply on Monday." : h >= 9 && h < 18 ? "Working hours. Expect a reply today." : h < 9 ? "Early morning here. Replying after 9am." : "After hours. I'll reply tomorrow morning.";
      $("#mStatus").textContent = status;
      $$(".hours li").forEach((li) => li.classList.toggle("today", li.dataset.day === day));
    };
    tick(); setInterval(tick, 20000);
  }
})();

/* Single service page: SERP climb animation + SEO health check */
(function () {
  "use strict";
  const { $, $$, reduce } = window.UV;

  const serp = $("#serp");
  if (serp) {
    const rankEl = $("#serpRank"), note = $("#serpNote"), you = $(".serp__you", serp);
    const steps = [[9, "Month 0 · invisible"], [7, "Month 1 · tracking fixed"], [5, "Month 2 · suburb pages live"], [3, "Month 4 · map pack"], [1, "Month 6 · #1 for this search"]];
    const show = (i) => { rankEl.textContent = "#" + steps[i][0]; note.textContent = steps[i][1]; you.classList.toggle("is-top", steps[i][0] === 1); };
    if (reduce) show(steps.length - 1);
    else {
      let i = 0, timer;
      const run = () => { clearInterval(timer); i = 0; show(0); timer = setInterval(() => { i++; if (i >= steps.length) { clearInterval(timer); setTimeout(run, 3500); return; } show(i); }, 1100); };
      new IntersectionObserver(([e], o) => { if (e.isIntersecting) { o.disconnect(); setTimeout(run, 900); } }, { threshold: 0.4 }).observe(serp);
    }
  }

  const boxes = $$(".qc");
  if (boxes.length) {
    const total = boxes.length;
    const verdicts = [
      [0, "Start ticking", "Your result and the first thing to fix will appear here."],
      [1, "Plenty of room to grow", "Good news: the biggest gains come fastest at this stage. Start with your service pages and Google Business Profile."],
      [4, "Solid start, real gaps", "The basics are partly there. Suburb pages and tracking enquiries are usually the next big unlock."],
      [7, "Strong foundations", "You're ahead of most Melbourne competitors. Content and local PR are where the next wins live."],
      [8, "SEO overachiever", "Impressive. Let's find the last few percent, or talk about scaling to new suburbs."],
    ];
    let touched = false;
    const update = () => {
      const n = boxes.filter((b) => b.checked).length;
      // before any interaction show the prompt; after it, 0 ticks counts as "room to grow"
      const v = touched ? verdicts.filter(([min]) => Math.max(n, 1) >= min).pop() : verdicts[0];
      $("#qcNum").textContent = n; $("#qcBar").style.width = (n / total * 100) + "%";
      $("#qcTitle").textContent = v[1]; $("#qcText").textContent = v[2];
    };
    boxes.forEach((b) => b.addEventListener("change", () => { touched = true; update(); }));
    update();
  }
})();
