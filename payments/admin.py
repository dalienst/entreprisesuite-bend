from django.contrib import admin

from payments.models import PaymentMethod


admin.site.register(PaymentMethod)
