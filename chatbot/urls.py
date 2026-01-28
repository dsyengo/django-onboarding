from django.urls import path, include
from .views import CSAdvisorView

urlpatterns =[
    path('chat/', CSAdvisorView.as_view(), name='cs_chat')
]