from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Problem, Tag


class TagAdmin(TreeAdmin):
    form = movenodeform_factory(Tag)


admin.site.register(Problem)
admin.site.register(Tag, TagAdmin)
