from tornado.testing import AsyncHTTPTestCase

from lib.session import HashSession

"""
    |  HTTP Response object.
 |
 |  Attributes:
 |
 |  * request: HTTPRequest object
 |
 |  * code: numeric HTTP status code, e.g. 200 or 404
 |
 |  * reason: human-readable reason phrase describing the status code
 |
 |  * headers: `tornado.httputil.HTTPHeaders` object
 |
 |  * effective_url: final location of the resource after following any
 |    redirects
 |
 |  * buffer: ``cStringIO`` object for response body
 |
 |  * body: response body as string (created on demand from ``self.buffer``)
 |
 |  * error: Exception object, if any
 |
 |  * request_time: seconds from request start to finish
 |
 |  * time_info: dictionary of diagnostic timing information from the request.
 |    Available data are subject to change, but currently uses timings
 |    available from http://curl.haxx.se/libcurl/c/curl_easy_getinfo.html,
 |    plus ``queue``, which is the delay (if any) introduced by waiting for
 |    a slot under `AsyncHTTPClient`'s ``max_clients`` setting.
 |
"""


class TestMainHandler(AsyncHTTPTestCase):
    def get_app(self):
        import app
        return app.Application()

    def test_unauthorized_main_get(self):
        """
        Check if redirection to /auth was successful
        """
        response = self.fetch('/')
        self.assertIn(b'<title>Welcome</title>', response.body)

    def test_authorized_main_get(self):
        """
        Check if user with access status '3' can get main.html through get
        """
        session = HashSession()
        key = '123456'
        user = {
            'id': '11',
            'login': 'allinc',
            'email': 'kkk@kkk.ua',
            'access': '1234',
            'activated': '1'
        }
        session[key] = user
        headers = {'Cookie': f'session={key}'}
        response = self.fetch('/', headers=headers)
        self.assertIn(b'<div class="menuItem" statistics>', response.body)

    def test_main_with_inline_get(self):
        """
        Test how main interacts with /?inline=1
        """
        session = HashSession()
        key = '123456'
        user = {
            'id': '11',
            'login': 'allinc',
            'email': 'kkk@kkk.ua',
            'access': '1234',
            'activated': '1'
        }
        session[key] = user
        headers = {'Cookie': f'session={key}'}
        response = self.fetch('/?inline=1', headers=headers)
        self.assertIn(b'<div class="menuItem" statistics>', response.body)