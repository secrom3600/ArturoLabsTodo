# ✅ views.py adaptado para tu caso: solo parsear XML y devolver JSON

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Parseo import (
    parse_nino,
    parse_embarazo,
    parse_control_salud,
    parse_vacunas
)
import os
import glob

class ParsearDesdeCI(APIView):
    def get(self, request):
        ci = request.query_params.get("ci")
        tipo_solicitado = request.query_params.get("tipo") # puede ser: nino, embarazo, vacunas, control
        if not ci:
            return Response({"error": "CI requerida"}, status=400)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(BASE_DIR, "tests")

        funciones = {
            "nino": parse_nino,
            "embarazo": parse_embarazo,
            "control": parse_control_salud,
            "vacunas": parse_vacunas,
        }

        if tipo_solicitado and tipo_solicitado not in funciones:
            return Response({"error": f"Tipo inválido: {tipo_solicitado}"}, status=400)

        tipos_a_procesar = [tipo_solicitado] if tipo_solicitado else funciones.keys()

        resultados = {}

        for tipo in tipos_a_procesar:
            parser_func = funciones[tipo]
            patron = os.path.join(base_path, f"{tipo}_{ci}_*.xml")
            archivos = glob.glob(patron)
            resultados[tipo] = []

            if not archivos:
                resultados[tipo].append(f"No se encontraron archivos para {tipo}_{ci}_*.xml")
                continue

            for archivo in archivos:
                try:
                    obj = parser_func(archivo)
                    resultados[tipo].append(obj.to_dict())
                except Exception as e:
                    resultados[tipo].append({
                        "archivo": os.path.basename(archivo),
                        "error": str(e)
                    })

        return Response(resultados, status=200)
