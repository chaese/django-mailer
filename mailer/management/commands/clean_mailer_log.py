import logging
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import connection

from mailer.models import MessageLog


class Command(NoArgsCommand):
    help = "Clean the message log table."
    base_options = (
        make_option(
            '-c', '--cron', default=0, type='int',
            help='If 1 don\'t print messages, but only errors.'
        ),
    )
    option_list = NoArgsCommand.option_list + base_options

    def handle_noargs(self, **options):
        if options['cron'] == 0:
            logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        else:
            logging.basicConfig(level=logging.ERROR, format="%(message)s")
        all_messages = MessageLog.objects.all()
        logging.debug("Deleting %d message log objects..." % len(all_messages))
        all_messages.delete()
        logging.debug("Done.")
        connection.close()
