import xml.etree.ElementTree as ET
import json
from datetime import datetime
from .Form1_CS import ControlDeSalud
from .Form1_Vac import Vacunas
from .Form2_child import Nino
from .Form4_embarazo import Embarazo

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return "Este dato no existe en el documento"

def get_text_or_default(element, path):
    try:
        found = element.find(path)
        return found.text if found is not None else "Este dato no existe en el documento"
    except:
        return "Este dato no existe en el documento"

def parse_nino(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    id_nino = get_text_or_default(root, ".//id")
    nombres = get_text_or_default(root, ".//nombres")
    apellidos = get_text_or_default(root, ".//apellidos")
    etnia = get_text_or_default(root, ".//etnia")
    sexo = get_text_or_default(root, ".//sexo")
    fecha_nac = parse_date(get_text_or_default(root, ".//fechaNacimiento"))
    nacionalidad = get_text_or_default(root, ".//nacionalidad")
    domicilio = get_text_or_default(root, ".//domicilio")
    telefono = get_text_or_default(root, ".//telefono")
    servicio_salud = get_text_or_default(root, ".//servicioSalud")
    emergencia = get_text_or_default(root, ".//emergenciaMovil")

    return Nino(
        int(id_nino) if id_nino.isdigit() else -1,
        nombres, apellidos, etnia, sexo, fecha_nac,
        nacionalidad, domicilio, int(telefono) if telefono.isdigit() else -1,
        servicio_salud, emergencia
    )

def parse_embarazo(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def b(path): return get_text_or_default(root, path) == "true"
    def i(path):
        val = get_text_or_default(root, path)
        return int(val) if val.isdigit() else -1
    def f(path):
        val = get_text_or_default(root, path)
        try: return float(val)
        except: return -1.0

    return Embarazo(
        id_nino=i(".//idNino"),
        embarazo_multiple=b(".//embarazoMultiple"),
        num_controles_prenatales=i(".//controlesPrenatales"),
        its=b(".//its"),
        resultado=get_text_or_default(root, ".//resultado"),
        tratamiento=get_text_or_default(root, ".//tratamiento"),
        tp_vaginal=b(".//tpVaginal"),
        tp_cesarea=b(".//tpCesarea"),
        tp_institucional=b(".//tpInstitucional"),
        otro_tipo_parto=get_text_or_default(root, ".//otroTipoParto"),
        acompanamiento_parto=b(".//acompanamiento"),
        nombre_acompanante=get_text_or_default(root, ".//nombreAcompanante"),
        apellido_acompanante=get_text_or_default(root, ".//apellidoAcompanante"),
        edad_gestacional_semanas=i(".//edadGestacional"),
        peso_al_nacer_gramos=f(".//pesoNacimiento")
    )

def parse_control_salud(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def get_float(path):
        val = get_text_or_default(root, path)
        try: return float(val)
        except: return -1.0

    def get_int(path):
        val = get_text_or_default(root, path)
        return int(val) if val.isdigit() else -1

    def get_bool(path):
        return get_text_or_default(root, path) == "true"

    return ControlDeSalud(
        id_nino=get_int(".//idNino"),
        fecha=parse_date(get_text_or_default(root, ".//fecha")),
        edad=get_int(".//edad"),
        peso=get_float(".//peso"),
        talla_cm=get_float(".//talla"),
        pc_cm=get_float(".//pc"),
        alimentacion_pd=get_bool(".//alimentacionPD"),
        alimentacion_ppl=get_bool(".//alimentacionPPL"),
        hierro_vit_d=get_bool(".//hierroVitD"),
        fecha_prox_consulta=parse_date(get_text_or_default(root, ".//fechaProximaConsulta")),
        circ_cintura_cm=get_float(".//circunferenciaCintura"),
        imc=get_float(".//imc"),
        pas=get_float(".//pas"),
        pad=get_float(".//pad")
    )

def parse_vacunas(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def get_bool(path):
        return get_text_or_default(root, path) == "true"

    def get_int(path):
        val = get_text_or_default(root, path)
        return int(val) if val.isdigit() else -1

    return Vacunas(
        id_nino=get_int(".//idNino"),
        bcg=get_bool(".//BCG"),
        pentavalente=get_bool(".//Pentavalente"),
        polio=get_bool(".//Polio"),
        sarampion_rubeola_paperas=get_bool(".//SarampionRubeolaPaperas"),
        varicela=get_bool(".//Varicela"),
        neumococo_13_v=get_bool(".//Neumococo13V"),
        hepatitis_a=get_bool(".//HepatitisA"),
        triple_bacteriana_dpt=get_bool(".//TripleBacterianaDPT"),
        triple_bacteriana_acelular_dpat=get_bool(".//TripleBacterianaDPAT"),
        vph=get_bool(".//VPH"),
        anti_influenza=get_bool(".//AntiInfluenza"),
        edad_meses=get_int(".//EdadMeses"),
        edad_anios=get_int(".//EdadAnios")
    )

# Ejemplo de uso con exportación a JSON
def exportar_a_json():
    nino = parse_nino("C:/Users/mnsen/OneDrive - Universidad de Montevideo/Tercer Año/Ingeniería de Software 2/Fin_semestre/nino.xml")
    embarazo = parse_embarazo("C:/Users/mnsen/OneDrive - Universidad de Montevideo/Tercer Año/Ingeniería de Software 2/Fin_semestre/embarazo.xml")
    control = parse_control_salud("C:/Users/mnsen/OneDrive - Universidad de Montevideo/Tercer Año/Ingeniería de Software 2/Fin_semestre/control_salud.xml")
    vacunas = parse_vacunas("C:/Users/mnsen/OneDrive - Universidad de Montevideo/Tercer Año/Ingeniería de Software 2/Fin_semestre/vacunas.xml")

    data = {
        "nino": nino.to_dict(),
        "embarazo": embarazo.to_dict(),
        "control_de_salud": control.to_dict(),
        "vacunas": vacunas.to_dict()
    }

    with open("salida.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("✅ Archivo JSON exportado correctamente.")

# Llamar si se ejecuta directamente
if __name__ == "__main__":
    exportar_a_json()

