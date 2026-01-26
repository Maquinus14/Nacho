from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import ErrorReport
from .serializer import StatusSerializer, ErrorSerializer

# --- Paso 2: Estado del servidor ---
@api_view(['GET'])
def get_server_status(request):
    return Response(StatusSerializer({
        'status': 'running', 
        'date': datetime.now()
    }).data)

# --- Paso 5: Errores ---
@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all()
    return Response(ErrorSerializer(errors, many=True).data)

@api_view(['GET'])
def get_error_from_code(request, code):
    e = ErrorReport.objects.get(code=code)
    return Response(ErrorSerializer(e).data)

# --- Paso 7: Crear y Actualizar ---

@api_view(['POST'])
def create_error(request):
    serialized_error = ErrorSerializer(data=request.data)
    if serialized_error.is_valid():
        serialized_error.save()
        return Response(serialized_error.data, status=status.HTTP_201_CREATED)
    return Response(serialized_error.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def object_update(request, code):
    try:
        # Buscamos por 'code' ya que es lo que definimos en el modelo
        obj = ErrorReport.objects.get(code=code)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serialized_data = ErrorSerializer(obj, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)