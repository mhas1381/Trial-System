from django.shortcuts import render

# Create your views here.
def exam_view(request):

    return render(request , "exam/exam.html")