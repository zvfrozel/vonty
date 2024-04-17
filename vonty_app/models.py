from django.db import models
from django.core.validators import MaxValueValidator, StepValueValidator
from django.contrib.auth import get_user_model


class Problem(models.Model):
    source = models.CharField(
        max_length=50,
        null=True, # avoid unique-constraint violations
        blank=True,
        unique=True,
        help_text=(
            "Problem source. This must be either blank or unique."
            "e.g. IMO 2023/6"
        )
    )
    author = models.CharField(
        max_length=50, blank=True, help_text=(
            "e.g. Abel George Mathew (IND)"
        )
    )
    desc = models.CharField(
        max_length=100, help_text=(
            "A short one-line description of the problem statement."
            "e.g. Fiendish inequality"
        )
    )
    aops_url = models.URLField(
        blank=True, help_text=(
            "A link to the problem on AOPS, if it exists."
        )
    )
    hardness = models.PositiveIntegerField(
        null=True, blank=True,
        help_text=(
            "Hardness of the problem according to the MOHS scale."
            "The rating can range from 0 to 60,"
            "and can be left blank if the problem is considered not-rateable."
            "See https://web.evanchen.cc/upload/MOHS-hardness.pdf"
            "for more information."
        ),
        validators=[
            MaxValueValidator(60, "MOHS rating cannot exceed 60"),
            StepValueValidator(5, "MOHS rating must be a multiple of 5")
        ]
    )
    proposer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=(
            "The author, if they are a member of this database."
            "Use this in problems you have proposed yourself, for example."
        )
    )
    proposal_date = models.DateField(
        null=True, blank=True, help_text=(
            "Date of problem creation."
        )
    )
    git_url = models.URLField(
        blank=True, help_text=(
            "Read-only link to pull the problem via git."
            "See LINK TO GIT PULL DOCUMENTATION."
        )
    )
    tags = models.ManyToManyField(
        "Tag", help_text="The list of tags associated with the problem."
    )


class Tag(models.Model):
    name = models.SlugField(
        help_text="Identifier slug. e.g. anglechase."
    )
    desc = models.CharField(
        max_length=200, help_text=(
            "Optional longer description."
        )
    )
    is_filter = models.BooleanField(
        default=True, help_text=(
            "Specifies whether users should use this tag to filter problems."
            "Uncheck this for tags that are purely meant to be."
            "used as umbrella parent tags and not as filters."
        )
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        on_delete=models.PROTECT, # TODO: Change PROTECT to SET grandparent
        related_name="children",
        help_text=(
            "The parent tag that this tag comes under."
            "Filtering by the parent tag filters by this tag too."
            "If this field is blank, the is_filter option must be unchecked."
        )
    )
