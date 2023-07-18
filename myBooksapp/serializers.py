from rest_framework import serializers
from .models import Book, BookReview
from rest_framework.exceptions import ValidationError
from datetime import date
from django.utils.html import strip_tags



class UniqueTitleValidator:
    def __call__(self, value):
        if Book.objects.filter(title=value).exists():
            raise ValidationError('Book with this title already exists')

class DateValidator:
    def __call__(self, value):
        if value > date.today():
            raise ValidationError('Date should be from past')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['review_text']

class Capitalize:
    def __call__(self, value):
        return value.title()

class BookSerializer(serializers.ModelSerializer):
    book_review = ReviewSerializer(many=True, read_only=True)
    title = serializers.CharField(required=True, max_length=255, validators=[UniqueTitleValidator()], trim_whitespace=True)
    published_date = serializers.DateField(validators=[DateValidator()])

    def validate_description(self, value):
        return strip_tags(value)

    def to_internal_value(self, data):
        if 'is_published' in data:
            data['is_published'] = True
        return super().to_internal_value(data)

    def to_representation(self, instance):
        instance.author = Capitalize()(instance.author)
        return super().to_representation(instance)


    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date', 'is_published', 'book_review']

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    
        


