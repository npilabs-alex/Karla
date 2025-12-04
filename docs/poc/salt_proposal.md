# Indian Venue Data - Proposal for Salt

Hey,

Did a quick PoC on Indian live music venues to see what's actually scrapeable and what the data looks like.

## What I Found

Tested 8 sources from outside India:

| Source | Result | Issue |
|--------|--------|-------|
| TripAdvisor.in | 403 Forbidden | Geo-blocked |
| Zomato | Timeout | Heavy JS + geo-blocking |
| LBB, Magicpin, Holidify | Empty response | Returns only CSS/JS, no content |
| JustDial | Partial success | Works but needs localisation |
| GigHub | Full success | Static site, 46 curated venues |
| Google Maps | Needs testing | Requires in-region browser |

The JS-heavy sites (which is most of them now) need headless browsers running in-region to render properly. Standard API scraping just returns empty shells.

Localised search also matters - Hindi queries ("लाइव संगीत रेस्टोरेंट मुंबई") returned different and more complete JustDial results than English equivalents.

**Bottom line:** Need to deploy Playwright browsers in AWS Mumbai (ap-south-1), use residential proxies, and run localised search terms per region. That's the approach I'd take.

From the sources that did work, got 46 curated venues from GigHub and 216 from JustDial Mumbai with full contact details. Reckon there's **4-5K venues** across India that meet the criteria (>10 pax, regular live music). Sample attached.

## Sample Data - What's Included

The attached sample has 59 venues. Being honest about what I captured vs what the full scrape would deliver:

**What's in the sample now:**
- Venue name, city, area
- Phone numbers (JustDial venues only)
- Ratings and review counts (JustDial only)
- Venue type (inferred from source/name)

**What's missing (needs in-region scraping + detail pages):**
- Full addresses
- Capacity / venue size
- Music genres
- Opening hours
- Parking, amenities

## What the Full Scrape Would Deliver

With in-region browsers hitting detail pages, we can extract and infer:

| Field | Source | Method |
|-------|--------|--------|
| Capacity estimate | Reviews, photos, venue descriptions | LLM inference ("large dance floor", "intimate 50-seater") |
| Genres | Event listings, venue descriptions, social | LLM classification |
| Unified rating | Google + Zomato + JustDial + TripAdvisor | Weighted average, normalised 0-5 |
| Parking | Google Maps, venue pages | Direct extraction |
| Amenities | Venue descriptions | LLM extraction (stage, sound system, outdoor area) |

The idea is to cross-reference multiple sources per venue, merge the data, and calculate a confidence score based on how many sources agree. Each venue gets a unified rating (weighted average across platforms) and a data quality score so you know which records are solid and which need verification.

## Approach

This isn't my first rodeo with regional data collection. The approach I've refined:

1. **In-region infrastructure** - Playwright browsers in AWS Mumbai, residential proxies, looks like a real user
2. **Localised discovery** - Hindi, Marathi, Kannada search terms surface venues that English-only queries miss entirely
3. **Source scoring** - System learns which sources yield best data per category/region, prioritises accordingly
4. **Entity resolution** - Fuzzy matching + LLM to dedupe "Kitty Su Mumbai" vs "KittySu, Lower Parel" vs "KITTYSU"
5. **Confidence scoring** - More sources = higher confidence. Single-source venues flagged for review

Built similar systems for other verticals. The pattern holds - you need to be in-region, speak the local language, and let the system learn which sources are worth hitting.

## Pricing

| Deliverable | Price |
|-------------|-------|
| **India Pilot** - 4-5K venues, verified contacts, unified schema | £5K |
| **Monthly Updates** - new venues, refresh contacts, remove closed | £500/mo |
| **Additional Regions** - Africa, SEA, LatAm (same approach) | £3-5K per region |

Delivery: 2-3 weeks from go.

Doesn't include any bespoke enrichment (email finding, social profiles etc) but can quote if needed.

## Why This Matters for PROs

The usual approach - buying a stale database or scraping from London - misses half the picture. India's live music scene is fragmented across regional platforms, local languages, and venues that don't show up on English Google searches. The same applies to Africa, SEA, LatAm.

If you're expanding licensing into these regions, you need data that reflects how locals actually find venues - not how a UK researcher Googles them.

Let me know if useful.

Alex
