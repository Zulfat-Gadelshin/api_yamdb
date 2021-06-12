import datetime

from django.core.exceptions import ValidationError


def validtate_title_year(year):
    if year <= -4000 or year > datetime.date.today().year:
        raise ValidationError(f'{year} не подходит')
    return year
