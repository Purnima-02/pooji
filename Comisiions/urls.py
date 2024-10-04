from django.urls import path,include
from .views import *


urlpatterns = [

    path('claim',disbursementRecords,name='is-claim'),
    path('postToAcnt',postToAccounts,name='postAcnt'),
    path('viewcomison',viewComissions,name='view-comisons'),
    path('payouts',payOuts,name='payouts'),
    path('commonComissions',commonComissions,name='commonComissions'),
]