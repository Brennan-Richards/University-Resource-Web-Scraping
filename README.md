# University Resource Scraping & Search Indexing

An end-to-end pipeline that turns a university's scattered public web pages into
a searchable index an LLM can answer from. Built against the University of Rhode
Island: scrape the pages, normalise them into structured records, push them into
Azure Cognitive Search, then query that index to ground a chat assistant.

This is the unglamorous half of a RAG system — the part that decides what the
assistant is actually able to know.

```
URI web pages ──▶ BeautifulSoup scrapers ──▶ CSV records
                                                  │
                                                  ▼
                                    Azure Cognitive Search index
                                                  │
                                                  ▼
                                    grounded GPT answers
```

## The notebooks

**`Web Scraping.ipynb`** — dissertation listings. Two-pass: parse the index page
for article links, then fetch each linked page and pull the fields out of it.
The two-pass shape is what makes the scraper resilient to listing pages that
only carry titles and URLs.

**`Web Scraping - Research Labs.ipynb`** — the same pattern applied to research
lab pages, which have a different DOM and a different set of fields.

**`scrape-courses.py`** — course catalogue scraping as a standalone script
rather than a notebook, for repeat runs.

**`Cognitive Search Indexing.ipynb`** — reads the scraped CSVs, builds a
formatted document per resource, and uploads them to an Azure Cognitive Search
index. Ends by querying the index through GPT to check that the retrieved
context actually answers real questions.

**`University GTM Strategy.ipynb`** — a separate piece of analysis over Rhode
Island universities, kept here because it reuses the same collection code.

## Running it

Each notebook needs its own credentials, supplied as environment variables
rather than edited into cells:

- Azure Cognitive Search: endpoint, index name, and an admin key
- Azure OpenAI or OpenAI: endpoint and key

Install: `pip install beautifulsoup4 requests pandas azure-search-documents openai`

## Notes and limitations

- **The selectors are tied to URI's markup as it was.** Any scraper of a site
  you don't control is a snapshot; these will need re-pointing when the pages
  change. That's inherent to the approach, not a defect of this code.
- **Respect `robots.txt` and rate limits** if you point this at another
  institution. The notebooks fetch politely but do not implement backoff.
- **No incremental indexing.** Each run rebuilds the document set rather than
  diffing against what is already indexed, which is fine at this scale and
  would not be at a larger one.
