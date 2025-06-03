
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
import xml.etree.ElementTree as ET
import os
from django.conf import settings
from datetime import datetime


#%%
'''
def generate_consultas_vacunas_xml(request):
    return generate_generic_xml(request, "Consultasvacunas")

def generate_form_consulta_xml(request):
    return generate_generic_xml(request, "Formconsulta")

def generate_form_datos_xml(request):
    return generate_generic_xml(request, "Formdatos")

def generate_form_datos_nino_xml(request):
    return generate_generic_xml(request, "Formdatosnino")

def generate_form_madre_xml(request):
    return generate_generic_xml(request, "Formmadre")

def generate_form_nino_xml(request):
    return generate_generic_xml(request, "Formnino")

def generate_form_tutor_xml(request):
    return generate_generic_xml(request, "Formtutor")

def generate_portal_tutor_xml(request):
    return generate_generic_xml(request, "Portaltutor")

def generate_verificar_2fa_xml(request):
    return generate_generic_xml(request, "Verificar2fa")


def generate_generic_xml(request, root_tag):
    if request.method not in ['POST', 'GET']:
        return JsonResponse({"error": "Solo GET o POST permitido"}, status=405)

    data = request.POST if request.method == 'POST' else request.GET
    root = ET.Element(root_tag)

    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = value

    xml_data = ET.tostring(root, encoding='utf-8', method='xml')

    output_dir = os.path.join(settings.BASE_DIR, "generated_xml")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{root_tag.lower()}_" + data.get('ci', 'unknown') + f"_{timestamp}.xml"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(xml_data)

    return JsonResponse({"message": "XML guardado", "file": file_name})


def parse_xml(request):
    if request.method != 'POST':
        return HttpResponse("Solo POST permitido", status=405)

    try:
        root = ET.fromstring(request.body)

        def to_dict(elem):
            return {child.tag: to_dict(child) if list(child) else child.text for child in elem}

        data = {root.tag: to_dict(root)}
        return JsonResponse(data)

    except ET.ParseError as e:
        return HttpResponse(f"Invalid XML: {str(e)}", status=400)
'''
#%%
class GenerateXMLView(APIView):
    def post(self, request, root_tag):
        return self.generate_xml(request, root_tag)

    def get(self, request, root_tag):
        return self.generate_xml(request, root_tag)

    def generate_xml(self, request, root_tag):
        data = request.data if request.method == 'POST' else request.query_params
        root = ET.Element(root_tag)

        for key, value in data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)

        xml_data = ET.tostring(root, encoding='utf-8', method='xml')

        output_dir = os.path.join(settings.BASE_DIR, "generated_xml")
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{root_tag.lower()}_" + data.get('ci', 'unknown') + f"_{timestamp}.xml"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(xml_data)

        return Response({"message": "XML guardado", "file": file_name})


class borradorParseXMLView(APIView):
    def post(self, request):
        try:
            root = ET.fromstring(request.body)

            def to_dict(elem):
                return {child.tag: to_dict(child) if list(child) else child.text for child in elem}

            data = {root.tag: to_dict(root)}
            return Response(data)

        except ET.ParseError as e:
            return Response({"error": f"Invalid XML: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class LeerDatosMadre(APIView):
    def post(self, request):
        print("Datos recibidos:", request.data)
        ci = request.data.get('ci')
        if not ci:
            return Response({"error": "No se proporcionó la cédula"}, status=status.HTTP_400_BAD_REQUEST)

        carpeta_tests = os.path.join(os.path.dirname(__file__), 'tests')
        archivo_xml = None

        for nombre_archivo in os.listdir(carpeta_tests):
            if ci in nombre_archivo and nombre_archivo.endswith('.xml'):
                archivo_xml = os.path.join(carpeta_tests, nombre_archivo)
                break

        if not archivo_xml:
            return Response({"error": "Archivo XML no encontrado para esa cédula"}, status=status.HTTP_404_NOT_FOUND)

        try:
            tree = ET.parse(archivo_xml)
            root = tree.getroot()
            ns = {'hl7': 'urn:hl7-org:v3'}

            def buscar_valor(xpath):
                elem = root.find(xpath, ns)
                if elem is not None:
                    return elem.attrib.get('displayName') or elem.attrib.get('value') or elem.text
                return None

            data = {
                "nro_controles_prenatales": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Número de controles prenatales"]]/hl7:value'),
                "ets_resultado": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Resultado enfermedades de transmisión sexual"]]/hl7:value'),
                "ets_tratamiento": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Tratamiento enfermedades de transmisión sexual"]]/hl7:value'),
                "tipo_parto": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Tipo de parto"]]/hl7:value'),
                "tipo_parte": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Tipo de parte"]]/hl7:value'),
                "acomp_nombre": buscar_valor('.//hl7:participant[hl7:functionCode[@displayName="Acompañante"]]/hl7:associatedEntity/hl7:associatedPerson/hl7:name/hl7:given'),
                "acomp_apellido": buscar_valor('.//hl7:participant[hl7:functionCode[@displayName="Acompañante"]]/hl7:associatedEntity/hl7:associatedPerson/hl7:name/hl7:family'),
                "edad_gestacional": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Edad gestacional"]]/hl7:value'),
                "peso_al_nacer": buscar_valor('.//hl7:section//hl7:observation[hl7:code[@displayName="Peso al nacer"]]/hl7:value'),
            }

            return Response(data)

        except ET.ParseError as e:
            return Response({"error": f"XML inválido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        