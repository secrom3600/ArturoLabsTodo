from rest_framework import status
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Tutor
from .serializers import TutorPostSerializer
from .models import Autenticacion 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



class NiñoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Niño.objects.all()
    serializer_class = NiñoSerializer

@api_view(['GET'])
def obtener_nino_por_ci(request, ci):
    nino = get_object_or_404(Niño, ci=ci)
    serializer = NiñoSerializer(nino)
    return Response(serializer.data)


class TutorPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorPostSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Datos recibidos:", request.data)
            response = super().create(request, *args, **kwargs)

            email = request.data.get('email', '').lower()
            tutor = Tutor.objects.filter(email=email).first()


            # Generar el código 2FA
            codigo_2fa = get_random_string(length=6, allowed_chars='0123456789')
            tutor.codigo_2fa = codigo_2fa
            tutor.verificado = False
            tutor.save()

            # Enviar correo con el código de verificación
            send_mail(
                'Verificación de tu cuenta - Código 2FA',
                f'Tu código de verificación es: {codigo_2fa}',
                'no-reply@tu-proyecto.com',
                [tutor.email],
                fail_silently=False,
            )
            print("Correo de verificación enviado.")
            return response

        except Exception as e:
            print("Error al registrar el tutor:", str(e))
            return Response({"message": "Error al registrar al tutor", "error": str(e)}, status=500)
        
@api_view(['POST'])
def verificar_codigo_2fa(request):
    email = request.data.get('email')
    codigo = request.data.get('codigo')

    try:
        tutor = Tutor.objects.get(email=email)  
    except Tutor.DoesNotExist:
        return Response({'message': 'Tutor no encontrado'}, status=404)
    except Tutor.MultipleObjectsReturned:
        return Response({'message': 'Hay más de un tutor con ese email'}, status=400)

    if tutor.codigo_2fa == codigo:
        tutor.verificado = True
        tutor.save()
        return Response({'message': 'Cuenta verificada correctamente.'})
    else:
        return Response({'message': 'Código incorrecto'}, status=400)



@api_view(['GET'])
def obtener_tutor_por_ci(request, ci):
    tutor = get_object_or_404(Tutor, CI=ci)
    serializer = TutorPostSerializer(tutor)
    return Response(serializer.data)


class AutenticacionAPIView(generics.ListCreateAPIView):
    queryset = Autenticacion.objects.all()
    serializer_class = AutenticacionSerializer

@api_view(['GET'])
def obtener_autenticacion_por_ci(request, ci):
    autenticacion = get_object_or_404(Autenticacion, tutorci=ci)
    serializer = AutenticacionSerializer(autenticacion)
    return Response(serializer.data)


@csrf_exempt
@require_POST
def login_tutor(request):
    try:
        data = json.loads(request.body)
        ci = data.get('ci')
        password = data.get('password')

        if not ci or not password:
            return JsonResponse({'error': 'Cédula y contraseña requeridas'}, status=400)

        auth = Autenticacion.objects.filter(tutorci=ci, password=password).first()

        if auth:
            return JsonResponse({'success': True, 'message': 'Inicio de sesión exitoso'})
        else:
            return JsonResponse({'success': False, 'message': 'Cédula o contraseña incorrecta'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
