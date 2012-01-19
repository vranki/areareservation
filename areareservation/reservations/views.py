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
    return render_to_response('reservations/sitedetails.html', {'site': site, 'reservations': Reservation.objects.filter(site=site), 'futurereservations': futurereservations(site)})

def newreservation(request, site_id):
    foundsite = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=foundsite)
    site = foundsite
    levels =  site.usedFlightLevels.split(',')
    return render_to_response('reservations/new.html', {'site': site, 'areas': areas, 'levels': levels}, context_instance=RequestContext(request))

def deletereservation(request, reservation_id):
    r = Reservation.objects.get(id=reservation_id)
    site = r.site
    r.delete()
    return sitedetails(request, site.icao)

def detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    areas = AreaReservation.objects.filter(reservation=reservation)
    return render_to_response('reservations/detail.html', {'reservation': reservation, 'areas': areas})

def createreservation(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=site)
    levels =  site.usedFlightLevels.split(',')
    print request.POST['day']
    if request.POST['day'] == 'today':
    	startdate = date.today()
    if request.POST['day'] == 'tomorrow':
    	startdate = date.today() + timedelta(days=1)
    if request.POST['day'] == 'customdate':
    	startdate = str2date(request.POST['date'])

    starttime = str2time(request.POST['startTime'])
    endtime = str2time(request.POST['endTime'])
    status = int(request.POST['status'])
    reservation = Reservation.objects.create(site=site, date=startdate, startTime=starttime, endTime=endtime, status=status)
#    reservation.comment = "kek"#request.POST['comment']

    for area in areas:
	print str(area)
	for level in levels:
		print str(level)
		imc = False
		paramname = 'area-' + str(area.id) + "/imc"
		if request.POST.has_key(paramname):
			imc = True
		if request.POST['area-' + str(area.id)] == level:
			areareservation = AreaReservation.objects.create(reservation=reservation,area=area,flightLevel=int(level),isImc=imc)
			print str(areareservation)

    return sitedetails(request, site.icao)

def futurereservations(site):
    numDays=7
    fr = []
    for i in range(0, numDays):
	d = date.today() + timedelta(days=i)
	resid = None
	res = None
	areas = None
	try:
	    res = Reservation.objects.get(site__exact=site,date__exact=d)
	except Reservation.DoesNotExist:
	    pass

	if res is not None:
	    areas = AreaReservation.objects.filter(reservation=res)
	    resid = res.id
        dayinfo = {'date': d, 'reservation': res, 'areas': areas, 'id': resid}
	fr.append(dayinfo)
    return fr

def str2time(s):
	splittime = s.split('.')
	return time(int(splittime[0]), int(splittime[1]))

def str2date(s):
	d = date.today()
	splitdate = s.split('.')
	d = d.replace(day=int(splitdate[0]),month=int(splitdate[1]))
	return d

