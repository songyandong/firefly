from webob import Request, Response
from webob.exc import HTTPNotFound
import json

class Firefly(object):
    def __init__(self):
        self.mapping = {}

    def add_route(self, path, function, **kwargs):
        self.mapping[path] = FireflyFunction(function, **kwargs)

    def __call__(self, environ, start_response):
        request = Request(environ)
        path = request.path_info
        if path in self.mapping:
            func = self.mapping[path]
            response = func(request)
        else:
            response = Response()
            response.status = "404 Not Found"
            response.text = json.dumps({"status": "not found"})
        return response(environ, start_response)


class FireflyFunction(object):
    def __init__(self, function, **kwargs):
        self.function = function

    def __call__(self, request):
        kwargs = self.get_inputs(request)
        result = self.function(**kwargs)
        return self.make_response(result)

    def get_inputs(self, request):
        return json.loads(request.body.decode('utf-8'))

    def make_response(self, result):
        response = Response(content_type='application/json',
                            charset='utf-8')
        response.text = json.dumps(result)
        return response