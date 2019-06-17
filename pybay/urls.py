from django.conf import settings
from django.conf.urls import include, url
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
    url(r"^$", views.FrontpageView.as_view(faq_filter="show_on_home"), name="home"),
    # url(r"^cfp$", views.pybay_cfp_create, name="pybay_cfp"),
    # url(r'^call-for-proposals/$', RedirectView.as_view(pattern_name='pybay_cfp', permanent=False)),
    url(r"^sponsors-prospectus/$", faq_view(template_name="frontend/sponsors_prospectus.html", faq_filter="show_on_sponsors"), name="pybay_sponsors"),
    url(r'^sponsors/$', RedirectView.as_view(pattern_name='pybay_sponsors', permanent=False)),
    url(r"^code-of-conduct$", TemplateView.as_view(template_name="frontend/code_of_conduct.html"), name="pybay_coc"),
    url(r"^coc-reporting$", TemplateView.as_view(template_name="frontend/coc_reporting.html"), name="pybay_coc_reporting"),
    url(r"^registration$", RedirectView.as_view(url='https://ti.to/sf-python/pybay2019')),
    url(r"^faq$", views.pybay_faq_index, name="pybay_faq"),

    url(r"^admin/", include(admin.site.urls)),
    url(r"^admin/blockstuff/docs", TemplateView.as_view(template_name="blockstuff/docs.html")),
    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),

    url(r"^account/", include("account.urls")),
    url(r"^speaker/", include(speaker_urls)),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^proposals/", include(proposals_urls)),
    url(r"^talks/", preview_views.index, name="pybay_preview"),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^boxes/", include("pinax.boxes.urls")),

    url(r"^schedule/", views.pybay_schedule, name='pybay_schedule'),
    url(r"^schedule-sym/", include("symposion.schedule.urls")),
    # url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    # url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
    # url(r"^teams/", include(teams_urls)),
    # url(r"^teams/", include("symposion.teams.urls")),
    # url(r"^markitup/", include("markitup.urls")),
    url(r"^our-sponsors/$", views.pybay_sponsors_list, name="pybay_sponsors_list"),
    url(r"^our-speakers/$", views.pybay_speakers_list, name="pybay_speakers_list"),
    url(r"^speaker/(?P<speaker_slug>[-\w]+)/$", views.pybay_speakers_detail, name="pybay_speakers_detail"),
    url(r"^api/undecided_proposals$", views.undecided_proposals, name="pybay_undecided_proposals"),
    url(r"^api/proposals/(?P<proposal_id>\d+)/$", views.proposal_detail, name="pybay_detail_proposal"),
    url(r"^404$", TemplateView.as_view(template_name="404.html")),  # Adding explicitly for template dev purposes
    url(r"^jobs/", include("jobs.urls")),
    # url(r"^", include("symposion.cms.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
