from reservations.models import Site
from reservations.models import Area
from reservations.models import Reservation
from reservations.models import AreaReservation
from reservations.models import WeekInfo
from reservations.models import DayInfo

from django.contrib import admin

admin.site.register(Site)
admin.site.register(Area)
admin.site.register(Reservation)
admin.site.register(AreaReservation)
admin.site.register(WeekInfo)
admin.site.register(DayInfo)

