from djx.views import page

# Create your views here.


def index(request):
    context = {}
    return page(request, "index.html", context)
