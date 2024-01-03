from django.shortcuts import render
from django.http import HttpResponse
from bookreservation.models import BookDetails, StudentDetails, BookReservationModel
from django.db import connection
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django import forms
from django.db.models import Avg
# Create your views here.

@login_required
def home(request):
    enrolledStudents = StudentDetails.objects.count()
    averageGPA = StudentDetails.objects.aggregate(avg_gpa = Avg('gpa'))['avg_gpa']
    seniorsCount = StudentDetails.objects.filter(year='Senior').count()
    juniorsCount = StudentDetails.objects.filter(year='Junior').count()
    freshmenCount = StudentDetails.objects.filter(year='Freshman').count()
    sophomoreCount = StudentDetails.objects.filter(year='Sophomore').count()

    context = {
        'enrolledStudents': enrolledStudents,
        'averageGPA': averageGPA,
        'seniorsCount': seniorsCount,
        'juniorsCount': juniorsCount,
        'freshmenCount': freshmenCount,
        'sophomoreCount': sophomoreCount,
    }

    return render(request, 'bookreservation/home.html',context)

class LoginView(LoginView):
    template_name = 'login.html'

@login_required
def studentView(request):
    students = StudentDetails.objects.all()
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    pagedata = paginator.get_page(page)

    context = {'data': pagedata}
    return render(request, 'bookreservation/StudentDetails.html',context)

@login_required
def bookView(request):
    books = BookDetails.objects.all().order_by('numberoftimescheckedout')
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    pagedata = paginator.get_page(page)

    context = {'data': pagedata}
    return render(request, 'bookreservation/BookDetails.html',context)

@login_required
def BookReservation(request):
    studentData = StudentDetails.objects.all()
    bookData = BookDetails.objects.all()
    bookReservationData = BookReservationModel.objects.all()
    context = {'studentID': studentData, 'bookName': bookData, 'bookReservationStatus': bookReservationData}
    return render(request, 'bookreservation/BookReservation.html',context)

def saveReservation(request):
    if('student' in request.GET and 'book' in request.GET):
        studentID = request.GET.get('student')
        bookData = request.GET.get('book')
        studentReserveCount = BookReservationModel.objects.filter(bookCount=bookData).count()
        if studentReserveCount >= 4:
            return HttpResponse('You are over your limit')
        if BookReservationModel.objects.filter(book=bookData).exists():
            return HttpResponse('This book is already reserved by another student.')
        reservation = BookReservationModel(student=studentID, book=bookData)
        reservation.save()
        book = BookModel.objects.get(bookData=bookData)
        book.currentlycheckedout = True
        book.numberoftimescheckedout += 1
        book.save()
        return HttpResponse('Reservation saved.')

    return HttpResponse('Try Again.')
