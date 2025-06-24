from datetime import date

class Embarazo:
    def __init__(self, id_nino: int, embarazo_multiple: bool, num_controles_prenatales: int,
                 its: bool, resultado: str, tratamiento: str, tp_vaginal: bool,
                 tp_cesarea: bool, tp_institucional: bool, otro_tipo_parto: str,
                 acompanamiento_parto: bool, nombre_acompanante: str, apellido_acompanante: str,
                 edad_gestacional_semanas: int, peso_al_nacer_gramos: float):
        self._id_nino = id_nino
        self._embarazo_multiple = embarazo_multiple
        self._num_controles_prenatales = num_controles_prenatales
        self._its = its
        self._resultado = resultado or "#N/A"
        self._tratamiento = tratamiento or "#N/A"
        self._tp_vaginal = tp_vaginal
        self._tp_cesarea = tp_cesarea
        self._tp_institucional = tp_institucional
        self._otro_tipo_parto = otro_tipo_parto or "#N/A"
        self._acompanamiento_parto = acompanamiento_parto
        self._nombre_acompanante = nombre_acompanante or "#N/A"
        self._apellido_acompanante = apellido_acompanante or "#N/A"
        self._edad_gestacional_semanas = edad_gestacional_semanas
        self._peso_al_nacer_gramos = peso_al_nacer_gramos

    def to_dict(self):
        return {
            "id_nino": self._id_nino,
            "embarazo_multiple": self._embarazo_multiple,
            "num_controles_prenatales": self._num_controles_prenatales,
            "its": self._its,
            "resultado": self._resultado,
            "tratamiento": self._tratamiento,
            "tp_vaginal": self._tp_vaginal,
            "tp_cesarea": self._tp_cesarea,
            "tp_institucional": self._tp_institucional,
            "otro_tipo_parto": self._otro_tipo_parto,
            "acompanamiento_parto": self._acompanamiento_parto,
            "nombre_acompanante": self._nombre_acompanante,
            "apellido_acompanante": self._apellido_acompanante,
            "edad_gestacional_semanas": self._edad_gestacional_semanas,
            "peso_al_nacer_gramos": self._peso_al_nacer_gramos
        }