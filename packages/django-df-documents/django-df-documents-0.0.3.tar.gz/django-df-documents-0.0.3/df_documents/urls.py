from django.urls import path

from df_documents.views import retrieve_document_view

urlpatterns = [
    path("<slug>/", retrieve_document_view, name="retrieve_document"),
]
