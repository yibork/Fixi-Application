from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Discount, PromoCode, UserPromoCode

admin.site.register(Discount)
admin.site.register(PromoCode)
admin.site.register(UserPromoCode)