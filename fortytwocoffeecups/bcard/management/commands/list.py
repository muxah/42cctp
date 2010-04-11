from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    statement = 'All project models with number of objects in each'
    help = "Prints %s." % statement.lower()

    def handle(self, **options):
        print '\n\t%s:\n' % Command.statement

        for ct in ContentType.objects.all():
            name = ct.model.capitalize()
            amount = len(ct.model_class().objects.all())

            print "\t%s (%d)" % (name, amount)

        print
