# coding=UTF-8
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from reservations.models import Site
from reservations.models import Area
from reservations.models import Reservation
from reservations.models import AreaReservation
from reservations.models import WeekInfo
from datetime import date, time, datetime, timedelta
#import time

def index(request):
    return render_to_response('reservations/index.html', {'sites': Site.objects.all()})

def sitedetails(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    return render_to_response('reservations/sitedetails.html', {'site': site, 'reservations': Reservation.objects.filter(site=site), 'futurereservations': futurereservations(site), 'sites': Site.objects.all()})

def newreservation(request, site_id, fields = {}):
    foundsite = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=foundsite)
    site = foundsite
    levels =  site.usedFlightLevels.split(',')
    return render_to_response('reservations/new.html', {'site': site, 'areas': areas, 'levels': levels, 'sites': Site.objects.all(), 'error': fields.get('error')}, context_instance=RequestContext(request))

def deletereservation(request, reservation_id):
    r = Reservation.objects.get(id=reservation_id)
    site = r.site
    r.delete()
    return sitedetails(request, site.icao)

def detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    areas = AreaReservation.objects.filter(reservation=reservation)
    return render_to_response('reservations/detail.html', {'reservation': reservation, 'areas': areas, 'sites': Site.objects.all()}, context_instance=RequestContext(request))

def createreservation(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    areas = Area.objects.filter(site=site)
    levels =  site.usedFlightLevels.split(',')

    if request.POST['day'] == 'today':
    	startdate = date.today()
    if request.POST['day'] == 'tomorrow':
    	startdate = date.today() + timedelta(days=1)
    if request.POST['day'] == 'customdate':
	try:
	    	startdate = str2date(request.POST['date'])
	except:
		return newreservation(request, site.icao, {'error': 2})

    starttime = str2time(request.POST['startTime'])
    endtime = str2time(request.POST['endTime'])
    status = int(request.POST['status'])
    comment = request.POST['comment']

    reservation = Reservation.objects.create(site=site, date=startdate, startTime=starttime, endTime=endtime, status=status, comment=request.POST['comment'])
    reservationcount = 0
    for area in areas:
	imc = request.POST.has_key('area-' + str(area.id) + "/imc")
	fl = None
	for level in levels:
		if request.POST['area-' + str(area.id)] == level:
			fl = int(level)
	if request.POST['area-' + str(area.id)] == "custom":
		try:
			fl = int(request.POST[str(area.id) + '/customlevel'])
		except:
			reservation.delete()
			return newreservation(request, site.icao, {'error': 3})
	if fl:
		areareservation = AreaReservation.objects.create(reservation=reservation, area=area, flightLevel=fl, isImc=imc)
		print str(areareservation)
		reservationcount += 1
# todo check that some areas are created
    if(reservationcount is 0):
	reservation.delete()
	return newreservation(request, site.icao, {'error': 1})
    return sitedetails(request, site.icao)

def setstatus(request, reservation_id, newstatus):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
# todo check value
    reservation.status = int(newstatus)
    reservation.save()
    return detail(request, reservation_id)

def addcomment(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    comment = request.POST['comment']
    reservation.comment = reservation.comment + "\n--\n" + comment
    reservation.save()
    return detail(request, reservation_id)


def personnel(request, site_id):
    foundsite = get_object_or_404(Site, pk=site_id)
    site = foundsite
    weeks = []
    for i in range(1, 53):
	try:
		wi = WeekInfo.objects.get(weeknumber=i)
	except WeekInfo.DoesNotExist:
		wi = None

	aa_person = request.POST['aa_person_'+str(i)]
	if aa_person is not None and len(aa_person) > 0:
		print "Set stuff"
 	# TODO jatka tästä
	if wi is not None:
		weeks.append({'number': i, 'aa_person': wi.aa_person, 'aa_backup': wi.aa_backup})
	else:
		weeks.append({'number': i, 'aa_person': '', 'aa_backup': ''})

    return render_to_response('reservations/personnel.html', {'site': site, 'weeks': weeks}, context_instance=RequestContext(request))


def futurereservations(site):
    numDays=7
    fr = []
    for i in range(0, numDays):
	d = date.today() + timedelta(days=i)
	res = Reservation.objects.filter(site__exact=site,date__exact=d)
        dayinfo = {'date': d, 'reservations': res, 'sites': Site.objects.all()}
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

