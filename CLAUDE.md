# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Karla** - Agentic websearch and scraping system for regional data collection. Named after the Soviet spymaster in le Carré's novels; the smiley logo references his adversary George Smiley. The system deploys Playwright browsers in regional AWS datacenters to scrape geo-restricted and JS-heavy websites, using localised search terms and intelligent source scoring.

## Key Concepts

### In-Region Scraping
Many data sources (Zomato, TripAdvisor, Magicpin) geo-block requests from outside their target region and return empty JS shells without proper browser rendering. Solution: deploy Playwright in regional AWS (e.g., ap-south-1 for India) with residential proxies.

### Source Scoring
System learns which sources yield best data per category/region based on:
- Completeness (% of schema fields filled) - 25%
- Contact Info availability - 25%
- Freshness (<6 months) - 20%
- Accuracy (cross-verified) - 15%
- Specificity (domain-specific data) - 15%

### Localised Discovery
Search in local languages surfaces data that English queries miss entirely. E.g., Hindi "लाइव संगीत रेस्टोरेंट मुंबई" returns different JustDial results than "live music restaurant Mumbai".

### Entity Resolution
Fuzzy matching + LLM to deduplicate records like "Kitty Su Mumbai" vs "KittySu, Lower Parel" vs "KITTYSU".

## Architecture Components

- **Orchestrator**: Claude-powered coordination layer that parses intent, generates search terms, selects sources, coordinates regional agents
- **Regional Agents**: Playwright browsers in AWS regions with proxy pools
- **Data Layer**: Postgres (structured), Vector DB (dedup embeddings), S3 (raw HTML/screenshots)

## Documentation

See `docs/poc/` for India venues proof of concept including technical analysis, proposals, and sample data.
