/* =========================================================================
   CONTENT.JS  —  Edit this file to change the site's content.
   Plain data only. Save the file and refresh the page to see changes.
   Hero headline, About text and Contact copy live in index.html.
   ========================================================================= */

window.SITE = {

  /* ---------- Identity ---------- */
  name: "Manjil Shrestha",
  role: "Data-Driven Digital Marketer",
  location: "Melbourne, Australia",
  email: "hello@manjilshrestha.online",
  replyTime: "Usually replies within 24 hours",
  calendlyUrl: "",   // optional: paste a Calendly link to replace the booking widget on /book/          // <- your real email
  availability: "Available for freelance & full-time",

  socials: [
    { label: "LinkedIn",  href: "https://www.linkedin.com/in/manjilshrestha" },
    { label: "Instagram", href: "https://www.instagram.com/mastha" },
    { label: "X",         href: "https://x.com/mastha" },
    { label: "GitHub",    href: "https://github.com/ma-stha" }
  ],

  /* ---------- Hero "campaign receipt" ---------- */
  receipt: {
    id: "MS-2026-11",
    lines: [
      { label: "Ad spend managed",    value: 1240000, prefix: "$", abbr: true },
      { label: "Revenue attributed",  value: 4200000, prefix: "$", abbr: true },
      { label: "Blended ROAS",        value: 3.4, suffix: "x", decimals: 1 },
      { label: "Avg. CPA change",     value: -41, suffix: "%" },
      { label: "Organic lead growth", value: 212, prefix: "+", suffix: "%" }
    ],
    total: { label: "Guesswork", value: "$0.00" }
  },

  /* ---------- Tapes (the two crossing marquee strips) ---------- */
  tapeA: ["SEO", "Google Ads", "Meta Ads", "GA4", "Looker Studio", "CRO", "Email Automation", "Attribution"],
  tapeB: ["Data > Opinions", "Melbourne", "Measure everything", "Growth you can prove", "Open for work"],

  /* ---------- Manifesto (words in [brackets] get the red highlight) ---------- */
  manifesto: "Most marketing fails quietly. Budgets drift, tracking breaks, and nobody notices until the quarter is gone. I do the opposite. I [measure] first, [build] second and [scale] only what the numbers prove. No vanity metrics. No black boxes. Just [growth you can see] in a dashboard you own.",

  /* ---------- Headline numbers (red section) ---------- */
  numbers: [
    { value: 5,   suffix: "+", label: "Years in digital marketing" },
    { value: 40,  suffix: "+", label: "Campaigns launched & optimised" },
    { value: 3.4, suffix: "x", label: "Average ROAS across paid media", decimals: 1 },
    { value: 212, suffix: "%", label: "Best organic lead growth (YoY)" }
  ],

  /* ---------- Services ---------- */
  services: [
    { id: "seo",       title: "SEO & Content",        blurb: "Technical audits, keyword architecture and content that ranks for what your Melbourne customers actually search.", tags: ["Technical SEO", "Local SEO", "Content"] },
    { id: "paid",      title: "Paid Media",           blurb: "Google, Meta and LinkedIn campaigns built on clean conversion tracking and ruthless budget allocation.",          tags: ["Google Ads", "Meta", "LinkedIn"] },
    { id: "analytics", title: "Analytics",            blurb: "GA4, Tag Manager and Looker Studio dashboards so every dollar has a traceable outcome.",                          tags: ["GA4", "GTM", "Looker Studio"] },
    { id: "cro",       title: "Conversion (CRO)",     blurb: "Hypothesis-led A/B tests, landing pages and funnel fixes that lift revenue without lifting spend.",                tags: ["A/B Testing", "Landing Pages", "Funnels"] },
    { id: "email",     title: "Email & Lifecycle",    blurb: "Automated flows and segmented campaigns that turn one-time buyers into repeat customers.",                         tags: ["Klaviyo", "HubSpot", "Automation"] },
    { id: "social",    title: "Social & Brand",       blurb: "Content systems and creative testing that build an audience you own, not just rent.",                             tags: ["Content", "Creative Testing", "Community"] }
  ],

  /* ---------- Growth calculator defaults ---------- */
  calculator: {
    visitors: 20000,      // monthly website visitors
    conversion: 1.5,      // % of visitors who buy / enquire
    value: 120,           // average order or lead value ($)
    lift: 30              // expected % improvement in conversion rate
  },

  /* ---------- Case studies ---------- */
  caseStudies: [
    {
      client: "Melbourne eCommerce Brand", industry: "Retail / eCommerce", year: "2025",
      title: "Doubling ROAS without doubling spend",
      summary: "Rebuilt a fragmented Google & Meta account into intent-based campaigns with full-funnel tracking.",
      problem: "Ad spend was spread across 30+ campaigns with no consistent conversion tracking. ROAS had fallen to 1.4x and the team could not tell which channel was driving revenue.",
      approach: "Rebuilt GA4 and server-side tagging first, then consolidated campaigns into Performance Max, Search and Retargeting. Introduced weekly creative testing and a budget model based on marginal ROAS.",
      result: "ROAS climbed from 1.4x to 3.6x in four months while total spend stayed flat. Revenue attributed to paid media grew 118%.",
      kpis: [ { value: 3.6, suffix: "x", label: "ROAS", decimals: 1 }, { value: 118, suffix: "%", label: "Paid revenue" }, { value: -41, suffix: "%", label: "Cost / order" } ],
      series: [14, 16, 15, 19, 22, 24, 28, 31, 30, 34, 36, 36],
      services: ["Paid Media", "Analytics"], image: "assets/img/case-ecom.jpg"
    },
    {
      client: "Multi-location Service Business", industry: "Home Services", year: "2024",
      title: "Owning local search across Melbourne suburbs",
      summary: "A local SEO programme that took a service business from invisible to top-3 for 60+ suburb keywords.",
      problem: "The business relied on word of mouth and paid leads. Organic search contributed under 5% of enquiries and the site had no location pages.",
      approach: "Built a suburb-level location page architecture, fixed Core Web Vitals, ran a Google Business Profile routine and a monthly content cadence for problem-aware searches.",
      result: "Organic enquiries grew 212% year on year and became the largest lead source. Blended cost per lead dropped by a third.",
      kpis: [ { value: 212, suffix: "%", label: "Organic leads" }, { value: 63, suffix: "", label: "Top-3 keywords" }, { value: -33, suffix: "%", label: "Blended CPL" } ],
      series: [4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31],
      services: ["SEO", "Content"], image: "assets/img/case-local.jpg"
    },
    {
      client: "B2B SaaS Startup", industry: "Software", year: "2024",
      title: "Turning traffic into trials with CRO",
      summary: "A twelve-week experimentation programme on the signup funnel of a growing SaaS product.",
      problem: "Strong traffic growth but a 1.1% visitor-to-trial rate. Marketing and product disagreed on what to fix first.",
      approach: "Instrumented the funnel in GA4, ran session recordings and interviews, then prioritised nine experiments. Shipped a new pricing page, a shorter signup form and intent-based CTAs.",
      result: "Trial conversion rose to 2.7% with trial-to-paid unchanged, which meant 145% more new MRR from the same traffic.",
      kpis: [ { value: 2.7, suffix: "%", label: "Trial conversion", decimals: 1 }, { value: 145, suffix: "%", label: "New MRR" }, { value: 9, suffix: "", label: "Experiments" } ],
      series: [11, 11, 12, 14, 13, 17, 19, 22, 24, 25, 27, 27],
      services: ["CRO", "Analytics"], image: "assets/img/case-saas.jpg"
    },
    {
      client: "DTC Wellness Brand", industry: "Health & Wellness", year: "2023",
      title: "Email flows that paid for the whole budget",
      summary: "A Klaviyo lifecycle programme that made email the most profitable channel.",
      problem: "Email was one weekly newsletter sent to everyone. Repeat purchase rate was 18% and there were no automated flows.",
      approach: "Designed seven automated flows, segmented the list by purchase behaviour and ran a monthly campaign calendar with subject-line and offer testing.",
      result: "Email went from 6% to 31% of revenue. Repeat purchase rate rose to 34% and the flows alone out-earned the total marketing spend.",
      kpis: [ { value: 31, suffix: "%", label: "Revenue from email" }, { value: 34, suffix: "%", label: "Repeat rate" }, { value: 7, suffix: "", label: "Flows" } ],
      series: [6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31],
      services: ["Email", "Lifecycle"], image: "assets/img/case-email.jpg"
    }
  ],

  /* ---------- Process (the loop) ---------- */
  process: [
    { title: "Diagnose", text: "Audit the data, the funnel and the market. Find where revenue leaks before touching a single ad." },
    { title: "Strategy", text: "Set measurable targets, pick the channels that can hit them, and agree how success is judged." },
    { title: "Build",    text: "Tracking, campaigns, pages and flows. Everything instrumented from day one so nothing runs blind." },
    { title: "Measure",  text: "Weekly reporting against the targets, in dashboards you can open without me." },
    { title: "Scale",    text: "Double down on what the data proves, cut what it doesn't, and compound the wins." }
  ],

  /* ---------- Tool stack ---------- */
  stack: [
    ["Google Analytics 4", "Tag Manager", "Google Ads", "Meta Ads", "Looker Studio", "Search Console", "Semrush", "Ahrefs", "Screaming Frog"],
    ["Klaviyo", "HubSpot", "Mailchimp", "Shopify", "WordPress", "Webflow", "Hotjar", "Clarity", "Zapier", "Notion", "Canva", "Figma"]
  ],

  /* ---------- Experience ---------- */
  experience: [
    { role: "Digital Marketing Consultant", org: "Independent · Melbourne", period: "2024 — Now", text: "Paid media, SEO and analytics for small and mid-sized Australian businesses. Strategy to reporting." },
    { role: "Podcast & Content Manager",    org: "Maven Entertainment",    period: "2024",       text: "Production, distribution and audience growth for a podcast network, including social clips, email and analytics." },
    { role: "Digital Marketing Specialist", org: "eCommerce brand · Remote", period: "2022 — 2024", text: "Ran Google and Meta campaigns, built the GA4 setup and launched the first lifecycle email programme." },
    { role: "Marketing Associate",          org: "Kathmandu, Nepal",       period: "2020 — 2022", text: "Social, content and campaign reporting for a consumer brand. Where the data habit started." }
  ],

  education: [
    { title: "Master's Degree", org: "Australian Institute of Higher Education", period: "2025 — Now" },
    { title: "Bachelor of Business Administration", org: "Uniglobe College, Kathmandu", period: "2018 — 2022" }
  ],

  certifications: [
    "Google Ads Search",
    "Google Analytics 4",
    "Meta Digital Marketing Associate",
    "HubSpot Inbound Marketing",
    "Semrush SEO Toolkit"
  ],

  /* ---------- Testimonials ---------- */
  testimonials: [
    { quote: "Manjil was the first marketer who showed us exactly where every dollar went. Within a quarter, paid went from a cost centre to the thing funding growth.", name: "Founder", org: "Melbourne eCommerce brand" },
    { quote: "The dashboards alone changed how we run the business. We make marketing decisions in minutes now, not meetings.", name: "Managing Director", org: "Home services company" },
    { quote: "Calm, methodical and obsessed with the numbers. He tells you what isn't working before you have to ask.", name: "Head of Growth", org: "B2B SaaS startup" }
  ],

  /* ---------- Insights ---------- */
  insights: [
    { tag: "Analytics",  title: "Why most GA4 setups lie to you (and five fixes)",       minutes: 7, href: "blog/ga4-setups-lie-to-you/" },
    { tag: "Local SEO",  title: "A suburb-by-suburb playbook for ranking in Melbourne", minutes: 8, href: "blog/melbourne-local-seo-playbook/" },
    { tag: "Paid Media", title: "Marginal ROAS: the only budget rule you need",          minutes: 5, href: "blog/marginal-roas-budget-rule/" }
  ],

  /* ---------- FAQ (also published as FAQ schema for Google) ---------- */
  faq: [
    { q: "What does a digital marketing expert in Melbourne actually do?", a: "I plan, run and measure the channels that bring customers to your business: search, paid ads, email, content and the analytics that tie them together. Every activity is tracked against revenue, not vanity metrics." },
    { q: "Do you work with small businesses?", a: "Yes. Most of my work is with Melbourne small and mid-sized businesses, startups and eCommerce brands that need senior-level marketing without a full agency retainer." },
    { q: "How quickly will I see results?", a: "Paid media and CRO usually move within four to eight weeks. SEO compounds and typically takes three to six months to produce meaningful organic growth." },
    { q: "Can you fix our Google Analytics and tracking first?", a: "Yes, and I usually insist on it. Clean measurement is the foundation for every decision that follows, so most engagements start with an analytics audit." },
    { q: "Are you open to full-time roles?", a: "Yes. I'm based in Melbourne and open to in-house roles as well as project and retainer work." }
  ]
};
