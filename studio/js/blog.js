/* blog.js — blog index filtering/search and article reading tools. */
(function () {
  "use strict";
  const { $, $$ } = window.UV;

  /* ---------- Index: filter chips + search ---------- */
  const cards = $$("[data-post]");
  if (cards.length && $(".blog-tools")) {
    let tag = "all", q = "";
    const apply = () => {
      let n = 0;
      cards.forEach((c) => {
        const ok = (tag === "all" || c.dataset.tags.split(",").includes(tag)) && (!q || c.dataset.text.includes(q));
        c.classList.toggle("is-hidden", !ok); if (ok && !c.classList.contains("post--soon")) n++;
      });
      $("#postCount").textContent = `${n} article${n === 1 ? "" : "s"}`;
      $("#emptyState").classList.toggle("is-on", !cards.some((c) => !c.classList.contains("is-hidden")));
    };
    const setTag = (t) => { tag = t; $$(".filter").forEach((b) => b.classList.toggle("is-on", b.dataset.filter === t)); apply(); };
    $$(".filter").forEach((b) => b.addEventListener("click", () => setTag(b.dataset.filter)));
    $$("[data-topic]").forEach((b) => b.addEventListener("click", () => { setTag(b.dataset.topic); window.UV.goTo($("#articles"), -120); }));
    $("#postSearch")?.addEventListener("input", (e) => { q = e.target.value.trim().toLowerCase(); apply(); });
    apply();
  }

  /* ---------- Article: table of contents, scroll-spy, progress, share ---------- */
  const prose = $(".prose");
  if (prose) {
    const heads = $$("h2[id]", prose);
    const items = heads.map((h) => `<li><a href="#${h.id}">${h.dataset.toc || h.textContent.replace(/^\d+\s*/, "")}</a></li>`).join("");
    $("#toc") && ($("#toc").innerHTML = items);
    $("#tocMobile") && ($("#tocMobile").innerHTML = items);
    const links = $$("#toc a");
    // active section = the last heading that has scrolled above 35% of the viewport
    const spy = () => {
      let cur = null;
      for (const h of heads) { if (h.getBoundingClientRect().top < innerHeight * 0.35) cur = h.id; else break; }
      links.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + cur));
    };

    const minutes = +(prose.dataset.minutes || 5), bar = $("#tocBar"), left = $("#tocLeft");
    const onScroll = () => {
      spy();
      const r = prose.getBoundingClientRect(), total = r.height - innerHeight * 0.6;
      const p = Math.min(1, Math.max(0, (innerHeight * 0.3 - r.top) / total));
      bar && (bar.style.width = (p * 100).toFixed(1) + "%");
      left && (left.textContent = p >= 0.99 ? "Finished. Nice work." : `${Math.max(1, Math.ceil(minutes * (1 - p)))} min left`);
    };
    addEventListener("scroll", onScroll, { passive: true }); onScroll();

    const url = encodeURIComponent(location.href), title = encodeURIComponent(document.title);
    $$("[data-share='linkedin']").forEach((a) => (a.href = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`));
    $$("[data-share='x']").forEach((a) => (a.href = `https://x.com/intent/tweet?url=${url}&text=${title}`));
    $$("[data-copy-link]").forEach((b) => b.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(location.href); window.UV.toast("✦ Link copied"); } catch { window.UV.toast("Copy the address bar link to share"); }
    }));
  }
})();
