# Copyright The IETF Trust 2012-2020, All Rights Reserved
# -*- coding: utf-8 -*-


import datetime
import hashlib
import os
import re
import tempfile
import itertools

from email import message_from_string
from email.header import decode_header
from email.iterators import typed_subpart_iterator
from email.utils import parseaddr

from django.db.models import Q
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str

from ietf.dbtemplate.models import DBTemplate
from ietf.person.models import Email, Person
from ietf.meeting.models import Meeting
from ietf.mailtrigger.utils import gather_address_lists
from ietf.utils.pipe import pipe
from ietf.utils.mail import send_mail_text, send_mail, get_payload_text
from ietf.utils.log import log
from ietf.person.name import unidecode_name

import debug                            # pyflakes:ignore

MAIN_NOMCOM_TEMPLATE_PATH = '/nomcom/defaults/'
QUESTIONNAIRE_TEMPLATE = 'position/questionnaire.txt'
HEADER_QUESTIONNAIRE_TEMPLATE = 'position/header_questionnaire.txt'
REQUIREMENTS_TEMPLATE = 'position/requirements'
HOME_TEMPLATE = 'home.rst'
INEXISTENT_PERSON_TEMPLATE = 'email/inexistent_person.txt'
NOMINEE_EMAIL_TEMPLATE = 'email/new_nominee.txt'
NOMINATION_EMAIL_TEMPLATE = 'email/new_nomination.txt'
NOMINEE_ACCEPT_REMINDER_TEMPLATE = 'email/nomination_accept_reminder.txt'
NOMINEE_QUESTIONNAIRE_REMINDER_TEMPLATE = 'email/questionnaire_reminder.txt'
NOMINATION_RECEIPT_TEMPLATE = 'email/nomination_receipt.txt'
FEEDBACK_RECEIPT_TEMPLATE = 'email/feedback_receipt.txt'
DESCRIPTION_TEMPLATE = 'topic/description'
IESG_GENERIC_REQUIREMENTS_TEMPLATE = 'iesg_requirements'

DEFAULT_NOMCOM_TEMPLATES = [HOME_TEMPLATE,
                            INEXISTENT_PERSON_TEMPLATE,
                            NOMINEE_EMAIL_TEMPLATE,
                            NOMINATION_EMAIL_TEMPLATE,
                            NOMINEE_ACCEPT_REMINDER_TEMPLATE,
                            NOMINEE_QUESTIONNAIRE_REMINDER_TEMPLATE,
                            NOMINATION_RECEIPT_TEMPLATE,
                            FEEDBACK_RECEIPT_TEMPLATE,
                            IESG_GENERIC_REQUIREMENTS_TEMPLATE,
                        ]

# See RFC8713 section 4.15
DISQUALIFYING_ROLE_QUERY_EXPRESSION = (   Q(group__acronym__in=['isocbot', 'ietf-trust', 'llc-board', 'iab'], name_id__in=['member', 'chair'])
                                        | Q(group__type_id='area', group__state='active',name_id='ad')
                                      )


def get_nomcom_by_year(year):
    from ietf.nomcom.models import NomCom
    return get_object_or_404(NomCom,
                             group__acronym__icontains=year,
                             )


def get_year_by_nomcom(nomcom):
    acronym = nomcom.group.acronym
    m = re.search(r'(?P<year>\d\d\d\d)', acronym)
    return m.group(0)


def get_user_email(user):
    # a user object already has an email field, but we don't want to
    # overwrite anything that might be there, and we don't know that
    # what's there is the right thing, so we cache the lookup results in a
    # separate attribute
    if not hasattr(user, "_email_cache"):
        user._email_cache = None
        if hasattr(user, "person"):
            emails = user.person.email_set.filter(active=True).order_by('-time')
            if emails:
                user._email_cache = emails[0]
                for email in emails:
                    if email.address == user.username:
                        user._email_cache = email
        else:
            try: 
                user._email_cache = Email.objects.get(address=user.username)
            except ObjectDoesNotExist:
                pass
    return user._email_cache

def get_hash_nominee_position(date, nominee_position_id):
    return hashlib.md5(('%s%s%s' % (settings.SECRET_KEY, date, nominee_position_id)).encode('utf-8')).hexdigest()


def initialize_templates_for_group(group):
    for template_name in DEFAULT_NOMCOM_TEMPLATES:
        template_path = MAIN_NOMCOM_TEMPLATE_PATH + template_name
        template = DBTemplate.objects.get(path=template_path)
        DBTemplate.objects.create(
            group=group.group,
            title=template.title,
            path='/nomcom/' + group.group.acronym + '/' + template_name,
            variables=template.variables,
            type_id=template.type_id,
            content=template.content)


