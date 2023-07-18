from django.urls import path
from .views import (
    BookList,
    book_detail,
    home,
    RegisterUser,
    LoginUser,
)

app_name = 'book-app'

urlpatterns = [
    path('books/', BookList.as_view(), name= 'book-list'),
    path('book/<int:pk>/', book_detail, name='book-detail'),
    path('token/', home, name='token'),
    path("register/", RegisterUser.as_view(), name='register_user'),
    path("login/", LoginUser.as_view(), name='login_user')
]