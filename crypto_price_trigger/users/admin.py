from django.contrib import admin

from crypto_price_trigger.users.models import Users


def get_fields_model(model):
    fields = [field.name for field in model._meta.get_fields() if
              field.many_to_many != True and field.one_to_many != True]
    return fields


class UsersAdmin(admin.ModelAdmin):
    list_display = get_fields_model(Users)


admin.site.register(Users, UsersAdmin)
