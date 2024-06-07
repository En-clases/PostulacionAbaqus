import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from portafolios.models import Portafolio, Activo, Precio, Weight

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_path = 'portafolios/datos.xlsx'
        
        weights_df = pd.read_excel(file_path, sheet_name='weights')
        precios_df = pd.read_excel(file_path, sheet_name='Precios')
        
        portafolio1, _ = Portafolio.objects.get_or_create(nombre='portafolio 1')
        portafolio2, _ = Portafolio.objects.get_or_create(nombre='portafolio 2')
        
        activos = {}
        for col in precios_df.columns[1:]:
            activo, _ = Activo.objects.get_or_create(nombre=col)
            activos[col] = activo
        
        for index, row in weights_df.iterrows():
            activo = activos[row['activos']]
            Weight.objects.update_or_create(
                portafolio=portafolio1,
                activo=activo,
                defaults={'weight': row['portafolio 1']}
            )
            Weight.objects.update_or_create(
                portafolio=portafolio2,
                activo=activo,
                defaults={'weight': row['portafolio 2']}
            )
        
        for index, row in precios_df.iterrows():
            fecha = parse_date(row['Dates'].strftime('%Y-%m-%d'))
            for col in precios_df.columns[1:]:
                activo = activos[col]
                Precio.objects.update_or_create(
                    activo=activo,
                    fecha=fecha,
                    defaults={'precio': row[col]}
                )
        
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
