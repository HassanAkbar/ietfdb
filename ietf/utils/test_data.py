from ietf.idtracker.models import IESGLogin, PersonOrOrgInfo, EmailAddress
from ietf.iesg.models import TelechatDates, WGAction
from redesign.doc.models import *
from redesign.name.models import *
from redesign.group.models import *
from redesign.person.models import *

def make_test_data():
    # groups
    area = Group.objects.create(
        name="Far Future",
        acronym="farfut",
        state_id="active",
        type_id="area",
        parent=None)
    group = Group.objects.create(
        name="Martian Special Interest Group",
        acronym="mars",
        state_id="active",
        type_id="wg",
        parent=area,
        )
    
    # persons
    Email.objects.get_or_create(address="(System)")

    # ad
    p = Person.objects.create(
        name="Aread Irector",
        ascii="Aread Irector",
        )
    ad = Email.objects.create(
        address="aread@ietf.org",
        person=p)
    Role.objects.create(
        name_id="ad",
        group=area,
        email=ad)
    porg = PersonOrOrgInfo.objects.create(
        first_name="Aread",
        last_name="Irector",
        middle_initial="",
        )
    EmailAddress.objects.create(
        person_or_org=porg,
        priority=1,
        address=ad.address,
        )
    IESGLogin.objects.create(
        login_name="ad",
        password="foo",
        user_level=1,
        first_name=porg.first_name,
        last_name=porg.last_name,
        person=porg,
        )

    # create a bunch of ads for swarm tests
    for i in range(1, 10):
        p = Person.objects.create(
            name="Ad No%s" % i,
            ascii="Ad No%s" % i,
            )
        email = Email.objects.create(
            address="ad%s@ietf.org" % i,
            person=p)
        Role.objects.create(
            name_id="ad" if i <= 5 else "ex-ad",
            group=area,
            email=email)
        porg = PersonOrOrgInfo.objects.create(
            first_name="Ad",
            last_name="No%s" % i,
            middle_initial="",
            )
        EmailAddress.objects.create(
            person_or_org=porg,
            priority=1,
            address=ad.address,
            )
        IESGLogin.objects.create(
            login_name="ad%s" % i,
            password="foo",
            user_level=1,
            first_name=porg.first_name,
            last_name=porg.last_name,
            person=porg,
            )

    # group chair
    p = Person.objects.create(
        name="WG Chair Man",
        ascii="WG Chair Man",
        )
    wgchair = Email.objects.create(
        address="wgchairman@ietf.org",
        person=p)
    Role.objects.create(
        name=RoleName.objects.get(slug="chair"),
        group=group,
        email=wgchair,
        )
    
    # secretary
    p = Person.objects.create(
        name="Sec Retary",
        ascii="Sec Retary",
        )
    Email.objects.create(
        address="sec.retary@ietf.org",
        person=p)
    porg = PersonOrOrgInfo.objects.create(
        first_name="Sec",
        last_name="Retary",
        middle_initial="",
        )
    EmailAddress.objects.create(
        person_or_org=porg,
        priority=1,
        address="sec.retary@ietf.org",
        )
    IESGLogin.objects.create(
        login_name="secretary",
        password="foo",
        user_level=0,
        first_name=porg.first_name,
        last_name=porg.last_name,
        person=porg,
        )
    
    # draft
    draft = Document.objects.create(
        name="draft-ietf-test",
        time=datetime.datetime.now(),
        type_id="draft",
        title="Optimizing Martian Network Topologies",
        state_id="active",
        iesg_state_id="pub-req",
        stream_id="ietf",
        group=group,
        abstract="Techniques for achieving near-optimal Martian networks.",
        rev="01",
        pages=2,
        intended_std_level_id="ps",
        ad=ad,
        notify="aliens@example.mars",
        note="",
        )

    DocAlias.objects.create(
        document=draft,
        name=draft.name,
        )

    DocumentAuthor.objects.create(
        document=draft,
        author=Email.objects.get(address="aread@ietf.org"),
        order=1
        )

    # draft has only one event
    Event.objects.create(
        type="started_iesg_process",
        by=ad,
        doc=draft,
        desc="Added draft",
        )
    
    # telechat dates
    t = datetime.date.today()
    dates = TelechatDates(date1=t,
                          date2=t + datetime.timedelta(days=7),
                          date3=t + datetime.timedelta(days=14),
                          date4=t + datetime.timedelta(days=21),
                          )
    super(dates.__class__, dates).save(force_insert=True) # work-around hard-coded save block

    # WG Actions
    group = Group.objects.create(
        name="Asteroid Mining Equipment Standardization Group",
        acronym="ames",
        state_id="proposed",
        type_id="wg",
        parent=area,
        )
    WGAction.objects.create(
        pk=group.pk,
        note="",
        status_date=datetime.date.today(),
        agenda=1,
        token_name="Aread",
        category=13,
        telechat_date=dates.date2
        )
    
    return draft
