from django.core.management.base import BaseCommand
from portafolios.utils import calcular_c_incial_compra_venta

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        resultados = calcular_c_incial_compra_venta()
        for portafolio, valores in resultados.items():
            self.stdout.write(f'Portafolio: {portafolio}')
            for activo, cantidad in valores.items():
                self.stdout.write(f'{activo}: {cantidad}')
