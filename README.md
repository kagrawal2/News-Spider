# News-Spider
Web spider that Collects news summaries from TechCrunch and MarketWatch. Future editions will have classification algorithms for objectivity in news titles.

##Features and Usage
* Utilize the automaticScraper by configuring GMAIL server with your credentials
* Utilize Mac launchd and launchctl to create a plist file that runs this script everyday
* Cache is deleted every 3 days by pickling a dictionary
* Collects news from two sources, compiles into a short html file and emails a mailing list everyday.
