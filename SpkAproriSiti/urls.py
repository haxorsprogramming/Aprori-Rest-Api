from django.contrib import admin
from django.urls import path

from MainApp import views as MainApp


urlpatterns = [
    path('', MainApp.RestPage),
    path('list-produk/', MainApp.ListProduk),
    path('export-excel/', MainApp.ExportExcel),
    path('import-data-transaksi/', MainApp.ImportDataTransaksi),
    path('write-to-csv/', MainApp.WriteCsv),
    path('proses-apriori', MainApp.ProsesApriori)
]
