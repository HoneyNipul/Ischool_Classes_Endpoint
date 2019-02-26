"""ischool_classes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

app_name = 'ischool_classes'

from django.conf.urls import include, url
from django.http import HttpResponse, HttpResponseRedirect
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from . import api_views

schema_view = get_schema_view(
   openapi.Info(
      title="iSchool Classes",
      default_version='v1',
      description="iSchool Classes API, View classes and waitlist information",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ndlyga@syr.edu"),
      license=openapi.License(name="MIT License"),
   ),
   validators=[],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/schema', schema_view.with_ui('redoc', cache_timeout=None), name='api_schema'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/classes/(?P<pk>[-\w]+)/$', api_views.ClassDetailView.as_view(), name='api_classes_detail'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/classes/$', api_views.ClassListView.as_view(), name='api_classes_list'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/terms/$', api_views.TermView.as_view(), name='api_terms_list'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/terms/schedule/current/$', api_views.CurrentTermView.as_view(), name='api_terms_current_details'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/terms/schedule/$', api_views.CurrentActiveTermsView.as_view(), name='api_terms_schedule_list'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/terms/waitlist/active/$', api_views.ActiveWaitlistsTermView.as_view(), name='api_terms_active_waitlist_terms'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/terms/(?P<termid>[0-9]+)/$', api_views.TermById.as_view(), name='api_terms_by_termId'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/waitlisted/(?P<classid>[-\w]+)/$', api_views.WaitListEnrollView.as_view(), name='api_my_waitlist_enroll'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/waitlisted/$', api_views.MyWaitListViewSet.as_view(), name='api_my_waitlist'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-classes/waitlist/(?P<termid>[0-9]+)/$', api_views.ClassWaitlistViewSet.as_view(), name='api_class_waitlist'),
    url(r'^healthcheck/$', lambda request: HttpResponse("Healthcheck Successful", status=200)),
    url(r'', lambda request: HttpResponseRedirect("/api/v1/ischool-classes/schema/", status=301)),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
