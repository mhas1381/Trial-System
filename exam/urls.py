from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path("" , views.home_view , name = "home"),
    path("exam/" , views.exam_view , name = "exam"),
    path("track-tab-change/" , views.track_tab_change , name="tab-change"),
    path("voice-record/" , views.voice_record , name = "voice-record"),
    path('upload_voice/', views.upload_voice, name='upload-voice'),

]