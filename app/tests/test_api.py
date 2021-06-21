from django.urls import reverse
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_get_product(product_factory, api_client):
    product = product_factory()
    url = reverse('product-detail', args=[product.id])
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    ids = resp_json['ids']
    assert len(ids) == 1


@pytest.mark.django_db
def test_product_list(product_factory, api_client):
    products = product_factory(_quantity=4)
    url = reverse('products-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(products) == len(resp_json)


@pytest.mark.django_db
def test_filter_id(product_factory, api_client):
    url = reverse('products-list')
    products = product_factory(_quantity=4)
    id = products[0].id
    resp = api_client.get(url, {"id": id})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]['id'] == id


@pytest.mark.django_db
def test_filter_name(api_client, product_factory):
    url = reverse('product-list')
    product = product_factory(name='Test')
    params = {
        'name': 'Test'
    }
    resp = api_client.get(url, params)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['name'] == product.name


@pytest.mark.django_db
def test_create_product(api_client):
    url = reverse('products-list')
    params = {
        'name': 'Test'
    }
    resp = api_client.post(url, params)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json['name'] == params['name']


@pytest.mark.django_db
def test_update_product(product_factory, api_client):
    product = product_factory()
    new_product = product_factory()
    url = reverse('products-detail', args=[product.id])
    params = {
        'id': new_product.id
    }
    resp = api_client.create(url, params)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['name'][0] == new_product.id


@pytest.mark.django_db
def test_success_delete(product_factory, api_client):
    product = product_factory()
    url = reverse('products-detail', args=[product.id])
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT