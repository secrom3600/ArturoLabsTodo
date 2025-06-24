from rest_framework import status
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Tutor
from .serializers import TutorPostSerializer
from .models import Autenticacion 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
import json
import matplotlib.pyplot as plt
import io
import base64
import numpy as np


class NinoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Nino.objects.all()
    serializer_class = NinoSerializer

@api_view(['GET'])
def obtener_nino_por_ci(request, ci):
    nino = get_object_or_404(Nino, ci=ci)
    serializer = NinoSerializer(nino)
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


class ControlByCIView(APIView):
    def get(self, request, ci, format=None):
        try:
            controls = Control.objects.filter(ci=ci).order_by('fecha')
            if not controls.exists():
                return Response({"message": "No data found for the given CI."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ControlSerializer(controls, many=True)

            edades = []
            imc_values = []

            for control in controls:
                try:
                    edad_anios = float(control.edad) / 12
                except (ValueError, TypeError):
                    edad_anios = None
                try:
                    peso = float(control.peso) if control.peso is not None else 0.0
                    talla_cm = float(control.talla) if control.talla is not None else 0.0
                    talla_m = talla_cm / 100
                    imc = round(peso / (talla_m ** 2), 2) if talla_m else None
                except (ValueError, TypeError, ZeroDivisionError):
                    imc = None

                if edad_anios is not None and imc is not None:
                    edades.append(edad_anios)
                    imc_values.append(imc)

            if not edades or not imc_values:
                return Response({"message": "No valid data for plotting IMC/Edad."}, status=status.HTTP_200_OK)

            # Curvas de referencia (definir siempre antes de graficar)
            edades_meses = np.arange(60, 181, 3)
            edad_ref = edades_meses / 12  # Convertido a años
            edad_ref = edad_ref[:40]

            P3 = np.array([13, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14, 14.2, 14.4, 14.6, 14.8, 15, 15.2, 15.4, 15.6, 15.8, 16,
                           16.2, 16.4, 16.6, 16.8, 17, 17.2, 17.4, 17.6, 17.8, 18, 18.2, 18.4, 18.6, 18.8, 19, 19.2, 19.4, 19.6, 19.8])
            P15 = np.array([14, 14.1, 14.3, 14.4, 14.6, 14.8, 15, 15.2, 15.4, 15.6, 15.8, 16, 16.2, 16.4, 16.6, 16.8, 17, 17.2, 17.4, 17.6, 17.8,
                            18, 18.2, 18.4, 18.6, 18.8, 19, 19.2, 19.4, 19.6, 19.8, 20, 20.2, 20.4, 20.6, 20.8, 21, 21.2, 21.4, 21.6])
            P50 = np.array([15, 15.2, 15.4, 15.6, 15.8, 16, 16.2, 16.4, 16.6, 16.8, 17, 17.2, 17.4, 17.6, 17.8, 18, 18.2, 18.4, 18.6, 18.8, 19,
                            19.2, 19.4, 19.6, 19.8, 20, 20.2, 20.4, 20.6, 20.8, 21, 21.2, 21.4, 21.6, 21.8, 22, 22.2, 22.4, 22.6, 22.8])
            P85 = np.array([16.5, 16.7, 16.9, 17.1, 17.3, 17.5, 17.7, 17.9, 18.1, 18.3, 18.5, 18.7, 18.9, 19.1, 19.3, 19.5, 19.7, 19.9, 20.1, 20.3, 20.5,
                            20.7, 20.9, 21.1, 21.3, 21.5, 21.7, 21.9, 22.1, 22.3, 22.5, 22.7, 22.9, 23.1, 23.3, 23.5, 23.7, 23.9, 24.1, 24.3])
            P97 = np.array([18, 18.3, 18.6, 18.9, 19.2, 19.5, 19.8, 20.1, 20.4, 20.7, 21, 21.3, 21.6, 21.9, 22.2, 22.5, 22.8, 23.1, 23.4, 23.7, 24,
                            24.3, 24.6, 24.9, 25.2, 25.5, 25.8, 26.1, 26.4, 26.7, 27, 27.3, 27.6, 27.9, 28.2, 28.5, 28.8, 29.1, 29.4, 29.7])

            # Graficar curvas de referencia
            plt.figure(figsize=(10, 6))
            plt.plot(edad_ref, P3, 'r', label='P3')
            plt.plot(edad_ref, P15, 'orange', label='P15')
            plt.plot(edad_ref, P50, 'g', label='P50')
            plt.plot(edad_ref, P85, 'orange', label='P85')
            plt.plot(edad_ref, P97, 'r', label='P97')

            # Graficar los puntos reales del paciente
            plt.plot(edades, imc_values, 'bo-', label='Paciente')

            plt.xlabel('Edad (años)')
            plt.ylabel('IMC (kg/m²)')
            plt.title(f'Curva de IMC - Paciente CI: {ci}')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='jpg')
            buffer.seek(0)
            plt.close()

            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return Response({
                "data": serializer.data,
                "imc_edad_graph": f"data:image/jpeg;base64,{image_base64}"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("ERROR EN LA VIEW:", e)
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hijos_del_tutor(request):
    tutor_ci = request.user.tutorci

    hijos = Nino.objects.filter(Q(tutorci=tutor_ci) | Q(tutordosci=tutor_ci))
    data = [{
        "full_name": f"{h.nombre} {h.apellido}",
        "ci": h.ci,
        "edad": h.edad,
    } for h in hijos]

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def datos_tutor(request):
    tutor_ci = request.user.tutorci  # CI del usuario autenticado

    # Buscar al tutor con ese CI
    tutor = get_object_or_404(Tutor, CI=tutor_ci)

    data = {
        "full_name": f"{tutor.Nombre} {tutor.Apellido}",
        "ci": tutor.CI
    }

    return Response(data)
    

class CustomLoginWithJWTView(APIView):
    def post(self, request):
        ci = request.data.get("ci")
        password = request.data.get("password")

        try:
            user = Autenticacion.objects.get(tutorci=ci)

            if user.password != password:
                return Response({"message": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

            # Crear tokens usando for_user
            refresh = RefreshToken.for_user(user)
            refresh["ci"] = user.tutorci  # extra info opcional

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login exitoso"
            })

        except Autenticacion.DoesNotExist:
            return Response({"message": "CI no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def datos_tutor_all(request):
    tutor_ci = request.user.tutorci
    tutor = get_object_or_404(Tutor, CI=tutor_ci)

    data = {
        "nombre": tutor.Nombre,
        "apellido": tutor.Apellido,
        "ci": tutor.CI,
        "nacionalidad": tutor.nacionalidad,
        "fec_nac": tutor.Fec_Nac.isoformat(),  # YYYY-MM-DD
        "sexo": tutor.sexo,
        "direccion": f"{tutor.Calle} {tutor.puerta}",
        "localidad": tutor.localidad,
        "email": tutor.email,
        "telefono": tutor.Telefono
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hijos_datos_perfil(request):
    tutor_ci = request.user.tutorci

    hijos = Nino.objects.filter(Q(tutorci=tutor_ci) | Q(tutordosci=tutor_ci))

    data = [{
        "nombre": h.nombre,
        "apellido": h.apellido,
        "ci": h.ci,
        "fecha_nac": h.fec_nac.strftime("%d/%m/%Y") if h.fec_nac else None,
    } for h in hijos]

    return Response(data)

