from urllib.parse import unquote, quote
import uuid
import hashlib
from sanic import Sanic
from sanic.response import json
import logging

logger = None
app = Sanic('rarticler_api')
app.config.SANIC_JWT_AUTHORIZATION_HEADER = "authorization2"

from sanic_jwt.decorators import protected
from sanic_jwt import exceptions
from sanic_jwt import initialize


class User(object):
    def __init__(self, id, username, password_hash):
        self.user_id = id
        self.username = username
        self.password_hash = password_hash

    def __str__(self):
        return f"User(id='{ self.user_id }')"


def compute_pass_hash(password):
    return hashlib.sha512(password.encode('utf-8') + b'q9890as89dfh').hexdigest()

async def get_user_from_mongo(username):
    user_data = await db2.find_one(dict(username=username))
    if not user_data:
        return None
    return User(id=user_data['user_id'], password_hash=user_data['password_hash'],
                username=user_data['username'])


async def put_user_to_mongo(username, password, email):
    uid = str(uuid.uuid4())
    exists = await get_user_from_mongo(username)
    if exists:
        return f'User { username } already exists!'
    pass_hash = compute_pass_hash(password)
    await db2.insert_one(dict(user_id=uid, email=email,
                        username=username, password_hash=pass_hash))
    return f'User { username } created. Please, sign in!'


async def authenticate(request, *args, **kwargs):
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await get_user_from_mongo(username)

    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if compute_pass_hash(password) != user.password_hash:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    user.password_hash = ''

    return user


initialize(app, authenticate)


@app.listener('before_server_start')
def init(sanic, loop):
    global db
    global db2
    global db3
    from elasticsearch_async import AsyncElasticsearch
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_uri = "mongodb://127.0.0.1:27017/"
    db = AsyncElasticsearch(hosts=['localhost'])
    db2 = AsyncIOMotorClient(mongo_uri)['highload']['users']
    db3 = AsyncIOMotorClient(mongo_uri)['highload']['library_documents']


@app.middleware("request")
async def log_uri(request):
    # Simple middleware to log the URI endpoint that was called
    logger.info(f"URI called: { request.url }")


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
async def search(request):
    query = request.args.get('query', '')
    page = int(request.args.get('page', '1'))
    docs, pages = await query_from_db(unquote(query), page)
    for doc in docs:
        doc['link'] = make_arxiv_link(doc['clean_id'])
        del doc['file']
    return json({'query': query, 'answer':
                    {'items': docs, 'page': page, 'pages': pages}})


@app.route('/register', methods=['POST'])
async def register(request):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    register_result = await put_user_to_mongo(username, password, email)
    return json({'register_result': register_result})


async def query_from_library(username, page):
    page_size = 10
    start = page_size * (page - 1)

    cursor = db3.find(dict(username=username))
    links = await cursor.to_list(1000000)
    hits = len(links)
    pages = max(1, hits // page_size + (hits % page_size > 0))

    if hits == 0:
        docs = []
    else:
        links = list(map(lambda x: quote(x['clean_id']),
                     links[start:page_size * page]))
        results = []
        for link in links:

            result = await db.get(index='abstracts', doc_type='abstract',
                               id=link)

            results.append(result['_source'])

        docs = results

    return docs, pages


@app.route('/library/list', methods=['GET'])
@protected()
async def library_list(request):
    username = request.args.get('username', None)
    page = int(request.args.get('page', '1'))
    docs, pages = await query_from_library(unquote(username), page)
    for doc in docs:
        doc['link'] = make_arxiv_link(doc['clean_id'])
        del doc['file']
    return json({'query': username, 'answer':
                    {'items': docs, 'page': page, 'pages': pages}})


async def add_to_library(username, clean_id):
    if (await db3.find(dict(username=username, clean_id=clean_id)).count()) > 0:
        return False
    result = await db3.insert_one(dict(username=username, clean_id=clean_id))
    return True

@app.route('/library/add', methods=['POST'])
@protected()
async def library_add(request):
    username = request.json['username']
    clean_id = request.json['clean_id']
    result = await add_to_library(username, clean_id)
    return json({'result': result})


async def remove_from_library(username, clean_id):
    result = await db3.delete_many(dict(username=username, clean_id=clean_id))
    return True


@app.route('/library/remove', methods=['POST'])
@protected()
async def library_remove(request):
    username = request.json['username']
    clean_id = request.json['clean_id']
    result = await remove_from_library(username, clean_id)
    return json({'result': result})


def setup_logging():
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        filename='api.log',  # app.config.APP_LOGFILE,
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
