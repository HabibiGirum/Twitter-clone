from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . models import Members


def members(request):
    mymembers = Members.objects.all().values()
    template = loader.get_template('all_members.html')

    context = {
        'mymembers':mymembers,
    }
    return HttpResponse(template.render(context,request))

def details(request,id):
    mymember = Members.objects.get(id=id)

    template = loader.get_template('details.html')

    context ={
        'mymember':mymember,
    }

    return HttpResponse(template.render(context, request))