from django.urls import path
from .views import exam_view

app_name = "exam"

urlpatterns = [
    path("exam/" , exam_view , name = "exam")

]