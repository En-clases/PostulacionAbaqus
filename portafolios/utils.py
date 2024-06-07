from portafolios.models import Portafolio, Activo, Precio, Weight

def calcular_cantidad_inicial_activos(portafolio_nombre, valor_inicial):
    try:
        portafolio = Portafolio.objects.get(nombre=portafolio_nombre)
    except Portafolio.DoesNotExist:
        raise ValueError(f"Portafolio {portafolio_nombre} no existe.")
    
    pesos = Weight.objects.filter(portafolio=portafolio).select_related('activo')
    
    c_inicial = {}
    for peso in pesos:
        activo = peso.activo
        precio_inicial = Precio.objects.filter(activo=activo, fecha='2022-02-15').first()
        if precio_inicial:
            c_i0 = (peso.weight * valor_inicial) / precio_inicial.precio
            c_inicial[activo.nombre] = c_i0
        else:
            raise ValueError(f"Precio inicial para {activo.nombre} no encontrado.")
    
    return c_inicial

def calcular_cantidad_inicial_activos_para_cada_portafolio():
    valor_unicial = 1000000000
    resultados = {}
    
    for portafolio_nombre in ['portafolio 1', 'portafolio 2']:
        c_inicial = calcular_cantidad_inicial_activos(portafolio_nombre, valor_unicial)
        resultados[portafolio_nombre] = c_inicial

    
    return resultados

def calcular_cantidad_inicial_activos_en_compra_venta():
    valor_inicial = 1000000000
    resultados = {}
    
    for portafolio_nombre in ['portafolio 1', 'portafolio 2']:
        c_inicial = calcular_cantidad_inicial_activos(portafolio_nombre, valor_inicial)
        resultados[portafolio_nombre] = c_inicial
    
    activo_eeuu = Activo.objects.get(nombre="EEUU")
    precio_eeuu = Precio.objects.filter(activo=activo_eeuu, fecha='2022-02-15').first()
    if precio_eeuu:
        c_i0_eeuu = resultados['portafolio 1']['EEUU'] - 200000000 / precio_eeuu.precio
        resultados['portafolio 1']['EEUU'] = c_i0_eeuu
    else:
        raise ValueError("Precio inicial para EEUU no encontrado.")

    activo_europa = Activo.objects.get(nombre="Europa")
    precio_europa = Precio.objects.filter(activo=activo_europa, fecha='2022-02-15').first()
    if precio_europa:
        c_i0_europa = resultados['portafolio 1']['Europa'] + 200000000 / precio_europa.precio
        resultados['portafolio 1']['Europa'] = c_i0_europa
    else:
        raise ValueError("Precio inicial para Europa no encontrado.")
    


    return resultados

def calcular_valor_y_peso_portafolios(fecha_inicio, fecha_fin, cantidades_iniciales_activos):
    resultados = {}
    portafolios = Portafolio.objects.filter(
        nombre__in=['portafolio 1', 'portafolio 2'])

    for portafolio in portafolios:
        pesos = Weight.objects.filter(
            portafolio=portafolio).select_related('activo')
        activos = [peso.activo for peso in pesos]

        datos = []
        fechas = Precio.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).values_list(
            'fecha', flat=True).distinct()

        for fecha in fechas:
            v_t = 0
            x_i_t = {}
            for activo in activos:
                precio = Precio.objects.filter(
                    activo=activo, fecha=fecha).first()
                if precio:
                    c_i0 = cantidades_iniciales_activos[portafolio.nombre][activo.nombre]
                    x_i_t[activo.nombre] = float(
                        precio.precio) * float(c_i0)
                    v_t += x_i_t[activo.nombre]

            w_i_t = {activo: x_i_t[activo] / v_t for activo in x_i_t}

            datos.append({
                'fecha': fecha,
                'v_t': v_t,
                'w_i_t': w_i_t
            })

        resultados[portafolio.nombre] = datos
    return resultados
    

