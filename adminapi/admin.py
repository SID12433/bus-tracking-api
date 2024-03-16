from django.contrib import admin

# Register your models here.


from adminapi.models import Admin,Route,Stop,BusOwner,Passenger,BusCategory,Bus,BusRoute,BusRouteStops,BusStopDetail


admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(BusRouteStops)
admin.site.register(BusStopDetail)
admin.site.register(Stop)
admin.site.register(Route)
