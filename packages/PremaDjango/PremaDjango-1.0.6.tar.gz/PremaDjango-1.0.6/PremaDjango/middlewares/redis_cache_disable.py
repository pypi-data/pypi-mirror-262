"""Middleware to disable client side caching."""

from django.utils.cache import add_never_cache_headers


class DisableClientSideCachingMiddleware:
    """Middleware to disable client side caching, that is on browser."""

    def __init__(self, get_response):
        """Initialize middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call middleware."""
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
