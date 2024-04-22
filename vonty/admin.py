"""Vonty administration."""

from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Problem, Tag


class TagForm(movenodeform_factory(Tag)):
    children_names = forms.CharField(
        required=False,
        help_text=_(
            "A list of child tags to add to the tag, "
            "in the form of space/comma/newline separated names. "
            "The children will be added with blank descriptions."
        ),
        widget=forms.Textarea
    )
    children_use_filter = forms.BooleanField(
        required=False, initial=True, help_text=_(
            "Whether the children should be used as filters or not."
        )
    )

    def save(self, **kwargs):
        super().save(**kwargs)
        # Create children and save the children too
        names = self.cleaned_data["children_names"]
        use_filter = self.cleaned_data["children_use_filter"]
        self.instance.add_children(names, use_filter)
        return self.instance


class TagAdmin(TreeAdmin):
    form = TagForm
    actions = ["use_filter", "disable_use_filter"]

    @admin.action(description="Use selected tags as filters")
    def use_filter(self, request, queryset):
        queryset.update(use_filter=True)
        self.message_user(
            request,
            _("Succefully enabled the selected tags as filters."),
            messages.SUCCESS,
        )

    @admin.action(description="Disable use of selected tags as filters")
    def disable_use_filter(self, request, queryset):
        queryset.update(use_filter=False)
        self.message_user(
            request,
            _("Succefully disabled the selected tags as filters."),
            messages.SUCCESS,
        )


admin.site.register(Problem)
admin.site.register(Tag, TagAdmin)
