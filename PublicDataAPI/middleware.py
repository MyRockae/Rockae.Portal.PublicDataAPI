from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip API key check for swagger docs
        if request.path == '/':
            return self.get_response(request)
        
        # Skip API key check for swagger docs
        if request.path.startswith('/api/public/schema/'):
            return self.get_response(request)

        # Get API key from header
        api_key = request.headers.get(settings.API_KEY_HEADER)
        
        if not api_key:
            return JsonResponse({
                'message': f'No API key provided. Please include your API key in the {settings.API_KEY_HEADER} header.',
                'code': 'no_api_key'
            }, status=401)

        # Strip any quotes and whitespace
        api_key = api_key.strip().strip('"\'')
        expected_key = settings.API_KEY.strip().strip('"\'')

        if api_key != expected_key:
            return JsonResponse({
                'message': 'Invalid API key',
                'code': 'invalid_api_key'
            }, status=401)

        return self.get_response(request) 
