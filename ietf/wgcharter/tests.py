# Copyright The IETF Trust 2011, All Rights Reserved

import os
import unittest
import django.test
from django.conf import settings
from ietf.utils.test_utils import SimpleUrlTestCase
from ietf.utils.test_runner import mail_outbox
from ietf.utils.test_data import make_test_data
from ietf.utils.test_utils import SimpleUrlTestCase, RealDatabaseTest, login_testing_unauthorized

import datetime
from pyquery import PyQuery
from tempfile import NamedTemporaryFile

from django.contrib.auth.models import User
from doc.models import *
from group.models import *
from name.models import *
from person.models import *
from name.utils import name

from utils import *

class WgUrlTestCase(SimpleUrlTestCase):
    def testUrls(self):
        self.doTestUrls(__file__)

    def setUp(self, *args, **kwargs):
        super(WgUrlTestCase, self).setUp(*args, **kwargs)
        # Make test data (because we use the new schema)
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        approved = name(CharterDocStateName, "approved", "Approved")

class WgFileTestCase(django.test.TestCase):
    def testFileExistence(self):
        print "     Testing if WG charter texts exist locally"
        fpath = os.path.join(settings.CHARTER_PATH, "charter-ietf-core-01.txt")
        if not os.path.exists(fpath):
            print "\nERROR: charter text not found in "+settings.CHARTER_PATH
            print "Needed for testing WG record pages."
            print "Remember to set CHARTER_PATH in settings.py\n"
        else:
            print "OK   (seem to exist)"

