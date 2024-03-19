import requests
import httpx
from fake_useragent import UserAgent
from urllib.parse import urljoin
from loguru import logger


class ApiRequestUtils:
    Accept = "application/json"
    ContentType = "application/json; charset=UTF-8"
    Proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    Http2Proxies = {
        "http://": "http://127.0.0.1:7890",
        "https://": "https://127.0.0.1:7890"
    }

    @staticmethod
    def get_requests_session():
        """会话保持 在外部调用 确保使用的是一个session"""
        return requests.session()

    @classmethod
    def get_requests_kwargs(cls, kwargs=None):
        kwargs = kwargs or {}  # 短路逻辑
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("User-Agent", cls.get_fake_useragent())
        kwargs["headers"].setdefault("Accept", cls.Accept)
        kwargs["headers"].setdefault("Content-Type", cls.ContentType)
        return kwargs

    @classmethod
    def handle_request(cls, client, method, url, kwargs):
        if hasattr(client, method):
            return getattr(client, method)(url, **kwargs)
        else:
            raise Exception("client unsupported method %s" % method)

    @classmethod
    def common_request(cls, url: str, method: str, kwargs=None, is_http2=False):
        kwargs = cls.get_requests_kwargs(kwargs)
        logger.info("common_request %s %s %s %s" % ("http1" if not is_http2 else "http2", method, url, kwargs))
        http2_dict = dict(http2=True)
        if is_http2 and "proxies" in kwargs:
            http2_dict["proxies"] = kwargs.pop("proxies", None)

        client = httpx.Client(**http2_dict) if is_http2 else requests

        if is_http2:
            with client as c:
                res = cls.handle_request(c, method, url, kwargs)
        else:
            res = cls.handle_request(client, method, url, kwargs)

        return res

    @classmethod
    def session_request(cls, url: str, method: str, kwargs=None, session=None):
        if not session:
            raise Exception("session_request session can not be None")
        kwargs = cls.get_requests_kwargs(kwargs)
        logger.info("session_request %s %s %s" % (method, url, kwargs))
        if method == "get":
            res = session.get(url, **kwargs)
        elif method == "post":
            res = session.post(url, **kwargs)
        else:
            raise Exception("session_request method error")

        return res

    @staticmethod
    def get_fake_useragent():
        return UserAgent().random

    @staticmethod
    def splicing_url_path(host: str, url: str):
        return urljoin(host, url)


if __name__ == '__main__':
    # logger.info(ApiRequestUtils.get_fake_useragent())
    logger.info(ApiRequestUtils.get_requests_kwargs())
