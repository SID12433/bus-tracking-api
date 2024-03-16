from rest_framework import serializers
from adminapi.models import Passenger,Route,Bus,Stop,BusCategory,BusRoute,BusRouteStops,BusStopDetail

class PassengerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Passenger
        fields=["id","phone","username","address","password","email_address"]

    def create(self, validated_data):
        return Passenger.objects.create_user(**validated_data)
    
    
class StopSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    route=serializers.CharField(read_only=True)
    class Meta:
        model = Stop
        fields = "__all__"
        
        
class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = BusCategory
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Route
        fields = "__all__"

        
        
class BusRouteSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    buscategory = serializers.CharField(source='buscategory.category', read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = BusRoute
        fields = "__all__"
        

class BusSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Bus
        fields = "__all__"
        
        
class BusRouteStopsSerializer(serializers.ModelSerializer):
    stop = StopSerializer()
    class Meta:
        model = BusRouteStops
        fields = ['stop']
        

class BusStopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStopDetail
        fields = "__all__"
    
        
        
class BusRouteDetailSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    route=RouteSerializer()
    bus=BusSerializer()
    buscategory=CategorySerializer()
    busroutestops = BusRouteStopsSerializer(many=True, read_only=True)
       
    class Meta:
        model = BusRoute
        fields = "__all__"