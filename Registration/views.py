from django.shortcuts import render, get_object_or_404
from .models import TimeSlot

# Create your views here.
def home(request):
    TimeSlots = TimeSlot.objects
    return render(request, 'Registration/home.html', {'TimeSlots': TimeSlots})

def details(request, id):
    TimeSlot_detail = get_object_or_404(TimeSlot, pk=id)
    return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail})
