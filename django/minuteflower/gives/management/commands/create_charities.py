from django.core.management.base import BaseCommand, CommandError

from minuteflower.gives.models import Charity, Category, Flower


class Command(BaseCommand):
    help = "Creates several charities"

    def handle(self, *args, **options):

        education = Category(name='Education', color='#e5a380', image='/tmpimg/education.png')
        education.save()

        art = Category(name='Art', color='#8197ac', image='/tmpimg/art.png')
        art.save()

        health = Category(name='Health', color='#d36e66', image='/tmpimg/health.png')
        health.save()

        planet = Category(name='Planet', color='#9ba850', image='/tmpimg/planet.png')
        planet.save()

        poverty = Category(name='Poverty', color='#f8d33c', image='/tmpimg/poverty.png')
        poverty.save()

        veterans = Category(name='Veterans', color='#a97695', image='/tmpimg/veterans.png')
        veterans.save()

        c = Charity(
            name='Teach For America',
            description='TFA is a national teacher corps of recent ' +
                'college graduates',
            paypal_email='tfa_1335157775_per@gmail.com',
            category=education,
        )
        c.image = '/tmpimg/tfa.png'
        c.save()

        Charity(
            name='Wikimedia Foundation',
            description='Imagine a world in which every single human ' +
                 'being can freely share in the sum of all knowledge.',
            paypal_email='test@paypal.com',
            category=art,
        ).save()

        Charity(
            name='Cancer Research UK',
            description='Cancer Research UK, the UK\'s leading cancer charity.',
            paypal_email='test@paypal.com',
            category=health
        ).save()

        Charity(
            name='Green Peace',
            description='Greenpeace is the leading independent campaigning organization',
            paypal_email='test@paypal.com',
            category=planet
        ).save()

        Charity(
            name='CARE',
            description='CARE is a leading humanitarian organization fighting global poverty.',
            paypal_email='test@paypal.com',
            category=poverty
        ).save()

        Charity(
            name='Disabled American Veterans',
            description='Building Better Lives for America\'s Disabled Veterans.',
            paypal_email='test@paypal.com',
            category=veterans
        ).save()

        Flower(
                name='Flower Power',
                rule='Give.objects.filter(user=user).count() > 1',
                ).save()
        Flower(
                name='Power Flower',
                rule='sum([g.time_to_present() for g in Give.objects.filter(user=user)]) > 15',
                ).save()
