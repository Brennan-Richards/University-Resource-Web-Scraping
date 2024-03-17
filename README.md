# University-Resource-Web-Scraping
A repository containing a collection of methods for gathering a large amount of data about a university. Data ultimately used to create a database for grounding a chat assistant.

# File descriptions

- Web Scraping.ipynb contains a notebook file used for collecting publicly available information about the University of Rhode Island using the Requests library and Beautiful Soup
- Web Scraping - Research Labs.ipynb is similar to above but for different source URLs with nested links
- scrape-courses.py uses selenium to scrape course description from a dynmically rendered webpage (dynamic rendering meant that requests + bs4 method did not suffice)
- Cognitive Search Indexing.ipynb stores all of the collected data into an Azure AI Search (formerly Cognitive Search) index, runs some test queries against the index, and leverages GPT-3 to generate answers based on available (grounding) data.
- University GTM Strategy.ipynb is a more-or-less separate set of methods leveraging Bing Search and GPT to determine which universities are likely to work with Microsoft. Used as part of a go-to-market strategy for determining which universities to partner with in the future.
