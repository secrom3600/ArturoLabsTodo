from datetime import date

class ControlDeSalud:
    def __init__(self, id_nino: int, fecha: date, edad: int, peso: float, talla_cm: float, pc_cm: float,
                 alimentacion_pd: bool, alimentacion_ppl: bool, hierro_vit_d: bool,
                 fecha_prox_consulta: date, circ_cintura_cm: float, imc: float, pas: float, pad: float):

        self._id_nino = id_nino
        self._fecha = fecha
        self._edad = edad
        self._peso = peso or 0.0
        self._talla_cm = talla_cm or 0.0
        self._pc_cm = pc_cm
        self._alimentacion_pd = alimentacion_pd
        self._alimentacion_ppl = alimentacion_ppl
        self._hierro_vit_d = hierro_vit_d
        self._fecha_prox_consulta = fecha_prox_consulta
        self._circ_cintura_cm = circ_cintura_cm
        self._imc = imc
        self._pas = pas
        self._pad = pad

    def to_dict(self):
        return {
            "id_nino": self._id_nino,
            "fecha": self._fecha.isoformat() if isinstance(self._fecha, date) else self._fecha,
            "edad": self._edad,
            "peso": self._peso,
            "talla": self._talla_cm,
            "pc": self._pc_cm,
            "alimentacion_pd": self._alimentacion_pd,
            "alimentacion_ppl": self._alimentacion_ppl,
            "hierro_vit_d": self._hierro_vit_d,
            "fecha_proxima_consulta": self._fecha_prox_consulta.isoformat() if isinstance(self._fecha_prox_consulta, date) else self._fecha_prox_consulta,
            "circunferencia_cintura": self._circ_cintura_cm,
            "imc": self._imc,
            "pas": self._pas,
            "pad": self._pad
        }