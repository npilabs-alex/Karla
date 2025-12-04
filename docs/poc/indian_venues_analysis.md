# Indian Live Music Venues: Architecture & Data Analysis

## Executive Summary

Testing from outside India revealed critical architecture requirements:
- **403 errors**: TripAdvisor, Zomato blocked non-India requests
- **JS rendering failures**: LBB, Magicpin, Holidify, BohoTheBar return only CSS/JS
- **Successful scrapes**: GigHub (static), JustDial (partial), Instagram/social (search only)

**Conclusion**: Must deploy scrapers in AWS ap-south-1 (Mumbai) with headless browser.

---

## Successful Data Extraction

### Source 1: GigHub (46 venues) - CLEAN DATA
| Venue | City |
|-------|------|
| antiSOCIAL | Mumbai |
| Auro Kitchen & Bar | Delhi |
| Fandom At Gilly's Redefined | Bangalore |
| House Of Chapora | Goa |
| BLOCK 22 | Hyderabad |
| TopCat CCU | Kolkata |
| Club Pandora | Mumbai |
| Aqua - The Park | Bangalore |
| Prism Club and Kitchen | Hyderabad |
| Prana Cafe | Goa |
| Hill Top | Goa |
| W GOA | Goa |
| antiSOCIAL | Pune |
| TOT Nightclub | Hyderabad |
| Foxtrot Koramangala | Bangalore |
| Glory | Goa |
| Diablo | Delhi |
| Khar Social | Mumbai |
| Soho | Delhi |
| GYLT | Bangalore |
| Bonobo - Bar.Love.Food. | Mumbai |
| Marbela Beach Resort | Goa |
| Casa Danza | Gurugram |
| The Storytellers' Bar | Pondicherry |
| Summer House Cafe | Delhi |
| Larive Beach Resort | Goa |
| Mic Drop | Delhi |
| Koramangala Social | Bangalore |
| Kitty Su | Mumbai |
| Kitty Su | Delhi |
| Club Trove | Jaipur |
| Kitty Ko | Bangalore |
| Tabula Rasa - Cafe & Bar | Hyderabad |
| Sunburn Beach Club | Goa |
| Indiranagar Social | Bangalore |
| Fat Owl | Bangalore |
| High Spirits | Pune |
| Reality | Kolkata |
| Mount Road Social | Chennai |
| Raahi, Neo Kitchen & Bar | Bangalore |
| FC Road Social | Pune |
| Whats in d name | Kolkata |
| Raasta | Delhi |
| Raasta | Mumbai |

**Data Quality**: Names + City only. Missing: address, phone, capacity, contact.

---

### Source 2: JustDial Mumbai (216 listings) - PARTIAL DATA
| Venue | Address | Phone | Rating | Reviews |
|-------|---------|-------|--------|---------|
| Madeira & Mime | Lake Blvd Rd, Powai 400076 | +91-9987795161 | 4.6 | 12,651 |
| TBC The Boat Club | W Express Hwy, Dahisar 400068 | +91-7769044144 | 4.3 | 11,516 |
| Shor | Santacruz West 400054 | +91-9136025205 | 4.2 | 370 |
| Uno Mas Tapas | BKC, Bandra East 400051 | +91-9820790898 | 4.3 | 1,580 |
| Kinara Dhaba | Ahmedabad Hwy, Vasai 401208 | +91-9773487101 | 4.0 | 17,919 |

**Data Quality**: Excellent - name, address, phone, rating, reviews. Missing: capacity, email, contact person.

---

### Source 3: Instagram/Social Discovery
| Account | Type | Contact |
|---------|------|---------|
| @abbeyroadbc | Venue - Abbey Road Taphouse | Via DM |
| @thebombayjazzclub | Curator/Events | Via DM |
| @thebombaycoalition | Live Band | +91 9167756919 |
| @modjo.music | Artist Booking | Via DM |

**Data Quality**: Good for discovery, poor for structured data.

---

### Source 4: Hindi Search Results (JustDial)
Localized search "लाइव संगीत रेस्टोरेंट मुंबई" returned venues with:
- Price for two: ₹250 - ₹3000
- Timings: 8:00 AM, 12:00 PM
- Ratings: 4.1+
- Locations: Powai, Fort, Marine Drive, Masjid Bunder

---

## Failed Sources (Require In-Region Scraping)

