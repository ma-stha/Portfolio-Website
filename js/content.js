/* =========================================================================
   CONTENT.JS  —  Edit this file to change the repeated content on the site.
   Everything below is plain data. No code knowledge needed.
   Hero, About and Contact copy live directly in index.html.
   ========================================================================= */

window.SITE = {

  /* ---------- Identity ---------- */
  name: "Manjil Shrestha",
  handle: "mastha",
  role: "Data-Driven Digital Marketer",
  location: "Melbourne, Australia",
  email: "hello@manjilshrestha.online",          // <- change to your real email
  phone: "",                                       // optional, e.g. "+61 4xx xxx xxx"
  bookingUrl: "#contact",                          // e.g. your Calendly link
  availability: "Open for freelance & full-time roles",

  socials: [
    { label: "LinkedIn",  href: "https://www.linkedin.com/in/manjilshrestha", short: "in" },
    { label: "Instagram", href: "https://www.instagram.com/mastha",           short: "ig" },
    { label: "X",         href: "https://x.com/mastha",                        short: "x"  },
    { label: "GitHub",    href: "https://github.com/ma-stha",                  short: "gh" }
  ],

  /* ---------- Ticker (scrolling strip under the hero) ---------- */
  ticker: [
    "SEO", "Google Ads", "Meta Ads", "GA4", "Looker Studio", "CRO",
    "Email Automation", "Attribution", "Content Strategy", "Landing Pages",
    "Marketing Analytics", "Growth Experiments", "Melbourne"
  ],

  /* ---------- Headline numbers ---------- */
  numbers: [
    { value: 5,    suffix: "+",  label: "Years in digital marketing" },
    { value: 40,   suffix: "+",  label: "Campaigns launched & optimised" },
    { value: 3.4,  suffix: "x",  label: "Average ROAS across paid media", decimals: 1 },
    { value: 1.2,  prefix: "$", suffix: "M", label: "Ad spend managed", decimals: 1 }
  ],

  /* ---------- Services ---------- */
  services: [
    {
      id: "seo", size: "wide",
      title: "SEO & Content Strategy",
      blurb: "Technical audits, keyword architecture and content that ranks for the searches your Melbourne customers actually make.",
      tags: ["Technical SEO", "Local SEO", "Content"]
    },
    {
      id: "paid",
      title: "Paid Media",
      blurb: "Google, Meta and LinkedIn campaigns built on clean conversion tracking and ruthless budget allocation.",
      tags: ["Google Ads", "Meta", "LinkedIn"]
    },
    {
      id: "analytics",
      title: "Analytics & Attribution",
      blurb: "GA4, Tag Manager and Looker Studio dashboards so every dollar has a traceable outcome.",
      tags: ["GA4", "GTM", "Looker Studio"]
    },
    {
      id: "cro", size: "wide",
      title: "Conversion Rate Optimisation",
      blurb: "Hypothesis-led A/B testing, landing page design and funnel fixes that lift revenue without lifting spend.",
      tags: ["A/B Testing", "Landing Pages", "Funnels"]
    },
    {
      id: "email",
      title: "Email & Lifecycle",
      blurb: "Automated flows and segmented campaigns that turn one-time buyers into repeat customers.",
      tags: ["Klaviyo", "HubSpot", "Automation"]
    },
    {
      id: "social",
      title: "Social & Brand",
      blurb: "Content systems and creative testing that build an audience you own, not just rent.",
      tags: ["Content", "Creative Testing", "Community"]
    }
  ],

  /* ---------- Case studies (horizontal scroll section) ---------- */
  caseStudies: [
    {
      id: "ecom-roas",
      client: "Melbourne eCommerce Brand",
      industry: "Retail / eCommerce",
      year: "2025",
      title: "Doubling ROAS without doubling spend",
      summary: "Restructured a fragmented Google & Meta account into intent-based campaigns with full-funnel tracking.",
      problem: "Ad spend was spread across 30+ campaigns with no consistent conversion tracking. ROAS had fallen to 1.4x and the team could not tell which channel was driving revenue.",
      approach: "Rebuilt GA4 and server-side tagging first, then consolidated campaigns into a Performance Max + Search + Retargeting structure. Introduced weekly creative testing and a shared budget-allocation model based on marginal ROAS.",
      result: "ROAS climbed from 1.4x to 3.6x in four months while total spend stayed flat. Revenue attributed to paid media grew 118%.",
      kpis: [
        { value: 3.6, suffix: "x", label: "ROAS", decimals: 1 },
        { value: 118, suffix: "%", label: "Paid revenue" },
        { value: -41, suffix: "%", label: "Cost per order" }
      ],
      series: [14, 16, 15, 19, 22, 24, 28, 31, 30, 34, 36, 36],
      services: ["Paid Media", "Analytics"],
      image: "assets/img/case-ecom.jpg"
    },
    {
      id: "local-seo",
      client: "Multi-location Service Business",
      industry: "Home Services",
      year: "2024",
      title: "Owning local search across Melbourne suburbs",
      summary: "A local SEO programme that took a service business from invisible to top-3 for 60+ suburb-level keywords.",
      problem: "The business relied entirely on word of mouth and paid leads. Organic search contributed under 5% of enquiries and the site had no location pages.",
      approach: "Built a suburb-level location page architecture, fixed Core Web Vitals, launched a Google Business Profile optimisation routine and a monthly content cadence targeting problem-aware searches.",
      result: "Organic enquiries grew 212% year on year and became the single largest lead source. Cost per lead across the blended channel mix dropped by a third.",
      kpis: [
        { value: 212, suffix: "%", label: "Organic enquiries" },
        { value: 63, suffix: "", label: "Top-3 keywords" },
        { value: -33, suffix: "%", label: "Blended CPL" }
      ],
      series: [4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31],
      services: ["SEO", "Content"],
      image: "assets/img/case-local.jpg"
    },
    {
      id: "saas-cro",
      client: "B2B SaaS Startup",
      industry: "Software",
      year: "2024",
      title: "Turning traffic into trials with CRO",
      summary: "A twelve-week experimentation programme on the signup funnel for a growing SaaS product.",
      problem: "Strong traffic growth but a 1.1% visitor-to-trial conversion rate. Marketing and product disagreed on what to fix first.",
      approach: "Instrumented the funnel in GA4, ran session recordings and user interviews, then prioritised nine experiments by expected impact. Shipped a new pricing page, a shorter signup form and intent-based CTAs.",
      result: "Trial conversion rose to 2.7% and trial-to-paid stayed constant, which translated into a 145% increase in new MRR from the same traffic.",
      kpis: [
        { value: 2.7, suffix: "%", label: "Trial conversion", decimals: 1 },
        { value: 145, suffix: "%", label: "New MRR" },
        { value: 9, suffix: "", label: "Experiments shipped" }
      ],
      series: [11, 11, 12, 14, 13, 17, 19, 22, 24, 25, 27, 27],
      services: ["CRO", "Analytics"],
      image: "assets/img/case-saas.jpg"
    },
    {
      id: "lifecycle",
      client: "DTC Wellness Brand",
      industry: "Health & Wellness",
      year: "2023",
      title: "Email flows that paid for the whole marketing budget",
      summary: "A Klaviyo lifecycle programme that lifted repeat purchase rate and made email the most profitable channel.",
      problem: "Email was a single weekly newsletter sent to everyone. Repeat purchase rate was 18% and there was no welcome, abandoned cart or post-purchase flow.",
      approach: "Designed seven automated flows, segmented the list by purchase behaviour and ran a monthly campaign calendar with subject-line and offer testing.",
      result: "Email went from 6% to 31% of total revenue. Repeat purchase rate rose to 34% and the flows alone generated more profit than the brand's total marketing spend.",
      kpis: [
        { value: 31, suffix: "%", label: "Revenue from email" },
        { value: 34, suffix: "%", label: "Repeat purchase rate" },
        { value: 7, suffix: "", label: "Automated flows" }
      ],
      series: [6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31],
      services: ["Email", "Lifecycle"],
      image: "assets/img/case-email.jpg"
    }
  ],

  /* ---------- Process ---------- */
  process: [
    { n: "01", title: "Diagnose",  text: "Audit the data, the funnel and the market. Find where revenue leaks before touching a single ad." },
    { n: "02", title: "Strategy",  text: "Set measurable targets, choose the channels that can hit them, and agree on how success will be judged." },
    { n: "03", title: "Build",     text: "Tracking, campaigns, pages, flows. Everything instrumented from day one so nothing runs blind." },
    { n: "04", title: "Measure",   text: "Weekly reporting against the targets we set, in dashboards you can open without me." },
    { n: "05", title: "Scale",     text: "Double down on what the data proves, cut what it does not, and compound the wins." }
  ],

  /* ---------- Tool stack (two marquee rows) ---------- */
  stack: [
    ["Google Analytics 4", "Google Tag Manager", "Google Ads", "Meta Ads Manager", "Looker Studio", "Search Console", "Semrush", "Ahrefs", "Screaming Frog"],
    ["Klaviyo", "HubSpot", "Mailchimp", "Shopify", "WordPress", "Webflow", "Hotjar", "Microsoft Clarity", "Zapier", "Notion", "Canva", "Figma"]
  ],

  /* ---------- Experience ---------- */
  experience: [
    {
      role: "Digital Marketing Consultant",
      org: "Independent · Melbourne",
      period: "2024 — Present",
      text: "Paid media, SEO and analytics for small and mid-sized Australian businesses. Full ownership from strategy to reporting."
    },
    {
      role: "Podcast & Content Manager",
      org: "Maven Entertainment",
      period: "2024",
      text: "Managed production, distribution and audience growth for a podcast network, including social clips, email and analytics."
    },
    {
      role: "Digital Marketing Specialist",
      org: "eCommerce brand · Remote",
      period: "2022 — 2024",
      text: "Ran Google and Meta campaigns, built the GA4 measurement setup and launched the brand's first lifecycle email programme."
    },
    {
      role: "Marketing Associate",
      org: "Kathmandu, Nepal",
      period: "2020 — 2022",
      text: "Social media, content and campaign reporting for a growing consumer brand. Where the data habit started."
    }
  ],

  education: [
    { title: "Master's Degree", org: "Australian Institute of Higher Education", period: "2025 — Present" },
    { title: "Bachelor of Business Administration", org: "Uniglobe College, Kathmandu", period: "2018 — 2022" }
  ],

  certifications: [
    "Google Ads Search Certification",
    "Google Analytics 4 Certification",
    "Meta Certified Digital Marketing Associate",
    "HubSpot Inbound Marketing",
    "Semrush SEO Toolkit"
  ],

  /* ---------- Testimonials ---------- */
  testimonials: [
    {
      quote: "Manjil was the first marketer who showed us exactly where every dollar went. Within a quarter our paid channels went from a cost centre to the thing funding growth.",
      name: "Founder",
      org: "Melbourne eCommerce brand"
    },
    {
      quote: "The dashboards alone changed how we run the business. We finally make marketing decisions in minutes instead of in meetings.",
      name: "Managing Director",
      org: "Home services company"
    },
    {
      quote: "Calm, methodical and obsessed with the numbers. He will tell you what is not working before you have to ask.",
      name: "Head of Growth",
      org: "B2B SaaS startup"
    }
  ],

  /* ---------- Insights / articles ---------- */
  insights: [
    {
      tag: "Analytics",
      title: "Why most GA4 setups lie to you (and the 5 fixes that stop it)",
      minutes: 7,
      href: "#"
    },
    {
      tag: "Local SEO",
      title: "A suburb-by-suburb playbook for ranking in Melbourne",
      minutes: 9,
      href: "#"
    },
    {
      tag: "Paid Media",
      title: "Marginal ROAS: the only budget rule you need",
      minutes: 5,
      href: "#"
    }
  ],

  /* ---------- FAQ (also injected as FAQ schema for Google) ---------- */
  faq: [
    {
      q: "What does a digital marketing expert in Melbourne actually do?",
      a: "I plan, run and measure the channels that bring customers to your business: search, paid ads, email, content and the analytics that tie them together. The difference is that every activity is tracked against revenue, not vanity metrics."
    },
    {
      q: "Do you work with small businesses or only larger companies?",
      a: "Both. Most of my work is with Melbourne small and mid-sized businesses, startups and eCommerce brands that need senior-level marketing without a full agency retainer."
    },
    {
      q: "How quickly can I expect results?",
      a: "Paid media and CRO usually show movement within four to eight weeks. SEO is a compounding channel and typically takes three to six months to produce meaningful organic growth."
    },
    {
      q: "Can you fix our Google Analytics and tracking first?",
      a: "Yes, and I usually insist on it. Clean measurement is the foundation for every decision that follows, so an analytics audit is where most engagements begin."
    },
    {
      q: "Are you available for full-time roles as well as freelance?",
      a: "Yes. I am based in Melbourne and open to both in-house roles and project or retainer work."
    }
  ]
};
