from app import app
from flask import render_template, redirect, url_for, request
import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import markdown as md

def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            return [item.get_text().strip() for item in ancestor.select(selector)]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "useful": ["button.vote-yes > span"],
    "useless": ["button.vote-no > span"],
    "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
    "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
}

@app.route('/')
def index():
    
    if os.path.isfile('README.md'):
        with open('README.md') as md_file:
            md_to_html = md.markdown(md_file.read(), extensions = ['tables', 'markdown.extensions.fenced_code'])
    else:
        md_to_html = None

    return render_template('index.html.jinja', markdown = md_to_html)

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        url = f"https://www.ceneo.pl/{product_id}#tab opinions"
        all_opinions = []
        
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, "html.parser")
            opinions = page.select("div.js_product-review")
            
            for opinion in opinions:
                single_opinion = {
                    key:get_item(opinion, *value)
                        for key, value in selectors.items()
                }
                single_opinion["opinion_id"] = opinion["data-entry-id"]
                all_opinions.append(single_opinion)
            
            try:
                url = "https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
            except TypeError:
                url = None
       
        if not os.path.exists("app/opinions"):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
        return redirect(url_for('product', product_id=product_id))
    
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    opinions = pd.read_json(f"app/opinions/{product_id}.json")
    opinions.columns = opinions.columns.str.replace(' ', '_')
    opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))
    stats = {
        "product_rating": opinions.stars.mean().round(2),
        "opinions_count": opinions.shape[0],
        "pros_count": opinions.pros.map(bool).sum(),
        "cons_count": opinions.cons.map(bool).sum(),
       # "pros_count": opinions.recommendation.value_counts().Polecam if hasattr(opinions, 'Polecam') else '0',
       # "cons_count": opinions.recommendation.value_counts().Nie_polecam if hasattr(opinions, 'Nie polecam') else '0'
    }

    recommendations = opinions.recommendation.value_counts(dropna=False)
    recommendations.plot.pie(
        label="",
        title="Rekomendacje",
        labels=["Polecam", "Nie polecam", "Nie udzielono"],
        colors=["palegreen", "salmon", "lightslategray"]
    )
    plt.savefig(f"app/static/plots/{product_id}_recommendation.png")
    plt.close()

    return render_template("product.html.jinja", stats=stats, product_id=product_id,  opinions=opinions.to_numpy(), tables=[opinions.to_html(classes='table table-sm table-hover table-bordered', header="true", table_id="opinions")])
