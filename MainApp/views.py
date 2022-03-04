from django.shortcuts import render
from django.http import JsonResponse
from matplotlib.style import context
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

from .models import Produk

# Create your views here.
def RestPage(request):
    dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)
    transactions = []
    for i in range(0, 7501):
        transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])

    rules = apriori(transactions = transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)

    results = list(rules)

    resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['A', 'B', 'Support', 'Confidence', 'Nilai'])
    hasilTerurut = resultsinDataFrame.nlargest(n = 10, columns = 'Nilai')

    sideA = resultsinDataFrame.nlargest(n = 10, columns = 'Nilai')["A"]
    sideB = resultsinDataFrame.nlargest(n = 10, columns = 'Nilai')["B"]
    nilai = resultsinDataFrame.nlargest(n = 10, columns = 'Nilai')["Nilai"]

    ord = 0
    hasilPola = []
    for x in sideA:
        pola = "Jika pelanggan membeli "+sideA[ord]+" maka juga akan membeli "+sideB[ord]+" dengan nilai "+str(nilai[ord])
        hasilPola.append(pola)
        ord = ord + 1

    context = {
        'nama' : 'Aditia',
        'hasil' : hasilPola
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