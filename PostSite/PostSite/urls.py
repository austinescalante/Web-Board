"""PostSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from boards import views
#When Django receives a request, it starts searching for a match in the project’s URLconf. 
# It starts with the first entry of the urlpatterns variable, and test the requested URL against each url entry.
#IF Django finds a match, it will pass the request to the view function, which is the second parameter of the url.
#The order in the urlpatterns matters, because Django will stop searching as soon as it finds a match. 


#The regex \d+ will match an integer of arbitrary size. This integer will be used to retrieve the Board from the database.(Use re_path for regex)
#Now observe that we wrote the regex as (?P<pk>\d+), this is telling Django to capture the value into a keyword argument named pk.

#Because we used the (?P<pk>\d+) regex, the keyword argument in the board_topics must be named pk.

#If Django finds a match, it will pass the request to the view function, which is the second parameter of the url
urlpatterns = [
    path('', views.home,name='home'),
    re_path(r'^boards/(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
    path('admin/', admin.site.urls),
]
