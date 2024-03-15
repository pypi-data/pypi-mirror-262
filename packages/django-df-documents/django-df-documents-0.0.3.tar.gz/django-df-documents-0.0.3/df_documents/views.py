from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from df_documents.models import Document


def retrieve_document_view(request: HttpRequest, slug: str) -> HttpResponse:
    document = get_object_or_404(Document, slug=slug)
    return HttpResponse(document.render_to_html())
