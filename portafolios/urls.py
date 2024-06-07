from django.urls import path

from . import views
from portafolios.views import ValoresView

urlpatterns = [
    path("", views.index, name="index"),
    path('valores/', ValoresView.as_view(), name='valores'),
    path('graficos/', views.graficos_view, name='graficos'),
    path('graficos_compra_venta/', views.graficos_con_compra_venta_view, name='grafico_compra_venta')
]
