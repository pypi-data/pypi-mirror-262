from urllib import parse

import requests
from django.conf import settings

from .base import BaseService


class ProxyService(BaseService):
    _scheme: str = "http"
    _ssl: bool = False
    _host: str
    _port: int

    @classmethod
    def _get_url(cls, path: str) -> str:
        scheme = cls._scheme
        if cls._ssl:
            scheme = f"{scheme}s"
        netloc = f"{cls._host}:{cls._port}"
        url = parse.urlunsplit((scheme, netloc, path, "", ""))
        return url

    @classmethod
    def _get_base_headers(cls, internal: bool = False) -> dict[str, str]:
        base_headers = {}
        if internal:
            base_headers.update({"X-Internal": settings.INTERNAL_KEY})
        return base_headers

    @classmethod
    def post(
        cls,
        path,
        data: dict,
        key: str = None,
        keys: list[str] = None,
        internal: bool = False,
        **kwargs,
    ) -> dict:
        data = data or {}
        url = cls._get_url(path)
        headers = kwargs.pop("headers", {})
        base_headers = cls._get_base_headers(internal=internal)
        response = requests.post(
            url=url, json=data, headers={**headers, **base_headers}, **kwargs
        )
        resp = response.json()
        if key:
            resp = resp.get(key)
        if keys:
            resp = {key: resp.get(key) for key in keys}
        return resp
