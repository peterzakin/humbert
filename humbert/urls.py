from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from views import * 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'humbert.views.home', name='home'),
    # url(r'^humbert/', include('humbert.foo.urls')),
      url(r'^$', home),
      url(r'^create/?$', create_annotation),
      url(r'^logout/?$', logout_view),
#      url(r'^post/(?P<post_id>(\d)+)/?', post_page),
      url(r'^ajax/create_annotation/?$', create_annotation),
      url(r'^ajax/save_annotation/?$', save_annotation),
      url(r'^ajax/fb_login/?$', fb_login_with_token_and_id),

      url(r'^(?P<username>(\w)+)/?$', render_profile),
      url(r'^(?P<username>(\w)+)/(?P<text_id>(\w)+)/?$', render_annotation),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
