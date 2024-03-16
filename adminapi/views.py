from django.shortcuts import render
from rest_framework.views import APIView,status
from adminapi.serializers import AdminSerializer,RouteSerializer,StopSerializer,BusownerviewSerializer,PassengerviewSerializer,CategorySerializer,BusSerializer,BusRouteSerializer,BusRouteStopsSerializer,BusStopDetailSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from adminapi.models import Admin,Route,Stop,BusOwner,Passenger,BusCategory,Bus,BusRoute,BusRouteStops,BusStopDetail
from rest_framework.decorators import action



# for creating owners
class AdminCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Admin")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# for route
class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def list(self,request,*args,**kwargs):
        qs=Route.objects.all()
        serializer=RouteSerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        try:
            route = Route.objects.get(pk=kwargs.get("pk"))
        except Route.DoesNotExist:
            return Response({"error": "Route does not exist"},status=status.HTTP_404_NOT_FOUND)
        route_serializer = RouteSerializer(route)
        stops_serializer = StopSerializer(route.stop_set.all(), many=True)
        response_data = route_serializer.data
        response_data['stops'] = stops_serializer.data
        return Response(response_data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Route.objects.get(id=id)
            instance.delete()
            return Response("route removed")
        except Route.DoesNotExist:
            return Response("route not found", status=status.HTTP_404_NOT_FOUND)
        
    
    @action(methods=["post"], detail=True)
    def add_stop(self, request, *args, **kwargs):
        serializer=StopSerializer(data=request.data)
        route_id=kwargs.get("pk")
        route_obj=Route.objects.get(id=route_id)
        if serializer.is_valid():
            serializer.save(route=route_obj)
            return Response(serializer.data)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
       
       
# for viewing stops  
class StopView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 
     
    def list(self,request,*args,**kwargs):
        qs=Stop.objects.all()
        serializer=StopSerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Stop.objects.get(id=id)
        serializer=StopSerializer(qs)
        return Response(serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Stop.objects.get(id=id)
            instance.delete()
            return Response("stop removed")
        except Route.DoesNotExist:
            return Response("stop not found", status=status.HTTP_404_NOT_FOUND)
    


# for bus category
class BusCategoryView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def list(self,request,*args,**kwargs):
        qs=BusCategory.objects.all()
        serializer=CategorySerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        qs=BusCategory.objects.get(id=id)
        serializer=CategorySerializer(qs)
        return Response(serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =BusCategory.objects.get(id=id)
            instance.delete()
            return Response({'response':"BusCategory removed"})
        except Route.DoesNotExist:
            return Response({'response':"BusCategory not found"}, status=status.HTTP_404_NOT_FOUND)



# for viewing busowners
class OwnersView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 
     
    def list(self,request,*args,**kwargs):
        qs=BusOwner.objects.all()
        serializer=BusownerviewSerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusOwner.objects.get(id=id)
        serializer=BusownerviewSerializer(qs)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=["post"])
    def owner_approval(self, request, *args, **kwargs):
        owner_id = kwargs.get("pk")     
        owner_obj = BusOwner.objects.get(id=owner_id)
        owner_obj.is_approved = True
        owner_obj.save()
        serializer = BusownerviewSerializer(owner_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def owner_reject(self, request, *args, **kwargs):
        owner_id = kwargs.get("pk")     
        owner_obj = BusOwner.objects.get(id=owner_id)
        owner_obj.is_approved = False
        owner_obj.save()
        serializer = BusownerviewSerializer(owner_obj)
        return Response(serializer.data)
    
    

# for viewing passengers
class PassengerView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 
     
    def list(self,request,*args,**kwargs):
        qs=Passenger.objects.all()
        serializer=PassengerviewSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Passenger.objects.get(id=id)
        serializer=PassengerviewSerializer(qs)
        return Response(serializer.data)          


    
# for viewing pending busowners   
class PendingOwnersView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 
     
    def list(self,request,*args,**kwargs):
        qs=BusOwner.objects.filter(is_approved=False)
        serializer=BusownerviewSerializer(qs,many=True)
        return Response(serializer.data)
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusOwner.objects.get(id=id)
        serializer=BusownerviewSerializer(qs)
        return Response(serializer.data)
    
    
    
#for viewing buses   
class BusView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    
    def list(self,request,*args,**kwargs):
        qs=Bus.objects.all()
        serializer=BusSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bus.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(serializer.data)  
    
    
    
class BusRoutesView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    
    def list(self,request,*args,**kwargs):
        qs=BusRoute.objects.all()
        serializer=BusRouteSerializer(qs,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusRoute.objects.get(id=id)
        serializer=BusRouteSerializer(qs)
        return Response(serializer.data) 