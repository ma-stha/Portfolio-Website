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
