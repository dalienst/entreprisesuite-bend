from django.contrib import admin

from contracts.models import Contract, ContractTemplate, Milestone, PaymentMethod

admin.site.register(Contract)
admin.site.register(ContractTemplate)
admin.site.register(Milestone)
admin.site.register(PaymentMethod)
