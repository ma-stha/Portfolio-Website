# Single service landing page: /services/seo/  (exec'd inside build_pages.py)

def seo_service_page():
    P = '../../'
    path = 'services/seo/'
    trail = [("Home", ""), ("Services", "services/"), ("SEO", path)]
    faqs = [
        ("How long does SEO take to work in Melbourne?", "Technical fixes and Google Business Profile improvements can move rankings within weeks. Meaningful growth in organic leads usually takes three to six months, and it compounds from there."),
        ("Do you guarantee number one rankings?", "No, and be wary of anyone who does. Nobody controls Google. I commit to the work, the reporting and the leads trend, and you can see every change I make."),
        ("What's the difference between local SEO and regular SEO?", "Local SEO targets searches with a place attached, like a suburb or \"near me\", and leans on your Google Business Profile, reviews and suburb pages. Most Melbourne service businesses need both."),
        ("Do I need to write the content myself?", "No. I write briefs and can produce the content, or work with your writer. You review everything before it goes live."),
        ("Will you work on my existing website?", "Yes. I work with WordPress, Shopify, Webflow and most other platforms. If something needs a developer, I'll write a clear ticket for yours or bring one in."),
        ("How do you report on SEO?", "A monthly report and a live Looker Studio dashboard showing rankings, organic traffic and, most importantly, the enquiries and revenue organic search produced."),
    ]
    checks = [
        "Your site loads in under 3 seconds on a phone",
        "Every key service has its own page",
        "You have pages for the suburbs you serve",
        "Your Google Business Profile is complete with recent photos",
        "You got at least two new Google reviews last month",
        "You track enquiries from organic search in GA4",
        "Each page has a unique title and meta description",
        "You published something useful in the last 60 days",
    ]
    check_html = ''.join(f'<li><label><input type="checkbox" class="qc"><span>{E(c)}</span></label></li>' for c in checks)
    serp = f'''<div class="serp fade" id="serp">
            <div class="serp__bar"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><span>emergency plumber fitzroy</span></div>
            <div class="serp__map"><span class="pin"></span><span class="pin pin--2"></span><span class="pin pin--you"></span><small>Map pack · Fitzroy VIC</small></div>
            <ol class="serp__list">
              <li class="serp__you"><b class="serp__rank" id="serpRank">#9</b><div><small>yourbusiness.com.au › fitzroy</small><strong>Emergency Plumber Fitzroy · 24/7, 60-min Callouts</strong><span>★★★★★ 4.9 · 186 reviews</span></div></li>
              <li><b>#2</b><div><small>competitor-one.com.au</small><strong>Plumbers Melbourne · Call Today</strong></div></li>
              <li><b>#3</b><div><small>directory-site.com.au</small><strong>Top 10 Plumbers in Fitzroy</strong></div></li>
            </ol>
            <p class="serp__foot mono"><span id="serpNote">Month 0</span><span>Illustrative · demo</span></p>
            <div class="note uv" data-note style="--nx:-38%;--ny:30%;--rot:-6deg"><span>this is what month six<br>can look like. ↗</span></div>
          </div>'''
    body = f'''    <section class="phero" id="top">
      <div class="container">
        {crumbs_html(P, trail)}
        <div class="phero__grid phero__grid--svc">
          <div>
            <p class="label fade">Service · Search &amp; SEO</p>
            <h1 class="phero__title" aria-label="SEO services in Melbourne">
{phero_title([("SEO services in", False), ("Melbourne.", True)])}
            </h1>
            <p class="phero__lead fade">Rank for what your customers actually search, suburb by suburb. Technical fixes, local SEO, content and tracking that ties every ranking to a real enquiry.</p>
            <div class="phero__cta fade"><a href="{P}book/" class="btn btn--violet" data-magnetic>Get a free SEO audit call <span class="arr">→</span></a><a href="#pricing" class="btn btn--ghost">See SEO pricing</a></div>
            <ul class="hero__proof fade"><li><b>+212%</b><span>organic leads*</span></li><li><b>63</b><span>top-3 keywords*</span></li><li><b>3–6 mo</b><span>to results</span></li></ul>
          </div>
          {serp}
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">Sound familiar?</p><h2 class="h2 reveal">You're paying for every click because <span class="goth glow">Google</span> can't find you.</h2></div>
        <div class="pains">
          <div class="pain reveal"><b>01</b><h3>Invisible in your own suburbs</h3><p>Competitors with worse reviews show up first in the map pack and on page one.</p></div>
          <div class="pain reveal"><b>02</b><h3>Ads are doing all the work</h3><p>Turn the ads off and the phone stops ringing. Every lead has a price tag.</p></div>
          <div class="pain reveal"><b>03</b><h3>Traffic, but no enquiries</h3><p>An old SEO agency sent ranking reports, but nobody could connect them to revenue.</p></div>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head head--row"><div><p class="label reveal">What's included</p><h2 class="h2 reveal">Six parts, one <span class="goth glow">system</span>.</h2></div><p class="lead reveal">Every engagement covers all six, weighted to where your biggest gaps are.</p></div>
        <div class="incl">
          <article class="incl__item reveal"><span class="svcx__icon">{ICONS["seo"]}</span><h3>Technical SEO</h3><p>Speed, Core Web Vitals, crawlability, indexing, schema and site structure fixed first.</p></article>
          <article class="incl__item reveal"><span class="svcx__icon">{ICONS["strategy"]}</span><h3>Keyword strategy</h3><p>A keyword map built from real search demand in Melbourne, matched to pages that can win.</p></article>
          <article class="incl__item reveal"><span class="svcx__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0112 2.5a7 7 0 017 7C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span><h3>Local SEO &amp; GBP</h3><p>Google Business Profile, suburb pages, reviews and local citations for the map pack.</p></article>
          <article class="incl__item reveal"><span class="svcx__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/></svg></span><h3>On-page &amp; content</h3><p>Service pages and articles that answer real questions, written to rank and to convert.</p></article>
          <article class="incl__item reveal"><span class="svcx__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/></svg></span><h3>Links &amp; local PR</h3><p>Earned mentions from Melbourne publications, associations and partners. No link farms.</p></article>
          <article class="incl__item reveal"><span class="svcx__icon">{ICONS["analytics"]}</span><h3>Tracking &amp; reporting</h3><p>Organic enquiries and revenue tracked in GA4, with a live dashboard you can open any time.</p></article>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">The roadmap</p><h2 class="h2 reveal">Your first <span class="goth glow">six months</span>.</h2></div>
        <ol class="roadmap">
          <li class="reveal"><span class="roadmap__when mono">Month 1</span><h3>Audit &amp; fix</h3><ul class="ticks"><li>Technical audit</li><li>Tracking set up in GA4</li><li>Critical fixes shipped</li></ul><p class="roadmap__ms">Milestone: clean foundation</p></li>
          <li class="reveal"><span class="roadmap__when mono">Month 2</span><h3>Architecture</h3><ul class="ticks"><li>Keyword map</li><li>Service pages rebuilt</li><li>First suburb pages</li></ul><p class="roadmap__ms">Milestone: pages that can rank</p></li>
          <li class="reveal"><span class="roadmap__when mono">Month 3</span><h3>Local &amp; content</h3><ul class="ticks"><li>GBP optimised</li><li>Review engine running</li><li>Content cadence starts</li></ul><p class="roadmap__ms">Milestone: map pack movement</p></li>
          <li class="reveal"><span class="roadmap__when mono">Months 4–6</span><h3>Compound</h3><ul class="ticks"><li>More suburbs and topics</li><li>Local PR and links</li><li>Double down on winners</li></ul><p class="roadmap__ms">Milestone: organic leads grow</p></li>
        </ol>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container qc-grid">
        <div>
          <p class="label reveal">Free SEO health check</p>
          <h2 class="h2 reveal">How healthy is your <span class="goth glow">SEO</span>?</h2>
          <p class="lead reveal">Tick what's true for your business. Thirty seconds, no email required.</p>
          <ul class="checklist qc-list reveal" style="margin-top:26px">{check_html}</ul>
        </div>
        <aside class="qc-score reveal" aria-live="polite">
          <p class="label-sm">Your score</p>
          <p class="qc-num"><span id="qcNum">0</span><small>/ {len(checks)}</small></p>
          <div class="qc-meter"><i id="qcBar"></i></div>
          <h3 id="qcTitle">Start ticking</h3>
          <p id="qcText" class="muted">Your result and the first thing to fix will appear here.</p>
          <a href="{P}book/" class="btn btn--violet btn--block" data-magnetic>Book a free SEO audit call →</a>
          <div class="note uv" data-note style="--nx:8%;--ny:-12%;--rot:-4deg"><span>honesty mode: on. nobody's watching.</span></div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <article class="case-mini reveal">
          <div class="case-mini__body">
            <p class="label-sm">Case file 002 · Home services · demo</p>
            <h2>Owning local search across 60+ Melbourne suburbs</h2>
            <p>A multi-location service business relied on word of mouth and paid leads. Organic search drove under 5% of enquiries. We rebuilt the site around suburb pages, fixed Core Web Vitals and ran a monthly GBP and content routine.</p>
            <div class="kpis">
              <div class="kpi"><b class="kpi__v" data-count="212" data-prefix="+" data-suffix="%">0</b><small>Organic enquiries</small></div>
              <div class="kpi"><b class="kpi__v" data-count="63">0</b><small>Top-3 keywords</small></div>
              <div class="kpi"><b class="kpi__v" data-count="-33" data-suffix="%">0</b><small>Blended cost per lead</small></div>
              <div class="kpi"><b class="kpi__v">12 mo</b><small>Programme</small></div>
            </div>
            <a href="{P}#work" class="link">More case files →</a>
          </div>
          <div class="case-mini__chart">{spark_svg([4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31], 480, 260).replace('class="svcx__spark"', 'class="case-mini__svg"')}<span class="mono muted small">Organic enquiries / month · 12 months</span></div>
        </article>
      </div>
    </section>

    <section class="section" id="pricing">
      <div class="container">
        <div class="head head--row"><div><p class="label reveal">SEO pricing</p><h2 class="h2 reveal">Clear prices, <span class="goth glow">no</span> lock-in.</h2></div><p class="lead reveal">Start with an audit or go straight to a monthly programme. Retainers are month to month after 90 days.</p></div>
        <div class="plans">
          <article class="plan reveal">
            <p class="plan__h">One-off</p><h3>SEO Audit</h3><p class="plan__for">A full diagnosis and a prioritised fix list.</p>
            <p class="plan__price">$1,500 <small>one-off</small></p>
            <ul class="ticks"><li>Technical and on-page audit</li><li>Keyword and competitor gap analysis</li><li>Local SEO and GBP review</li><li>Prioritised 90-day plan</li><li>60-minute walkthrough</li></ul>
            <a href="{P}book/" class="btn btn--ghost btn--block">Book an audit</a>
          </article>
          <article class="plan plan--hot reveal">
            <span class="plan__badge">Most popular</span>
            <p class="plan__h">Monthly</p><h3>Local SEO</h3><p class="plan__for">For service businesses winning in their suburbs.</p>
            <p class="plan__price">$1,800 <small>/ month</small></p>
            <ul class="ticks"><li>Everything in the audit</li><li>Up to 5 suburb or service pages a month</li><li>GBP management and review engine</li><li>Local citations and PR</li><li>Monthly report and live dashboard</li></ul>
            <a href="{P}book/" class="btn btn--violet btn--block" data-magnetic>Start local SEO →</a>
          </article>
          <article class="plan reveal">
            <p class="plan__h">Monthly</p><h3>Growth SEO</h3><p class="plan__for">For eCommerce and multi-location brands.</p>
            <p class="plan__price">$3,200 <small>/ month</small></p>
            <ul class="ticks"><li>Everything in Local SEO</li><li>Category and product page SEO</li><li>4 long-form articles a month</li><li>Digital PR outreach</li><li>Fortnightly strategy call</li></ul>
            <a href="{P}book/" class="btn btn--ghost btn--block">Talk growth SEO</a>
          </article>
        </div>
        <p class="fine-print">Demo pricing in AUD, excluding GST. *Results shown are from a demo case study.</p>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container faq__grid">
        <div><p class="label reveal">SEO FAQ</p><h2 class="h2 reveal">SEO questions, <span class="goth glow">straight</span> answers.</h2><p class="lead reveal">Still unsure? <a class="link" href="{P}contact/">Ask me directly.</a></p></div>
        <div class="faq__list">
{faq_block(faqs)}
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head head--row"><div><p class="label reveal">Pairs well with</p><h2 class="h2 reveal">Related <span class="goth glow">services</span>.</h2></div><a href="{P}services/" class="link reveal">All services →</a></div>
        <div class="related-svc">
          <a class="method reveal" href="{P}services/#analytics"><span class="method__icon">{ICONS["analytics"]}</span><h3>Analytics &amp; Tracking</h3><p>Know exactly which rankings produce enquiries.</p><span class="method__go">Explore →</span></a>
          <a class="method reveal" href="{P}services/#cro"><span class="method__icon">{ICONS["cro"]}</span><h3>Conversion (CRO)</h3><p>Turn more of your new organic traffic into leads.</p><span class="method__go">Explore →</span></a>
          <a class="method reveal" href="{P}services/#paid"><span class="method__icon">{ICONS["paid"]}</span><h3>Paid Media</h3><p>Cover the keywords you don't rank for yet.</p><span class="method__go">Explore →</span></a>
          <a class="method reveal" href="{P}blog/melbourne-local-seo-playbook/"><span class="method__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h12l4 4v12H4z"/><path d="M8 12h8M8 16h5"/></svg></span><h3>Read the playbook</h3><p>A suburb-by-suburb guide to ranking in Melbourne.</p><span class="method__go">Read article →</span></a>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="cta-band reveal">
          <div><h2>Find out what's stopping you <span class="goth glow">ranking</span>.</h2><p>Free 30-minute SEO audit call. I'll look at your site and Google Business Profile live and tell you the three things I'd fix first.</p></div>
          <div class="cta-band__actions"><a href="{P}book/" class="btn btn--violet btn--lg" data-magnetic>Book a free SEO audit call →</a></div>
        </div>
      </div>
    </section>'''
    import json
    svc_ld = json.dumps({"@context": "https://schema.org", "@type": "Service", "name": "SEO services in Melbourne", "serviceType": "Search engine optimisation",
                         "description": "Technical SEO, local SEO, content and tracking for Melbourne businesses, by Manjil Shrestha (mastha).",
                         "url": SITE + path, "areaServed": {"@type": "City", "name": "Melbourne"},
                         "provider": {"@type": "ProfessionalService", "@id": SITE + "#service", "name": "mastha — Digital Marketing Expert in Melbourne"},
                         "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "AUD"} for n, p in [("SEO Audit", "1500"), ("Local SEO (monthly)", "1800"), ("Growth SEO (monthly)", "3200")]]}, ensure_ascii=False)
    write(path + 'index.html', layout(P, path, 'SEO Services in Melbourne | Local SEO Expert | mastha',
                                      'SEO services in Melbourne from Manjil Shrestha (mastha). Technical SEO, local SEO, Google Business Profile, content and tracking that turns rankings into enquiries. Free audit call.',
                                      'services', body, scripts=['pages.js'], ld=[svc_ld, faq_ld(faqs), crumbs_ld(trail)]))