def initialize_questionnaire_for_position(position):
    questionnaire_path = MAIN_NOMCOM_TEMPLATE_PATH + QUESTIONNAIRE_TEMPLATE
    header_questionnaire_path = MAIN_NOMCOM_TEMPLATE_PATH + HEADER_QUESTIONNAIRE_TEMPLATE
    template = DBTemplate.objects.get(path=questionnaire_path)
    header_template = DBTemplate.objects.get(path=header_questionnaire_path)
    DBTemplate.objects.create(
        group=position.nomcom.group,
        title=header_template.title + ' [%s]' % position.name,
        path='/nomcom/' + position.nomcom.group.acronym + '/' + str(position.id) + '/' + HEADER_QUESTIONNAIRE_TEMPLATE,
        variables=header_template.variables,
        type_id=header_template.type_id,
        content=header_template.content)
    questionnaire = DBTemplate.objects.create(
        group=position.nomcom.group,
        title=template.title + ' [%s]' % position.name,
        path='/nomcom/' + position.nomcom.group.acronym + '/' + str(position.id) + '/' + QUESTIONNAIRE_TEMPLATE,
        variables=template.variables,
        type_id=template.type_id,
        content=template.content)
    return questionnaire


def initialize_requirements_for_position(position):
    requirements_path = MAIN_NOMCOM_TEMPLATE_PATH + REQUIREMENTS_TEMPLATE
    template = DBTemplate.objects.get(path=requirements_path)
    return DBTemplate.objects.create(
            group=position.nomcom.group,
            title=template.title + ' [%s]' % position.name,
            path='/nomcom/' + position.nomcom.group.acronym + '/' + str(position.id) + '/' + REQUIREMENTS_TEMPLATE,
            variables=template.variables,
            type_id=template.type_id,
            content=template.content)

def initialize_description_for_topic(topic):
    description_path = MAIN_NOMCOM_TEMPLATE_PATH + DESCRIPTION_TEMPLATE
    template = DBTemplate.objects.get(path=description_path)
    return DBTemplate.objects.create(
            group=topic.nomcom.group,
            title=template.title + ' [%s]' % topic.subject,
            path='/nomcom/' + topic.nomcom.group.acronym + '/topic/' + str(topic.id) + '/' + DESCRIPTION_TEMPLATE,
            variables=template.variables,
            type_id=template.type_id,
            content=template.content)

def delete_nomcom_templates(nomcom):
    nomcom_template_path = '/nomcom/' + nomcom.group.acronym
    DBTemplate.objects.filter(path__contains=nomcom_template_path).delete()


def retrieve_nomcom_private_key(request, year):
    private_key = request.session.get('NOMCOM_PRIVATE_KEY_%s' % year, None)

    if not private_key:
        return private_key

    command = "%s bf -d -in /dev/stdin -k \"%s\" -a"
    code, out, error = pipe(command % (settings.OPENSSL_COMMAND,
                                       settings.SECRET_KEY), private_key)
    if code != 0:
        log("openssl error: %s:\n  Error %s: %s" %(command, code, error))        
    return out


def store_nomcom_private_key(request, year, private_key):
    if not private_key:
        request.session['NOMCOM_PRIVATE_KEY_%s' % year] = ''
    else:
        command = "%s bf -e -in /dev/stdin -k \"%s\" -a"
        code, out, error = pipe(command % (settings.OPENSSL_COMMAND,
                                           settings.SECRET_KEY), private_key)
        if code != 0:
            log("openssl error: %s:\n  Error %s: %s" %(command, code, error))        
        if error:
            out = ''
        request.session['NOMCOM_PRIVATE_KEY_%s' % year] = out


def validate_private_key(key):
    key_file = tempfile.NamedTemporaryFile(delete=False)
    key_file.write(key.encode('utf-8'))
    key_file.close()

    command = "%s rsa -in %s -check -noout"
    code, out, error = pipe(command % (settings.OPENSSL_COMMAND,
                                       key_file.name))
    if code != 0:
        log("openssl error: %s:\n  Error %s: %s" %(command, code, error))        

    os.unlink(key_file.name)
    return (not error, error)


def validate_public_key(public_key):
    key_file = tempfile.NamedTemporaryFile(delete=False)
    for chunk in public_key.chunks():
        key_file.write(chunk)
    key_file.close()

    command = "%s x509 -in %s -noout"
    code, out, error = pipe(command % (settings.OPENSSL_COMMAND,
                                       key_file.name))
    if code != 0:
        log("openssl error: %s:\n  Error %s: %s" %(command, code, error))        

    os.unlink(key_file.name)
    return (not error, error)


