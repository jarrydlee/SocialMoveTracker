from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'system.views.home', name='test'),
    url(r'^search$', 'system.views.search', name='search'),
    url(r'^get_data$', 'system.views.getData', name='getData'),

    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
