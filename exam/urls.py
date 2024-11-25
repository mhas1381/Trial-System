from django.urls import path
from .views import exam_view , track_tab_change , home_view

app_name = "exam"

urlpatterns = [
    path("" , home_view , name = "home"),
    path("exam/" , exam_view , name = "exam"),
    path("track-tab-change/" , track_tab_change , name="tab-change")

]