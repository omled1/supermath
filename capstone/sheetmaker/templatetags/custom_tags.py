from django import template
from datetime import datetime
from dateutil import tz
import time

register = template.Library()

@register.filter
def action(user):
    pass

@register.filter
def test(var):
    print(type(var))
    return var

@register.filter
def toLocalDateTime(dt):
    dt1 = utc2local(dt)
    print(dt, dt1)
    print('timezone,', dt.tzinfo)
    return dt1

def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset
    