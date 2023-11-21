from django.db import models

# Create your models here.

class StudentDetails(models.Model):
    studentID = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    major = models.CharField(max_length = 100)
    year = models.CharField(max_length = 50)
    gpa = models.DecimalField(max_digits = 3, decimal_places=2)

class BookDetails(models.Model):
    bookid = models.IntegerField(primary_key=True)
    bookname = models.CharField(max_length = 100)
    authorname = models.CharField(max_length = 100)
    currentlycheckedout = models.CharField(max_length = 50)
    numberoftimescheckedout = models.IntegerField()
