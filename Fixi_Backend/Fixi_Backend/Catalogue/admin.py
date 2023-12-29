from django.contrib import admin
from .models import Service,Taxonomy,ServiceTaxonomy,FixiService
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


admin.site.register(Service)
admin.site.register(ServiceTaxonomy)
admin.site.register(FixiService)

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Taxonomy)


admin.site.register(Taxonomy, MyAdmin)
