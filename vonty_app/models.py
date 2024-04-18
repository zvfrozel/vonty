"""
Vonty models:
1. Problem
2. Tag
"""

from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, StepValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Problem(models.Model):
    source = models.CharField(
        max_length=50,
        null=True, # avoid unique-constraint violations
        blank=True,
        unique=True,
        help_text=_(
            "Problem source. This must be either blank or unique. " # TODO
            "e.g. IMO 2023/6"
        )
    )
    author = models.CharField(
        max_length=50, blank=True, help_text=_(
            "e.g. Abel George Mathew (IND)"
        )
    )
    desc = models.CharField(
        max_length=100, help_text=_(
            "A short one-line description of the problem statement. "
            "e.g. Fiendish inequality"
        )
    )
    aops_url = models.URLField(
        blank=True, help_text=_(
            "A link to the problem on AOPS, if it exists. "
        )
    )
    hardness = models.PositiveIntegerField(
        null=True, blank=True,
        help_text=_(
            "Hardness of the problem according to the MOHS scale. "
            "The rating can range from 0 to 60, "
            "and can be left blank if the problem is considered not-rateable. "
            "See https://web.evanchen.cc/upload/MOHS-hardness.pdf "
            "for more information."
        ),
        validators=[
            MaxValueValidator(60, _("MOHS rating cannot exceed 60")),
            StepValueValidator(5, _("MOHS rating must be a multiple of 5"))
        ]
    )
    proposer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "The author, if they are a member of this database. "
            "Use this in problems you have proposed yourself, for example."
        )
    )
    proposal_date = models.DateField(
        null=True, blank=True, help_text=_("Date of problem creation.")
    )
    git_url = models.URLField(
        blank=True, help_text=_(
            "Read-only link to pull the problem via git. "
            "See LINK TO GIT PULL DOCUMENTATION."
        )
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="problem_set",
        help_text=_("The list of tags associated with the problem.")
    )

    def __str__(self):
        return self.desc


class Tag(models.Model):
    name = models.SlugField(
        help_text=_("Identifier slug. e.g. angle-chase")
    )
    desc = models.TextField(
        max_length=200, help_text=_("Optional longer description.")
    )
    use_filter = models.BooleanField(
        default=True, help_text=_(
            "Specifies whether users should use this tag to filter problems. "
            "Uncheck this for tags that are purely meant to be "
            "used as umbrella parent tags and not as filters."
        )
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT, # TODO: Change PROTECT to SET grandparent
        related_name="children",
        help_text=_(
            "The parent tag that this tag comes under. "
            "Filtering by the parent tag filters by this tag too. "
            "If this field is blank, the use filter option must be unchecked."
        )
    )

    def __str__(self):
        return self.name.replace("-", " ").replace("_", " ").title()

    def check_ancestor(self, tag):
        """
        Check whether ``tag'' is an ancestor of ``self''.
        A tag is an ancestor of itself.
        """
        if tag == self:
            return True
        if self.parent is None:
            return False
        else:
            return self.parent.check_ancestor(tag)

    def check_descendant(self, tag):
        """
        Check whether ``tag'' is a descendant of ``self''.
        A tag is a descendant of itself.
        """
        return tag.check_ancestor(self)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(use_filter=False) | Q(parent__isnull=False),
                name="filter_implies_parent",
                violation_error_message=_(
                    "Tag meant to be used as a filter "
                    "must have a parent tag."
                )
            ),
        ]
