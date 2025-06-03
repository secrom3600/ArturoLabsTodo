from datetime import date, timedelta
from django.db import models

 
class Niño(models.Model):
    ci = models.IntegerField(primary_key=True, db_column='ci')
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    fec_nac = models.DateField(db_column='fec_nac')
    sexo = models.CharField(max_length=1, db_column='sexo')
    nacionalidad = models.CharField(max_length=100, db_column='nacionalidad')
    tutorci = models.IntegerField(db_column='tutorci')  
    tutordosci = models.IntegerField(db_column='tutordosci', null=True, blank=True)  

    class Meta:
        db_table = 'niño'



class Tutor(models.Model):
    CI = models.IntegerField(primary_key=True, db_column='ci')
    sexo = models.CharField(max_length=1, db_column='sexo')
    Nombre = models.CharField(max_length=100, db_column='nombre')
    Apellido = models.CharField(max_length=100, db_column='apellido')
    email = models.EmailField(max_length=100, db_column='email')  
    Telefono = models.CharField(max_length=20, db_column='telefono')
    localidad = models.CharField(max_length=100, db_column='localidad')
    Calle = models.CharField(max_length=100, db_column='calle')
    puerta = models.CharField(max_length=10, db_column='num_puer')
    Fec_Nac = models.DateField(db_column='fec_nac')
    nacionalidad = models.CharField(max_length=100, db_column='nacionalidad')
    codigo_2fa = models.CharField(max_length=6, blank=True, null=True)
    verificado = models.BooleanField(default=False)


    class Meta:
        db_table = 'tutor' 


class Autenticacion(models.Model):
    tutorci = models.IntegerField(primary_key=True, db_column='tutor_ci')
    password = models.CharField(max_length=100, db_column='contrasenia')
    

    class Meta:
        db_table = 'autenticacion' 








    
    


    
