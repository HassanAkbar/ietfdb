import datetime


from django import forms
from django.template.loader import render_to_string
from workflows.models import State

from ietf.idtracker.models import PersonOrOrgInfo
from ietf.wgchairs.accounts import get_person_for_user
from ietf.ietfworkflows.models import Stream
from ietf.ietfworkflows.utils import (get_workflow_for_draft,
                                      get_state_for_draft,
                                      update_state, FOLLOWUP_TAG,
                                      get_annotation_tags_for_draft,
                                      update_tags, update_stream)
from ietf.ietfworkflows.streams import get_stream_from_draft


class StreamDraftForm(forms.Form):

    can_cancel = False
    template = None

    def __init__(self, *args, **kwargs):
        self.draft = kwargs.pop('draft', None)
        self.user = kwargs.pop('user', None)
        self.person = get_person_for_user(self.user)
        self.workflow = get_workflow_for_draft(self.draft)
        self.message = {}
        super(StreamDraftForm, self).__init__(*args, **kwargs)

    def get_message(self):
        return self.message

    def set_message(self, msg_type, msg_value):
        self.message = {'type': msg_type,
                        'value': msg_value,
                       }

    def __unicode__(self):
        return render_to_string(self.template, {'form': self})


class DraftTagsStateForm(StreamDraftForm):

    comment = forms.CharField(widget=forms.Textarea)
    new_state = forms.ChoiceField()
    weeks = forms.IntegerField(required=False)
    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    template = 'ietfworkflows/state_form.html'

    def __init__(self, *args, **kwargs):
        super(DraftTagsStateForm, self).__init__(*args, **kwargs)
        self.state = get_state_for_draft(self.draft)
        self.fields['new_state'].choices = self.get_states()
        if self.is_bound:
            for key, value in self.data.items():
                if key.startswith('transition_'):
                    new_state = self.get_new_state(key)
                    if new_state:
                        self.data = self.data.copy()
                        self.data.update({'new_state': new_state.id})
        self.available_tags = self.workflow.get_tags()
        self.tags = [i.annotation_tag for i in get_annotation_tags_for_draft(self.draft)]
        self.fields['tags'].choices = [(i.pk, i.name) for i in self.available_tags]
        self.fields['tags'].initial = [i.pk for i in self.tags]

    def get_new_state(self, key):
        transition_id = key.replace('transition_', '')
        transition = self.get_transitions().filter(id=transition_id)
        if transition:
            return transition[0].destination
        return None

    def get_transitions(self):
        return self.state.transitions.filter(workflow=self.workflow)

    def get_states(self):
        return [(i.pk, i.name) for i in self.workflow.get_states()]

    def save_tags(self):
        comment = self.cleaned_data.get('comment')
        new_tags = self.cleaned_data.get('tags')

        set_tags = [tag for tag in self.available_tags if str(tag.pk) in new_tags and tag not in self.tags]
        reset_tags = [tag for tag in self.available_tags if str(tag.pk) not in new_tags and tag in self.tags]
        followup = bool([tag for tag in set_tags if tag.name == FOLLOWUP_TAG])
        extra_notify = []
        if followup:
            try:
                shepherd = self.draft.shepherd
                if shepherd:
                    extra_notify = ['%s <%s>' % shepherd.email()]
            except PersonOrOrgInfo.DoesNotExist:
                pass
        if not set_tags and not reset_tags:
            return
        update_tags(self.draft,
                    comment=comment,
                    person=self.person,
                    set_tags=set_tags,
                    reset_tags=reset_tags,
                    extra_notify=extra_notify)

    def save_state(self):
        comment = self.cleaned_data.get('comment')
        state = State.objects.get(pk=self.cleaned_data.get('new_state'))
        weeks = self.cleaned_data.get('weeks')
        estimated_date = None
        if weeks:
            now = datetime.date.today()
            estimated_date = now + datetime.timedelta(weeks=weeks)
        update_state(obj=self.draft,
                     comment=comment,
                     person=self.person,
                     to_state=state,
                     estimated_date=estimated_date)

    def save(self):
        self.save_tags()
        if 'only_tags' in self.data.keys():
            return
        self.save_state()


class DraftStreamForm(StreamDraftForm):

    comment = forms.CharField(widget=forms.Textarea)
    stream = forms.ModelChoiceField(Stream.objects.all())

    template = 'ietfworkflows/stream_form.html'

    def __init__(self, *args, **kwargs):
        super(DraftStreamForm, self).__init__(*args, **kwargs)
        self.stream = get_stream_from_draft(self.draft)
        self.tags = [i.annotation_tag for i in get_annotation_tags_for_draft(self.draft)]
        if self.stream:
            self.fields['stream'].initial = self.stream.pk

    def save(self):
        comment = self.cleaned_data.get('comment')
        to_stream = self.cleaned_data.get('stream')

        update_stream(self.draft,
                      comment=comment,
                      person=self.person,
                      to_stream=to_stream)
