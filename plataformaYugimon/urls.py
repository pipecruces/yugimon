from django.urls import path
from plataformaYugimon.views import SignUpView, EditarCuentaView, PasswordsChangeView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('signup/', SignUpView, name="signup"),
    path('editarPerfil/', login_required(EditarCuentaView.as_view()), name="editarPerfil"),
    path('password/', login_required(PasswordsChangeView.as_view(template_name='registration/change-password.html')), name='changePasswd'),
    
]
