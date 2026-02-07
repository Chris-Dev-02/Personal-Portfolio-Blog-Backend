from django.urls import path
# from .views import (
#     EntryContentListView,
#     EntryContentDetailView,
#     ContentBlockListAllView,
#     ContentBlockListByEntryContentIdView,
#     ContentBlockListView,
#     ContentBlockDetailView,
#     TechnologyListAllView,
#     TechnologyListView,
#     TechnologyDetailView
# )
from . import views

urlpatterns = [
    # ---------------------------
    # API Views
    # ---------------------------
    # Entry content
    path('entry-content/', views.EntryContentListView.as_view(), name='entry-content-list'),
    path('entry-content/<uuid:id>/', views.EntryContentDetailView.as_view(), name='entry-content-detail'),

    # Content Blocks
    path('content-blocks/all/', views.ContentBlockListAllView().as_view(), name='contentblock-all-list'),
    path('content-blocks/entry-content/<uuid:entry_content_id>/all/', views.ContentBlockListByEntryContentIdView().as_view(), name='contentblock-byarticle'),
    path('content-blocks/entry-content/<uuid:entry_content_id>/', views.ContentBlockListView.as_view(), name='contentblock-list'),
    path('content-blocks/<uuid:id>/', views.ContentBlockDetailView.as_view(), name='contentblock-detail'),

    # Technologies
    path('technologies/all/', views.TechnologyListAllView.as_view(), name='technology-all-list'),
    path('technologies/', views.TechnologyListView.as_view(), name='technology-list'),
    path('technologies/<slug:slug>/', views.TechnologyDetailView.as_view(), name='technology-detail'),
]