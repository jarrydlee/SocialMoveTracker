from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'system.views.home', name='home'),
    url(r'^test$', 'system.views.test', name='test'),
    url(r'^search$', 'system.views.search', name='search'),
    url(r'^api/get_data$', 'system.views.getData', name='getData'),
    url(r'^api/get_sidebar$', 'system.views.getSidebar', name='getSidebar'),
    url(r'^api/get_linechartdata$', 'system.views.getLineChartData', name='getLineChartData'),
    url(r'^api/get_posts$', 'system.views.getPosts', name='getPosts'),
    url(r'^api/get_doughnutdata$', 'system.views.getDoughnutData', name='getDoughtnutData'),

    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
