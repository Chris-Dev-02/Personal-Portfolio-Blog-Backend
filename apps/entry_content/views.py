from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EntryContent, ContentBlock, Technology
from .serializers import EntryContentSerializer, EntryContentDetailSerializer, ContentBlockSerializer, TechnologySerializer
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


class ContentBlockListByEntryContentIdView(APIView):
    """
    Returns an unpaginated list of content blocks for a specific entry content (identified by UUID).
    Useful for displaying all blocks in their correct order.
    """

    def get(self, request, entry_content_id):
        if not entry_content_id:
            return Response({'detail': 'The "Entry Content" parameter is required.'}, status=400)

        blocks = ContentBlock.objects.filter(entry_content__id=entry_content_id).order_by('order')
        serializer = ContentBlockSerializer(blocks, many=True)
        return Response(serializer.data)


class ContentBlockListView(generics.ListAPIView):
    """
    Paginated list view for content blocks, optionally filtered by article ID.
    Designed for standard frontend consumption.
    """
    serializer_class = ContentBlockSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        entry_content_id = self.kwargs.get('entry_content_id')
        if entry_content_id:
            return ContentBlock.objects.filter(entry_content__id=entry_content_id).order_by('order')
        return ContentBlock.objects.none()


class ContentBlockDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information for a specific content block by ID.
    """
    queryset = ContentBlock.objects.all()
    serializer_class = ContentBlockSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

# ---------------------------
# Technology Views
# ---------------------------

class TechnologyListAllView(APIView):
    """
    Returns an unpaginated list of all technologies (up to 500), including their owners.
    Typically used for dropdowns or admin panels.
    """

    def get(self, request):
        queryset = Technology.objects.all().select_related('user_owner')[:500]
        serializer = TechnologySerializer(queryset, many=True)
        return Response(serializer.data)