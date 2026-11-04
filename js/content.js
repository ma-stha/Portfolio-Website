/* =========================================================================
   CONTENT.JS — every piece of copy and data on the site lives here.
   Everything marked DEMO is placeholder content. Replace it with your
   real data before launch. Save, refresh, done.
   ========================================================================= */

window.SITE = {

  /* ---------- Identity ---------- */
  name: "Manjil Shrestha",
  brand: "mastha",
  role: "Data-Driven Digital Marketer",
  location: "Melbourne, Australia",
  email: "hello@manjilshrestha.online",            // DEMO: your real email
  calendlyUrl: "",   // optional: paste a Calendly link to replace the built-in booking widget on /book/
  availability: "Taking 2 new clients for Q1",      // DEMO
  replyTime: "Usually replies within 24 hours",

  socials: [
    { label: "LinkedIn",  href: "https://www.linkedin.com/in/manjilshrestha" },
    { label: "Instagram", href: "https://www.instagram.com/mastha" },
    { label: "X",         href: "https://x.com/mastha" },
    { label: "GitHub",    href: "https://github.com/ma-stha" }
  ],

  /* ---------- Client marquee (DEMO brand names) ---------- */
  clients: ["Northside Dental", "Fitzroy Coffee Co.", "Yarra Home Services", "Kinetic SaaS", "Brunswick Bikes", "Southbank Legal", "Ember Skincare", "Laneway Eats", "Carlton Physio", "Arcade Studio"],

  /* ---------- About stats (DEMO) ---------- */
  stats: [
    { value: 5,   suffix: "+", label: "Years in growth marketing", spark: [2, 3, 3, 4, 5, 6, 8, 9] },
    { value: 3.4, suffix: "x", label: "Average ROAS on paid media", decimals: 1, spark: [1.4, 1.7, 2.1, 2.4, 2.6, 3, 3.2, 3.4] },
    { value: 1.2, prefix: "$", suffix: "M", label: "Ad spend managed", decimals: 1, spark: [.1, .2, .3, .5, .6, .8, 1, 1.2] },
    { value: 40,  suffix: "+", label: "Campaigns launched", spark: [4, 8, 12, 17, 22, 29, 34, 40] }
  ],

  /* ---------- Services ---------- */
  services: [
    { title: "Search & SEO", short: "Rank for what Melbourne actually searches.", text: "Technical audits, keyword architecture, local SEO and content that compounds month after month.", deliver: ["Technical SEO audit", "Keyword & content strategy", "Local SEO / Google Business Profile", "Monthly ranking reports"] },
    { title: "Paid Media", short: "Ads judged on revenue, not clicks.", text: "Google, Meta and LinkedIn campaigns built on clean tracking and a budget model that follows marginal ROAS.", deliver: ["Account audit & restructure", "Performance Max & Search", "Meta creative testing", "Weekly budget reallocation"] },
    { title: "Analytics & Tracking", short: "Every dollar traced to an outcome.", text: "GA4, Tag Manager, server-side tagging and Looker Studio dashboards your whole team can read.", deliver: ["GA4 + GTM implementation", "Conversion & event tracking", "Attribution modelling", "Looker Studio dashboards"] },
    { title: "Conversion (CRO)", short: "More revenue from the same traffic.", text: "Funnel analysis, session research and A/B tests prioritised by expected impact.", deliver: ["Funnel & UX audit", "A/B test roadmap", "Landing page design", "Experiment reporting"] },
    { title: "Email & Lifecycle", short: "Turn one-time buyers into regulars.", text: "Automated flows and segmented campaigns in Klaviyo or HubSpot that keep earning while you sleep.", deliver: ["Welcome / cart / post-purchase flows", "Segmentation", "Campaign calendar", "Deliverability fixes"] },
    { title: "Strategy & Fractional CMO", short: "A senior marketer without the full-time cost.", text: "Quarterly growth plans, channel mix, hiring support and a reporting rhythm for founders and small teams.", deliver: ["90-day growth plan", "Channel mix & budget", "Team & agency briefs", "Monthly board-ready report"] }
  ],

  /* ---------- Case files (DEMO) ---------- */
  caseStudies: [
    {
      file: "001", client: "Melbourne eCommerce brand", industry: "Retail / eCommerce", year: "2025", duration: "4 months",
      title: "Doubling ROAS without doubling spend",
      summary: "Rebuilt a fragmented Google & Meta account around intent, with full-funnel tracking underneath.",
      problem: "Spend was spread across 30+ campaigns with no consistent conversion tracking. ROAS had fallen to 1.4x and nobody could say which channel drove revenue.",
      approach: "Rebuilt GA4 and server-side tagging first. Consolidated into Performance Max, Search and Retargeting. Introduced weekly creative testing and a budget model based on marginal ROAS.",
      result: "ROAS climbed from 1.4x to 3.6x in four months with flat spend. Paid-media revenue grew 118%.",
      kpis: [ { v: "3.6x", l: "ROAS" }, { v: "+118%", l: "Paid revenue" }, { v: "-41%", l: "Cost / order" }, { v: "4 mo", l: "Time to result" } ],
      series: [14, 16, 15, 19, 22, 24, 28, 31, 30, 34, 36, 36], tags: ["Paid Media", "Analytics", "GA4"]
    },
    {
      file: "002", client: "Multi-location service business", industry: "Home Services", year: "2024", duration: "12 months",
      title: "Owning local search across 60+ suburbs",
      summary: "A local SEO programme that took a service business from invisible to top-3 across Melbourne suburbs.",
      problem: "The business lived on word of mouth and paid leads. Organic search drove under 5% of enquiries and there were no location pages.",
      approach: "Built suburb-level location architecture, fixed Core Web Vitals, ran a Google Business Profile routine and a monthly content cadence.",
      result: "Organic enquiries grew 212% year on year and became the largest lead source. Blended cost per lead fell by a third.",
      kpis: [ { v: "+212%", l: "Organic leads" }, { v: "63", l: "Top-3 keywords" }, { v: "-33%", l: "Blended CPL" }, { v: "12 mo", l: "Programme" } ],
      series: [4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31], tags: ["SEO", "Local SEO", "Content"]
    },
    {
      file: "003", client: "B2B SaaS startup", industry: "Software", year: "2024", duration: "12 weeks",
      title: "Turning traffic into trials",
      summary: "A twelve-week experimentation sprint on the signup funnel of a growing SaaS product.",
      problem: "Strong traffic, weak 1.1% visitor-to-trial rate. Marketing and product disagreed on what to fix first.",
      approach: "Instrumented the funnel, ran recordings and interviews, then shipped nine prioritised experiments: new pricing page, shorter signup, intent-based CTAs.",
      result: "Trial conversion rose to 2.7% with trial-to-paid unchanged: 145% more new MRR from the same traffic.",
      kpis: [ { v: "2.7%", l: "Trial conversion" }, { v: "+145%", l: "New MRR" }, { v: "9", l: "Experiments" }, { v: "12 wk", l: "Sprint" } ],
      series: [11, 11, 12, 14, 13, 17, 19, 22, 24, 25, 27, 27], tags: ["CRO", "Analytics", "UX"]
    },
    {
      file: "004", client: "DTC wellness brand", industry: "Health & Wellness", year: "2023", duration: "6 months",
      title: "Email that paid for the whole budget",
      summary: "A Klaviyo lifecycle programme that made email the most profitable channel in the business.",
      problem: "One weekly newsletter to everyone. 18% repeat purchase rate. No automation at all.",
      approach: "Seven automated flows, behaviour-based segments and a tested monthly campaign calendar.",
      result: "Email went from 6% to 31% of revenue. Repeat purchase rate reached 34% and flows out-earned total marketing spend.",
      kpis: [ { v: "31%", l: "Revenue from email" }, { v: "34%", l: "Repeat rate" }, { v: "7", l: "Flows built" }, { v: "6 mo", l: "Programme" } ],
      series: [6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31], tags: ["Email", "Klaviyo", "Lifecycle"]
    }
  ],

  /* ---------- Process (typed into the terminal) ---------- */
  process: [
    { cmd: "mastha diagnose --funnel --tracking", out: "Audit complete. 14 leaks found, 3 critical.", title: "Diagnose", text: "Audit the data, the funnel and the market. Find where revenue leaks before spending a dollar." },
    { cmd: "mastha strategy --target=revenue", out: "90-day plan locked. KPIs agreed with you.", title: "Strategy", text: "Set measurable targets, pick the channels that can hit them, agree how success is judged." },
    { cmd: "mastha build --channels=search,paid,email", out: "Campaigns live. Every event tracked.", title: "Build", text: "Tracking, campaigns, pages and flows, instrumented from day one." },
    { cmd: "mastha measure --weekly", out: "Dashboard shared. Zero vanity metrics.", title: "Measure", text: "Weekly reporting against targets, in dashboards you can open without me." },
    { cmd: "mastha scale --only=what-works", out: "Budget moved to winners. Repeat.", title: "Scale", text: "Double down on what the data proves. Cut what it doesn't. Compound the wins." }
  ],

  /* ---------- Growth lab defaults ---------- */
  calculator: { visitors: 20000, conversion: 1.5, value: 120, lift: 30 },

  /* ---------- Toolkit ---------- */
  stack: [
    { group: "Analytics", tools: ["GA4", "Tag Manager", "Looker Studio", "BigQuery", "Server-side GTM"] },
    { group: "Search", tools: ["Search Console", "Semrush", "Ahrefs", "Screaming Frog", "GBP"] },
    { group: "Paid", tools: ["Google Ads", "Meta Ads", "LinkedIn Ads", "TikTok Ads", "Microsoft Ads"] },
    { group: "Lifecycle", tools: ["Klaviyo", "HubSpot", "Mailchimp", "Zapier"] },
    { group: "Build & CRO", tools: ["Shopify", "WordPress", "Webflow", "Hotjar", "Clarity", "Figma"] }
  ],

  /* ---------- Experience (DEMO dates & roles) ---------- */
  experience: [
    { period: "2024 — Now", role: "Digital Marketing Consultant", org: "Independent · Melbourne", text: "Paid media, SEO and analytics for small and mid-sized Australian businesses. Strategy to reporting.", tags: ["Consulting", "Paid", "SEO"] },
    { period: "2024", role: "Podcast & Content Manager", org: "Maven Entertainment", text: "Production, distribution and audience growth for a podcast network, including clips, email and analytics.", tags: ["Content", "Audience"] },
    { period: "2022 — 2024", role: "Digital Marketing Specialist", org: "eCommerce brand · Remote", text: "Ran Google and Meta, built the GA4 setup and launched the first lifecycle email programme.", tags: ["Google Ads", "Meta", "GA4"] },
    { period: "2020 — 2022", role: "Marketing Associate", org: "Kathmandu, Nepal", text: "Social, content and campaign reporting for a consumer brand. Where the data habit started.", tags: ["Social", "Reporting"] }
  ],
  education: [
    { title: "Master's Degree", org: "Australian Institute of Higher Education", period: "2025 — Now" },
    { title: "Bachelor of Business Administration", org: "Uniglobe College, Kathmandu", period: "2018 — 2022" }
  ],
  certifications: ["Google Ads Search", "Google Analytics 4", "Meta Digital Marketing Associate", "HubSpot Inbound", "Semrush SEO Toolkit", "Klaviyo Email Fundamentals"],

  /* ---------- Testimonials (DEMO) ---------- */
  testimonials: [
    { quote: "Manjil showed us exactly where every dollar went. Within a quarter, paid went from a cost centre to the thing funding our growth.", name: "Sarah K.", role: "Founder, eCommerce brand" },
    { quote: "The dashboards alone changed how we run the business. We make marketing decisions in minutes now, not meetings.", name: "Daniel P.", role: "Managing Director, Home services" },
    { quote: "Calm, methodical and obsessed with the numbers. He tells you what isn't working before you have to ask.", name: "Priya R.", role: "Head of Growth, B2B SaaS" }
  ],

  /* ---------- Insights (DEMO) ---------- */
  insights: [
    { tag: "Analytics", date: "Oct 2026", minutes: 7, title: "Why most GA4 setups lie to you (and five fixes)", href: "blog/ga4-setups-lie-to-you/" },
    { tag: "Local SEO", date: "Sep 2026", minutes: 9, title: "A suburb-by-suburb playbook for ranking in Melbourne", href: "blog/melbourne-local-seo-playbook/" },
    { tag: "Paid Media", date: "Aug 2026", minutes: 5, title: "Marginal ROAS: the only budget rule you need", href: "blog/marginal-roas-budget-rule/" }
  ],

  /* ---------- FAQ (also published as FAQ schema) ---------- */
  faq: [
    { q: "What does a digital marketing expert in Melbourne actually do?", a: "I plan, run and measure the channels that bring customers to your business: search, paid ads, email, content and the analytics tying them together. Every activity is judged on revenue, not vanity metrics." },
    { q: "Do you work with small businesses?", a: "Yes. Most of my clients are Melbourne small and mid-sized businesses, startups and eCommerce brands that need senior-level marketing without a full agency retainer." },
    { q: "How fast will I see results?", a: "Paid media and CRO usually move within four to eight weeks. SEO compounds and typically shows meaningful growth in three to six months." },
    { q: "Can you fix our tracking first?", a: "Yes, and I usually insist on it. Clean measurement is the foundation for every decision after it, so most engagements start with an analytics audit." },
    { q: "How do you price your work?", a: "Fixed-price audits and sprints, or a monthly retainer for ongoing work. You'll get a clear scope and price after a free 30-minute call." },
    { q: "Are you open to full-time roles?", a: "Yes. I'm based in Melbourne and open to the right in-house role as well as project and retainer work." }
  ]
};
