"""
OpenAPI / Swagger documentation for API v1
Using drf-spectacular
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)

from .serializers import (
    EntryContentSerializer,
    EntryContentDetailSerializer,
    ContentBlockSerializer,
    TechnologySerializer,
)

# ============================================================
# ENTRY CONTENT
# ============================================================

entry_content_list_docs = extend_schema(
    summary="List Entry Contents",
    description=(
        "Returns a paginated list of entry contents.\n\n"
        "Supports filtering by title, type, status, date range, parent entry "
        "and associated technologies.\n"
        "Supports ordering by title and created_at."
    ),
    tags=["Entry Content"],
    parameters=[
        OpenApiParameter(
            name="title_contains",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by title substring.",
        ),
        OpenApiParameter(
            name="type",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by entry content type (project, blog, comment).",
        ),
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by publication status (draft, published).",
        ),
        OpenApiParameter(
            name="from_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by creation date (ISO 8601).",
        ),
        OpenApiParameter(
            name="to_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by creation date (ISO 8601).",
        ),
        OpenApiParameter(
            name="parent_article",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by parent entry content UUID.",
        ),
        OpenApiParameter(
            name="technologies",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter by associated technology UUID.",
        ),
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Order by fields. Example: ordering=-created_at",
        ),
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Page number for paginated results.",
        ),
    ],
    responses=EntryContentSerializer(many=True),
)

entry_content_detail_docs = extend_schema(
    summary="Retrieve Entry Content Detail",
    description=(
        "Returns detailed information for a single entry content, "
        "including related content blocks and technologies."
    ),
    tags=["Entry Content"],
    responses=EntryContentDetailSerializer,
)

# ============================================================
# CONTENT BLOCKS
# ============================================================

content_block_list_all_docs = extend_schema(
    summary="List All Content Blocks",
    description=(
        "Returns an unpaginated list of content blocks ordered by the "
        "'order' field. Limited to 500 records."
    ),
    tags=["Content Blocks"],
    responses=ContentBlockSerializer(many=True),
)

content_block_list_by_entry_content_docs = extend_schema(
    summary="List Content Blocks by Entry Content",
    description=(
        "Returns all content blocks associated with a specific entry content "
        "identified by its UUID."
    ),
    tags=["Content Blocks"],
    parameters=[
        OpenApiParameter(
            name="entry_content_id",
            type=str,
            location=OpenApiParameter.PATH,
            description="UUID of the entry content.",
        )
    ],
    responses=ContentBlockSerializer(many=True),
)

content_block_list_docs = extend_schema(
    summary="Paginated List of Content Blocks",
    description=(
        "Returns a paginated list of content blocks. "
        "If entry_content_id is present in the URL, results are filtered."
    ),
    tags=["Content Blocks"],
    responses=ContentBlockSerializer(many=True),
)

content_block_detail_docs = extend_schema(
    summary="Retrieve Content Block Detail",
    description="Returns detailed information for a specific content block.",
    tags=["Content Blocks"],
    responses=ContentBlockSerializer,
)

# ============================================================
# TECHNOLOGIES
# ============================================================

technology_list_all_docs = extend_schema(
    summary="List All Technologies",
    description=(
        "Returns an unpaginated list of all technologies including their owners. "
        "Limited to 500 records."
    ),
    tags=["Technologies"],
    responses=TechnologySerializer(many=True),
)

technology_list_docs = extend_schema(
    summary="Paginated List of Technologies",
    description="Returns a paginated list of technologies ordered by name.",
    tags=["Technologies"],
    responses=TechnologySerializer(many=True),
)

technology_detail_docs = extend_schema(
    summary="Retrieve Technology Detail",
    description="Returns detailed information for a single technology by UUID.",
    tags=["Technologies"],
    responses=TechnologySerializer,
)
