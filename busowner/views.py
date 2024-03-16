from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


from rest_framework.views import APIView,status
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response

from busowner.serializers import BusOwnerSerializer,BusSerializer,BusCategorySerializer,BusRouteSerializer,RouteSerializer,BusRouteStopsSerializer,BusStopDetailSerializer,StopSerializer,BusRouteListSerializer,StopViewSerializer
from adminapi.models import BusOwner,Route,Bus,BusDriver,BusCategory,BusRoute,BusRouteStops,BusStopDetail,Stop




class IsBusOwnerApproved(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'busowner'):
            return request.user.busowner.is_approved
        return False    
    


class BusOwnerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=BusOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Bus Owner")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class profileView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        busowner_id=request.user.id
        qs=BusOwner.objects.get(id=busowner_id)
        serializer=BusOwnerSerializer(qs)
        return Response(serializer.data)



class CategoriesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
            
    def list(self,request,*args,**kwargs):
        qs=BusCategory.objects.all()
        serializer=BusSerializer(qs,many=True)
        return Response(serializer.data)

        
        
class BusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def create(self,request,*args,**kwargs):
        serializer=BusSerializer(data=request.data)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=Bus.objects.filter(busowner=busowner_obj)
        serializer=BusSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bus.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Bus.objects.get(id=id)
            instance.delete()
            return Response({'response':"bus removed"})
        except Bus.DoesNotExist:
            return Response({'response':"bus not found"}, status=status.HTTP_404_NOT_FOUND)
        


class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]

            
    def list(self,request,*args,**kwargs):
        qs=Route.objects.all()
        serializer=RouteSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        route_instance=Route.objects.get(id=id)
        route_serializer=RouteSerializer(route_instance)
        stops_qs=route_instance.stop_set.all()
        stop_serializer=StopSerializer(stops_qs, many=True)
        data = {
            'route': route_serializer.data,
            'stops': stop_serializer.data
        }
        return Response(data)
    
    

class BusRouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def create(self,request,*args,**kwargs):
        serializer=BusRouteSerializer(data=request.data)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        routetime=request.data.get("routetime")
        existing_routes=BusRoute.objects.filter(routetime=routetime)
        if existing_routes.exists():
            return Response({"error": "A route at this time already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=BusRoute.objects.filter(busowner=busowner_obj)
        serializer=BusRouteListSerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        busroute_obj = BusRoute.objects.get(id=id)
        bus_route = BusRouteListSerializer(busroute_obj)
        stops = BusRouteStops.objects.filter(busroute=busroute_obj)
        bus_route_stops_data = []
        for stop in stops:
            bus_route_stop_data = {
                'stopid':stop.id,
                'busowner': stop.busowner.username,
                'busroute': stop.busroute.route.name,
                'stop': stop.stop.place
            }
            bus_route_stops_data.append(bus_route_stop_data)
        data = {
            'bus_route': bus_route.data,
            'bus_route_stops': bus_route_stops_data
        }
        return Response(data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =BusRoute.objects.get(id=id)
            instance.delete()
            return Response({'response':"BusRoute removed"})
        except BusRoute.DoesNotExist:
            return Response({'response':"BusRoute not found"}, status=status.HTTP_404_NOT_FOUND)  
        
        
        
    @action(methods=["get"], detail=True)
    def available_stops(self, request, *args, **kwargs):
        route_assign_id=kwargs.get("pk")
        route_assign_obj=BusRoute.objects.get(id=route_assign_id)
        route =route_assign_obj.route
        available_stops = Stop.objects.filter(route=route)
        serializer = StopViewSerializer(available_stops, many=True)
        return Response(serializer.data)
    
       
        
    @action(methods=["post"], detail=True)
    def add_routestop(self, request, *args, **kwargs):
        busowner_id = request.user.id
        busowner_obj = BusOwner.objects.get(id=busowner_id)
        route_id = kwargs.get("pk")
        route_obj = BusRoute.objects.get(id=route_id)
        route_instance = route_obj.route
        stop_ids = request.data.get("stops", [])
        for stop_id in stop_ids:
            stop_id = int(stop_id)
            existing_stop = BusRouteStops.objects.filter(busroute=route_obj, stop_id=stop_id).exists()
            if existing_stop:
                return Response({"error": f"Stop with ID {stop_id} is already present in the route."}, status=status.HTTP_400_BAD_REQUEST)
        for stop_id in stop_ids:
            stop_id = int(stop_id)
            stop = Stop.objects.filter(route=route_instance, id=stop_id).first()
            if stop:
                serializer = BusRouteStopsSerializer(data={"stop": stop_id}, context={'route_stops': route_instance})
                if serializer.is_valid():
                    serializer.save(busroute=route_obj, busowner=busowner_obj)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": f"Stop with ID {stop_id} not found for this route."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Stops added to the route successfully."})
  
    
    
class BusRouteStopView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]

            
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=BusRouteStops.objects.filter(busowner=busowner_obj)
        serializer=BusRouteStopsSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusRouteStops.objects.get(id=id)
        serializer=BusRouteStopsSerializer(qs)
        return Response(serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =BusRouteStops.objects.get(id=id)
            instance.delete()
            return Response("stop removed")
        except Route.DoesNotExist:
            return Response("stop not found", status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=["post"], detail=True)
    def stopdetail(self, request, *args, **kwargs):
        serializer=BusStopDetailSerializer(data=request.data)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        stop_id=kwargs.get("pk")
        stop_obj=BusRouteStops.objects.get(id=stop_id)
        if serializer.is_valid():
            serializer.save(busstop=stop_obj,busowner=busowner_obj)
            return Response(serializer.data)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
