import django_filters
from .models import EntryContent


class EntryContentFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    from_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    to_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    type = django_filters.ChoiceFilter(choices=EntryContent.ENTRY_CONTENT_TYPES)
    status = django_filters.ChoiceFilter(choices=EntryContent.STATUS_CHOICES)
    parent_article = django_filters.UUIDFilter(field_name="parent_article__id")
    technologies = django_filters.UUIDFilter(field_name="technologies__id", lookup_expr='exact')

    class Meta:
        model = EntryContent
        fields = [
            'title_contains',
            'type',
            'status',
            'from_date',
            'to_date',
            'parent_article',
            'technologies',
        ]