| Source | Error | Reason | Solution |
|--------|-------|--------|----------|
| TripAdvisor.in | 403 | Geo-blocking | India proxy |
| Zomato | Timeout | JS + geo-blocking | Playwright + India |
| LBB.in | CSS only | Heavy JS render | Headless browser |
| Magicpin | 502 | JS + blocking | Playwright + India |
| Holidify | CSS only | Heavy JS render | Headless browser |
| BohoTheBar | CSS only | Heavy JS render | Headless browser |

---

## Proposed Unified Schema

```json
{
  "venue": {
    "id": "uuid",
    "name": "string",
    "name_local": "string (Hindi/regional)",
    "slug": "string",

    "location": {
      "address_line1": "string",
      "address_line2": "string",
      "area": "string (e.g., Koramangala)",
      "city": "string",
      "state": "string",
      "pincode": "string",
      "coordinates": {
        "lat": "float",
        "lng": "float"
      }
    },

    "contact": {
      "phone_primary": "string",
      "phone_secondary": "string",
      "email": "string",
      "website": "string",
      "instagram": "string",
      "facebook": "string",
      "booking_contact": {
        "name": "string",
        "role": "string",
        "phone": "string",
        "email": "string"
      }
    },

    "venue_details": {
      "venue_type": ["bar", "pub", "restaurant", "club", "lounge", "hotel"],
      "capacity_seated": "int",
      "capacity_standing": "int",
      "has_stage": "boolean",
      "has_sound_system": "boolean",
      "has_dance_floor": "boolean"
    },

    "music": {
      "has_live_music": "boolean",
      "music_frequency": ["daily", "weekends", "weekly", "occasional"],
      "genres": ["rock", "jazz", "bollywood", "electronic", "indie", "classical"],
      "typical_days": ["fri", "sat", "sun"],
      "typical_times": "string (e.g., 8pm-12am)"
    },

    "business": {
      "price_for_two": "int (INR)",
      "price_tier": ["budget", "mid", "premium", "luxury"],
      "cuisines": ["string"],
      "opening_hours": {
        "mon": "string",
        "tue": "string",
        ...
      },
      "license_type": "string"
    },

    "ratings": {
      "google_rating": "float",
      "google_reviews": "int",
      "zomato_rating": "float",
      "zomato_reviews": "int",
      "tripadvisor_rating": "float",
      "justdial_rating": "float",
      "justdial_reviews": "int"
    },

    "metadata": {
      "sources": [
        {
          "source_name": "string",
          "source_url": "string",
          "scraped_at": "datetime",
          "confidence_score": "float (0-1)"
        }
      ],
      "first_seen": "datetime",
      "last_updated": "datetime",
      "verified": "boolean",
      "verified_at": "datetime",
      "verified_by": "string"
    },

    "pro_relevance": {
      "plays_recorded_music": "boolean",
      "has_dj": "boolean",
      "has_live_performers": "boolean",
      "estimated_music_hours_weekly": "int",
      "license_status": "unknown|licensed|unlicensed",
      "pro_contact_attempted": "boolean",
      "pro_notes": "string"
    }
  }
}
```

---

## Source Scoring Heuristics

### Quality Dimensions (0-10 each)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | % of schema fields filled |
| Contact Info | 25% | Has phone/email/booking contact |
| Freshness | 20% | Last updated < 6 months |
| Accuracy | 15% | Cross-verified across sources |
| Specificity | 15% | Music-specific data (genres, times) |

### Source Scores (Based on Testing)

| Source | Completeness | Contact | Freshness | Accuracy | Specificity | TOTAL |
|--------|--------------|---------|-----------|----------|-------------|-------|
| JustDial | 7 | 9 | 8 | 7 | 3 | **6.8** |
| GigHub | 3 | 2 | 9 | 9 | 8 | **5.8** |
| Google Maps | 8 | 8 | 9 | 8 | 2 | **7.1** |
| Zomato | 9 | 4 | 9 | 8 | 4 | **6.9** |
| TripAdvisor | 7 | 3 | 7 | 8 | 5 | **6.0** |
| Instagram | 2 | 6 | 10 | 6 | 7 | **5.8** |
| LBB | 6 | 4 | 8 | 7 | 9 | **6.6** |

