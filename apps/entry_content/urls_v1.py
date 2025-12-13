from django.urls import path
from .views import (
    EntryContentListView,
    EntryContentDetailView,
    ContentBlockListAllView,
    ContentBlockListByEntryContentIdView,
    ContentBlockListView,
    ContentBlockDetailView,
    TechnologyListAllView,
    TechnologyListView,
    TechnologyDetailView
)

urlpatterns = [
    # Entry content
    path('entry-content/', EntryContentListView.as_view(), name='entry-content-list'),
    path('entry-content/<uuid:id>/', EntryContentDetailView.as_view(), name='entry-content-detail'),

    # Content Blocks
    path('content-blocks/all/', ContentBlockListAllView().as_view(), name='contentblock-all-list'),
    path('content-blocks/entry-content/<uuid:entry_content_id>/all/', ContentBlockListByEntryContentIdView().as_view(), name='contentblock-byarticle'),
    path('content-blocks/entry-content/<uuid:entry_content_id>/', ContentBlockListView.as_view(), name='contentblock-list'),
    path('content-blocks/<uuid:id>/', ContentBlockDetailView.as_view(), name='contentblock-detail'),

    # Technologies
    path('technologies/all/', TechnologyListAllView.as_view(), name='technology-all-list'),
    path('technologies/', TechnologyListView.as_view(), name='technology-list'),
    path('technologies/<uuid:id>/', TechnologyDetailView.as_view(), name='technology-detail'),
]