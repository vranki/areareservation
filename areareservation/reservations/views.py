from django.conf.urls.defaults import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from reservations.models import Site
from reservations.models import Area
from reservations.models import Reservation
from reservations.models import AreaReservation

def index(request):
    return render_to_response('reservations/index.html', {'sites': Site.objects.all()})

def newreservation(request, site_id):
    foundsite = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=foundsite)
    site = foundsite
    levels =  site.usedFlightLevels.split(',')
    return render_to_response('reservations/new.html', {'site': site, 'areas': areas, 'levels': levels}, context_instance=RequestContext(request))

def detail(request, reservation_id):
    return HttpResponse("You're looking at reservation %s." % reservation_id)

def createreservation(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=site)
    levels =  site.usedFlightLevels.split(',')
    return render_to_response('reservations/index.html', {'sites': Site.objects.all()})

