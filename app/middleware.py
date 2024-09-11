class HtmxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.htmx = self.is_htmx(request)
        return self.get_response(request)

    def is_htmx(self, request):
        return request.headers.get('HX-Request') == 'true'
            
