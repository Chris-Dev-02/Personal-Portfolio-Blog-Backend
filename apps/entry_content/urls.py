from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.entry_content.urls_v1')),
]