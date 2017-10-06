import sys
import logging

logger = logging.getLogger(__name__)


def api_app():
    pass


def article_scrapper_app():
    pass


def article_processor_app():
    pass


def data_consolidation_app():
    pass


def feed_processor_app():
    pass


if __name__ == '__main__':
    apps = {k: v for k, v in globals().items() if k.endswith('_app')}
    if len(sys.argv) > 1 and sys.argv[1] in apps:
        app = sys.argv[1]
        apps[app]()
    else:
        logger.error(f'No application specified or application not exists, '
                     f'select one from {list(apps.keys())}')
