# python-scrapy-scraper

-> Create virtual enviroment and install necessary library
    pip install virtualenv
    python -m venv venv
    venv\Scripts\activate
    pip install scrapy, scrapeops_scrapy_proxy_sdk, scrapy-user-agents, pymongo
    pip install scrapy-fake-useragent

-> Optional for known only how to create project from scratch 
    scrapy startproject ['name]
    cd ['name]
    scrapy genspider ['name]_spider ['name].com

-> Start scraping
    scrapy crawl ['name]

-> In setting add

--> If you are using scrapy-fake-useragent
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1


--> If you are using scrapeops_scrapy_proxy_sdk, scrapy-user-agents
SCRAPEOPS_API_KEY = '1618e303-e0a3-456e-b3fe-eb7b5c4de5'
SCRAPEOPS_PROXY_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1

