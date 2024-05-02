from django.contrib import admin

from modules.authentication.models import User, Tenant, BusinessActivity


# Register your models here.
class vis_user(admin.ModelAdmin):
    search_fields = ['user_type']
    filter_horizontal = ("groups", "user_permissions")
    list_display = ('email', 'last_name', 'identification_card', 'phone')

    # list_filter = ['user_type']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        # is_staff = request.user.is_staff
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                # 'username',
                'is_superuser',
                'user_permissions',
            }

        #     # Prevent non-superusers from editing their own permissions
        if (
                not is_superuser
                and obj is not None
                and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(User, vis_user)
admin.site.register(Tenant)
admin.site.register(BusinessActivity)
