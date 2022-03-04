import imp
import csv
import os
from pydoc import apropos
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from matplotlib.style import context
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

from .models import Produk
from .models import Transaksi

# Create your views here.
def RestPage(request):
    context  = {
        'judul' : 'REST API PERHITUNGAN APRIORI'
    }
    return JsonResponse(context, safe=False)
    
@csrf_exempt
def ProsesApriori(request):
    dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)

    NoTransaksi = []
    DataTransaksiArr = []
    DataTransaksi = Transaksi.objects.all().values()
    ord = 0
    for x in DataTransaksi:
        kodeFaktur = DataTransaksi[ord]['kode_faktur']
        CekKode = kodeFaktur in NoTransaksi
        if CekKode == False:
            NoTransaksi.append(kodeFaktur)
        ord = ord + 1
    DataMerge = []
    for x in NoTransaksi:
        NoTransaksi = x
        DtGroup = Transaksi.objects.filter(kode_faktur=NoTransaksi).values()
        ordp = 0
        DataListSub = []
        for k in DtGroup:
            kodeProdukTransaksi = DtGroup[ordp]['kode_produk']
            DpCek = Produk.objects.filter(kode_produk=str(kodeProdukTransaksi)).count()
            if DpCek > 0:
                DataProduk = Produk.objects.filter(kode_produk=str(kodeProdukTransaksi)).first()
                DataListSub.append(DataProduk.nama_produk)
            ordp = ordp + 1
        DataMerge.append(DataListSub)
    
    transactions = []
    for i in range(0, 7501):
        transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])

    # print(transactions[0])
    # print(DataMerge[0])
    # pritn()
    transactions2 = [
    ['beer', 'nuts'],
    ['beer', 'cheese']
]
    rules = apriori(transactions = transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)
    rules2 = apriori(transactions = DataMerge,  min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)
    results2 = list(rules2)
    results = list(rules)

    resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['A', 'B', 'Support', 'Confidence', 'Lift'])
    hasilTerurut = resultsinDataFrame.nlargest(n = 10, columns = 'Lift')
    ordHasil = 0
    hasilBismillah = []

    for x in results2:
        stringAwal = str(results2[ordHasil].items)
        StringAwal2 = str(results2[ordHasil].ordered_statistics[0].items_add)
        stringPisah = stringAwal.split("'")
        StringPisah2 = StringAwal2.split("'")
        support = str(results2[ordHasil].support)
        confidence = str(results2[ordHasil].ordered_statistics[0].confidence)
        lift = str(results2[ordHasil].ordered_statistics[0].lift)
        hasilBismillah.append([stringPisah[1],StringPisah2[1], support, confidence, lift])

        ordHasil = ordHasil + 1
        
    sideA = resultsinDataFrame.nlargest(n = 10, columns = 'Lift')["A"]
    sideB = resultsinDataFrame.nlargest(n = 10, columns = 'Lift')["B"]
    nilai = resultsinDataFrame.nlargest(n = 10, columns = 'Lift')["Lift"]

    ord = 0
    hasilPola = []
    for x in sideA:
        pola = "Jika pelanggan membeli "+sideA[ord]+" maka juga akan membeli "+sideB[ord]+" dengan nilai "+str(nilai[ord])
        hasilPola.append(pola)
        ord = ord + 1

    context = {
        'hasil' : hasilBismillah
    }
    return JsonResponse(context, safe=False)

def ExportExcel(request):
    Produk.objects.all().delete()
    exd = pd.read_excel("DataProduk.xlsx")
    all = exd.iloc[:,0:2]
    arrData = all.to_numpy()
    ord = 0
    DataProduk = []
    for x in arrData:
        qSaveProduk = Produk.objects.create(kode_produk=arrData[ord][1], nama_produk=arrData[ord][0])
        qSaveProduk.save()
        DataProduk.append([arrData[ord][0], arrData[ord][1]])
        ord = ord + 1
    # print(arrData[0])
    context  = {
        'produk' : DataProduk
    }
    return JsonResponse(context, safe=False)

def ImportDataTransaksi(request):
    Transaksi.objects.all().delete()
    exd = pd.read_excel("DataTransaksi.xlsx")
    all = exd.iloc[:,0:2]
    arrData = all.to_numpy()
    ord = 0
    DataTransaksi = []
    for x in arrData:
        kodeProduk = str(arrData[ord][1])
        noTransaksi = str(arrData[ord][0])
        finKodeProduk = kodeProduk.replace(".0","")
        finNoTransaksi = noTransaksi.replace(".0","")

        # print(finKodeProduk)
        qSaveTransaksi = Transaksi.objects.create(kode_faktur=finNoTransaksi, kode_produk=finKodeProduk)
        qSaveTransaksi.save()
        ord = ord + 1
    context  = {
        'produk' : 'sukses'
    }
    return JsonResponse(context, safe=False)


def WriteCsv(request):
    NoTransaksi = []
    DataTransaksiArr = []
    DataTransaksi = Transaksi.objects.all().values()
    os.remove("RawTransaksi.csv")
    
    ord = 0
    for x in DataTransaksi:
        kodeFaktur = DataTransaksi[ord]['kode_faktur']
        CekKode = kodeFaktur in NoTransaksi
        if CekKode == False:
            NoTransaksi.append(kodeFaktur)
        DataTransaksiArr.append(DataTransaksi[ord]['kode_faktur'])
        ord = ord + 1
    DataMarge = []
    for x in NoTransaksi:
        StringKode = ""
        DtGroup = Transaksi.objects.filter(kode_faktur=x).values()
        ordp = 0
        for k in DtGroup:
            kodeProdukTransaksi = DtGroup[ordp]['kode_produk']
            DpCek = Produk.objects.filter(kode_produk=str(kodeProdukTransaksi)).count()
            DpDp = ""
            if DpCek > 0:
                DataProduk = Produk.objects.filter(kode_produk=str(kodeProdukTransaksi)).first()
                DpDp = DataProduk.nama_produk
            StringKode = StringKode + "," + str(DpDp)
            StrCv = StringKode[1:]
            
            ordp = ordp + 1
        
        DataMarge.append([x, StrCv])

    with open('RawTransaksi.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        ord2 = 0
        for k in DataMarge:
            spamwriter.writerow([DataMarge[ord2][1]])
            ord2 = ord2 + 1

    context  = {
        'produk' : 'sukses',
        'dataMarge' : DataMarge
    }
    return JsonResponse(context, safe=False)

def ListProduk(request):
    DataProduk = Produk.objects.all().values()
    produk = []
    ord = 0
    for x in DataProduk:
        produk.append(DataProduk[ord])
        ord = ord + 1

    context  = {
        'produk' : produk
    }
    return JsonResponse(context, safe=False)

def inspect(results):
    lhs = [tuple(result[2][0][0])[0] for result in results]
    rhs = [tuple(result[2][0][1])[0] for result in results]
    supports = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))