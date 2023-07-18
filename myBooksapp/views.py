
from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser, IsAuthenticated
from . permissions import IsAdminOrReadOnly, IsActiveUserOnly, IsNamedUserOnly
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

def home(request):
    user = User.objects.get(username='postman_client')
    token = Token.objects.create(user=user)
    return HttpResponse('token was created')

# Create your views here.
class BookList(APIView):
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]
    permission_classes = [AllowAny]

    def get(self, request):

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, permissions.IsAuthenticatedOrReadOnly])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=400)
    if request.method =='GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)

class RegisterUser(APIView):
    permission_classes = [AllowAny] # allow any user to register

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            # Create new User
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            # Create a token for User
            Token.objects.create(user=user)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginUser(APIView):
    permission_classes = [AllowAny] #allow any user to login

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                data = {"token": str(token), "username": username}
                return Response(data, status=200)
        return Response(serializer.errors, status=400)













