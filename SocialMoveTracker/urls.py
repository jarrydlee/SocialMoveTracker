from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'system.views.home', name='home'),
    url(r'^test$', 'system.views.test', name='test'),
    url(r'^search$', 'system.views.search', name='search'),
    url(r'^api/get_data$', 'system.views.getData', name='getData'),
    url(r'^api/get_arrows$', 'system.views.getMovieArrow', name='getMovieArrow'),
    url(r'^api/get_titles$', 'system.views.getMovieTitles', name='getMovieTitles'),


    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
