
from django.urls import path
from .views import NinoListCreateAPIView, obtener_nino_por_ci
from .views import TutorPostListCreateAPIView, obtener_tutor_por_ci
from .views import AutenticacionAPIView, obtener_autenticacion_por_ci
from .views import TutorPostListCreateAPIView, verificar_codigo_2fa
from .views import login_tutor
from .views import ControlByCIView
from .views import CustomLoginWithJWTView
from .views import hijos_del_tutor
from .views import datos_tutor
from .views import datos_tutor_all
from .views import hijos_datos_perfil

urlpatterns = [
    path('nino/', NinoListCreateAPIView.as_view(), name='nino-list-create'),
    path('nino/<int:ci>/', obtener_nino_por_ci, name='nino-get-by-ci'),

    path('tutor/', TutorPostListCreateAPIView.as_view(), name='tutor-list-create'),
    path('tutor/<int:ci>', obtener_tutor_por_ci, name='tutor-get-by-ci'),

    path('autenticacion/', AutenticacionAPIView.as_view(), name='autenticacion-list-create'),
    path('autenticacion/<int:ci>/', obtener_autenticacion_por_ci, name='autenticacion-get-by-ci'),

    path('tutor/', TutorPostListCreateAPIView.as_view(), name='tutor'),
    path('tutor/verify/', verificar_codigo_2fa, name='verificar_codigo_2fa'),

    path('login/', login_tutor, name='login_tutor'),
    
    path('control/<int:ci>/', ControlByCIView.as_view(), name='control_by_ci'),

    path("token/", CustomLoginWithJWTView.as_view(), name="custom_token"),
    
    path('hijos/', hijos_del_tutor, name='hijos_del_tutor'),

    path('tutorDatos/', datos_tutor),

    path('tutorDatosAll/', datos_tutor_all),

    path('hijosTutor/', hijos_datos_perfil)
]
