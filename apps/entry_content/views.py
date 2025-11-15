from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EntryContent, ContentBlock
from .serializers import EntryContentSerializer, EntryContentDetailSerializer, ContentBlockSerializer
from .filters import EntryContentFilter

# Create your views here.
# ---------------------------
# Article Views
# ---------------------------
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


class EntryContentDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information about a single EntryContent, including related content blocks and technologies.
    """
    queryset = EntryContent.objects.all().prefetch_related('content_blocks', 'technologies')
    serializer_class = EntryContentDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

# ---------------------------
# Content Block Views
# ---------------------------
class ContentBlockListAllView(APIView):
    """
    Returns an unpaginated list of all content blocks (limited to 500).
    This is useful for internal tools or cases where you need the full dataset.
    """

    def get(self, request):
        queryset = ContentBlock.objects.all().order_by('order')[:500]
        serializer = ContentBlockSerializer(queryset, many=True)
        return Response(serializer.data)