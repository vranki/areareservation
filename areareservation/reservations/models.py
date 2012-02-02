from django.db import models

class Site(models.Model):
	icao = models.CharField("ICAO code of the site", max_length=4, primary_key=True)
	name = models.CharField("Name of the site", max_length=128, blank=True)
	usedFlightLevels = models.CommaSeparatedIntegerField("List of ceiling flight levels used on site, separated by commas", blank=True, max_length=256)
	def __unicode__(self):
		return self.name + " (" + self.icao + ")" 

class Area(models.Model):
	site = models.ForeignKey(Site)
	name = models.CharField("Name of the area", max_length=128)
	def __unicode__(self):
		return self.name + " (" + self.site.name + ")" 

class Reservation(models.Model):
	PLANNED_STATUS=1
	REQUESTED_STATUS=2
	ACCEPTED_STATUS=3
	REJECTED_STATUS=4
	STATUS_CHOICES = (
		(PLANNED_STATUS, 'Planned'), 
		(REQUESTED_STATUS, 'Requested'), 
		(ACCEPTED_STATUS, 'Accepted'), 
		(REJECTED_STATUS, 'Rejected'), 
	)
	site = models.ForeignKey(Site)
	date = models.DateField('Date active')
	startTime = models.TimeField('Starting time')
	endTime = models.TimeField('Ending time')
	comment = models.CharField("Comment text", blank=True, null=True, max_length=2048)
	status = models.IntegerField(choices=STATUS_CHOICES)
#	created = models.DateTimeField()
	def __unicode__(self):
		return str(self.site) + " " + str(self.date)

	def areas(self):
		return AreaReservation.objects.filter(reservation=self)
	
	def statusname(self):
		return dict(self.STATUS_CHOICES)[self.status]


class AreaReservation(models.Model):
	reservation = models.ForeignKey(Reservation)
	area = models.ForeignKey(Area)
	startTime = models.TimeField('Starting time', null=True)
	endTime = models.TimeField('Ending time', null=True)
	flightLevel = models.IntegerField('Ceiling flight level')
	isImc = models.BooleanField("Reservation is IMC")
	def __unicode__(self):
		return "Reservation of " + self.area.name + " FL" + str(self.flightLevel) + " on " + str(self.reservation.date) + " imc: " + str(self.isImc)

	def areaName(self):
		return self.area.name

