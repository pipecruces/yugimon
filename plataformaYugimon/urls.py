from django.urls import path
from plataformaYugimon.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView, name="signup")
]