def send_accept_reminder_to_nominee(nominee_position):
    today = datetime.date.today().strftime('%Y%m%d')
    subject = 'Reminder: please accept (or decline) your nomination.'
    domain = Site.objects.get_current().domain
    position = nominee_position.position
    nomcom = position.nomcom
    from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
    nomcom_template_path = '/nomcom/%s/' % nomcom.group.acronym
    mail_path = nomcom_template_path + NOMINEE_ACCEPT_REMINDER_TEMPLATE
    nominee = nominee_position.nominee
    (to_email, cc) = gather_address_lists('nomination_accept_reminder',nominee=nominee.email.address)

    hash = get_hash_nominee_position(today, nominee_position.id)
    accept_url = reverse('ietf.nomcom.views.process_nomination_status',
                          None,
                          args=(get_year_by_nomcom(nomcom),
                          nominee_position.id,
                          'accepted',
                          today,
                          hash))
    decline_url = reverse('ietf.nomcom.views.process_nomination_status',
                          None,
                          args=(get_year_by_nomcom(nomcom),
                          nominee_position.id,
                          'declined',
                          today,
                          hash))

    context = {'nominee': nominee.person.name,
               'position': position,
               'domain': domain,
               'accept_url': accept_url,
               'decline_url': decline_url,
               'year': nomcom.year(),
           }
    body = render_to_string(mail_path, context)
    path = '%s%d/%s' % (nomcom_template_path, position.id, QUESTIONNAIRE_TEMPLATE)
    body += '\n\n%s' % render_to_string(path, context)
    send_mail_text(None, to_email, from_email, subject, body, cc=cc)

def send_questionnaire_reminder_to_nominee(nominee_position):
    subject = 'Reminder: please complete the Nomcom questionnaires for your nomination.'
    domain = Site.objects.get_current().domain
    position = nominee_position.position
    nomcom = position.nomcom
    from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
    nomcom_template_path = '/nomcom/%s/' % nomcom.group.acronym
    mail_path = nomcom_template_path + NOMINEE_QUESTIONNAIRE_REMINDER_TEMPLATE
    nominee = nominee_position.nominee
    (to_email,cc) = gather_address_lists('nomcom_questionnaire_reminder',nominee=nominee.email.address)

    context = {'nominee': nominee.person.name,
               'position': position,
               'domain': domain,
               'year': nomcom.year(),
           }
    body = render_to_string(mail_path, context)
    path = '%s%d/%s' % (nomcom_template_path, position.id, QUESTIONNAIRE_TEMPLATE)
    body += '\n\n%s' % render_to_string(path, context)
    send_mail_text(None, to_email, from_email, subject, body, cc=cc)

def send_reminder_to_nominees(nominees,type):
    addrs = []
    if type=='accept':
        for nominee in nominees:
            for nominee_position in nominee.nomineeposition_set.pending():
                send_accept_reminder_to_nominee(nominee_position)
                addrs.append(nominee_position.nominee.email.address)
    elif type=='questionnaire':
        for nominee in nominees:
            for nominee_position in nominee.nomineeposition_set.accepted().without_questionnaire_response():
                send_questionnaire_reminder_to_nominee(nominee_position)
                addrs.append(nominee_position.nominee.email.address)
    return addrs


def make_nomineeposition(nomcom, candidate, position, author):
    from ietf.nomcom.models import Nominee, NomineePosition

    nomcom_template_path = '/nomcom/%s/' % nomcom.group.acronym

    # Add the nomination for a particular position
    nominee, created = Nominee.objects.get_or_create(person=candidate,email=candidate.email(), nomcom=nomcom)
    while nominee.duplicated:
        nominee = nominee.duplicated
    nominee_position, nominee_position_created = NomineePosition.objects.get_or_create(position=position, nominee=nominee)

    if nominee_position_created:
        # send email to nominee
        subject = 'IETF Nomination Information'
        from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
        (to_email, cc) = gather_address_lists('nomination_new_nominee',nominee=nominee.email.address)
        domain = Site.objects.get_current().domain
        today = datetime.date.today().strftime('%Y%m%d')
        hash = get_hash_nominee_position(today, nominee_position.id)
        accept_url = reverse('ietf.nomcom.views.process_nomination_status',
                              None,
                              args=(nomcom.year(),
                              nominee_position.id,
                              'accepted',
                              today,
                              hash))
        decline_url = reverse('ietf.nomcom.views.process_nomination_status',
                              None,
                              args=(nomcom.year(),
                              nominee_position.id,
                              'declined',
                              today,
                              hash))

        context = {'nominee': nominee.person.name,
                   'position': position.name,
                   'year': nomcom.year(),
                   'domain': domain,
                   'accept_url': accept_url,
                   'decline_url': decline_url,
               }

        path = nomcom_template_path + NOMINEE_EMAIL_TEMPLATE
        send_mail(None, to_email, from_email, subject, path, context, cc=cc)

        # send email to nominee with questionnaire
        if nomcom.send_questionnaire:
            subject = '%s Questionnaire' % position
            from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
            (to_email, cc) = gather_address_lists('nomcom_questionnaire',nominee=nominee.email.address)
            context = {'nominee': nominee.person.name,
                      'position': position.name,
                      'year'    : nomcom.year(),
                  }
            path = '%s%d/%s' % (nomcom_template_path,
                                position.id, HEADER_QUESTIONNAIRE_TEMPLATE)
            body = render_to_string(path, context)
            path = '%s%d/%s' % (nomcom_template_path,
                                position.id, QUESTIONNAIRE_TEMPLATE)
            body += '\n\n%s' % render_to_string(path, context)
            send_mail_text(None, to_email, from_email, subject, body, cc=cc)

    # send emails to nomcom chair
    subject = 'Nomination Information'
    from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
    (to_email, cc) = gather_address_lists('nomination_received',nomcom=nomcom)
    context = {'nominee': nominee.person.name,
               'nominee_email': nominee.email.address,
               'position': position.name,
               'year': nomcom.year(),
           }

    if author:
        context.update({'nominator': author.person.name,
                        'nominator_email': author.address})
    else:
        context.update({'nominator': 'Anonymous',
                        'nominator_email': ''})

    path = nomcom_template_path + NOMINATION_EMAIL_TEMPLATE
    send_mail(None, to_email, from_email, subject, path, context, cc=cc)

    return nominee

