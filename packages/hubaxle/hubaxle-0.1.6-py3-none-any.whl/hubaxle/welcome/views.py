import os
import socket
import time

from django.shortcuts import render

from .diagnostics import get_all_diagnostics

def homepage_view(request):
    system_info = get_all_diagnostics()
    return render(request, 'homepage.html', {'system_info': system_info})
