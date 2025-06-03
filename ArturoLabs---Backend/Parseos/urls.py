from django.urls import path
from .views import GenerateXMLView, LeerDatosMadre

urlpatterns = [
    path('api/generate/<str:root_tag>/', GenerateXMLView.as_view(), name='generate-xml'),
    path('api/leer/form-madre/', LeerDatosMadre.as_view(), name='leer_datos_madre'),

    
]