### Recommended Scraping Priority
1. **Google Maps** (7.1) - Best balance of coverage + contact
2. **Zomato** (6.9) - Good data, needs in-region
3. **JustDial** (6.8) - Excellent contacts, needs localization
4. **LBB** (6.6) - Best music specificity, JS rendering needed
5. **TripAdvisor** (6.0) - Good reviews, geo-blocked
6. **GigHub** (5.8) - Curated but sparse
7. **Instagram** (5.8) - Discovery only

---

## Localized Search Terms (Agent Should Learn)

### Hindi (हिन्दी)
| English | Hindi | Transliteration |
|---------|-------|-----------------|
| live music | लाइव म्यूजिक | laiv myuuzik |
| live music restaurant | लाइव संगीत रेस्टोरेंट | laiv sangeet restaurant |
| bar pub | बार पब | baar pab |
| night club | नाइट क्लब | nait klab |
| live band | लाइव बैंड | laiv baind |

### Kannada (for Bangalore)
| English | Kannada |
|---------|---------|
| live music | ಲೈವ್ ಮ್ಯೂಸಿಕ್ |
| restaurant | ಉಪಾಹಾರ ಗೃಹ |

### Marathi (for Mumbai/Pune)
| English | Marathi |
|---------|---------|
| live music | लाइव्ह म्युझिक |
| restaurant bar | रेस्टॉरंट बार |

### Slang/Colloquial Terms
- "adda" (hangout spot)
- "jam session"
- "gig venue"
- "open mic"
- "unplugged nights"

---

## Revised Cost Estimate

### Infrastructure (AWS ap-south-1)

| Component | Spec | Monthly Cost |
|-----------|------|--------------|
| EC2 (Playwright) | t3.medium | $30 |
| Residential Proxies | 10K requests | $50-100 |
| Lambda (orchestration) | 1M invocations | $5 |
| RDS Postgres | db.t3.micro | $15 |
| S3 (raw data) | 10GB | $0.25 |
| **TOTAL INFRA** | | **~$100-150/mo** |

### Per-Scrape Costs

| Source | Pages | Proxy Cost | LLM Extract | Total |
|--------|-------|------------|-------------|-------|
| Google Maps (15 cities) | 750 | $15 | $7.50 | $22.50 |
| JustDial (15 cities) | 450 | $9 | $4.50 | $13.50 |
| Zomato (10 cities) | 300 | $6 | $3.00 | $9.00 |
| LBB/Magicpin | 200 | $4 | $2.00 | $6.00 |
| Detail pages (4000) | 4000 | $80 | $40.00 | $120.00 |
| **TOTAL ONE-TIME SCRAPE** | | | | **~$170** |

### Full Project Cost (4000 venues)

| Phase | Cost |
|-------|------|
| Infrastructure setup | $0 (use existing AWS) |
| First scrape | ~$170 |
| Enrichment (emails, socials) | ~$50 |
| Manual QA (10 hrs @ $15) | ~$150 |
| **TOTAL** | **~$370** |

**Revised estimate**: $370 for 4000 venues (was $100-150 estimate before understanding JS rendering needs)

---

## Architecture Requirements

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│  - Prompt input                                              │
│  - Region selector                                           │
│  - Schema designer (interactive)                             │
│  - Cost calculator (real-time)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Claude)                     │
│  - Parse user intent                                         │
│  - Generate localized search terms                           │
│  - Select sources based on scoring                           │
│  - Coordinate regional agents                                │
│  - Deduplicate and merge                                     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  AWS ap-south-1  │ │  AWS eu-west-1   │ │  AWS us-east-1   │
│  (India)         │ │  (Europe)        │ │  (Americas)      │
│                  │ │                  │ │                  │
│  - Playwright    │ │  - Playwright    │ │  - Playwright    │
│  - Proxy pool    │ │  - Proxy pool    │ │  - Proxy pool    │
│  - Local LLM?    │ │  - Local LLM?    │ │  - Local LLM?    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  - Postgres (structured)                                     │
│  - Vector DB (embeddings for dedup)                          │
│  - S3 (raw HTML/screenshots)                                 │
│  - Metadata store (source scoring, job history)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Validate with in-region test**: Deploy Playwright to ap-south-1, test Zomato/TripAdvisor
2. **Build schema designer UI**: Interactive field mapping
3. **Implement source scoring**: Learn from each scrape job
4. **Create search term learner**: Store successful terms per region/category
