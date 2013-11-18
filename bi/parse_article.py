from app import config, app

import requests


def parse_article(article, share):
    endpoint = config['ARTICLE_PARSE_ENDPOINT']

    payload = {
        'token': config.get('DIFFBOT_TOKEN', None),
        'url': article.url
    }

    resp = requests.get(endpoint, params=payload)

    if not resp.ok:
        app.logger.error('Failed to parse %s (error code: %s). Reason: %s'
                % (article, resp.status_code, resp.json() if resp.json() else 'unknown'))
        return

    json = resp.json()
    article.url = json['resolved_url']
    article.icon = json['icon']
    article.title = (json['title'][:252] + '...') if len(json['title']) > 255 else json['title']
    article.text = json['text']
    article.date = json['date']
    article.author = json.get('author', '')

    article.save()

    notify_new_article(article, share)


def notify_new_article(article, share):
    # FIXME todo sent notification mails
    app.logger.debug("Sending mail to %s from %s about %s" % (share.receiver, share.originator, article.title))
