# twitter-notifier
twitter-notifier is a docker application to delivering
new tweet notifications to webhooks you own
since you may not want to receive notifications from
Twitter official app.

## About
Many Japanese use Twitter to send information.
I play *Blue Archive* and the new information about it
is sent on Twitter, so I had used Twitter API to retrieve
new tweets.

But Elon Musk sucked. He ruined everything.

When the API became unavailable without EXTREMELY EXPENSIVE cost,
I created this repo, named `scrapy-twitter`, to use `scrapy`
to crawl the timeline.

And in July, Twitter became more awful.
They disabled crawling without authentication, so
my scrapper became trash.
Therefore, I archived this repo.

I de-archive this repo because I found `rss-bridge` can help me.
This repo is named `twitter-notifier` now as this name is more general.

## Notice
Without Twitter API, all the methods are not fully correct,
e.g., you may see a fairly old tweet appear suddenly
or you need to see a new tweet several hour later from its publishing,
but it is not a fatal issue in general.

We, who just want to deliver notifications for individual use,
is helpless and have no better choice, yeah.