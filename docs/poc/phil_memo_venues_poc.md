# Regional Data Collection Platform - PoC Summary

**To:** Phil
**From:** Alex
**Date:** 2 December 2024
**Re:** Indian Venues Data Collection - Quick PoC & Proposal

---

Hey Phil,

Did a quick PoC on scraping Indian live music venues, if only to reinforce what I already know to be true.

## The Problem with Traditional Scraping

Tried hitting the obvious sources (Zomato, TripAdvisor, Magicpin) from outside India - got blocked or returned empty JS shells. JustDial worked partially, GigHub gave us 46 curated venues. The usual story.

## What Actually Works

I've always found that an **in-region approach** using localised search terms and heuristics to determine the best data sources gives the best results. For example:

- Hindi search "लाइव संगीत रेस्टोरेंट मुंबई" returned different (and better) JustDial results than English
- Source scoring based on data completeness, contact info availability, and freshness lets the system learn which sources to prioritise per region/category
- Dynamic unified schema approach means we're not constantly rebuilding pipelines when adding new data types

That way, scaling to other regions, business types, and data sources is much easier. Build once, configure for each job.

## Rough Numbers

### Build Cost
- **~3-4 weeks** to stand this up properly (orchestrator, regional agents, schema builder, source scoring)
- Could cut to 2 weeks for MVP with manual schema definition

### Operating Costs
- **~£0.04-0.06 per website scraped** (includes proxy, compute, LLM extraction)
- Detail page enrichment adds ~£0.02 per venue
- Bulk pricing improves significantly at scale

### For the India Venues Project Specifically

| Metric | Estimate |
|--------|----------|
| Target venues | ~4,000 |
| Sources to scrape | 5-6 (JustDial, Google Maps, Zomato, LBB, GigHub, Instagram discovery) |
| Pages to process | ~5,000-6,000 |
| **Estimated scraping cost** | **~£250-300** |
| Timeline (single agent) | ~2-3 weeks |
| Timeline (parallel agents with backoff/retry) | ~1 week |

That doesn't include data storage or transfer costs, which I think would be negligible (<£10/month for this volume).

Also no margin baked in above.

## Commercial Model (If Productising)

Would look to:
1. **Cover NRE fees** through a minimum commitment to data volumes collected (e.g., 10K records minimum)
2. **Monthly service fee** to cover AWS hosting (probably £50-100/month depending on usage)
3. **Per-record pricing** at £0.05-0.08 for basic scrape, £0.10-0.15 with enrichment

### Support Model
- **UK first-line** (general queries, job setup, data delivery)
- **SG second-line** (technical issues, custom schema work)
- **Channels:** Slack / email

---

## Recommendation

For the immediate India PRO use case, we could:

**Option A:** Just do the job manually using existing tools (~£300-400, delivered in 2 weeks)

**Option B:** Build the platform properly, use India as first customer, then offer to similar verticals (music rights orgs, venue booking platforms, event companies)

Option B is more work upfront but gives us a repeatable capability. The "in-region + localised search + source scoring" approach is genuinely differentiated from the Apify/Clay offerings which are very US/EU-centric.

Let me know how you want to proceed.

Alex

---

*P.S. - Full technical analysis with schema, source scores, and architecture diagram saved separately if you want the details.*
