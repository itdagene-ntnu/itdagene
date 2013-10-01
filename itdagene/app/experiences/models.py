from django.db import models
from itdagene.core.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from itdagene.core.models import Preference

BOARD_POSITION = (
    (0, 'Leder'),
    (1, 'Nestleder'),
    (2, 'Okonomi'),
    (3, 'Bedriftskontaktansvarlig'),
    (4, 'Logistikk'),
    (5, 'Markedsforing'),
    (6, 'Web'),
    (7, 'Bankett'),
    (8, 'Bedriftskontakt'),
)

PREF = Preference.objects.get(active=True)

class Experience(BaseModel):
	year = models.DateField(auto_now_add=True)
	position = models.PositiveIntegerField(choices=BOARD_POSITION, default=8, verbose_name=_('Position'))
	last_updated = models.DateField(auto_now=True)
	text = models.TextField(blank=True, null=True, verbose_name=_('Experiences'))

	def __unicode__(self):
		return str(BOARD_POSITION[self.position][1])
