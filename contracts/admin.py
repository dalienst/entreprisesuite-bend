from django.contrib import admin

from contracts.models import PaymentMethod, Contract

admin.site.register(PaymentMethod)
admin.site.register(Contract)
