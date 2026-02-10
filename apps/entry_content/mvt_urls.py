from django.urls import path
from . import views

urlpatterns = [
        # ---------------------------
    # Additional Views for Frontend Rendering
    # ---------------------------
    # Blogs
    path("blogs/", views.BlogListView.as_view(), name="blog_list"),
    path("blogs/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),

    # Projects
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),

    # Technologies
    path("technologies/", views.TechnologyListView.as_view(), name="technology_list"),
    path("technologies/<slug:slug>/", views.TechnologyDetailView.as_view(), name="technology_detail"),
]