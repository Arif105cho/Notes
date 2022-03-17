from django.shortcuts import render
from .serializer import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import *
from rest_framework.views import APIView

# Create your views here.


#### SinUp ####
class Resgiteration(APIView):

    permission_class = (AllowAny,)

    def post(self, request):
        serializer = SignUp(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Resgistration successfully', 'data': data, 'status': HTTP_201_CREATED})
        return Response({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST})


### Login ###

class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message':'login successfully','data':serializer.data},status=HTTP_200_OK)
        return Response({'error':serializer.errors},status=HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            stu = User.objects.get(id=request.user.id)
            serializer = SignUp(stu)
            return Response(serializer.data,status=HTTP_200_OK)

        except Exception as e:
            return Response({'messgae': 'The Key Does Not exist..', 'error': str(e), 'status': HTTP_400_BAD_REQUEST})

    def put(self, request):

        try:

            obj = User.objects.get(id=request.user.id)
            serializer = SignUp(instance=obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Updaated Successfulyy", 'status': HTTP_202_ACCEPTED})
            return Response({'message': 'Key Does not found', 'error': serializer.errors})
        except Exception as e:
            return Response({'error': str(e)})

    def delete(self, request):
        try:
            obj = User.objects.get(id=request.user.id)
            obj.delete()
            return Response({'message': 'The Data Deleted'})
        except Exception as e:
            return Response({'message': str(e)})


class NoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = NoteSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Note updload successfully', 'data': data, 'status': HTTP_200_OK})
        return Response({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST})


    def get(self, request):
        try:
            obj = Notes.objects.get(user=request.user)
            serializer = NoteSerializer(obj,many=True)
            return Response({'data': serializer.data,'status': HTTP_200_OK})
        except Exception as e:
            return Response({'error':str(e), 'status': HTTP_400_BAD_REQUEST})

    def put(self,request):
        try:

            obj=Notes.objects.get(user=request.user)
            serializer=NoteSerializer(obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message" : "Updaated Successfulyy",'status':HTTP_202_ACCEPTED})
            return Response({'message':'Key Does not found','status': HTTP_400_BAD_REQUEST})
        except Exception as e:
            return Response({'error':str(e), 'status': HTTP_400_BAD_REQUEST})

    def delete(self, request, **kwargs):

        try:

            obj = Notes.objects.get(user=request.user)
            obj.delete()
            return Response({'message': 'The Data Deleted','status':HTTP_200_OK})
        except Exception as e:
            return Response({'message': str(e),'status': HTTP_400_BAD_REQUEST})



class AdminView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        try:

            id = pk
            if id is not None:
                stu = User.objects.get(id=id)
                serializer = SignUp(stu)

                return Response(serializer.data)

            stu = User.objects.all()
            serializer = SignUp(stu, many=True)
            return Response({'message':serializer.data,'status':HTTP_200_OK })
        except Exception as e:
            return Response({'messgae':'The Key Does Not exist..', 'error':str(e), 'status':HTTP_400_BAD_REQUEST})

    def put(self,request,pk):
        try:
            id=pk
            obj=User.objects.get(pk=id)
            serializer=SignUp(instance=obj,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Updaated Successfulyy", 'status': HTTP_202_ACCEPTED})
            return Response({'message':'Key Does not found','error':serializer.errors})
        except Exception as e:
            return Response({'error':str(e)})

    def delete(self, request, pk):
        try:
            id = pk
            obj = User.objects.get(pk=id)
            obj.delete()
            return Response({'message': 'The Data Deleted'})
        except Exception as e:
            return Response({'message': str(e)})

