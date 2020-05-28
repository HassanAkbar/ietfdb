# Copyright The IETF Trust 2020, All Rights Reserved
import calendar
import datetime
from io import StringIO

from django.core.management.base import CommandError

from ietf.utils.test_utils import TestCase
from ietf.group.factories import GroupFactory, RoleFactory
from ietf.person.factories import PersonFactory
from ietf.meeting.models import Session, Constraint, TimerangeName
from ietf.meeting.factories import MeetingFactory, RoomFactory, TimeSlotFactory, SessionFactory
from ietf.meeting.management.commands.schedule_generator import ScheduleHandler


class ScheduleGeneratorTest(TestCase):
    def setUp(self):
        # Create a meeting of 2 days, 4 sessions per day, in 2 rooms.
        # Two rooms is a fairly low level of simultaneous schedules, this is needed
        # because the schedule in these tests is much more complex than a real schedule.
        self.meeting = MeetingFactory(type_id='ietf', days=2)
        self.rooms = [
            RoomFactory(meeting=self.meeting, capacity=100),
            RoomFactory(meeting=self.meeting, capacity=10)
        ]
        
        self.timeslots = []
        for room in self.rooms:
            for day in range(0, 2):
                for hour in range(12, 16): 
                    t = TimeSlotFactory(
                        meeting=self.meeting,
                        location=room,
                        time=datetime.datetime.combine(
                            self.meeting.date + datetime.timedelta(days=day),
                            datetime.time(hour, 0),
                        ),
                        duration=datetime.timedelta(minutes=60),
                    )
                    self.timeslots.append(t)
                            
        self.first_meeting_day = calendar.day_name[self.meeting.date.weekday()].lower()
        
        self.area1 = GroupFactory(acronym='area1', type_id='area')
        self.area2 = GroupFactory(acronym='area2', type_id='area')
        self.wg1 = GroupFactory(acronym='wg1', parent=self.area1)
        self.wg2 = GroupFactory(acronym='wg2', )
        self.wg3 = GroupFactory(acronym='wg3', )
        self.bof1 = GroupFactory(acronym='bof1', parent=self.area1, state_id='bof')
        self.bof2 = GroupFactory(acronym='bof2', parent=self.area2, state_id='bof')
        self.prg1 = GroupFactory(acronym='prg1', parent=self.area2, type_id='rg', state_id='proposed')

        self.ad_role = RoleFactory(group=self.wg1, name_id='ad')
        RoleFactory(group=self.bof1, name_id='ad', person=self.ad_role.person)

        self.person1 = PersonFactory()

    def test_normal_schedule(self):
        stdout = StringIO()
        self._create_basic_sessions()
        generator = ScheduleHandler(stdout, self.meeting.number, verbosity=3)
        violations, cost = generator.run()
        self.assertEqual(violations, self.fixed_violations)
        self.assertEqual(cost, self.fixed_cost)

        stdout.seek(0)
        output = stdout.read()
        self.assertIn('WARNING: session wg2 (pk 13) has no attendees set', output)
        self.assertIn('scheduling 13 sessions in 16 timeslots', output)
        self.assertIn('Optimiser starting run 0', output)
        self.assertIn('Optimiser found an optimal schedule', output)
        
        schedule = self.meeting.schedule_set.get(name__startswith='Auto-')
        self.assertEqual(schedule.assignments.count(), 13)

    def test_unresolvable_schedule(self):
        stdout = StringIO()
        self._create_basic_sessions()
        self.wg2.parent = self.area1
        self.wg2.save()
        self.bof2.parent = self.area1
        self.bof2.save()

        generator = ScheduleHandler(stdout, self.meeting.number, verbosity=2)
        violations, cost = generator.run()
        self.assertNotEqual(violations, [])
        self.assertGreater(cost, self.fixed_cost)

        stdout.seek(0)
        output = stdout.read()
        self.assertIn('Optimiser did not find perfect schedule', output)

    def test_too_many_sessions(self):
        stdout = StringIO()
        self._create_basic_sessions()
        self._create_basic_sessions()
        with self.assertRaises(CommandError):
            generator = ScheduleHandler(stdout, self.meeting.number, verbosity=0)
            generator.run()

    def test_invalid_meeting_number(self):
        stdout = StringIO()
        with self.assertRaises(CommandError):
            generator = ScheduleHandler(stdout, 'not-valid-meeting-number-aaaa', verbosity=0)
            generator.run()

    def _create_basic_sessions(self):
        for group in [self.area1, self.area2, self.wg1, self.wg2, self.wg3, self.bof1,
                      self.bof2, self.prg1]:
            SessionFactory(meeting=self.meeting, group=group, add_to_schedule=False, attendees=5,
                           requested_duration=datetime.timedelta(hours=1))
        for group in self.bof1, self.bof2, self.wg2:
            SessionFactory(meeting=self.meeting, group=group, add_to_schedule=False, attendees=55,
                           requested_duration=datetime.timedelta(hours=1))
        SessionFactory(meeting=self.meeting, group=self.wg2, add_to_schedule=False, attendees=500,
                       requested_duration=datetime.timedelta(hours=2))

        joint_session = SessionFactory(meeting=self.meeting, group=self.wg2, add_to_schedule=False)
        joint_session.joint_with_groups.add(self.wg3)

        Constraint.objects.create(meeting=self.meeting, source=self.wg1,
                                  name_id='wg_adjacent', target=self.area1)
        Constraint.objects.create(meeting=self.meeting, source=self.wg2,
                                  name_id='conflict', target=self.bof1)
        Constraint.objects.create(meeting=self.meeting, source=self.bof1,
                                  name_id='bethere', person=self.person1)
        Constraint.objects.create(meeting=self.meeting, source=self.wg2,
                                  name_id='bethere', person=self.person1)
        Constraint.objects.create(meeting=self.meeting, source=self.bof1,
                                  name_id='time_relation', time_relation='subsequent-days')
        Constraint.objects.create(meeting=self.meeting, source=self.bof2,
                                  name_id='time_relation', time_relation='one-day-separation')

        timerange_c1 = Constraint.objects.create(meeting=self.meeting, source=self.wg2,
                                                 name_id='timerange')
        timerange_c1.timeranges.set(TimerangeName.objects.filter(slug__startswith=self.first_meeting_day))

        self.fixed_violations = ['No timeslot with sufficient duration available for wg2, '
                                 'requested 2:00:00, trimmed to 1:00:00', 
                                 'No timeslot with sufficient capacity available for wg2, '
                                 'requested 500, trimmed to 100']
        self.fixed_cost = 10000 + 10000
