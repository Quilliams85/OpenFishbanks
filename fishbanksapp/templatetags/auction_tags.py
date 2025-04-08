# In templatetags/auction_tags.py
from django import template
from django.utils import timezone
import datetime

register = template.Library()

@register.filter
def time_remaining(end_time):
    now = timezone.now()
    return end_time - now if end_time > now else None

@register.filter
def format_time_remaining(end_time):
    now = timezone.now()
    if end_time <= now:
        return "Auction ended"
    
    delta = end_time - now
    total_seconds = int(delta.total_seconds())
    
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)

@register.filter
def dict_get(d, key):
    return d.get(key)