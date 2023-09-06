from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Review, ReviewCategory, ReviewMedia, ReviewReport, ReviewReportReason, ReviewTag, Tag

admin.site.register(Review)
admin.site.register(ReviewTag)
admin.site.register(ReviewMedia)
admin.site.register(ReviewReport)
admin.site.register(ReviewReportReason)
admin.site.register(ReviewCategory)
admin.site.register(Tag)
