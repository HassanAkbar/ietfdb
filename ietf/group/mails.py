# generation of mails 

import datetime
import re


from django.utils.html import strip_tags
from django.utils.text import wrap
from django.conf import settings
from django.core.urlresolvers import reverse as urlreverse

from ietf.utils.mail import send_mail, send_mail_text
from ietf.group.models import Group
from ietf.group.utils import milestone_reviewer_for_group_type
from ietf.mailtoken.utils import gather_address_list

def email_admin_re_charter(request, group, subject, text, mailtoken):
    to = gather_address_list(mailtoken,group=group)
    full_subject = u"Regarding %s %s: %s" % (group.type.name, group.acronym, subject)
    text = strip_tags(text)

    send_mail(request, to, None, full_subject,
              "group/email_iesg_secretary_re_charter.txt",
              dict(text=text,
                   group=group,
                   group_url=settings.IDTRACKER_BASE_URL + group.about_url(),
                   charter_url=settings.IDTRACKER_BASE_URL + urlreverse('doc_view', kwargs=dict(name=group.charter.name)) if group.charter else "[no charter]",
                   )
              )

def email_personnel_change(request, group, text, changed_personnel):
    to = gather_address_list('group_personnel_change',group=group,changed_personnel=changed_personnel)
    full_subject = u"Personnel change for %s working group" % (group.acronym)
    send_mail_text(request, to, None, full_subject,text)


def email_milestones_changed(request, group, changes):
    def wrap_up_email(to, text):

        subject = u"Milestones changed for %s %s" % (group.acronym, group.type.name)
        if re.search("Added .* for review, due",text):
            subject = u"Review Required - " + subject

        text = wrap(strip_tags(text), 70)
        text += "\n\n"
        text += u"URL: %s" % (settings.IDTRACKER_BASE_URL + group.about_url())

        send_mail_text(request, to, None, subject, text)

    # first send to those who should see any edits (such as management and chairs)
    to = gather_address_list('group_milestones_edited',group=group)
    if to:
        wrap_up_email(to, u"\n\n".join(c + "." for c in changes))

    # then send only the approved milestones to those who shouldn't be 
    # bothered with milestones pending approval 
    review_re = re.compile("Added .* for review, due")
    to = gather_address_list('group_approved_milestones_edited',group=group)
    msg = u"\n\n".join(c + "." for c in changes if not review_re.match(c))
    if to and msg:
        wrap_up_email(to, msg)


def email_milestone_review_reminder(group, grace_period=7):
    """Email reminders about milestones needing review to management."""
    to = gather_address_list('milestone_review_reminder',group=group)
    cc = gather_address_list('milestone_review_reminder_cc',group=group)

    if not to:
        return False

    now = datetime.datetime.now()
    too_early = True

    milestones = group.groupmilestone_set.filter(state="review")
    for m in milestones:
        e = m.milestonegroupevent_set.filter(type="changed_milestone").order_by("-time")[:1]
        m.days_ready = (now - e[0].time).days if e else None

        if m.days_ready == None or m.days_ready >= grace_period:
            too_early = False

    if too_early:
        return False

    subject = u"Reminder: Milestone%s needing review in %s %s" % ("s" if len(milestones) > 1 else "", group.acronym, group.type.name)

    send_mail(None, to, None,
              subject,
              "group/reminder_milestones_need_review.txt",
              dict(group=group,
                   milestones=milestones,
                   reviewer=milestone_reviewer_for_group_type(group.type_id),
                   url=settings.IDTRACKER_BASE_URL + urlreverse("group_edit_milestones", kwargs=dict(group_type=group.type_id, acronym=group.acronym)),
                   cc=cc,
               )
             )

    return True

def groups_with_milestones_needing_review():
    return Group.objects.filter(groupmilestone__state="review").distinct()

def email_milestones_due(group, early_warning_days):
    to = gather_address_list('milestones_due_soon',group=group)

    today = datetime.date.today()
    early_warning = today + datetime.timedelta(days=early_warning_days)

    milestones = group.groupmilestone_set.filter(due__in=[today, early_warning],
                                                 resolved="", state="active")

    subject = u"Reminder: Milestone%s are soon due in %s %s" % ("s" if len(milestones) > 1 else "", group.acronym, group.type.name)

    send_mail(None, to, None,
              subject,
              "group/reminder_milestones_due.txt",
              dict(group=group,
                   milestones=milestones,
                   today=today,
                   early_warning_days=early_warning_days,
                   url=settings.IDTRACKER_BASE_URL + group.about_url(),
                   ))

def groups_needing_milestones_due_reminder(early_warning_days):
    """Return groups having milestones that are either
    early_warning_days from being due or are due today."""
    today = datetime.date.today()
    return Group.objects.filter(state="active", groupmilestone__due__in=[today, today + datetime.timedelta(days=early_warning_days)], groupmilestone__resolved="", groupmilestone__state="active").distinct()

def email_milestones_overdue(group):
    to = gather_address_list('milestones_overdue',group=group)

    today = datetime.date.today()

    milestones = group.groupmilestone_set.filter(due__lt=today, resolved="", state="active")
    for m in milestones:
        m.months_overdue = (today - m.due).days // 30

    subject = u"Reminder: Milestone%s overdue in %s %s" % ("s" if len(milestones) > 1 else "", group.acronym, group.type.name)

    send_mail(None, to, None,
              subject,
              "group/reminder_milestones_overdue.txt",
              dict(group=group,
                   milestones=milestones,
                   url=settings.IDTRACKER_BASE_URL + group.about_url(),
                   ))

def groups_needing_milestones_overdue_reminder(grace_period=30):
    cut_off = datetime.date.today() - datetime.timedelta(days=grace_period)
    return Group.objects.filter(state="active", groupmilestone__due__lt=cut_off, groupmilestone__resolved="", groupmilestone__state="active").distinct()

