from rest_framework import serializers
from adminapi.models import BusOwner,Bus,BusCategory,BusRoute,Route,BusRouteStops,BusStopDetail,Stop

class BusOwnerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    is_approved=serializers.CharField(read_only=True)

    class Meta:
        model=BusOwner
        fields=["id","username","password","phone","address","is_approved","proof"]
   
    def create(self, validated_data):
        return BusOwner.objects.create_user(**validated_data)


class BusOwnerProfileSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(read_only=True)
    username=serializers.CharField(read_only=True)
    proof=serializers.CharField(read_only=True)
    is_approved=serializers.CharField(read_only=True)
    
    class Meta:
        model=BusOwner
        fields=["id","username","password","phone","address","is_approved","proof"]


    
class BusSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    class Meta:
        model = Bus
        fields = "__all__"
        

class BusCategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    class Meta:
        model = BusCategory
        fields = "__all__"
        

class RouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Route
        fields = "__all__"
        
class StopSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Stop
        fields = "__all__"
        
class StopViewSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField(source='route.name')
    id=serializers.CharField(read_only=True)

    class Meta:
        model = Stop
        fields = ['id','route', 'stop_number', 'place', 'image', 'link']

    def get_route(self, obj):
        return obj.route.name if obj.route else None
        
        
class BusRouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    
    class Meta:
        model = BusRoute
        fields = "__all__"
        
class BusRouteListSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    route=RouteSerializer()
    bus=BusSerializer()
    buscategory=BusCategorySerializer()
    
    class Meta:
        model = BusRoute
        fields = "__all__"
        
        
class BusRouteStopsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    busowner = serializers.CharField(read_only=True)
    busroute = serializers.CharField(read_only=True)

    class Meta:
        model = BusRouteStops
        fields = "__all__"
        
        
# class RouteStopSerializer(serializers.ModelSerializer):
#     id=serializers.CharField(read_only=True)
#     busowner=serializers.CharField(read_only=True)
#     class Meta:
#         model = BusRouteStops
#         fields = "__all__"
        

class BusStopDetailSerializer(serializers.ModelSerializer):
    busstop=serializers.CharField(read_only=True)
    
    class Meta:
        model = BusStopDetail
        fields = "__all__"
        