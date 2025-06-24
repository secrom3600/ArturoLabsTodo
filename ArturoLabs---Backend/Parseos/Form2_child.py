from datetime import date

class Nino:
    def __init__(self, id_nino: int, nombres: str, apellidos: str, etnia_raza: str,
                 sexo: str, fecha_nacimiento: date, nacionalidad: str, domicilio: str,
                 telefono: int, servicio_salud: str, emergencia_movil: str):
        self._id_nino = id_nino
        self._nombres = nombres or "#N/A"
        self._apellidos = apellidos or "#N/A"
        self._etnia_raza = etnia_raza or "#N/A"
        self._sexo = sexo or "#N/A"
        self._fecha_nacimiento = fecha_nacimiento
        self._nacionalidad = nacionalidad or "#N/A"
        self._domicilio = domicilio or "#N/A"
        self._telefono = telefono
        self._servicio_salud = servicio_salud or "#N/A"
        self._emergencia_movil = emergencia_movil or "#N/A"

    # Getters
    def get_id_nino(self):
        return self._id_nino

    def get_nombres(self):
        return self._nombres

    def get_apellidos(self):
        return self._apellidos

    def get_etnia_raza(self):
        return self._etnia_raza

    def get_sexo(self):
        return self._sexo

    def get_fecha_nacimiento(self):
        return self._fecha_nacimiento

    def get_nacionalidad(self):
        return self._nacionalidad

    def get_domicilio(self):
        return self._domicilio

    def get_telefono(self):
        return self._telefono

    def get_servicio_salud(self):
        return self._servicio_salud

    def get_emergencia_movil(self):
        return self._emergencia_movil

    # Setters
    def set_id_nino(self, id_nino: int):
        self._id_nino = id_nino

    def set_nombres(self, nombres: str):
        self._nombres = nombres

    def set_apellidos(self, apellidos: str):
        self._apellidos = apellidos

    def set_etnia_raza(self, etnia_raza: str):
        self._etnia_raza = etnia_raza

    def set_sexo(self, sexo: str):
        self._sexo = sexo

    def set_fecha_nacimiento(self, fecha_nacimiento: date):
        self._fecha_nacimiento = fecha_nacimiento

    def set_nacionalidad(self, nacionalidad: str):
        self._nacionalidad = nacionalidad

    def set_domicilio(self, domicilio: str):
        self._domicilio = domicilio

    def set_telefono(self, telefono: int):
        self._telefono = telefono

    def set_servicio_salud(self, servicio_salud: str):
        self._servicio_salud = servicio_salud

    def set_emergencia_movil(self, emergencia_movil: str):
        self._emergencia_movil = emergencia_movil

    def to_dict(self):
        return {
            "id_nino": self._id_nino,
            "nombres": self._nombres,
            "apellidos": self._apellidos,
            "etnia_raza": self._etnia_raza,
            "sexo": self._sexo,
            "fecha_nacimiento": self._fecha_nacimiento.isoformat() if isinstance(self._fecha_nacimiento, date) else self._fecha_nacimiento,
            "nacionalidad": self._nacionalidad,
            "domicilio": self._domicilio,
            "telefono": self._telefono,
            "servicio_salud": self._servicio_salud,
            "emergencia_movil": self._emergencia_movil
        }