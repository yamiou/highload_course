from urllib.parse import unquote
import uuid
import hashlib
from sanic import Sanic
from sanic.response import json
import logging

logger = None
app = Sanic('rarticler_api')

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

    return user

initialize(app, authenticate)


@app.route("/protected")
@protected()
async def protected_route(request):
    return json({"protected": True})


@app.listener('before_server_start')
def init(sanic, loop):
    global db
    global db2
    from elasticsearch_async import AsyncElasticsearch
    from motor.motor_asyncio import AsyncIOMotorClient
    mongo_uri = "mongodb://127.0.0.1:27017/"
    db = AsyncElasticsearch(hosts=['localhost'])
    db2 = AsyncIOMotorClient(mongo_uri)['highload']['users']


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
