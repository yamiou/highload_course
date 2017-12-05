from urllib.parse import unquote
from sanic import Sanic
from sanic.response import json
import logging

logger = None
app = Sanic('rarticler_api')


@app.listener('before_server_start')
def init(sanic, loop):
    global db
    from elasticsearch_async import AsyncElasticsearch
    db = AsyncElasticsearch(hosts=['localhost'])


@app.middleware("request")
async def log_uri(request):
    # Simple middleware to log the URI endpoint that was called
    logger.info("URI called: {0}".format(request.url))


async def query_from_db(query, page):
    page_size = 10
    start = page_size * (page - 1)

    result = await db.search(index='abstracts', doc_type='abstract',
                             body = {
                                "query": {
                                    "multi_match" : {
                                        "query" : query,
                                        "type": "most_fields",
                                        "operator": "and",
                                        "fields": [
                                            'abstract',
                                            'title']
                                    }
                                }
                             },
                             size=page_size,
                             from_=start)
    hits = result['hits']['total']
    pages = min(max(1, hits // page_size + (hits % page_size > 0)), 100)

    if hits == 0:
        docs = []
    else:
        docs = [hit['_source'] for hit in result['hits']['hits']]
    return docs, pages


def make_arxiv_link(clean_id):
    return f'https://arxiv.org/abs/{clean_id}'


@app.route('/search', methods=['GET'])
async def abstracts(request):
    query = request.args.get('query', '')
    page = int(request.args.get('page', '1'))
    docs, pages = await query_from_db(unquote(query), page)
    for doc in docs:
        doc['link'] = make_arxiv_link(doc['clean_id'])
        del doc['file']
    return json({'query': query, 'answer':
                    {'items': docs, 'page': page, 'pages': pages}})


def setup_logging():
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        filename='api.log/',  # app.config.APP_LOGFILE,
        format=logging_format,
        level=logging.DEBUG)


def configure():
    setup_logging()


def main():
    global logger
    configure()
    logger = logging.getLogger()
    app.run(host="127.0.0.1", port=7080)


if __name__ == "__main__":
    main()
