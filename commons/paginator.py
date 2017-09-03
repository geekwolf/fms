#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginator(request,model_data):

    data = {}
    current_page = request.GET.get("page", 1)
    page_number = request.GET.get("pagenumber", 30)

    pages = Paginator(model_data, page_number)
    try:
        content = pages.page(current_page)
    except EmptyPage:
        content = pages.page(1)
    data["pagenumber"] = page_number
    data["content"] = content
    data["pages"] = pages
    data["request"] = request

    return data
