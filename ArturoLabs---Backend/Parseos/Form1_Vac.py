from datetime import date

class Vacunas:
    def __init__(self, id_nino: int, bcg: bool, pentavalente: bool, polio: bool, sarampion_rubeola_paperas: bool,
                 varicela: bool, neumococo_13_v: bool, hepatitis_a: bool, triple_bacteriana_dpt: bool,
                 triple_bacteriana_acelular_dpat: bool, vph: bool, anti_influenza: bool,
                 edad_meses: int, edad_anios: int):
        self._id_nino = id_nino
        self._bcg = bcg
        self._pentavalente = pentavalente
        self._polio = polio
        self._sarampion_rubeola_paperas = sarampion_rubeola_paperas
        self._varicela = varicela
        self._neumococo_13_v = neumococo_13_v
        self._hepatitis_a = hepatitis_a
        self._triple_bacteriana_dpt = triple_bacteriana_dpt
        self._triple_bacteriana_acelular_dpat = triple_bacteriana_acelular_dpat
        self._vph = vph
        self._anti_influenza = anti_influenza
        self._edad_meses = edad_meses
        self._edad_anios = edad_anios

    def to_dict(self):
        return {
            "id_nino": self._id_nino,
            "bcg": self._bcg,
            "pentavalente": self._pentavalente,
            "polio": self._polio,
            "srp": self._sarampion_rubeola_paperas,
            "varicela": self._varicela,
            "neumococo_13v": self._neumococo_13_v,
            "hepatitis_a": self._hepatitis_a,
            "triple_bacteriana_dpt": self._triple_bacteriana_dpt,
            "triple_bacteriana_dpat": self._triple_bacteriana_acelular_dpat,
            "vph": self._vph,
            "anti_influenza": self._anti_influenza,
            "edad_meses": self._edad_meses,
            "edad_anios": self._edad_anios
        }