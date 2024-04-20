"""
Vonty models:
1. Problem
2. Tag
"""

from django.core.validators import MaxValueValidator, StepValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from treebeard.mp_tree import MP_Node


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
    problem_number = models.PositiveIntegerField(
        null=True, blank=True, help_text=_(
            "Problem number of this problem "
            "in the contest/problem-set that it appeared in. "
            "Leave this blank for standalone problems, "
            "but it's always useful to keep a number for ordering problems."
        )
    )
    hardness = models.PositiveIntegerField(
        null=True, blank=True, help_text=_(
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


class Tag(MP_Node):
    name = models.SlugField(
        unique=True,
        help_text=_("Unique dentifier slug. e.g. angle-chase")
    )
    desc = models.TextField(
        max_length=200,
        blank=True,
        help_text=_("Optional longer description.")
    )
    use_filter = models.BooleanField(
        default=True, help_text=_(
            "Specifies whether users should use this tag to filter problems. "
            "Uncheck this for tags that are purely meant to be "
            "used as umbrella parent tags and not as filters."
        )
    )

    #  Tree structure implementation using MP_Node from django-treebeard
    node_order_by = ["name",]

    def __str__(self):
        return self.name.replace("-", " ").replace("_", " ").title()
