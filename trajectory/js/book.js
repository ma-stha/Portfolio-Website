/* =========================================================================
   book.js — free consultation booking widget.
   Slots are generated in Melbourne time (weekdays, set hours) and shown in
   the visitor's own time zone too. Requests go through Formspree when the
   form id is set, otherwise the visitor's email app. Set SITE.calendlyUrl
   in content.js to swap this widget for a Calendly embed.
   ========================================================================= */
(function () {
  "use strict";
  const { S, $, $$, esc } = window.UV;
  const booker = $("#booker"); if (!booker) return;

  if (S.calendlyUrl) {
    booker.innerHTML = `<iframe class="embed-cal" src="${esc(S.calendlyUrl)}" title="Book a free consultation"></iframe>`;
    return;
  }

  const TZ = "Australia/Melbourne";
  const LOCAL = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const SLOTS = ["09:30", "10:30", "11:30", "13:00", "14:00", "15:00", "16:30"];   // Melbourne time
  const DAYS_AHEAD = 30, LENGTH = 30;                                                 // minutes

  function offsetMin(date, tz) {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(date).map((x) => [x.type, x.value]));
    return (Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second) - date.getTime()) / 60000;
  }
  function zoned(y, m, d, h, mi) {
    let t = Date.UTC(y, m, d, h, mi); const o1 = offsetMin(new Date(t), TZ); t -= o1 * 60000;
    const o2 = offsetMin(new Date(t), TZ); if (o2 !== o1) t -= (o2 - o1) * 60000; return new Date(t);
  }
  const melbParts = (date) => Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: TZ, year: "numeric", month: "numeric", day: "numeric", weekday: "short" }).formatToParts(date).map((x) => [x.type, x.value]));
  const hash = (s) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
  const key = (y, m, d) => `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;

  /* Build availability: weekdays from tomorrow, with a few slots "taken" (demo) */
  const today = melbParts(new Date());
  const base = new Date(Date.UTC(+today.year, +today.month - 1, +today.day));
  const avail = new Map();
  for (let i = 1; i <= DAYS_AHEAD; i++) {
    const dt = new Date(base.getTime() + i * 864e5), y = dt.getUTCFullYear(), m = dt.getUTCMonth(), d = dt.getUTCDate(), wd = dt.getUTCDay();
    if (wd === 0 || wd === 6) continue;
    const list = SLOTS.filter((s) => hash(key(y, m, d) + s) % 3 !== 0).map((s) => { const [h, mi] = s.split(":").map(Number); return { label: s, start: zoned(y, m, d, h, mi) }; });
    if (list.length) avail.set(key(y, m, d), list);
  }
  const keys = [...avail.keys()];
  const first = keys[0].split("-").map(Number), last = keys[keys.length - 1].split("-").map(Number);
  let view = { y: first[0], m: first[1] - 1 }, selDay = keys[0], selSlot = null;

  const fmtLocal = (d, o) => new Intl.DateTimeFormat("en-AU", { timeZone: LOCAL, ...o }).format(d);
  const fmtMelb = (d, o) => new Intl.DateTimeFormat("en-AU", { timeZone: TZ, ...o }).format(d);
  const sameTz = offsetMin(new Date(), LOCAL) === offsetMin(new Date(), TZ);

  function renderCal() {
    const { y, m } = view, firstDow = (new Date(Date.UTC(y, m, 1)).getUTCDay() + 6) % 7, dim = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    $("#calMonth").textContent = new Intl.DateTimeFormat("en-AU", { month: "long", year: "numeric", timeZone: "UTC" }).format(new Date(Date.UTC(y, m, 1)));
    let html = ""; for (let i = 0; i < firstDow; i++) html += "<span></span>";
    const tKey = key(+today.year, +today.month - 1, +today.day);
    for (let d = 1; d <= dim; d++) {
      const k = key(y, m, d), has = avail.has(k);
      html += `<button type="button" data-day="${k}" class="${has ? "has" : ""}${k === selDay ? " is-sel" : ""}${k === tKey ? " is-today" : ""}" ${has ? "" : "disabled"} aria-label="${d}${has ? ", available" : ", unavailable"}">${d}</button>`;
    }
    $("#calDays").innerHTML = html;
    $("#calPrev").disabled = y < first[0] || (y === first[0] && m <= first[1] - 1);
    $("#calNext").disabled = y > last[0] || (y === last[0] && m >= last[1] - 1);
  }
  function renderSlots() {
    const list = avail.get(selDay) || [], [y, m, d] = selDay.split("-").map(Number);
    $("#slotsDay").textContent = new Intl.DateTimeFormat("en-AU", { weekday: "long", day: "numeric", month: "long", timeZone: "UTC" }).format(new Date(Date.UTC(y, m - 1, d)));
    $("#slotsTz").textContent = sameTz ? `Times in Melbourne (${fmtMelb(new Date(), { timeZoneName: "short" }).split(" ").pop()})` : `Melbourne time · your time (${LOCAL.replace(/_/g, " ")}) below`;
    $("#slotsList").innerHTML = list.length ? list.map((s, i) => `<button type="button" class="slot${selSlot && selSlot.start.getTime() === s.start.getTime() ? " is-sel" : ""}" data-i="${i}">${s.label}${sameTz ? "" : `<small>${fmtLocal(s.start, { weekday: "short", hour: "numeric", minute: "2-digit" })} your time</small>`}</button>`).join("") : `<p class="slots__empty">No times left on this day.</p>`;
  }
  const slotText = (s) => `${fmtMelb(s.start, { weekday: "long", day: "numeric", month: "long" })}, ${fmtMelb(s.start, { hour: "numeric", minute: "2-digit" })} Melbourne time` + (sameTz ? "" : ` (${fmtLocal(s.start, { weekday: "short", hour: "numeric", minute: "2-digit" })} your time)`);
  function updateBar() {
    $("#bookSum").innerHTML = selSlot ? `Selected: <b>${esc(slotText(selSlot))}</b>` : "Pick a day, then a time.";
    $("#toDetails").disabled = !selSlot;
  }
  function go(step) {
    $$(".panel-step", booker).forEach((p) => p.classList.toggle("is-on", p.dataset.step === String(step)));
    $$(".stepper li", booker).forEach((li, i) => { li.classList.toggle("is-on", i + 1 === step); li.classList.toggle("is-done", i + 1 < step); });
    $("#bookBar").hidden = step !== 1;
    window.UV.goTo(booker, -110);
  }

  booker.addEventListener("click", (e) => {
    const day = e.target.closest("[data-day]"); if (day && !day.disabled) { selDay = day.dataset.day; selSlot = null; renderCal(); renderSlots(); updateBar(); return; }
    const slot = e.target.closest(".slot"); if (slot) { selSlot = avail.get(selDay)[+slot.dataset.i]; renderSlots(); updateBar(); return; }
  });
  $("#calPrev").addEventListener("click", () => { view.m--; if (view.m < 0) { view.m = 11; view.y--; } renderCal(); });
  $("#calNext").addEventListener("click", () => { view.m++; if (view.m > 11) { view.m = 0; view.y++; } renderCal(); });
  $("#toDetails").addEventListener("click", () => { if (!selSlot) return; $("#pickedText").textContent = slotText(selSlot); go(2); });
  $$("[data-back]", booker).forEach((b) => b.addEventListener("click", () => go(1)));

  const form = $("#bookForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); if (!window.UV.validate(form) || !selSlot) return;
    $("#bfSlot").value = slotText(selSlot) + " · " + selSlot.start.toISOString();
    const d = new FormData(form);
    const lines = [`Requested time: ${slotText(selSlot)}`, `UTC: ${selSlot.start.toISOString()}`, `Name: ${d.get("name")}`, `Email: ${d.get("email")}`, `Website: ${d.get("website") || "—"}`, `Focus: ${d.get("focus") || "—"}`, `Budget: ${d.get("budget") || "—"}`, "", d.get("notes") || ""];
    await window.UV.sendForm(form, { subject: "Free consultation request from " + d.get("name"), lines, onDone: () => confirm(d) });
  });

  function ics(s) {
    const f = (dt) => dt.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const end = new Date(s.start.getTime() + LENGTH * 60000);
    return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//mastha//consultation//EN", "BEGIN:VEVENT", `UID:${f(s.start)}-mastha@manjilshrestha.online`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(s.start)}`, `DTEND:${f(end)}`,
      "SUMMARY:Free consultation with Manjil Shrestha (mastha)", "DESCRIPTION:30-minute growth call. Manjil will confirm by email with a meeting link.", "LOCATION:Online (link to follow)", "END:VEVENT", "END:VCALENDAR"].join("\r\n");
  }
  function confirm(d) {
    const s = selSlot, f = (dt) => dt.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""), end = new Date(s.start.getTime() + LENGTH * 60000);
    $("#cWhen").textContent = slotText(s); $("#cWho").textContent = `${d.get("name")} · ${d.get("email")}`; $("#cFocus").textContent = d.get("focus") || "General growth chat";
    $("#icsLink").href = URL.createObjectURL(new Blob([ics(s)], { type: "text/calendar" }));
    $("#gcalLink").href = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent("Free consultation with Manjil Shrestha")}&dates=${f(s.start)}/${f(end)}&details=${encodeURIComponent("30-minute growth call. Manjil will confirm by email with a meeting link.")}`;
    go(3);
    const r = $(".confirm__icon").getBoundingClientRect(); setTimeout(() => window.UV.burst(r.left + r.width / 2, r.top + r.height / 2, 24), 350);
  }

  renderCal(); renderSlots(); updateBar();
})();