class WgStateTestCase(django.test.TestCase):
    fixtures = ['names']

    def test_change_state(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # And make a charter for group
        group = Group.objects.get(acronym="mars")
        charter = set_or_create_charter(group)
        
        charter.charter_state = infrev
        charter.save()

        # -- Test change state --
        url = urlreverse('wg_change_state', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        first_state = charter.charter_state

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form select[name=state]')), 1)
        
        # faulty post
        r = self.client.post(url, dict(state="foobarbaz"))
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form ul.errorlist')) > 0)
        self.assertEquals(charter.charter_state, first_state)
        
        # change state
        for s in ("intrev", "extrev", "iesgrev", "approved"):
            events_before = charter.docevent_set.count()
            mailbox_before = len(mail_outbox)
        
            r = self.client.post(url, dict(state="active", charter_state=s, message="test message"))
            self.assertEquals(r.status_code, 302)
        
            charter = Document.objects.get(name="charter-ietf-%s" % group.acronym)
            self.assertEquals(charter.charter_state_id, s)
            self.assertEquals(charter.docevent_set.count(), events_before + 1)
            self.assertTrue("State changed" in charter.docevent_set.all()[0].desc)
            if s == "extrev":
                self.assertEquals(len(mail_outbox), mailbox_before + 2)
                self.assertTrue("State changed" in mail_outbox[-1]['Subject'])
                self.assertTrue("State changed" in mail_outbox[-2]['Subject'])
            else:
                self.assertEquals(len(mail_outbox), mailbox_before + 1)
                if s == "approved":
                    self.assertTrue("Charter approved" in mail_outbox[-1]['Subject'])
                else:
                    self.assertTrue("State changed" in mail_outbox[-1]['Subject'])
                    
    def test_conclude(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # And make a charter for group
        group = Group.objects.get(acronym="mars")
        charter = set_or_create_charter(group)
        
        charter.charter_state = approved
        charter.save()
        
        # -- Test conclude WG --
        url = urlreverse('wg_conclude', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form textarea[name=instructions]')), 1)
        
        # faulty post
        r = self.client.post(url, dict(instructions="")) # No instructions
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form ul.errorlist')) > 0)
        group = Group.objects.get(acronym="mars")

        # conclusion request
        r = self.client.post(url, dict(instructions="Test instructions"))
        self.assertEquals(r.status_code, 302)
        # The WG remains active until the state is set to conclude via change_state
        self.assertEquals(group.state_id, "active") 

class WgInfoTestCase(django.test.TestCase):
    fixtures = ['names']

    def test_create(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # -- Test WG creation --
        url = urlreverse('wg_create')
        login_testing_unauthorized(self, "secretary", url)

        num_wgs = len(Group.objects.filter(type="wg"))

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form input[name=acronym]')), 1)
        
        # faulty post
        r = self.client.post(url, dict(acronym="foobarbaz")) # No name
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form ul.errorlist')) > 0)
        self.assertEquals(len(Group.objects.filter(type="wg")), num_wgs)

        # creation
        r = self.client.post(url, dict(acronym="testwg", name="Testing WG"))
        self.assertEquals(r.status_code, 302)
        self.assertEquals(len(Group.objects.filter(type="wg")), num_wgs + 1)
        group = Group.objects.get(acronym="testwg")
        self.assertEquals(group.name, "Testing WG")
        # check that a charter was created with the correct name
        self.assertEquals(group.charter.name, "charter-ietf-testwg")
        # and that it has no revision
        self.assertEquals(group.charter.rev, "")


    def test_edit_info(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # And make a charter for group
        group = Group.objects.get(acronym="mars")
        charter = set_or_create_charter(group)
        
        url = urlreverse('wg_edit_info', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form select[name=parent]')), 1)
        self.assertEquals(len(q('form input[name=acronym]')), 1)

        # faulty post
        Group.objects.create(name="Collision Test Group", acronym="collide")
        r = self.client.post(url, dict(acronym="collide"))
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form ul.errorlist')) > 0)

        # Create old acronym
        group.acronym = "oldmars"
        group.save()
        save_group_in_history(group)
        group.acronym = "mars"
        group.save()

        # post with warning
        r = self.client.post(url, dict(acronym="oldmars"))
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form ul.errorlist')) > 0)
        
        # edit info
        r = self.client.post(url,
                             dict(name="Mars Not Special Interest Group",
                                  acronym="mnsig",
                                  parent=2,
                                  ad=1,
                                  chairs="aread@ietf.org",
                                  secr="aread@ietf.org",
                                  techadv="aread@ietf.org",
                                  list_email="mars@mail",
                                  list_subscribe="subscribe.mars",
                                  list_archive="archive.mars",
                                  urls="http://mars.mars (MARS site)"
                                  ))
        self.assertEquals(r.status_code, 302)

        group = Group.objects.get(acronym="mnsig")
        self.assertEquals(group.name, "Mars Not Special Interest Group")
        self.assertEquals(group.parent_id, 2)
        self.assertEquals(group.ad.name, "Aread Irector")
        for k in ("chair", "secr", "techadv"):
            self.assertEquals(group.role_set.filter(name="chair")[0].email.address, "aread@ietf.org")
        self.assertEquals(group.list_email, "mars@mail")
        self.assertEquals(group.list_subscribe, "subscribe.mars")
        self.assertEquals(group.list_archive, "archive.mars")
        self.assertEquals(group.groupurl_set.all()[0].url, "http://mars.mars")
        self.assertEquals(group.groupurl_set.all()[0].name, "MARS site")

    def test_edit_telechat_date(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # And make a charter for group
        group = Group.objects.get(acronym="mars")
        charter = set_or_create_charter(group)
        
        url = urlreverse('wg_edit_info', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        from ietf.iesg.models import TelechatDates

        # add to telechat
        self.assertTrue(not charter.latest_event(TelechatDocEvent, "scheduled_for_telechat"))
        telechat_date = TelechatDates.objects.all()[0].date1.isoformat()
        r = self.client.post(url, dict(name=group.name, acronym=group.acronym, telechat_date=telechat_date))
        self.assertEquals(r.status_code, 302)

        charter = Document.objects.get(name=charter.name)
        self.assertTrue(charter.latest_event(TelechatDocEvent, "scheduled_for_telechat"))
        self.assertEquals(charter.latest_event(TelechatDocEvent, "scheduled_for_telechat").telechat_date, TelechatDates.objects.all()[0].date1)

        # change telechat
        telechat_date = TelechatDates.objects.all()[0].date2.isoformat()
        r = self.client.post(url, dict(name=group.name, acronym=group.acronym, telechat_date=telechat_date))
        self.assertEquals(r.status_code, 302)

        charter = Document.objects.get(name=charter.name)
        self.assertEquals(charter.latest_event(TelechatDocEvent, "scheduled_for_telechat").telechat_date, TelechatDates.objects.all()[0].date2)

        # remove from agenda
        telechat_date = ""
        r = self.client.post(url, dict(name=group.name, acronym=group.acronym, telechat_date=telechat_date))
        self.assertEquals(r.status_code, 302)

        charter = Document.objects.get(name=charter.name)
        self.assertTrue(not charter.latest_event(TelechatDocEvent, "scheduled_for_telechat").telechat_date)

    def test_submit_charter(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        # And make a charter for group
        group = Group.objects.get(acronym="mars")
        charter = set_or_create_charter(group)

        url = urlreverse('wg_submit', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form input[name=txt]')), 1)

        prev_rev = charter.rev

        file = NamedTemporaryFile()
        file.write("Test content")
        file.seek(0)

        r = self.client.post(url, dict(txt=file))
        self.assertEquals(r.status_code, 302)

        file.close()

        charter = Document.objects.get(name="charter-ietf-mars")
        self.assertEquals(charter.rev, next_revision(prev_rev))
        self.assertTrue("new_revision" in charter.latest_event().type)

class WgAddCommentTestCase(django.test.TestCase):
    fixtures = ['names']

    def test_add_comment(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")

        group = Group.objects.get(acronym="mars")
        url = urlreverse('wg_add_comment', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertEquals(len(q('form textarea[name=comment]')), 1)

        # request resurrect
        comments_before = group.groupevent_set.filter(type="added_comment").count()

        r = self.client.post(url, dict(comment="This is a test."))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(group.groupevent_set.filter(type="added_comment").count(), comments_before + 1)
        self.assertTrue("This is a test." in group.groupevent_set.filter(type="added_comment").order_by('-time')[0].desc)

class WgEditPositionTestCase(django.test.TestCase):
    fixtures = ['names', 'ballot']

    def test_edit_position(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")
        no = name(GroupBallotPositionName, 'no', 'No'),
        yes = name(GroupBallotPositionName, 'yes', 'Yes'),
        abstain = name(GroupBallotPositionName, 'abstain', 'Abstain'),
        block = name(GroupBallotPositionName, 'block', 'Block'),
        norecord = name(GroupBallotPositionName, 'norecord', 'No record'),

        group = Group.objects.get(acronym="mars")
        url = urlreverse('wg_edit_position', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "ad", url)

        charter = set_or_create_charter(group)

        p = Person.objects.get(name="Aread Irector")

        e = DocEvent()
        e.type = "started_iesg_process"
        e.by = p
        e.doc = charter
        e.desc = "IESG process started"
        e.save()
        
        charter.charter_state = iesgrev
        charter.save()

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form input[name=position]')) > 0)
        self.assertEquals(len(q('form textarea[name=comment]')), 1)

        # vote
        pos_before = charter.docevent_set.filter(type="changed_ballot_position").count()
        self.assertTrue(not charter.docevent_set.filter(type="changed_ballot_position", by__name="Aread Irector"))
        
        r = self.client.post(url, dict(position="block",
                                       block_comment="This is a blocking test.",
                                       comment="This is a test."))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(charter.docevent_set.filter(type="changed_ballot_position").count(), pos_before + 1)
        e = charter.latest_event(GroupBallotPositionDocEvent)
        self.assertTrue("This is a blocking test." in e.block_comment)
        self.assertTrue("This is a test." in e.comment)
        self.assertTrue(e.pos_id, "block")

        # recast vote
        pos_before = charter.docevent_set.filter(type="changed_ballot_position").count()
        
        r = self.client.post(url, dict(position="yes"))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(charter.docevent_set.filter(type="changed_ballot_position").count(), pos_before + 1)
        e = charter.latest_event(GroupBallotPositionDocEvent)
        self.assertTrue(e.pos_id, "yes")

        # clear vote
        pos_before = charter.docevent_set.filter(type="changed_ballot_position").count()
        
        r = self.client.post(url, dict(position="norecord"))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(charter.docevent_set.filter(type="changed_ballot_position").count(), pos_before + 1)
        e = charter.latest_event(GroupBallotPositionDocEvent)
        self.assertTrue(e.pos_id, "norecord")

    def test_edit_position_as_secretary(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")
        no = name(GroupBallotPositionName, 'no', 'No'),
        yes = name(GroupBallotPositionName, 'yes', 'Yes'),
        abstain = name(GroupBallotPositionName, 'abstain', 'Abstain'),
        block = name(GroupBallotPositionName, 'block', 'Block'),
        norecord = name(GroupBallotPositionName, 'norecord', 'No record'),

        group = Group.objects.get(acronym="mars")
        url = urlreverse('wg_edit_position', kwargs=dict(name=group.acronym))
        p = Person.objects.get(name="Aread Irector")
        url += "?ad=%d" % p.id
        login_testing_unauthorized(self, "secretary", url)

        charter = set_or_create_charter(group)

        e = DocEvent()
        e.type = "started_iesg_process"
        e.by = p
        e.doc = charter
        e.desc = "IESG process started"
        e.save()
        
        charter.charter_state = iesgrev
        charter.save()

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form input[name=position]')) > 0)

        # vote for rhousley
        pos_before = charter.docevent_set.filter(type="changed_ballot_position").count()
        self.assertTrue(not charter.docevent_set.filter(type="changed_ballot_position", by__name="Sec Retary"))
        
        r = self.client.post(url, dict(position="no"))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(charter.docevent_set.filter(type="changed_ballot_position").count(), pos_before + 1)
        e = charter.latest_event(GroupBallotPositionDocEvent)
        self.assertTrue(e.pos_id, "no")
        
    def test_send_ballot_comment(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")
        no = name(GroupBallotPositionName, 'no', 'No'),
        yes = name(GroupBallotPositionName, 'yes', 'Yes'),
        abstain = name(GroupBallotPositionName, 'abstain', 'Abstain'),
        block = name(GroupBallotPositionName, 'block', 'Block'),
        norecord = name(GroupBallotPositionName, 'norecord', 'No record'),

        group = Group.objects.get(acronym="mars")
        url = urlreverse('wg_send_ballot_comment', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "ad", url)

        charter = set_or_create_charter(group)

        p = Person.objects.get(name="Aread Irector")

        e = DocEvent()
        e.type = "started_iesg_process"
        e.by = p
        e.doc = charter
        e.desc = "IESG process started"
        e.save()
        
        charter.charter_state = iesgrev
        charter.save()

        GroupBallotPositionDocEvent.objects.create(
            doc=charter,
            by=p,
            type="changed_ballot_position",
            pos=GroupBallotPositionName.objects.get(slug="block"),
            ad=p,
            block_comment="This is a block test",
            comment="This is a test",
            )

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue(len(q('form input[name="cc"]')) > 0)

        # send
        p = Person.objects.get(name="Aread Irector")
        mailbox_before = len(mail_outbox)
        
        r = self.client.post(url, dict(cc="test@example.com", cc_state_change="1"))
        self.assertEquals(r.status_code, 302)

        self.assertEquals(len(mail_outbox), mailbox_before + 1)
        self.assertTrue("BLOCKING COMMENT" in mail_outbox[-1]['Subject'])
        self.assertTrue("COMMENT" in mail_outbox[-1]['Subject'])

class WgApproveBallotTestCase(django.test.TestCase):
    fixtures = ['base', 'names', 'ballot']

    def test_approve_ballot(self):
        make_test_data()
        # Make sure all relevant names are created 
        type_charter = name(DocTypeName, "charter", "Charter")
        proposed = name(GroupStateName, "proposed", "Proposed")
        active = name(GroupStateName, "active", "Active")
        notrev=name(CharterDocStateName, slug="notrev", name="Not currently under review")
        infrev=name(CharterDocStateName, slug="infrev", name="Informal IESG review")
        intrev=name(CharterDocStateName, slug="intrev", name="Internal review")
        extrev=name(CharterDocStateName, slug="extrev", name="External review")
        iesgrev=name(CharterDocStateName, slug="iesgrev", name="IESG review")
        approved=name(CharterDocStateName, slug="approved", name="Approved")
        no = name(GroupBallotPositionName, 'no', 'No'),
        yes = name(GroupBallotPositionName, 'yes', 'Yes'),
        abstain = name(GroupBallotPositionName, 'abstain', 'Abstain'),
        block = name(GroupBallotPositionName, 'block', 'Block'),
        norecord = name(GroupBallotPositionName, 'norecord', 'No record'),

        group = Group.objects.get(acronym="mars")
        url = urlreverse('wg_approve_ballot', kwargs=dict(name=group.acronym))
        login_testing_unauthorized(self, "secretary", url)

        charter = set_or_create_charter(group)

        p = Person.objects.get(name="Aread Irector")

        e = DocEvent()
        e.type = "started_iesg_process"
        e.by = p
        e.doc = charter
        e.desc = "IESG process started"
        e.save()
        
        charter.charter_state = iesgrev
        charter.save()

        # normal get
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200)
        q = PyQuery(r.content)
        self.assertTrue("Send out the announcement" in q('input[type=submit]')[0].get('value'))
        self.assertEquals(len(q('pre')), 1)

        # approve
        mailbox_before = len(mail_outbox)

        # Dont copy the actual txt file
        from django.conf import settings
        settings.DONT_COPY_CHARTER_ON_APPROVE = True

        r = self.client.post(url, dict())
        self.assertEquals(r.status_code, 302)

        charter = Document.objects.get(name=charter.name)
        self.assertEquals(charter.charter_state_id, "approved")

        self.assertEquals(charter.rev, "01")
        
        self.assertEquals(len(mail_outbox), mailbox_before + 2)

        self.assertTrue("WG Action" in mail_outbox[-1]['Subject'])
        self.assertTrue("Charter approved" in mail_outbox[-2]['Subject'])
