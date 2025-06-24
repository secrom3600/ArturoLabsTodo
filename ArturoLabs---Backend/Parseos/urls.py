from django.urls import path
from .views import ParsearDesdeCI

urlpatterns = [
    path("nino/", ParsearDesdeCI.as_view()),

    
]