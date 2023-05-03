from django.contrib import admin

from crypto_price_trigger.alert.models import Alert


def get_fields_model(model):
    """
    The get_fields_model function takes a model as an argument and returns a list of the fields in that model.
        This is useful for getting all the fields in a given table, which can then be used to create new tables with
        only those columns.

    :param model: Get the fields from a model
    :return: A list of field names for a given model
    """
    return [field.name for field in model._meta.get_fields()]


class AlertAdmin(admin.ModelAdmin):
    list_display = get_fields_model(Alert)


admin.site.register(Alert, AlertAdmin)
