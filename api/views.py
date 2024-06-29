from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.views import APIView

from budget.models import Income


from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

from api.serializers import UserSerializer,IncomeSerializer
# Create your views here.


class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        seriliazer_instance=UserSerializer(data=request.data)

        if seriliazer_instance.is_valid():

            seriliazer_instance.save()

            return Response(data=seriliazer_instance.data)
        
        else:
            return Response(data=seriliazer_instance.errors)
        

class IncomeViewSet(ModelViewSet):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]


