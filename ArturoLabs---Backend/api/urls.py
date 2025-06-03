
from django.urls import path
from .views import NiñoListCreateAPIView, obtener_nino_por_ci
from .views import TutorPostListCreateAPIView, obtener_tutor_por_ci
from .views import AutenticacionAPIView, obtener_autenticacion_por_ci
from .views import TutorPostListCreateAPIView, verificar_codigo_2fa
from .views import login_tutor


urlpatterns = [
    path('nino/', NiñoListCreateAPIView.as_view(), name='nino-list-create'),
    path('nino/<int:ci>/', obtener_nino_por_ci, name='nino-get-by-ci'),

    path('tutor/', TutorPostListCreateAPIView.as_view(), name='tutor-list-create'),
    path('tutor/<int:ci>', obtener_tutor_por_ci, name='tutor-get-by-ci'),

    path('autenticacion/', AutenticacionAPIView.as_view(), name='autenticacion-list-create'),
    path('autenticacion/<int:ci>/', obtener_autenticacion_por_ci, name='autenticacion-get-by-ci'),

    path('tutor/', TutorPostListCreateAPIView.as_view(), name='tutor'),
    path('tutor/verify/', verificar_codigo_2fa, name='verificar_codigo_2fa'),

    path('login/', login_tutor, name='login_tutor'),

]
