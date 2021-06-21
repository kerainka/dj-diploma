import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from .conftest import user, user_api


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make('Review', **kwargs)
    return factory


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make('Collection', **kwargs)
    return factory

