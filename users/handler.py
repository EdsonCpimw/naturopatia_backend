from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # method = context['request'].method
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {'detail': 'Nenhuma conta ativa encontrada com as credenciais fornecidas.'}

    return response