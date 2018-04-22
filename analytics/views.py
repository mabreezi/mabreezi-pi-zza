# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def goods(request):
    return render(request, 'analytics/goods.html',{'section_name':'Goods Report'})

def cash(request):
    return render(request, 'analytics/cash.html', {'section_name':'Cash Report'})

def demographic(request):
    return render(request, 'analytics/demographic.html', {'section_name':'Demographic Report'})