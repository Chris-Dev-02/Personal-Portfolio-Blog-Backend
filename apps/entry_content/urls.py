from django.urls import path, include

app_name = "entry_content"

urlpatterns = [
    path('v1/', include('apps.entry_content.api_urls_v1')),
    path('', include('apps.entry_content.mvt_urls')),
]