from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView,status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action


from passenger.serializers import PassengerSerializer,RouteSerializer,StopSerializer,BusRouteSerializer,BusRouteStopsSerializer,BusStopDetailSerializer,BusSerializer,BusRouteDetailSerializer
from adminapi.models import Passenger,Route,BusRoute,BusRouteStops,BusStopDetail




# Create your views here.


class PassengerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Passenger")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 

class profileView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        busowner_id=request.user.id
        qs=Passenger.objects.get(id=busowner_id)
        serializer=PassengerSerializer(qs)
        return Response(serializer.data)

       
        
class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
        
        
    # def list(self,request,*args,**kwargs):
    #     qs=BusRoute.objects.all()
    #     serializer=BusRouteSerializer(qs,many=True)
    #     return Response(serializer.data)
    
    
    
    def list(self, request, *args, **kwargs):
        qs = BusRoute.objects.all()
        route_data = []
        for route in qs:
            route_serializer = BusRouteDetailSerializer(route)
            bus_route_stops = route.busroutestops_set.all()
            stop_data = []
            for bus_route_stop in bus_route_stops:
                stop_serializer = BusRouteStopsSerializer(bus_route_stop)
                stop_detail = BusStopDetail.objects.get(busstop=bus_route_stop)
                stop_detail_serializer = BusStopDetailSerializer(stop_detail)
                stop_data.append({
                    'stop': {
                        **stop_serializer.data,
                        'stop_detail': {
                            'time': stop_detail_serializer.data.get('time'),
                            'amount': stop_detail_serializer.data.get('amount')
                        }
                    }
                })
            route_data.append({
                'busroute': route_serializer.data,
                'bus_route_stops': stop_data
            })
        return Response(route_data, status=status.HTTP_200_OK)

    
    
    
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            bus_route = BusRoute.objects.get(id=id)
        except BusRoute.DoesNotExist:
            return Response({"message": "Bus route does not exist"}, status=status.HTTP_404_NOT_FOUND)
        route_serializer = BusRouteDetailSerializer(bus_route)
        bus_route_stops = bus_route.busroutestops_set.all()
        stop_data = []
        for bus_route_stop in bus_route_stops:
            stop_serializer = BusRouteStopsSerializer(bus_route_stop)
            stop_detail = BusStopDetail.objects.get(busstop=bus_route_stop)
            stop_detail_serializer = BusStopDetailSerializer(stop_detail)
            stop_data.append({
                'stop': {
                    **stop_serializer.data,
                    'stop_detail': { 
                        'time': stop_detail_serializer.data.get('time'),
                        'amount': stop_detail_serializer.data.get('amount')
                    }
                }
            })
        data={
            'busroute': route_serializer.data,
            'bus_route_stops': stop_data
        }
        return Response(data, status=status.HTTP_200_OK)
    

# class Search_route(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    # 
    # def get(self, request, *args, **kwargs):
    #     start_stop = request.data.get('start_stop')
    #     end_stop = request.data.get('end_stop')
    #     category = request.data.get('category')
    #     bus_routes = BusRoute.objects.all()
    #     if start_stop and end_stop:
    #         start_stops = BusRouteStops.objects.filter(stop__place=start_stop)
    #         end_stops = BusRouteStops.objects.filter(stop__place=end_stop)
    #         start_routes = start_stops.values_list('busroute_id', flat=True)
    #         end_routes = end_stops.values_list('busroute_id', flat=True)
    #         common_routes = set(start_routes) & set(end_routes)
    #         bus_routes = bus_routes.filter(id__in=common_routes)

    #     if category:
    #         bus_routes = bus_routes.filter(buscategory=category)
    #     serializer = BusRouteSerializer(bus_routes, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
