from django.urls import path
from busowner import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
router.register("bus",views.BusView,basename="bus-add")  
router.register("route",views.RouteView,basename="route") 
router.register("category",views.CategoriesView,basename="category")
router.register("routeassign",views.BusRouteView,basename="routeassign")
router.register("stops",views.BusRouteStopView,basename="stops")


urlpatterns = [
    path("register/",views.BusOwnerCreationView.as_view(),name="signup"),
    path("profile/",views.profileView.as_view(),name="profile"),
    path("token/",ObtainAuthToken.as_view(),name="token")
   
]+router.urls