from django.shortcuts import render

def show_dashboard_pelatih(request):
  
  return render(request, "dashboard_pelatih.html", context)