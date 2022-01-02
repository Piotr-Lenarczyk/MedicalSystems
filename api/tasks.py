from api.models import Country
from api.serializers import request_currency_rate
import datetime


def update_rates():
    for country in Country.objects.all():
        country.rate = request_currency_rate(country.currency)
        country.last_update = datetime.datetime.now()
        country.save()
