from django.shortcuts import render
from .agente_ia import ejecutar_agente_ia_inteligente

def resumen_agente_ia(request):
    creadas, aprobadas = ejecutar_agente_ia_inteligente()
    datos = {
        "creadas": creadas,
        "aprobadas": aprobadas
    }
    return render(request, "admin/resumen_agente_ia.html", {"datos": datos})
