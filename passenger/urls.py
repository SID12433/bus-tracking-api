from django.urls import path
from passenger import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("route",views.RouteView,basename="route")


urlpatterns = [
    path("register/",views.PassengerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    # path("search/",views.Search_route.as_view(),name="search_route"),
    path("profile/",views.profileView.as_view(),name="profile"),


    
] + router.urls