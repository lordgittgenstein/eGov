from django.conf.urls import patterns, url

urlpatterns = patterns('corect.views',
    url(r'^$', 'index'),

    url(r'^ajax_form_a1/$', 'ajax_form_a1'),
    url(r'^ajax_form_a2/$', 'ajax_form_a2'),
    url(r'^ajax_form_check/$', 'ajax_form_check'),
    url(r'^ajax_locations_under/$', 'ajax_locations_under'),
    
    url(r'^ajax_search/(?P<string>\w+)$', 'ajax_search'),
    
    url(r'^ajax_home/$', 'ajax_home'),
    url(r'^ajax_subordinates/$', 'ajax_subordinates'),
    
    url(r'^ajax_home/(?P<page>\d+)/$', 'ajax_home'),
    url(r'^ajax_subordinates/(?P<page>\d+)$', 'ajax_subordinates'),
    url(r'^ajax_recent/(?P<page>\d+)$', 'ajax_recent'),
    
    url(r'^ajax_mydeadlines/(?P<page>\d+)$', 'ajax_mydeadlines'),
    url(r'^ajax_subdeadlines/(?P<page>\d+)$', 'ajax_subdeadlines'),
    
    url(r'^ajax_openlist/$', 'ajax_openlist'),
    url(r'^ajax_openlist/(?P<page>\d+)/$', 'ajax_openlist'),

    url(r'^openlist/$', 'openlist'),
    url(r'^openlist/(?P<complaint_id>\d+)/$', 'detail_anonymous'),

    url(r'^home/$', 'home'),
    url(r'^home/(?P<page>\d+)$', 'home'),
    url(r'^home/leave/$', 'leave'),

    url(r'^home/change_password/$', 'change_password'),
    url(r'^home/change_official_contact/$', 'change_official_contact'),
    url(r'^home/change_profile/$', 'change_profile'),
    
    url(r'^home/filter/$', 'history'),
    url(r'^home/recent/$', 'recent'),
    url(r'^home/deadlines/$', 'deadlines'),

    url(r'^home/(?P<complaint_id>\d+)/$', 'detail_officer'),
    
    url(r'^home/subordinates/$', 'subordinates'),
    url(r'^home/subordinates/(?P<complaint_id>\d+)/$', 'detail_officer'),
    url(r'^home/subordinates/(?P<complaint_id>\d+)/mark/$', 'mark'),
    url(r'^home/subordinates/(?P<complaint_id>\d+)/wake_up/$', 'wake_up'),
    
    url(r'^home/\d+/leave/$', 'leave'),
    url(r'^home/\w+/leave/$', 'leave'),
    
    url(r'^check/$', 'check'),
    
    url(r'^check/change_contact/$', 'change_contact'),
    url(r'^check/change_key/$', 'change_key'),

    url(r'^check/(?P<complaint_id>\d+)/$', 'detail_anonymous'),
    
    url(r'^check/\d+/leave/$', 'leave'),
    url(r'^check/\w+/leave/$', 'leave'),
    
    url(r'^refer/$', 'refer'),
    url(r'^refer/(?P<complaint_id>\d+)/$', 'forward'),
    url(r'^refer/\d+/leave/$', 'leave'),

    url(r'^complaint/$', 'form_a'),
    url(r'^complaint/details/$', 'form_b'),
)