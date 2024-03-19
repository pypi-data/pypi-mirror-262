import requests


class authRequests():

    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    def add_auth_headers(self, **kargs):
        if not kargs.get("headers"):
            kargs["headers"] = {}
        kargs["headers"]["x-access-token"] = self.token
        return kargs

    def raise_or_success(self, r: requests.Response):
        if r.status_code in [403, 404]:
            raise Exception(f"got status_code: {r.status_code}, {r.url}")
        if r.status_code == 500:
            raise Exception(
                f"got status_code: {r.status_code}, {r.request.headers}, {r.request.body}")
        if r.status_code != 200:
            raise Exception(f"got status_code: {r.status_code}, {r.text}")
        return r.json()

    def get(self, **kargs):
        r = requests.get(**self.add_auth_headers(**kargs))
        return self.raise_or_success(r)

    def post(self, **kargs):
        r = requests.post(**self.add_auth_headers(**kargs))
        return self.raise_or_success(r)

    def delete(self, **kargs):
        r = requests.delete(**self.add_auth_headers(**kargs))
        return self.raise_or_success(r)

    def patch(self, **kargs):
        r = requests.patch(**self.add_auth_headers(**kargs))
        return self.raise_or_success(r)

    def put(self, **kargs):
        r = requests.put(**self.add_auth_headers(**kargs))
        return self.raise_or_success(r)
