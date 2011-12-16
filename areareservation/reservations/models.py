from django.db import models

class Site(models.Model):
	icao = models.CharField("ICAO code of the site", maxlength=4, primary_key=True)
	name = models.CharField("Name of the site", maxlength=128)
	usedFlightLevels = models.CommaSeparatedIntegerField("List of ceiling flight levels used on site")

class Area(models.Model):
	site = models.ForeignKey(Site)
	name = models.CharField("Name of the area", maxlength=128)

class Reservation(models.Model):
	site = models.ForeignKey(Site)
	date = models.DateField('Date active')
	startTime = models.TimeField('Starting time')
	endTime = models.TimeField('Ending time')
	comment = models.CharField("Comment text")

class AreaReservation(models.Model):
	reservation = models.ForeignKey(Reservation)
	area = models.ForeignKey(Area)
	startTime = models.TimeField('Starting time', blank=True)
	endTime = models.TimeField('Ending time', blank=True)
	flightLevel = models.IntegerField('Ceiling flight level')
	isImc = models.BooleanField("Reservation is IMC")

