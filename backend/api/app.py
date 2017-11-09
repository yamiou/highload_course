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


async def query_from_db(query):
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
                             size=250)
    if result['hits']['total'] == 0:
        docs = []
    else:
        docs = [hit['_source'] for hit in result['hits']['hits']]
    return docs


def make_arxiv_link(clean_id):
    return f'https://arxiv.org/abs/{clean_id}'


@app.route('/search/<query>', methods=['GET'])
async def abstracts(request, query):
    docs = await query_from_db(query)
    for doc in docs:
        doc['link'] = make_arxiv_link(doc['clean_id'])
        del doc['file']
    return json({'query': query, 'answer': docs})


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
