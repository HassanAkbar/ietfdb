import datetime

from django.db import models

from ietf.doc.models import Document
from ietf.group.models import Group
from ietf.person.models import Person, Email
from ietf.name.models import ReviewTypeName, ReviewRequestStateName, ReviewResultName
from ietf.utils.validators import validate_regular_expression_string

class ReviewerSettings(models.Model):
    """Keeps track of admin data associated with a reviewer in a team."""
    team        = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    person      = models.ForeignKey(Person)
    INTERVALS = [
        (7, "Once per week"),
        (14, "Once per fortnight"),
        (30, "Once per month"),
        (61, "Once per two months"),
        (91, "Once per quarter"),
    ]
    min_interval = models.IntegerField(verbose_name="Can review at most", choices=INTERVALS, blank=True, null=True)
    filter_re   = models.CharField(max_length=255, verbose_name="Filter regexp", blank=True,
        validators=[validate_regular_expression_string, ],
        help_text="Draft names matching this regular expression should not be assigned")
    skip_next   = models.IntegerField(default=0, verbose_name="Skip next assignments")
    remind_days_before_deadline = models.IntegerField(null=True, blank=True, help_text="To get an email reminder in case you forget to do an assigned review, enter the number of days before review deadline you want to receive it. Clear the field if you don't want a reminder.")

    def __unicode__(self):
        return u"{} in {}".format(self.person, self.team)

    class Meta:
        verbose_name_plural = "reviewer settings"

class ReviewSecretarySettings(models.Model):
    """Keeps track of admin data associated with a secretary in a team."""
    team        = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    person      = models.ForeignKey(Person)
    remind_days_before_deadline = models.IntegerField(null=True, blank=True, help_text="To get an email reminder in case a reviewer forgets to do an assigned review, enter the number of days before review deadline you want to receive it. Clear the field if you don't want a reminder.")

    def __unicode__(self):
        return u"{} in {}".format(self.person, self.team)

    class Meta:
        verbose_name_plural = "review secretary settings"

class UnavailablePeriod(models.Model):
    team         = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    person       = models.ForeignKey(Person)
    start_date   = models.DateField(default=datetime.date.today, null=True, help_text="Choose the start date so that you can still do a review if it's assigned just before the start date - this usually means you should mark yourself unavailable for assignment some time before you are actually away.")
    end_date     = models.DateField(blank=True, null=True, help_text="Leaving the end date blank means that the period continues indefinitely. You can end it later.")
    AVAILABILITY_CHOICES = [
        ("canfinish", "Can do follow-ups"),
        ("unavailable", "Completely unavailable"),
    ]
    LONG_AVAILABILITY_CHOICES = [
        ("canfinish", "Can do follow-up reviews and finish outstanding reviews"),
        ("unavailable", "Completely unavailable - reassign any outstanding reviews"),
    ]
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES)

    def state(self):
        import datetime
        today = datetime.date.today()
        if self.start_date is None or self.start_date <= today:
            if not self.end_date or today <= self.end_date:
                return "active"
            else:
                return "past"
        else:
            return "future"

    def __unicode__(self):
        return u"{} is unavailable in {} {} - {}".format(self.person, self.team.acronym, self.start_date or "", self.end_date or "")

class ReviewWish(models.Model):
    """Reviewer wishes to review a document when it becomes available for review."""
    time        = models.DateTimeField(default=datetime.datetime.now)
    team        = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    person      = models.ForeignKey(Person)
    doc         = models.ForeignKey(Document)

    def __unicode__(self):
        return u"{} wishes to review {} in {}".format(self.person, self.doc.name, self.team.acronym)

    class Meta:
        verbose_name_plural = "review wishes"
    

class NextReviewerInTeam(models.Model):
    team        = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    next_reviewer = models.ForeignKey(Person)

    def __unicode__(self):
        return u"{} next in {}".format(self.next_reviewer, self.team)

    class Meta:
        verbose_name = "next reviewer in team setting"
        verbose_name_plural = "next reviewer in team settings"

class ReviewRequest(models.Model):
    """Represents a request for a review and the process it goes through.
    There should be one ReviewRequest entered for each combination of
    document, rev, and reviewer."""
    state         = models.ForeignKey(ReviewRequestStateName)

    old_id        = models.IntegerField(blank=True, null=True, help_text="ID in previous review system") # FIXME: remove this when everything has been migrated

    # Fields filled in on the initial record creation - these
    # constitute the request part.
    time          = models.DateTimeField(default=datetime.datetime.now)
    type          = models.ForeignKey(ReviewTypeName)
    doc           = models.ForeignKey(Document, related_name='reviewrequest_set')
    team          = models.ForeignKey(Group, limit_choices_to=~models.Q(reviewteamsettings=None))
    deadline      = models.DateField()
    requested_by  = models.ForeignKey(Person)
    requested_rev = models.CharField(verbose_name="requested revision", max_length=16, blank=True, help_text="Fill in if a specific revision is to be reviewed, e.g. 02")
    comment       = models.CharField(verbose_name="Requester's comments and instructions", max_length=2048, blank=True, help_text="Provide any additional information to show to the review team secretary and reviewer", default='')

    # Fields filled in as reviewer is assigned and as the review is
    # uploaded. Once these are filled in and we progress beyond being
    # requested/assigned, any changes to the assignment happens by
    # closing down the current request and making a new one, copying
    # the request-part fields above.
    reviewer      = models.ForeignKey(Email, blank=True, null=True)

    review        = models.OneToOneField(Document, blank=True, null=True)
    reviewed_rev  = models.CharField(verbose_name="reviewed revision", max_length=16, blank=True)
    result        = models.ForeignKey(ReviewResultName, blank=True, null=True)

    def __unicode__(self):
        return u"%s review on %s by %s %s" % (self.type, self.doc, self.team, self.state)

def get_default_review_types():
    return ReviewTypeName.objects.filter(slug__in=['early','lc','telechat'])

def get_default_review_results():
    return ReviewResultName.objects.filter(slug__in=['not-ready', 'right-track', 'almost-ready', 'ready-issues', 'ready-nits', 'ready'])

class ReviewTeamSettings(models.Model):
    """Holds configuration specific to groups that are review teams"""
    group = models.OneToOneField(Group)
    autosuggest = models.BooleanField(default=True, verbose_name="Automatically suggest possible review requests")
    review_types = models.ManyToManyField(ReviewTypeName, default=get_default_review_types)
    review_results = models.ManyToManyField(ReviewResultName, default=get_default_review_results)

    def __unicode__(self):
        return u"%s" % (self.group.acronym,)

    class Meta:
        verbose_name = "Review team settings"
        verbose_name_plural = "Review team settings"
