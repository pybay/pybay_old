from django.template import Library
from django.conf import settings

from symposion.schedule.models import Presentation, Slot

import logging


register = Library()
log = logging.getLogger(__name__)


@register.simple_tag
def slot_desc(talk):
    try:
        slot = talk.presentation.slot
    except (Presentation.DoesNotExist, Slot.DoesNotExist):
        log.error("Talk %s does not have a slot", talk.name)
        slot = None

    if slot is None:
        return None

    return "{} | {}-{} | {}".format(
        slot.day.date.strftime("%-m/%-d/%Y"), slot.start.strftime("%-I:%M %p"),
        slot.end.strftime("%-I:%M %p"), slot.rooms[0],
    )
