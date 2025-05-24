from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    request={'application/json': {'type': 'object', 'properties': {'message': {'type': 'string'}}}},
    responses={200: {'type': 'object', 'properties': {
        'status': {'type': 'string'},
        'greeting': {'type': 'string'}
    }}},
    description='A simple health check endpoint that accepts an optional message and returns a greeting',
    examples=[
        OpenApiExample(
            'Basic Example',
            value={'message': 'World'},
            request_only=True,
        ),
        OpenApiExample(
            'Success Response',
            value={'status': 'healthy', 'greeting': 'Hello, World!'},
            response_only=True,
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def health_check(request):
    """
    A simple health check endpoint that accepts an optional message
    and returns a greeting response
    """
    message = request.data.get('message', 'World')
    
    response_data = {
        "status": "healthy",
        "greeting": f"Hello, {message}!"
    }
    
    return Response(response_data)
