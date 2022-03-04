from django.contrib import admin
from django.urls import path

from MainApp import views as MainApp


urlpatterns = [
    path('', MainApp.RestPage),
    path('list-produk/', MainApp.ListProduk),
    path('export-excel/', MainApp.ExportExcel)
]
