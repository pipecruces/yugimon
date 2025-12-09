from plataformaYugimon.models import Notificacion

def notificaciones_context(request):
    if request.user.is_authenticated:
        return {
            "notificaciones_no_leidas": Notificacion.objects.filter(
                receptor=request.user, leida=False
            ).count(),
            "notificaciones_lista": Notificacion.objects.filter(
                receptor=request.user
            ).order_by("-fecha")[:5]
        }
    return {
        "notificaciones_no_leidas": 0,
        "notificaciones_lista": []
    }
