from django.conf import settings
from django.conf.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from django.contrib import admin

import symposion.views
from symposion.teams import urls as teams_urls
from symposion.proposals import urls as proposals_urls
from symposion.sponsorship import urls as sponsor_urls
from symposion.speakers import urls as speaker_urls

from pybay import views
from pybay.proposals import views as preview_views


WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"


faq_view = views.FaqTemplateView.as_view


urlpatterns = [
    path('', views.FrontpageView.as_view(faq_filter="show_on_home"), name="home"),
    # path('cfp', views.pybay_cfp_create, name="pybay_cfp"),
    # path('call-for-proposals/', RedirectView.as_view(pattern_name='pybay_cfp', permanent=False)),
    path('sponsors-prospectus/', faq_view(template_name="frontend/sponsors_prospectus.html", faq_filter="show_on_sponsors"), name="pybay_sponsors"),
    path('sponsors/', RedirectView.as_view(pattern_name='pybay_sponsors', permanent=False)),
    path('code-of-conduct', TemplateView.as_view(template_name="frontend/code_of_conduct.html"), name="pybay_coc"),
    path('coc-reporting', TemplateView.as_view(template_name="frontend/coc_reporting.html"), name="pybay_coc_reporting"),
    path('registration', RedirectView.as_view(url='https://ti.to/sf-python/pybay2019')),
    path('faq', views.pybay_faq_index, name="pybay_faq"),

    path('admin/', include(admin.site.urls)),
    path('admin/blockstuff/docs', TemplateView.as_view(template_name="blockstuff/docs.html")),
    path('dashboard/', symposion.views.dashboard, name="dashboard"),

    path('account/', include("account.urls")),
    #path('speaker/', include(speaker_urls)),
    path('sponsors/', include("symposion.sponsorship.urls")),
    path('proposals/', include(proposals_urls)),
    path('talks/', preview_views.index, name="pybay_preview"),
    path('reviews/', include("symposion.reviews.urls")),
    path('boxes/', include("pinax.boxes.urls")),

    path('schedule/', views.pybay_schedule, name='pybay_schedule'),
    path('schedule-sym/', include("symposion.schedule.urls")),
    # path('account/signup/', SignupView.as_view(), name="account_signup"),
    # path('account/login/', symposion.views.LoginView.as_view(), name="account_login"),
    # path('teams/', include(teams_urls)),
    # path('teams/', include("symposion.teams.urls")),
    # path('markitup/', include("markitup.urls")),
    path('our-sponsors/', views.pybay_sponsors_list, name="pybay_sponsors_list"),
    path('our-speakers/', views.pybay_speakers_list, name="pybay_speakers_list"),
    path('speaker/<slug:speaker_slug>/', views.pybay_speakers_detail, name="pybay_speakers_detail"),
    path('api/undecided_proposals', views.undecided_proposals, name="pybay_undecided_proposals"),
    path('api/proposals/<int:proposal_id>/', views.proposal_detail, name="pybay_detail_proposal"),
    path('404', TemplateView.as_view(template_name="404.html")),  # Adding explicitly for template dev purposes
    path('jobs/', include("jobs.urls")),
    path('registration', RedirectView.as_view(url='https://ti.to/sf-python/pybay2019'), name='pybay_tickets'),
    # path('', include("symposion.cms.urls")),
   ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
