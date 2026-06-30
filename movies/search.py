from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=[settings.ELASTICSEARCH_HOST],
    basic_auth=(
        settings.ELASTICSEARCH_USERNAME,
        settings.ELASTICSEARCH_PASSWORD,
    ),
)
