from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255)
    description = models.TextField()
    published_date = models.DateField()
    is_published = models.BooleanField(default=False)

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_review')
    review_text = models.TextField()
