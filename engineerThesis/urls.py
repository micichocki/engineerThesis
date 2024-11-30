"""
URL configuration for engineerThesis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from engineerThesis import settings
from engineerThesis.views import RegisterView, TokenVerifyView, AuthorizeGoogleCalendarView, GoogleCalendarCallbackView, \
    CreateGoogleMeetView

schema_view = get_schema_view(
    openapi.Info(
        title="App API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tutoring/lessons/authorize-google-calendar/', AuthorizeGoogleCalendarView.as_view(), name='authorize_google_calendar'),
    path('api/tutoring/lessons/create_google_credential/', GoogleCalendarCallbackView.as_view(), name='create_google_credentials'),
    path('api/tutoring/lessons/<int:lesson_id>/create-google-meet/', CreateGoogleMeetView.as_view(),
         name='create_google_meet'),
    path('api/tutoring/', include('tutoring.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

