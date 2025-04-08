import json
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

class ErrorHandlerMiddleware:
    """
    Middleware para manejar errores de la API
    Formato actual:
    {
        "detail": "mensaje de error"
    }
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Solo procesar respuestas de la API
        if '/api/' in request.path:
            # Convertir respuestas de error a nuestro formato estándar
            if 400 <= response.status_code < 600:
                try:
                    # Asegurarnos de que la respuesta esté renderizada
                    if hasattr(response, 'render'):
                        response.render()
                    
                    # Si ya es JSON, convertirlo a dict
                    if hasattr(response, 'data'):
                        data = response.data
                    else:
                        data = json.loads(response.content.decode('utf-8'))

                    # Formatear el mensaje de error
                    error_message = self.format_error_message(data)
                    
                    # Crear una nueva respuesta HTTP
                    return HttpResponse(
                        json.dumps({'detail': error_message}),
                        content_type='application/json',
                        status=response.status_code
                    )
                except (json.JSONDecodeError, AttributeError) as e:
                    # Si no es JSON, usar el contenido como está
                    return HttpResponse(
                        json.dumps({'detail': str(response.content, 'utf-8')}),
                        content_type='application/json',
                        status=response.status_code
                    )

        return response

    def format_error_message(self, data):
        """
        Formatea los mensajes de error según el tipo de error
        """
        # Diccionario de traducciones de campos
        field_translations = {
            'username': 'nombre de usuario',
            'email': 'correo electrónico',
            'password': 'contraseña',
            'first_name': 'nombre',
            'last_name': 'apellido',
            # Agrega más campos según necesites
        }

        # Mensajes de error comunes
        error_messages = {
            'required': 'El campo {} es obligatorio',
            'blank': 'El campo {} no puede estar vacío',
            'invalid': 'El valor proporcionado para {} no es válido',
            'unique': 'Este {} ya está registrado',
            'max_length': 'El {} no puede tener más de {} caracteres',
            'min_length': 'El {} debe tener al menos {} caracteres',
            'invalid_choice': 'El valor seleccionado para {} no es válido',
        }

        # Traducciones específicas de mensajes de error
        specific_error_translations = {
            'No active account found with the given credentials': 'Correo electrónico o contraseña incorrectos'
        }

        # Si ya está en el formato que queremos, verificar si hay una traducción específica
        if isinstance(data, dict) and 'detail' in data:
            error_message = data['detail']
            return specific_error_translations.get(error_message, error_message)

        # Si es un diccionario de errores de validación
        if isinstance(data, dict):
            for field, errors in data.items():
                # Traducir el nombre del campo
                field_name = field_translations.get(field, field)
                
                # Obtener el primer error
                if isinstance(errors, list):
                    error = errors[0]
                else:
                    error = errors

                # Buscar si coincide con algún mensaje predefinido
                for error_key, message_template in error_messages.items():
                    if error_key in str(error).lower():
                        return message_template.format(field_name)

                # Si no coincide con ningún mensaje predefinido
                return f"Error en {field_name}: {error}"

        # Si es una lista de errores
        if isinstance(data, list):
            return data[0]

        # Si es un string
        return str(data)

    def process_exception(self, request, exception):
        """
        Maneja excepciones no capturadas
        """
        if isinstance(exception, ValidationError):
            return Response(
                {'detail': self.format_error_message(exception.detail)},
                status=400
            )
        
        # Para otras excepciones, devolver un error 500
        return Response(
            {'detail': 'Ha ocurrido un error en el servidor'},
            status=500
        )