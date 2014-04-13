from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response


# Create your views here.
def index(request):
    args = {}
    args['greet'] = "Hello, world. You're at the polls index."
    return render_to_response('index.html', args)

