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
