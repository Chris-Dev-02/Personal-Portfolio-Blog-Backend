from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import EntryContent
from .serializers import EntryContentSerializer
from .filters import EntryContentFilter

# Create your views here.
class EntryContentListView(generics.ListAPIView):
    """
    Returns a paginated list of entry contents.
    Supports filtering and ordering using DjangoFilterBackend and DRF OrderingFilter.
    """
    queryset = EntryContent.objects.all().select_related('author', 'parent_article').prefetch_related('technologies')
    serializer_class = EntryContentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EntryContentFilter
    ordering_fields = ['title', 'created_at']
    ordering = ['title', '-created_at']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)