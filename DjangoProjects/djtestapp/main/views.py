from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList


# Create your views here.
def home(response):
    return render(response, 'main/home.html', {})


def rolam(response):
    return render(response, 'main/rolam.html', {})


def versek(response):
    return render(response, 'main/versek.html', {})


def haiku(response):
    return render(response, 'main/haiku.html', {})


def fotok(response):
    return render(response, 'main/fotok.html', {})


def programozas(response):
    return render(response, 'main/programozas.html', {})