def make_nomineeposition_for_newperson(nomcom, candidate_name, candidate_email, position, author):

    # This is expected to fail if called with an existing email address
    email = Email.objects.create(address=candidate_email, origin="nominee: %s" % nomcom.group.acronym)
    person = Person.objects.create(name=candidate_name,
                                   ascii=unidecode_name(candidate_name),
                                   )
    email.person = person
    email.save()

    # send email to secretariat and nomcomchair to warn about the new person
    subject = 'New person is created'
    from_email = settings.NOMCOM_FROM_EMAIL.format(year=nomcom.year())
    (to_email, cc) = gather_address_lists('nomination_created_person',nomcom=nomcom)
    context = {'email': email.address,
               'fullname': email.person.name,
               'person_id': email.person.id,
               'year': nomcom.year(),
           }
    nomcom_template_path = '/nomcom/%s/' % nomcom.group.acronym
    path = nomcom_template_path + INEXISTENT_PERSON_TEMPLATE
    send_mail(None, to_email, from_email, subject, path, context, cc=cc)

    return make_nomineeposition(nomcom, email.person, position, author)

def getheader(header_text, default="ascii"):
    """Decode the specified header"""

    tuples = decode_header(header_text)
    header_sections = [ text.decode(charset or default) if isinstance(text, bytes) else text for text, charset in tuples]
    return "".join(header_sections)


def get_charset(message, default="ascii"):
    """Get the message charset"""

    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default


