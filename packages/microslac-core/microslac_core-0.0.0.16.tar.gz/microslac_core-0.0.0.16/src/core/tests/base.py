import pytest
from faker import Factory, Generator
from rest_framework.test import APIClient

from core.utils import utils


class TestBase:
    @staticmethod
    def objectify(data: dict):
        return utils.objectify(data)


@pytest.mark.django_db(databases=["default", "replication"])
class ApiTestBase(TestBase):
    fake: Generator
    client: APIClient

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.fake = Factory.create()

    def client_request(
        self,
        url: str,
        *,
        method: str = None,
        data: dict = None,
        format: str = None,
        ok: bool = None,
        status: int = None,
        client: APIClient = None
    ):
        data = data or {}
        format = format or "json"
        method = method or "post"
        assert method in ("get", "post", "put", "patch", "delete")
        client = client or self.client
        client_method = getattr(client, method)
        response = client_method(url, data=data, format=format)
        if status is not None:
            assert response.status_code == status
        resp = self.objectify(response.data)
        if ok is not None:
            assert resp.ok == ok
        return resp


@pytest.mark.django_db(databases=["default", "replication"])
class UnitTestBase(TestBase):
    pass
