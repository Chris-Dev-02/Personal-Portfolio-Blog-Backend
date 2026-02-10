from django.shortcuts import render
from django.views.generic import TemplateView
from apps.entry_content.models import EntryContent, Technology

# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["technologies"] = Technology.objects.all()[:6]

        context["projects"] = EntryContent.objects.filter(
            type=EntryContent.PROJECT,
            status=EntryContent.PUBLISHED
        ).select_related("author").prefetch_related("technologies")[:6]

        context["blogs"] = EntryContent.objects.filter(
            type=EntryContent.BLOG,
            status=EntryContent.PUBLISHED
        ).select_related("author").prefetch_related("technologies")[:6]

        return context