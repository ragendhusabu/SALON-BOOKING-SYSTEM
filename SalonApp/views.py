
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from SalonApp.models import StaffDb,AppoinmentDb
from SalonApp.serializers import Staff_Serializer,Appoinment_Serializer
from datetime import time,timedelta,datetime

# Create your views here.

class StaffListCreateView(APIView):
    def get(self,request):
        qs = StaffDb.objects.all()
        serializer_instance = Staff_Serializer(qs,many=True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = Staff_Serializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)
        else:
            return Response(data= serializer_instance.errors)


class StaffRetrieveUpdateDeleteView(APIView):

    def get(self,request,pk):
        qs = get_object_or_404(StaffDb,id=pk)
        serializer_instance = Staff_Serializer(qs)
        return Response(data = serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        staff_object = get_object_or_404(StaffDb,id=pk)
        serializer_instance = Staff_Serializer(data = form_data,instance=staff_object)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)
        return Response(data= serializer_instance.errors)

    def delete(self,request,pk):
        staff_object = get_object_or_404(StaffDb,id=pk)
        staff_object.delete()
        return Response(data ={
            "Status" :"Data deleted Successfully...!"
        })


class AppoinmentListCreateView(APIView):
    def get(self,request):
        qs = AppoinmentDb.objects.all()
        serializer_instance = Appoinment_Serializer(qs,many=True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = Appoinment_Serializer(data= form_data)

        if serializer_instance.is_valid():
            appoinment_date = serializer_instance.validated_data.get("appointment_date")
            staff = serializer_instance.validated_data.get("staff")

            last_appoinment = AppoinmentDb.objects.filter(
                appointment_date=appoinment_date,
                staff=staff
            ).order_by("-appointment_time").first()

            form_data = serializer_instance.validated_data.copy()

            if last_appoinment is None:
                form_data["appointment_time"] = time(10,0)
            else:
                current_time = datetime.combine(
                    appoinment_date,
                    last_appoinment.appointment_time
                )
                form_data["appointment_time"] = (
                    current_time + timedelta(minutes=15)
                ).time()

            qs = AppoinmentDb.objects.create(**form_data)

            return Response(data={
                "Status" : "Booking Successfull..!",
                "Appointment" : Appoinment_Serializer(qs).data
            })

        else:
            return Response(data=serializer_instance.errors)


class AppoinmentRetrieveUpdateDeleteView(APIView):

    def get(self,request,pk):
        qs = get_object_or_404(AppoinmentDb,id=pk)
        serializer_instance = Appoinment_Serializer(qs)
        return Response(data = serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        appoinment_object = get_object_or_404(AppoinmentDb,id=pk)
        serializer_instance = Appoinment_Serializer(
            data=form_data,
            instance=appoinment_object
        )

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)

        return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        appoinment_object = get_object_or_404(AppoinmentDb,id=pk)
        appoinment_object.delete()
        return Response(data={
            "Status" : "Appointment deleted Successfully...!"
        })
