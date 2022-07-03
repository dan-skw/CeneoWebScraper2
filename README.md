## Single opinion structure on [Ceneo.pl](https://www.ceneo.pl/)

|Element|Selector|Variable|Data type|
|-------|--------|--------|---------|
|Opinion|div.js_product-review|opinion|bs4.element.Tag|
|Opinion id|\["data-entry-id"\]|opinion_id|str|
|Author|span.user-post__author-name|author|str|
|Recommendation|span.user-post__author-recomendation > em|rcmd|bool|
|Stars score|span.user-post__score-count|score|float|
|Content|div.user-post__text|content|str|
|List of adventages|div.review-feature__title--positives  ~ div.review-feature__item|pros|str|
|List of disadventages|div.review-feature__title--negatives  ~ div.review-feature__item|cons|str|
|Date of posting opinion|span.user-post__published > time:nth-child(1)\["datetime"\]|posted_on|str|
|Date of purchasing product|span.user-post__published > time:nth-child(2)\["datetime"\]|bought_on|str|
|For how many users useful|button.vote-yes > span|useful_for|int|
|For how many users useless|button.vote-no > span|useless_for|int|


## Requirements and tech stack
- Python - main programming language
- Flask - web framework
- Bootstrap - for styling
- BeautifulSoup - scraping data
- Matplotlib and pandas
- Markdown - renderning on the main site
- JQuery and Datatables - for dynamically rendered table of opinions

## Getting started

Download and open then run python virutal enviroment. Type in terminal

`source venv/scripts/activate`

`pip install -r requirements.txt`

And run flask server

`flask run`

then open [http://localhost:5000/](http://localhost:5000/) in your browser

## Etapy pracy nad projektem strukturalnym
I couldn't resolve problem with polish special chars so still have to do it...