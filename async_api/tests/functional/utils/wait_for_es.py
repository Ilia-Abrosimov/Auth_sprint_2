import backoff
from elasticsearch import Elasticsearch
from tests.functional.settings import settings
from tests.functional.utils.tools import backoff_hdlr


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError, on_backoff=backoff_hdlr)
def wait_elastic():
    es = Elasticsearch(hosts=[f"{settings.ES_HOST}:{settings.ES_PORT}"])
    if not es.ping():
        raise ConnectionError('ES is not ready yet...')
    es.close()


if __name__ == '__main__':
    wait_elastic()
