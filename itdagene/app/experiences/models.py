from django.db.models import (
    CASCADE,
    DateField,
    ForeignKey,
    PositiveIntegerField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from itdagene.core.models import BaseModel, Preference


BOARD_POSITION = (
    (0, "Leder"),
    (1, "Nestleder"),
    (2, "Okonomi"),
    (3, "Bedriftskontaktansvarlig"),
    (4, "Logistikk"),
    (5, "Markedsforing"),
    (6, "Web"),
    (7, "Bankett"),
    (8, "Bedriftskontakt"),
)


class Experience(BaseModel):
    year = ForeignKey(Preference, verbose_name=_("Preference"), on_delete=CASCADE)
    position = PositiveIntegerField(
        choices=BOARD_POSITION, default=8, verbose_name=_("Position")
    )
    last_updated = DateField(auto_now=True)
    text = TextField(blank=True, null=True, verbose_name=_("Experiences"))

    def __str__(self) -> str:
        return BOARD_POSITION[self.position][1]
