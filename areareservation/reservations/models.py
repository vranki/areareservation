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
	STATUS_CHOICES = (
		(1, 'Planned'), 
		(2, 'Requested'), 
		(3, 'Accepted'), 
		(4, 'Rejected'), 
	)
	site = models.ForeignKey(Site)
	date = models.DateField('Date active')
	startTime = models.TimeField('Starting time')
	endTime = models.TimeField('Ending time')
	comment = models.CharField("Comment text", blank=True, max_length=2048)
	status = models.IntegerField(choices=STATUS_CHOICES)
	def __unicode__(self):
		return self.site.icao + " " + str(self.date) + " (" + str(self.id) + ")"

class AreaReservation(models.Model):
	reservation = models.ForeignKey(Reservation)
	area = models.ForeignKey(Area)
	startTime = models.TimeField('Starting time', blank=True)
	endTime = models.TimeField('Ending time', blank=True)
	flightLevel = models.IntegerField('Ceiling flight level')
	isImc = models.BooleanField("Reservation is IMC")

