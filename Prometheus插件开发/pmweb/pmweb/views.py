# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse


def toMain(request):
    return render(request, "main.html")


def firstPage(request):
    return render(request, "firstPage.html")