from operator import mod
from django.db import models
from sympy import Max, mobius

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    kata_sandi = models.CharField(max_length=200)
    tipe_user = models.CharField(max_length=30)
    login_last = models.CharField(max_length=40)
    aktif = models.CharField(max_length=1)
    class Meta:
        db_table = "tbl_user"

class Produk(models.Model):
    kode_produk = models.CharField(max_length=150)
    nama_produk = models.CharField(max_length=150)
    class Meta:
        db_table = "tbl_produk"

class Faktur(models.Model):
    kode_faktur = models.CharField(max_length=100)
    class Meta:
        db_table = "tbl_faktur"

class Transaksi(models.Model):
    kode_faktur = models.CharField(max_length=100)
    kode_produk = models.CharField(max_length=100)
    class Meta:
        db_table = "tbl_transaksi"