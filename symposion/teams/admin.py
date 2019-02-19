from django.contrib import admin

from symposion.teams.models import Team, Membership

admin.site.register(Team,
                    prepopulated_fields={"slug": ("name",)})


class MembershipAdmin(admin.ModelAdmin):
    list_display = ["team", "user", "state"]
    list_filter = ["team"]
    search_fields = ["user__username"]

admin.site.register(Membership, MembershipAdmin)
