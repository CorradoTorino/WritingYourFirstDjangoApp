from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world! My polls app")
# Create your views here.
