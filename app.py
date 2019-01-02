# The Data Incubator: Capstone Project
#
# Deep Metal: A Sentiment Classifier
#
# Copyright 2019, Alexander Sack

import io
import os
import re
import requests
import spacy
import sys

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from flask import Flask, render_template, request, redirect, flash, url_for, Markup
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'deepmetal')

# We load on-demand but only once
nlp = None

# MA checks for a valid header.
MA_HEADERS = {
        'User-Agent': str(UserAgent().firefox),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.metal-archives.com'
}
MA_STATS_URL = "https://www.metal-archives.com/stats"

def update_ma_stats():
    """ Retrieve latest stats from MA """

    r = requests.get(MA_STATS_URL, headers=MA_HEADERS)
    if r.status_code == 200:
        r_soup = BeautifulSoup(r.content, 'lxml')
        strongs = r_soup.find_all('strong')
        if strongs:
            return (strongs[0].text, strongs[1].text, strongs[-2].text, strongs[3].text, strongs[-1].text, strongs[4].text)
    return ("","","")

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """ Perform inference using pretrained model """

    global nlp
    if not nlp:
        nlp = spacy.load('data/ma_model1')

    output = ""
    review = request.data.decode()
    if review:
        doc = nlp(review)
        if doc.cats['POSITIVE'] >= 0.5:
            color = "green"
            output += '<p class="text-left"><i class="fa fa-thumbs-up" aria-hidden="true"></i></p>'
        else:
            color = "red"
            output += '<p class="text-left"><i class="fa fa-thumbs-down" aria-hidden="true"></i></p>'
        output += '<p class="text-left"><strong style="color:{0}">POSITIVE = {1}</strong></p>'.format(color, str(doc.cats['POSITIVE']))

    return encode_utf8(output)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Main page """

    # Static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    (bands, reviews, albums, labels, songs, artists) = update_ma_stats()

    # Render our results (if any)
    html = render_template('index.html',
            bands=bands,
            reviews=reviews,
            albums=albums,
            labels=labels,
            songs=songs,
            artists=artists,
            avgratingsworldmap='avgratingsbandsworldmap-plot.html',
            avgnumworldmap='avgnumbandsworldmap-plot.html',
            genres='genres-plot.html',
            avgratingbygenre='avgratingbygenre-plot.html',
            avgwordsbyyear='avgwordsbyyear-plot.html',
            tsne='tsne-plot.html',
            heatmap='heatmap-plot.html')

    return encode_utf8(html)

if __name__ == '__main__':
    # FIXME: Move to separate settings file.
    app.run(port=33507, debug=True) # Heroku reserved port for flask applications
