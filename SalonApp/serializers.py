from rest_framework.serializers import ModelSerializer
from SalonApp.models import StaffDb,AppoinmentDb


class Staff_Serializer(ModelSerializer):
    class Meta:
        model = StaffDb
        fields = "__all__"
        read_only_fields = ["id"]

class Appoinment_Serializer(ModelSerializer):
    class Meta:
        model = AppoinmentDb
        fields = "__all__"
        read_only_fields = ["id"]