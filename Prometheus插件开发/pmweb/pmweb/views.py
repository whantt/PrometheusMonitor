# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os


def toMain(request):
    return render(request, "main.html")


def firstPage(request):
    return render(request, "firstPage.html")


def refresh(request):
    x = os.popen("curl -X POST http://127.0.0.1:9090/-/reload").read()
    return render(request, "firstPage.html", {'rs': x})
