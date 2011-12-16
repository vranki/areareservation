# coding=UTF-8
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from reservations.models import Site
from reservations.models import Area
from reservations.models import Reservation
from reservations.models import AreaReservation
from datetime import date, time, datetime, timedelta
#import time

def index(request):
    return render_to_response('reservations/index.html', {'sites': Site.objects.all()})

def sitedetails(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    return render_to_response('reservations/sitedetails.html', {'site': site, 'reservations': Reservation.objects.filter(site=site)})

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
    if request.POST.has_key('today'):
    	startdate = date.today()	
    if request.POST.has_key('tomorrow'):
    	startdate = date.today() + timedelta(days=1)
    starttime = str2time(request.POST['startTime'])
    endtime = str2time(request.POST['endTime'])
    print str(startdate) + " " + str(starttime) + "-" + str(endtime)
    status = int(request.POST['status'])
    reservation = Reservation.objects.create(site=site, date=startdate, startTime=starttime, endTime=endtime, status=status)

#    reservation.comment = "kek"#request.POST['comment']

    for area in areas:
	for level in levels:
		imc = False
		paramname = 'area-' + str(area.id) + "/imc"
		if request.POST.has_key(paramname):
			imc = True
		if request.POST['area-' + str(area.id)] == level:
			areareservation = AreaReservation.objects.create(reservation=reservation,area=area,flightLevel=int(level),isImc=imc)
			print str(areareservation)

    return render_to_response('reservations/index.html', {'sites': Site.objects.all()})

def str2time(s):
	splittime = s.split('.')
	return time(int(splittime[0]), int(splittime[1]))

