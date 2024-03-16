from django.urls import path
from adminapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
router.register("route",views.RouteView,basename="route")
router.register("stop",views.StopView,basename="stop")
router.register("category",views.BusCategoryView,basename="category")
router.register("ownerview",views.OwnersView,basename="ownerview")
router.register("pendingowners",views.PendingOwnersView,basename="pendingownerview")
router.register("passengerview",views.PassengerView,basename="passengerlist")
router.register("bus",views.BusView,basename="bus-list")
router.register("busroutes",views.BusRoutesView,basename="busroutes")




urlpatterns = [
    path("register/",views.AdminCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token")

    
]+router.urls