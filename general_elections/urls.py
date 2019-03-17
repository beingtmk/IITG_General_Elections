from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# VOTER URLS
	url(r'^login/$', views.voter_login, name='login'),
	url('^voting_start/$', (views.VoteWizard.as_view()), name='voting_start'),
	url(r'^logout/$', views.voter_logout, name='logout'),
	# ADMIN URLS
	url(r'^admin_login/$', views.admin_login_new, name='admin_login'),
	url(r'^admin_personal_login/$', views.admin_personal_login, name='admin_personal_login'),
	url(r'^admin_panel/$', views.admin_panel, name='admin_panel'),
	url(r'^create_volunteer/$', views.create_volunteer, name='create_volunteer'),
	url(r'^view_volunteers/$', views.view_volunteers, name='view_volunteers'),
	url(r'^add_contestant/$', views.add_contestant, name='add_contestant'),
	url(r'^view_contestants/$', views.view_contestants, name='view_contestant'),
	url(r'^delete_contestant/$', views.delete_contestant, name='delete_contestant'),
	url(r'^voter_list/$', views.voter_list, name='voter_list'),
	url(r'^voting_stats/$', views.voting_stats, name='voting_stats'),
	url(r'^ajax/show_voter/(?P<webmail_id>\w+[.]?\w+)/$', views.save_voter, name='show_voter'),
	url(r'^save_voter/$', views.save_voter, name='save_voter'),
	url(r'^delete_voter/(?P<webmail_id>\w+[.]?\w+)/$', views.delete_voter, name='delete_voter'),
	url(r'^add_voter/$', views.add_voter, name='add_voter'),
	url(r'^admin_logout/$', views.admin_logout, name='admin_logout'),
	url(r'^results/$', views.results_login, name='results'),
	url(r'^results_logout/$', views.results_logout, name='results_logout'),
	url(r'^bulk_upload/$', views.bulk_upload, name='bulk_upload'),
	# VOLUNTEER URLS
	url(r'^volunteer_login/$', views.volunteer_login_new, name='volunteer_login'),
	url(r'^volunteer_panel/$', views.volunteer_panel, name='volunteer_panel'),
	url(r'^volunteer_logout/$', views.volunteer_logout, name='volunteer_logout'),
]
