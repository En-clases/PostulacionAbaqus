from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
import os
import random
from django.conf import settings
import matplotlib.pyplot as plt
import pandas as pd
import io
from django.http import JsonResponse
import json


from portafolios.models import Portafolio, Precio, Weight
from portafolios.utils import calcular_cantidad_inicial_activos_para_cada_portafolio, calcular_valor_y_peso_portafolios, calcular_cantidad_inicial_activos_en_compra_venta


def index(request):
    return render(request, 'index.html')


class ValoresView(APIView):
    def get(self, request):

        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Los parámetros 'fecha_inicio' y 'fecha_fin' son necesarios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultados = calcular_valor_y_peso_portafolios(fecha_inicio, fecha_fin, calcular_cantidad_inicial_activos_para_cada_portafolio())
        return Response(resultados, status=status.HTTP_200_OK)


def graficos_view(request):

    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)

    if fecha_inicio and fecha_fin:
        valores_api = ValoresView()
        request.query_params = {
            'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        response = valores_api.get(request)
    else:
        return HttpResponse("Ha ocurrido un error obteniendo los datos entre las fechas indicadas.")

    data = response.data
    for item in data["portafolio 1"]:
        item['fecha'] = item['fecha'].strftime('%Y-%m-%d')
    for item in data["portafolio 2"]:
        item['fecha'] = item['fecha'].strftime('%Y-%m-%d')

    return render(request, 'graficos.html', {
        'data_portafolio_1': json.dumps(data["portafolio 1"]), 
        'data_portafolio_2': json.dumps(data["portafolio 2"]),
        'data_line': json.dumps(data)
        })


def graficos_con_compra_venta_view(request):

    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)

    if not fecha_inicio or not fecha_fin:
        return HttpResponse("Ha ocurrido un error obteniendo los datos entre las fechas indicadas.")

    data = calcular_valor_y_peso_portafolios(fecha_inicio, fecha_fin, calcular_cantidad_inicial_activos_en_compra_venta())
    for item in data["portafolio 1"]:
        item['fecha'] = item['fecha'].strftime('%Y-%m-%d')
    for item in data["portafolio 2"]:
        item['fecha'] = item['fecha'].strftime('%Y-%m-%d')
    return render(request, 'graficos.html', {
        'data_portafolio_1': json.dumps(data["portafolio 1"]), 
        'data_portafolio_2': json.dumps(data["portafolio 2"]),
        'data_line': json.dumps(data)
        })
