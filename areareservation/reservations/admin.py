from reservations.models import Site
from reservations.models import Area
from reservations.models import Reservation
from reservations.models import AreaReservation
from django.contrib import admin

admin.site.register(Site)
admin.site.register(Area)
admin.site.register(Reservation)
admin.site.register(AreaReservation)

