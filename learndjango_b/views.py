from django.shortcuts import render

def Hello(request):
    array = [3, 2, 1]
    context = {}
    context["name"] = "Hello hello"
    context["array"] = array
    return render(request, "index.html", context)
