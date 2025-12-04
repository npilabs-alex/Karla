# Karla Features

## Core Features

### 1. In-Region Scraping
Deploy Playwright browsers in regional AWS datacenters to bypass geo-blocking and render JS-heavy sites.

**Problem**: Sites like Zomato, TripAdvisor, Magicpin return 403 errors or empty JS shells when accessed from outside their target region.

**Solution**:
- Playwright browsers running in AWS regions (ap-south-1 for India, eu-west-1 for Europe, etc.)
- Residential proxy pools to appear as real local users
- Automatic region detection and routing

**Status**: Design complete

---

### 2. Localised Discovery
Search in local languages to surface data that English queries miss.

**Problem**: English searches miss venues that are listed in local languages. Hindi search "लाइव संगीत रेस्टोरेंट मुंबई" returns different (and more complete) results than "live music restaurant Mumbai".

**Solution**:
- LLM generates localised search terms per region/category
- Support for Hindi, Kannada, Marathi, and regional slang ("adda", "gig venue")
- System learns which terms work best per source

**Status**: Design complete

---

### 3. Source Scoring
System learns which sources yield best data per category/region.

**Problem**: Not all sources are equal. Some have great contact info but poor specificity. Others are curated but sparse.

**Solution**:
Weighted scoring across 5 dimensions:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | % of schema fields filled |
| Contact Info | 25% | Has phone/email/booking contact |
| Freshness | 20% | Last updated < 6 months |
| Accuracy | 15% | Cross-verified across sources |
| Specificity | 15% | Domain-specific data (genres, times) |

System re-scores after each job and adjusts source priority.

**Status**: Design complete

---

### 4. Entity Resolution
Fuzzy matching + LLM to deduplicate records across sources.

**Problem**: Same venue appears differently across sources:
- "Kitty Su Mumbai"
- "KittySu, Lower Parel"
- "KITTYSU"

**Solution**:
- Fuzzy string matching on name + location
- Vector embeddings for semantic similarity
- LLM confirmation for edge cases
- Merge records, retain source attribution

**Status**: Design complete

---

### 5. Confidence Scoring
Multi-source verification with quality scores.

**Problem**: Single-source data is unreliable. Need to know which records are solid and which need verification.

**Solution**:
- Each record gets a confidence score (0-1)
- More sources agreeing = higher confidence
- Single-source venues flagged for review
- Conflicting data triggers LLM resolution

**Status**: Design complete

---

### 6. Dynamic Schema
Unified schema that adapts to different data types without rebuilding pipelines.

**Problem**: Different jobs need different fields. Rebuilding pipelines for each client is expensive.

**Solution**:
- Core schema with extensible metadata
- LLM extracts fields based on job definition
- Schema designer UI for custom jobs
- Automatic field mapping from source to schema

**Status**: Design complete

---

### 7. Orchestrator
Claude-powered coordination layer.

**Responsibilities**:
- Parse user intent from natural language prompt
- Generate localised search terms
- Select sources based on scoring
- Coordinate regional agents
- Deduplicate and merge results
- Calculate costs in real-time

**Status**: Design complete

---

## Planned Features

### 8. Cost Calculator
Real-time cost estimation before running jobs.

---

### 9. Schema Designer UI
Interactive field mapping and job configuration.

---

### 10. Search Term Learner
Store and rank successful search terms per region/category.

---

## Feature Status Key

- **Design complete**: Architecture defined, ready for implementation
- **In progress**: Currently being built
- **Shipped**: Available in production
