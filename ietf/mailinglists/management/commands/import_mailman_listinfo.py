# Copyright The IETF Trust 2016, All Rights Reserved

import sys
from textwrap import dedent

import debug                            # pyflakes:ignore

from django.conf import settings
from django.core.management.base import BaseCommand

from ietf.mailinglists.models import List, Subscribed

class Command(BaseCommand):
    """
    Import list information from Mailman.

    Import announced list names, descriptions, and subscribers, by calling the
    appropriate Mailman functions and adding entries to the database.

    Run this from cron regularly, with sufficient permissions to access the
    mailman database files.

    """

    help = dedent(__doc__).strip()
            
    #option_list = BaseCommand.option_list + (       )

    def note(self, msg):    
        if self.verbosity > 1:
            self.stdout.write(msg)

    def handle(self, *filenames, **options):
        """

        * Import announced lists, with appropriate meta-information.

        * For each list, import the members.

        """

        self.verbosity = int(options.get('verbosity'))

        sys.path.append(settings.MAILMAN_LIB_DIR)

        from Mailman import Utils
        from Mailman import MailList

        for name in Utils.list_names():
            mlist = MailList.MailList(name, lock=False)
            self.note("List: %s" % mlist.internal_name())
            if mlist.advertised:
                list, created = List.objects.get_or_create(name=mlist.real_name, description=mlist.description, advertised=mlist.advertised)
                # The following calls return lowercased addresses
                members = mlist.getRegularMemberKeys() + mlist.getDigestMemberKeys()
                known = [ s.address for s in Subscribed.objects.filter(lists__name=name) ]
                for addr in members:
                    if not addr in known:
                        self.note("  Adding subscribed: %s" % (addr))
                        new, created = Subscribed.objects.get_or_create(address=addr)
                        new.lists.add(list)
