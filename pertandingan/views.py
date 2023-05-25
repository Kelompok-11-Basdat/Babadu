from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from util.query import *
from atlet.query import *
from Babadu.helper.function import *

# Create your views here.
def pertandingan_perempat(request):

    context = {
        'role' : 'Umpire',
    }
    return render(request, 'pertandingan_perempat.html', context)


def pertandingan_semifinal(request):

    context = {
        'role' : 'Umpire',
    }
    return render(request, 'pertandingan_semifinal.html', context)


def pertandingan_juara_tiga(request):

    context = {
        'role' : 'Umpire',
    }
    return render(request, 'pertandingan_juara_tiga.html', context)


def pertandingan_final(request):

    context = {
        'role' : 'Umpire',
    }
    return render(request, 'pertandingan_final.html', context)