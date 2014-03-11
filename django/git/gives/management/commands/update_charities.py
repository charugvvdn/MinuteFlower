import datetime

from django.core.management.base import BaseCommand

from minuteflower.philanthropedia import pull_charity_data
from minuteflower.gives.models import Charity


# Only updates charities that haven't updated within the last day
# unless 'all' is passed in.  Then, all charities are done.  We can
# also pass in a list of eins for specific charities.
class Command(BaseCommand):
    help = "Updates charity information from the Philanthropedia API"
    args = '<ein ein ...>'

    def handle(self, *args, **options):

        # top declaration
        options = {}

        # handles the setting of charity attributes
        def set_attribute(charity, val, data):
            # needed to flatten the reviews_ parts
            if isinstance(data, dict):
                for key in [x for x in data if (val + x) in options]:
                    set_attribute(charity, options[val + key][1], data[key])
            else:
                setattr(charity, val, data)

        def set_reviews(charity, reviews, review_list):
            section_opts = {
                'impact': 'IM',
                'strengths': 'ST',
                'areasForImprovement': 'AR',
            }

            # remove all reviews - they have no IDs
            charity.review_set.all().delete()

            # They give it to us in different formats...
            if isinstance(review_list, dict):
                for section in review_list:
                    review_type = section_opts[section]
                    for review_section in review_list[section]:
                        label = review_section['label']
                        for review in review_section['comments']:
                            expert_type = review['expertType']
                            comment = review['comment']
                            charity.review_set.create(
                                review_type=review_type, label=label,
                                expert_type=expert_type, comment=comment)
            elif isinstance(review_list, (list, tuple)):
                for comment in [x['comment'] for x in review_list]:
                    charity.review_set.create(
                        review_type='', label='',
                        expert_type='', comment=comment)

        # format: input attribute: function to call, output attribute
        options = {
            'name': (set_attribute, 'philanthropedia_name'),
            'publicReportPageUrl': (set_attribute, 'public_report_url'),
            'researhReportUrl': (set_attribute, 'research_url'),
            'thumbsDown': (set_attribute, 'thumbs_down'),
            'socialCause': (set_attribute, 'social_cause'),
            'reviewSummaries': (set_attribute, 'reviews_'),
            'reviews': (set_reviews, 'reviews'),
            'medalYear': (set_attribute, 'medal_year'),
            'guidestarOrgId': (set_attribute, 'guidestar_id'),
            'thumbsUp': (set_attribute, 'thumbs_up'),
            'medalUrl': (set_attribute, 'medal_url'),
            'orgType': (set_attribute, 'org_type'),
            'reviews_impact': (set_attribute, 'reviews_impact'),
            'reviews_strengths': (set_attribute, 'reviews_strengths'),
            'reviews_areasForImprovement': (set_attribute, 'reviews_toimprove'),
        }

        charity_update_days = 1
        # we can run it on a specific charity if we want
        if(len(args) > 0):
            if args[0] == 'all':
                charities = Charity.objects.exclude(ein='').exclude(
                    ein__isnull=True)
            else:
                charities = Charity.objects.filter(ein__in=args)
        else:
            charities = Charity.objects.exclude(ein='').exclude(
                ein__isnull=True).filter(last_updated__lt=(
                    datetime.datetime.utcnow() - datetime.timedelta(
                        days=charity_update_days)))

        for charity in charities:
            data = pull_charity_data(charity.ein)
            for key in [x for x in data if x in options]:
                options[key][0](charity, options[key][1], data[key])

            charity.last_updated = datetime.datetime.utcnow()
            charity.save()
