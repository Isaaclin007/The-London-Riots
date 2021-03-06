from londonriots.scripts import environment
import sys
import londonriots.models as models
import londonriots.feeds.currency as currency
import transaction
import time
from BeautifulSoup import BeautifulSoup
import nltk
import londonriots.feeds.tagged_words as tagged_words
import pprint as pp
import logging
import traceback as tb

log = logging.getLogger(__name__)

def main():
    with environment(sys.argv) as env:
        try:
            tag_articles()
            transaction.commit()
        except:
            log.error(tb.format_exc())
            transaction.abort()

        models.DBSession.close()
        log.info("End tagging")

def tag_articles():
    for article in models.DBSession.query(models.Article):
        if len(article.entity_frequencies):
            continue

        log.info("Tagging article %d", article.id)
        entities = tagged_words.tag_article(article)
        if not len(entities):
            log.warn("Article %d had no named entities extracted (%s).", 
                     article.id,
                     article.url)
            open(("article-%d.html" % article.id).encode("utf-8"),
                 "w").write(article.source_text.encode("utf-8"))
