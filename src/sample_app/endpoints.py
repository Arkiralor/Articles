from tkinter import N
from django.urls import path

from sample_app.apis import SampleDataAPI, AlternateItemEditAPI

URL_REFIX = 'api/main/'

urlpatterns = [
    path('data/<int:page>/', SampleDataAPI.as_view(), name='main-api'),
    path('data/edit/', AlternateItemEditAPI.as_view(), name='alternate-put-api')
]