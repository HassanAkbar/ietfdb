import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.decorators import login_required

from ietf.doc.models import Document, NewRevisionDocEvent, DocEvent
from ietf.doc.utils import can_request_review_of_doc, can_manage_review_requests_for_team
from ietf.ietfauth.utils import is_authorized_in_doc_stream, user_is_person
from ietf.review.models import ReviewRequest, ReviewRequestStateName
from ietf.review.utils import active_review_teams
from ietf.utils.fields import DatepickerDateField

class RequestReviewForm(forms.ModelForm):
    deadline_date = DatepickerDateField(date_format="yyyy-mm-dd", picker_settings={ "autoclose": "1", "start-date": "+0d" })
    deadline_time = forms.TimeField(widget=forms.TextInput(attrs={ 'placeholder': "HH:MM" }), help_text="If time is not specified, end of day is assumed", required=False)

    class Meta:
        model = ReviewRequest
        fields = ('type', 'team', 'deadline', 'requested_rev')

    def __init__(self, user, doc, *args, **kwargs):
        super(RequestReviewForm, self).__init__(*args, **kwargs)

        self.doc = doc

        self.fields['type'].widget = forms.RadioSelect(choices=[t for t in self.fields['type'].choices if t[0]])

        f = self.fields["team"]
        f.queryset = active_review_teams()
        if not is_authorized_in_doc_stream(user, doc): # user is a reviewer
            f.queryset = f.queryset.filter(role__name="reviewer", role__person__user=user)
        if len(f.queryset) < 6:
            f.widget = forms.RadioSelect(choices=[t for t in f.choices if t[0]])

        self.fields["deadline"].required = False
        self.fields["requested_rev"].label = "Document revision"

    def clean_deadline_date(self):
        v = self.cleaned_data.get('deadline_date')
        if v < datetime.date.today():
            raise forms.ValidationError("Select a future date.")
        return v

    def clean_requested_rev(self):
        rev = self.cleaned_data.get("requested_rev")
        if rev:
            rev = rev.rjust(2, "0")

            if not NewRevisionDocEvent.objects.filter(doc=self.doc, rev=rev).exists():
                raise forms.ValidationError("Could not find revision '{}' of the document.".format(rev))

        return rev

    def clean(self):
        deadline_date = self.cleaned_data.get('deadline_date')
        deadline_time = self.cleaned_data.get('deadline_time', None)

        if deadline_date:
            if deadline_time is None:
                deadline_time = datetime.time(23, 59, 59)

            self.cleaned_data["deadline"] = datetime.datetime.combine(deadline_date, deadline_time)

        return self.cleaned_data

@login_required
def request_review(request, name):
    doc = get_object_or_404(Document, name=name)

    if not can_request_review_of_doc(request.user, doc):
        return HttpResponseForbidden("You do not have permission to perform this action")

    if request.method == "POST":
        form = RequestReviewForm(request.user, doc, request.POST)

        if form.is_valid():
            review_req = form.save(commit=False)
            review_req.doc = doc
            review_req.state = ReviewRequestStateName.objects.get(slug="requested", used=True)
            review_req.save()

            DocEvent.objects.create(
                type="requested_review",
                doc=doc,
                by=request.user.person,
                desc="Requested {} review by {}".format(review_req.type.name, review_req.team.acronym.upper()),
                time=review_req.time,
            )

            # FIXME: if I'm a reviewer, auto-assign to myself?
            return redirect('doc_view', name=doc.name)

    else:
        form = RequestReviewForm(request.user, doc)

    return render(request, 'doc/review/request_review.html', {
        'doc': doc,
        'form': form,
    })

def review_request(request, name, request_id):
    doc = get_object_or_404(Document, name=name)
    review_req = get_object_or_404(ReviewRequest, pk=request_id)

    is_reviewer = review_req.reviewer and user_is_person(request.user, review_req.reviewer.role.person)
    can_manage_req = can_manage_review_requests_for_team(request.user, review_req.team)

    can_withdraw_request = (review_req.state_id in ["requested", "accepted"]
                            and is_authorized_in_doc_stream(request.user, doc))

    can_reject_request_assignment = (review_req.state_id in ["requested", "accepted"]
                                     and review_req.reviewer_id is not None
                                     and (is_reviewer or can_manage_req))

    return render(request, 'doc/review/review_request.html', {
        'doc': doc,
        'review_req': review_req,
        'can_withdraw_request': can_withdraw_request,
        'can_reject_request_assignment': can_reject_request_assignment,
    })

def withdraw_request(request, name, request_id):
    doc = get_object_or_404(Document, name=name)
    review_req = get_object_or_404(ReviewRequest, pk=request_id, state__in=["requested", "accepted"])

    if not is_authorized_in_doc_stream(request.user, doc):
        return HttpResponseForbidden("You do not have permission to perform this action")

    if request.method == "POST" and request.POST.get("action") == "withdraw":
        review_req.state = ReviewRequestStateName.objects.get(slug="withdrawn")
        review_req.save()

        DocEvent.objects.create(
            type="changed_review_request",
            doc=doc,
            by=request.user.person,
            desc="Withdrew request for {} review by {}".format(review_req.type.name, review_req.team.acronym.upper()),
        )

        if review_req.state_id != "requested":
            # FIXME: handle this case - by emailing?
            pass

        return redirect(review_request, name=review_req.doc.name, request_id=review_req.pk)

    return render(request, 'doc/review/withdraw_request.html', {
        'doc': doc,
        'review_req': review_req,
    })

class RejectRequestAssignmentForm(forms.Form):
    message_to_secretary = forms.CharField(widget=forms.Textarea, required=False, help_text="Optional explanation of rejection, will be emailed to team secretary")

def reject_request_assignment(request, name, request_id):
    doc = get_object_or_404(Document, name=name)
    review_req = get_object_or_404(ReviewRequest, pk=request_id, state__in=["requested", "accepted"])

    if not review_req.reviewer:
        return redirect(review_request, name=review_req.doc.name, request_id=review_req.pk)

    is_reviewer = user_is_person(request.user, review_req.reviewer.role.person)
    can_manage_req = can_manage_review_requests_for_team(request.user, review_req.team)

    if not (is_reviewer or can_manage_req):
        return HttpResponseForbidden("You do not have permission to perform this action")

    if request.method == "POST" and request.POST.get("action") == "reject":
        # reject the old request
        prev_state = review_req.state
        review_req.state = ReviewRequestStateName.objects.get(slug="rejected")
        review_req.save()

        # assignment of reviewer is currently considered minutia, so
        # not reported in the log
        if prev_state.slug == "accepted":
            DocEvent.objects.create(
                type="changed_review_request",
                doc=doc,
                by=request.user.person,
                desc="Request for {} review by {} is unassigned".format(review_req.type.name, review_req.team.acronym.upper()),
            )

        # make a new, open review request
        ReviewRequest.objects.create(
            time=review_req.time,
            type=review_req.type,
            doc=review_req.doc,
            team=review_req.team,
            deadline=review_req.deadline,
            requested_rev=review_req.requested_rev,
            state=prev_state,
        )

        return redirect(review_request, name=review_req.doc.name, request_id=review_req.pk)

    return render(request, 'doc/review/reject_request_assignment.html', {
        'doc': doc,
        'review_req': review_req,
    })
