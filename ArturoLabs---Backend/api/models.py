from datetime import date, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

 
class Nino(models.Model):
    ci = models.IntegerField(primary_key=True, db_column='ci')
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    fec_nac = models.DateField(db_column='fec_nac')
    sexo = models.CharField(max_length=1, db_column='sexo')
    nacionalidad = models.CharField(max_length=100, db_column='nacionalidad')
    tutorci = models.IntegerField(db_column='tutorci')  
    tutordosci = models.IntegerField(db_column='tutordosci', null=True, blank=True)  
    edad = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'nino'



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



class Control(models.Model):
    ci = models.IntegerField(db_column='ci',primary_key=True)
    fecha = models.DateField(db_column='fecha')
    edad = models.SmallIntegerField(db_column='edad')
    peso = models.DecimalField(max_digits=4, decimal_places=1, db_column='peso')
    talla = models.DecimalField(max_digits=4, decimal_places=1, db_column='talla')
    pc = models.BooleanField(default=False, db_column='pc')
    ppl = models.BooleanField(default=False, db_column='ppl')
    complemento = models.BooleanField(default=False, db_column='complemento')
    hierro = models.BooleanField(default=False, db_column='hierro')
    vitamina_d = models.BooleanField(default=False, db_column='vitamina_d')
    circunferencia_cintura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, db_column='cc')
    pas = models.SmallIntegerField(null=True, blank=True, db_column='pas')
    pad = models.SmallIntegerField(null=True, blank=True, db_column='pad')

    class Meta:
        db_table = 'control_medico'
        unique_together = (('ci', 'fecha'),)




class AutenticacionManager(BaseUserManager):
    def create_user(self, tutorci, password=None, **extra_fields):
        if not tutorci:
            raise ValueError("El campo tutorci es obligatorio")
        user = self.model(tutorci=tutorci, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tutorci, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(tutorci, password, **extra_fields)


class Autenticacion(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    tutorci = models.IntegerField(unique=True, db_column='tutor_ci')
    password = models.CharField(max_length=100, db_column='contrasenia')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AutenticacionManager()

    USERNAME_FIELD = 'tutorci'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'autenticacion'

    def __str__(self):
        return str(self.tutorci)
    


    