def get_body(message):
    """Get the body of the email message"""

    if message.is_multipart():
        # get the plain text version only
        text_parts = [part for part in typed_subpart_iterator(message,
                                                             'text',
                                                             'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(message)
            body.append(get_payload_text(part, default_charset=charset))

        return "\n".join(body).strip()

    else:  # if it is not multipart, the payload will be a string
           # representing the message body
        body = get_payload_text(message)
        return body.strip()


def parse_email(text):
    msg = message_from_string(force_str(text))

    body = get_body(msg)
    subject = getheader(msg['Subject'])
    __, addr = parseaddr(msg['From'])
    return addr.lower(), subject, body


def create_feedback_email(nomcom, msg):
    from ietf.nomcom.models import Feedback
    by, subject, body = parse_email(msg)
    #name, addr = parseaddr(by)

    feedback = Feedback(nomcom=nomcom,
                        author=by,
                        subject=subject or '',
                        comments=nomcom.encrypt(body))
    feedback.save()
    return feedback

class EncryptedException(Exception):
    pass

def previous_five_meetings(date = datetime.date.today()):
    return Meeting.objects.filter(type='ietf',date__lte=date).order_by('-date')[:5]

def three_of_five_eligible(date = datetime.date.today(), previous_five = None):
    """ Return a list of Person records who attended at least 
        3 of the 5 type_id='ietf' meetings before the given
        date. Does not disqualify anyone based on held roles.
    """
    # It would be nicer if this returned a queryset
    if not previous_five:
        previous_five = previous_five_meetings(date)
    attendees = {}
    potentials = set()
    for m in previous_five:
        registration_emails = m.meetingregistration_set.values_list('email',flat=True)
        attendees[m] = Person.objects.filter(email__address__in=registration_emails).distinct()
        # See RFC8713 section 4.15
        potentials.update(attendees[m])
    eligible_persons = []
    for p in potentials:
        count = 0
        for m in previous_five:
            if p in attendees[m]:
                count += 1
        if count >= 3:
            eligible_persons.append(p)  
    return eligible_persons

def iab_iesg(start_date, end_date):
    ''' Return a rough approximation of who was on either the IAB or IESG between the given dates. '''

    meeting_numbers = [int(m.number) for m in Meeting.objects.filter(type='ietf', date__gte=start_date) if m.end_date() <= end_date]

    # map of names to meeting numbers (more or less >=84 and <108) that the person was either on the IESG or IAB
    now = 109
    names = {
        'Dr. Bernard D. Aboba': [range(77,90)],
        'Jari Arkko': [range(84,87),range(87,99),range(99,now)],
        'Alia Atlas': [range(90,102)],
        'Ignas Bagdonas': [range(102,108)],
        'Mary Barnes': [range(89,96)],
        'Richard Barnes': [range(87,93)],
        'Marc Blanchet': [range(83,96)],
        'Ron Bonica': [range(69,87)],
        'Deborah Brungard': [range(93,now)],
        'Stewart Bryant': [range(78,90)],
        'Ross Callon': [range(77,90)],
        'Gonzalo Camarillo': [range(78,90)],
        'Ben Campbell': [range(93,105),range(107,now)],
        'Benoît Claise': [range(84,102)],
        'Alissa Cooper': [range(90,109)],
        'Roman Danyliw': [range(105,now)],
        'Spencer Dawkins': [range(77,87),range(87,105)],
        'Ralph Droms': [range(75,87),range(92,99)],
        'Martin Duke': [range(107,now)],
        'Wesley Eddy': [range(81,87)],
        'Adrian Farrel': [range(75,93)],
        'Stephen Farrell': [range(81,99),range(104,now)],
        'Brian Haberman': [range(84,96)],
        'Joel M. Halpern': [range(80,93)],
        'Ted Hardie': [range(89,96)],
        'Wes Hardaker': [range(104,now)],
        'Joe Hildebrand': [range(89,102)],
        'Russ Housley': [range(57,87),range(86,99)],
        'Lee Howard': [range(95,102)],
        'Christian Huitema': [range(101,108)],
        'Joel Jaeggli': [range(87,99)],
        'Cullen Jennings': [range(66,78),range(107,now)],
        'Benjamin Kaduk': [range(102,now)],
        'David Kessens': [range(80,87)],
        'Erik Kline': [range(107,now)],
        'Suresh Krishnan': [range(96,108)],
        'Murray Kucherawy': [range(107,now)],
        'Mirja Kühlewind': [range(96,now)],
        'Warren "Ace" Kumari': [range(99,now)],
        'Eliot Lear': [range(86,93)],
        'Barry Leiba': [range(84,96),range(105,now)],
        'Ted Lemon': [range(87,93)],
        'Zhenbin Li': [range(104,now)],
        'Xing Li': [range(86,93)],
        'Terry Manderson': [range(93,105)],
        'Jared Mauch': [range(107,now)],
        'Danny R. McPherson': [range(68,87)],
        'Alexey Melnikov': [range(75,81),range(96,108)],
        'Gabriel Montenegro': [range(98,105)],
        'Kathleen Moriarty': [range(90,102)],
        'Erik Nordmark': [range(86,108)],
        'Mark Nottingham': [range(98,now)],
        'Tommy Pauly': [range(107,now)],
        'Eric Rescorla': [range(99,105)],
        'Pete Resnick': [range(81,93)],
        'Jon Peterson': [range(74,89)],
        'Alvaro Retana': [range(93,now)],
        'Adam Roach': [range(99,108)],
        'Melinda Shore': [range(101,108)],
        'Robert Sparks': [range(75,87),range(92,105)],
        'Martin Stiemerling': [range(84,96)],
        'Andrew Sullivan': [range(86,99)],
        'Hannes Tschofenig': [range(77,90)],
        'Sean Turner': [range(78,90)],
        'Jeff Tantsura': [range(98,now)],
        'Martin Thomson': [range(95,108)],
        'Brian Trammell': [range(89,108)],
        'Martin Vigoureux': [range(102,now)],
        'Éric Vyncke': [range(105,now)],
        'Magnus Westerlund': [range(66,78),range(105,now)],
        'Robert Wilton': [range(107,now)],
        'Suzanne Woolf': [range(92,105)],
        'Jiankang Yao': [range(107,now)],
    }

    # This flattens the list of ranges into a list of numbers
    for name in names:
        names[name] = list(itertools.chain(*names[name]))

    assert len(Person.objects.filter(name__in=names.keys())) == len(names)

    name_in_range = [n for n in names if set(names[n])&set(meeting_numbers) ]

    return Person.objects.filter(name__in=name_in_range)

def actual_volunteers(year):

    volunteer_names = {
        2020: [
            'Melchior Aelmans',
            'Zafar Ali',
            'Ignas Bagdonas',
            'Fred Baker',
            'Sarah Banks',
            'Vishnu Pavan Beeram',
            'Lou Berger',
            'Vittorio Bertola',
            'Henk Birkholz',
            'Mike Bishop',
            'Matthew Bocci',
            'Ron Bonica',
            'Chris Bowers',
            'Stewart Bryant',
            'LucAndré Burdet',
            'Randy Bush',
            'Italo Busi',
            'Pablo Camarillo',
            'Daniele Ceccarelli',
            'Tommy Charles',
            'Mach Chen',
            'Huaimo Chen',
            'Uma Chunduri',
            'Laurent Ciavaglia',
            'Alexander Clemm',
            'Spencer Dawkins',
            'Dhruv Dhody',
            'Jie Dong',
            'Linda Dunbar',
            'Donald E. Eastlake 3rd',
            'Charles Eckel',
            'Toerless Eckert',
            'Lars Eggert',
            'Theresa Enghardt',
            'Dawei Fan',
            'Adrian Farrel',
            'Liang Geng',
            'Xuesong Geng',
            'Joey Salazar',
            'Bron Gondwana',
            'James Gruessing',
            'Jeffrey Haas',
            'Brian Haberman',
            'Wassim Haddad',
            'Phillip Hallam-Baker',
            'Dick Hardt',
            'Susan Hares',
            'Nick Harper',
            'Leif Hedstrom',
            'SHRADDHA HEGDE',
            'Bob Hinden',
            'Marco Hogewoning',
            'Christian Hopps',
            'Russ Housley',
            'Daniel Huang',
            'Christian Huitema',
            'Geoff Huston',
            'Luigi Iannone',
            'Jaehoon Jeong',
            'Yuanlong Jiang',
            'Jaime Jimenez',
            'Michael Jones',
            'Georgios Karagiannis',
            'Daniel King',
            'Dirk Kutscher',
            'David C Lawrence',
            'Eliot Lear',
            'Ted Lemon',
            'Cheng Li',
            'Guangpeng Li',
            'Yizhou Li',
            'Tony Li',
            'Bing Liu (Remy)',
            'Julien Maisonneuve',
            'Kiran Makhijani',
            'Allison Mankin',
            'Scott Mansfield',
            'Mark McFadden',
            'Patrick McManus',
            'George G. Michaelson',
            'Matthew A. Miller',
            'Greg Mirsky',
            'Mankamana Mishra',
            'Sanjay Mishra',
            'Tal Mizrahi',
            'Gabriel Montenegro',
            'Marie-Jose Montpetit',
            'Anthony Nadalin',
            'Yoav Nir',
            'Benno Overeinder',
            'Kirsty Paine',
            'Wei Pan',
            'Shuping Peng',
            'Tony Przygienda',
            'Yingzhen Qu',
            'Reshad Rahman',
            'Eric Rescorla',
            'Pete Resnick',
            'Michael Richardson',
            'Ines Robles',
            'Simon Pietro Romano',
            'Kyle Rose',
            'Brian Rosen',
            'David Schinazi',
            'Benjamin M. Schwartz',
            'John Scudder',
            'Göran Selander',
            'Yaron Sheffer',
            'Yimin Shen',
            'Valery Smyslov',
            'Job Snijders',
            'Haoyu Song',
            'Michael StJohns',
            'Ketan Talaulikar',
            'Darshak Thakore',
            'Martin Thomson',
            'Pascal Thubert',
            'Nathalie Trenaman',
            'Hannes Tschofenig',
            'Stig Venaas',
            'Rüdiger Volk',
            'Aijun Wang',
            'Tim Wattenberg',
            'YUEHUA (Corona) WEI',
            'Samuel Weiler',
            'Timothy Winters',
            'Christopher A. Wood',
            'Suzanne Woolf',
            'Bo Wu',
            'Qin Wu',
            'Min Xiao',
            'Jingrong Xie',
            'Quan Xiong',
            'GANG YAN',
            'Huaru Yang',
            'Jeffrey Yasskin',
            'XIANG YU',
            'Zhaohui (Jeffrey) Zhang',
            'Zheng Zhang',
            'Haomian Zheng',
            'Guangying Zheng',
            'Xingwang Zhou',
            'Shunwan Zhuang',
        ],
        2019: [
            'Adrian Farrel',
            'Alberto Rodriguez-Natal',
            'Alexander Clemm',
            'Allison Mankin',
            'Andrew Dolganow',
            'Andrew G. Malis',
            'Anthony Nadalin',
            'Ari Keränen',
            'Barbara Stark',
            'Benno Overeinder',
            'Benoît Claise',
            'Bernie Hoeneisen',
            'Bing (Leo) Liu',
            'Bing Liu (Remy)',
            'Bingyang Liu',
            'Bob Briscoe',
            'Börje Ohlman',
            'Brian Haberman',
            'Bron Gondwana',
            'Bryan Call',
            'Charles Eckel',
            'Charles E. Perkins',
            'Chris Seal',
            'Christer Holmberg',
            'Christian Hopps',
            'Christopher A. Wood',
            'Cullen Jennings',
            'Daniel King',
            'Daniel Migault',
            'Daniele Ceccarelli',
            'Darshak Thakore',
            'David Carrel',
            'David C Lawrence',
            'David Schinazi',
            'Dave Sinicrope',
            'Dean Bogdanović',
            'Desiree Miloshevic',
            'Dhruv Dhody',
            'Di Ma',
            'Dick Hardt',
            'Dirk Kutscher',
            'Donald E. Eastlake 3rd',
            'Eliot Lear',
            'Eric Gray',
            'Eric McMurry',
            'Eric Rescorla',
            'Fangwei Hu',
            'Francesca Palombini',
            'Fred Baker',
            'Gabriele Galimberti',
            'Geoff Huston',
            'George G. Michaelson',
            'Göran Selander',
            'Gonzalo Salgueiro',
            'Greg Mirsky',
            'Guangpeng Li',
            'Hannes Tschofenig',
            'Haomian Zheng',
            'Haoyu Song',
            'Henrik Levkowetz',
            'Hermin Anggawijaya',
            'Hirotaka Nakajima',
            'Huaimo Chen',
            'Huaru Yang',
            'Ian Duncan',
            'Ian Swett',
            'Ines Robles',
            'Italo Busi',
            'Jaime Jimenez',
            'Jared Mauch',
            'Jéferson Campos Nobre',
            'Jeffrey Haas',
            'Jie Dong',
            'Jim Fenton',
            'Job Snijders',
            'Joe Abley',
            'John Bradley',
            'John Drake',
            'John Mattsson',
            'John Scudder',
            'Joseph Lorenzo Hall',
            'Julien Maisonneuve',
            'Kiran Makhijani',
            'Kyle Rose',
            'Lars Eggert',
            'Laurent Ciavaglia',
            'Leif Hedstrom',
            'Li Qiang',
            'Li Yizhou',
            'Liang Geng',
            'Frank Xia',
            'Linda Dunbar',
            'Lixia Zhang',
            'Luigi Iannone',
            'Mach Chen',
            'Mallory Knodel',
            'Marie-Jose Montpetit',
            'Mark McFadden',
            'Mary Barnes',
            'Massimiliano Pala',
            'Matthew Bocci',
            'Matthew A. Miller',
            'Michael Richardson',
            'Michael StJohns',
            'Mike Bishop',
            'Mike Jones',
            'Mike McBride',
            'Min Xiao',
            'Min Ye',
            'Mingliang Pei',
            'Miya Kohno',
            'Mohamed Boucadair',
            'Mohit Sethi',
            'Murray Kucherawy',
            'Nick Harper',
            'Niels ten Oever',
            'Nik Teague',
            'Nils Ohlmeier',
            'Ole Trøan',
            'Ondřej Surý',
            'Padma Pillay-Esnault',
            'Pascal Thubert',
            'Patrick McManus',
            'Paul Wouters',
            'Pete Resnick',
            'Peter Lei',
            'Philipp S. Tiesel',
            'Rachel Huang',
            'Randy Bush',
            'Rick Taylor',
            'Ritesh Mukherjee',
            'Bob Hinden',
            'Robert Wilton',
            'Ron Bonica',
            "Ronald in 't Velt",
            'Dr. Ross Finlayson',
            'Russ Housley',
            'Salvatore Loreto',
            'Sam Aldrin',
            'Sandoche Balakrichenan',
            'Sanjay Mishra',
            'Sarah Banks',
            'Shraddha Hegde',
            'Shumon Huque',
            'Simon Pietro Romano',
            'Sri Gundavelli',
            'Stan Ratliff',
            'Stewart Bryant',
            'Stig Venaas',
            'Susan Hares',
            'Tal Mizrahi',
            'Ted Lemon',
            'Tianran Zhou',
            'Tim Wicinski',
            'Timothy Winters',
            'Toerless Eckert',
            'Tom Harrison',
            'Tommy Pauly',
            'Tony Przygienda',
            'Ulrich Wisser',
            'Uma Chunduri',
            'Vittorio Bertola',
            'Wassim Haddad',
            'Will LIU',
            'Yi Zhao',
            'Yingzhen Qu',
            'Yoav Nir',
            'Youenn Fablet',
            'Yuanlong Jiang',
            'Yutaka Oiwa',
            'Zafar Ali',
            'Zaheduzzaman Sarker',
            'Zhaohui (Jeffrey) Zhang',
            'Zhe Chen',
            'Zhen Cao',
            'Zheng Zhang',
            'Zitao Wang',
        ],
        2018:[
            'Aaron Falk',
            'Adam W. Montville',
            'Adrian Farrel',
            'Alexander Clemm',
            'Alia Atlas',
            'Andrew Dolganow',
            'Andrew Newton',
            'Andy Bierman',
            'Zaheduzzaman Sarker',
            'Anthony Nadalin',
            'Tony Przygienda',
            'Ari Keränen',
            'Barbara Stark',
            'Behcet Sarikaya',
            'Benno Overeinder',
            'Bernie Hoeneisen',
            'Bing Liu',
            'Bob Briscoe',
            'Börje Ohlman',
            'Bret Jordan',
            'Brian Rosen',
            'Bron Gondwana',
            'Bryan Call',
            'Carlos M. Martínez',
            'Charles Eckel',
            'Charles E. Perkins',
            'Christer Holmberg',
            'Christian Hopps',
            'Cullen Jennings',
            'Daniel C. Burnett',
            'Daniel King',
            'Daniele Ceccarelli',
            'Dapeng Liu',
            'Darshak Thakore',
            'David C Lawrence',
            'Dave Sinicrope',
            'Dean Bogdanović',
            'Dhruv Dhody',
            'Di Ma',
            'Dirk Kutscher',
            'Donald E. Eastlake 3rd',
            'Dragana Damjanovic',
            'Edward Lemon',
            'Eliot Lear',
            'Eric Gray',
            'Éric Vyncke',
            'Fangwei Hu',
            'Fernando Gont',
            'Francesca Palombini',
            'Francis Teague',
            'Fred Baker',
            'Frode Kileng',
            'Geoff Huston',
            'George G. Michaelson',
            'George Swallow',
            'Georgios Karagiannis',
            'Giuseppe Fioccola',
            'Glenn Parsons',
            'Gonzalo Salgueiro',
            'Göran Selander',
            'Greg Mirsky',
            'Haomian Zheng',
            'Harish Chowdhary',
            'Hermin Anggawijaya',
            'Hiroki Nakano',
            'Huaimo Chen',
            'Huaru Yang',
            'Ian Swett',
            'Jaime Jimenez',
            'Javier Salazar',
            'Jéferson Campos Nobre',
            'Jeffrey Haas',
            'Jie Dong',
            'Jim Guichard',
            'Jing Zuo',
            'Job Snijders',
            'Joel M. Halpern',
            'Joel Jaeggli',
            'John Bradley',
            'John Drake',
            'John Kaippallimalil',
            'John Mattsson',
            'John Scudder',
            'John Jason Brzozowski',
            'Jon Mitchell',
            'Jonathan Looney',
            'Joe Abley',
            'Joseph Lorenzo Hall',
            'Joe Hildebrand',
            'Juliao Braga',
            'Julien Maisonneuve',
            'Keyur Patel',
            'Kiran Makhijani',
            'Kyle Rose',
            'Laurent Ciavaglia',
            'Leif Hedstrom',
            'Leon Portman',
            'Li Qiang',
            'Liang Geng',
            'Liang Xia',
            'Linda Dunbar',
            'Lixia Zhang',
            'Luigi Iannone',
            'Mach Chen',
            'Marc Blanchet',
            'Margaret Cullen',
            'Maria Ines Robles',
            'Mark J Donnelly',
            'Mark Townsley',
            'Mary Barnes',
            'Matthew Bocci',
            'Matthew A. Miller',
            'Mike Bishop',
            'Michael Jones',
            'Michael Richardson',
            'Michael StJohns',
            'Mike McBride',
            'Min Ye',
            'Min Xiao',
            'Mingui Zhang',
            'Mohamed Boucadair',
            'Mohit Sethi',
            'Muhammad Sajjad Akbar',
            'Murray Kucherawy',
            'Nick Harper',
            'Nick Sullivan',
            'Niels ten Oever',
            'Nils Ohlmeier',
            'Ning Kong',
            'Ólafur Guðmundsson',
            'Ole J. Jacobsen',
            'Ondřej Surý',
            'Padma Pillay-Esnault',
            'Pascal Thubert',
            'Patrick McManus',
            'Patrick Wetterwald',
            'Paul E. Hoffman',
            'Paul Wouters',
            'Pete Resnick',
            'Philipp S. Tiesel',
            'Phil Sorber',
            'Qin Wu',
            'Randall R. Stewart',
            'Randy Bush',
            'Ranjeeth Dasineni',
            'Ritesh Mukherjee',
            'Rob Shakir',
            'Bob Hinden',
            'Robert Raszuk',
            'Ron Bonica',
            "Ronald in 't Velt",
            'Rong Gu',
            'Russ Housley',
            'Salvatore Loreto',
            'Sam Aldrin',
            'Sandoche Balakrichenan',
            'Sanjay Mishra',
            'Sarah Banks',
            'Sheng Jiang',
            'Shraddha Hegde',
            'Will (Shucheng) LIU',
            'Shumon Huque',
            'Shwetha Bhandari',
            'Simon Perreault',
            'Simon Pietro Romano',
            'Sri Gundavelli',
            'Stephan Wenger',
            'Stephen Farrell',
            'Stewart Bryant',
            'Stig Venaas',
            'Suhas Nandakumar',
            'Susan Hares',
            'Tal Mizrahi',
            'Thomas Fossati',
            'Tianran Zhou',
            'Tim Wicinski',
            'Timothy Terriberry',
            'Timothy Winters',
            'Tobias Gondrom',
            'Toerless Eckert',
            'Tom Herbert',
            'Tomohiro Fujisaki',
            'Uma Chunduri',
            'Vicky Risk',
            'Victor Kuarsingh',
            'Vishnu Pavan Beeram',
            'Wassim Haddad',
            'Xiaodong Duan',
            'Xiaodong Deng',
            'Xufeng Liu',
            'Zhuangyan',
            'Yi Zhao',
            'Yihong Huang',
            'Li Yizhou',
            'Yoav Nir',
            'Yuanlong Jiang',
            'Zhaohui (Jeffrey) Zhang',
            'Zhen Cao',
            'Zhenbin Li',
            'Zheng Zhang',
       ],
    }

    names = volunteer_names[year]

    people = Person.objects.filter(name__in=names)
    
    unmatched = set(names) - set(people.values_list('name',flat=True))
    if unmatched:
        debug.say("Warning: Can't match these names to Person records")
        debug.show('unmatched')
        """
            2019: unmatched: '{'Min Xiao', 'Bing (Leo) Liu', 'Fangwei Hu', 'Will LIU'}'
            2018: unmatched: '{'Min Xiao', 'Fangwei Hu', 'Xiaodong Deng', 'Edward Lemon', 'Francis Teague', 'Yihong Huang', 'Tomohiro Fujisaki', 'Harish Chowdhary'}'
        """

    return people

