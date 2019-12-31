from django.shortcuts import render


def all_rooms(request):
    return render(request, "all_rooms.html")
