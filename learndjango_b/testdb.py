from django.http import HttpResponse
from TestModel.models import Test


def add(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    test = Test(name=name, age=age)
    test.save()
    return HttpResponse("<p>Added database!</p>")

