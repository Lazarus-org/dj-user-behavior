from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EventType(TextChoices):
    CLICK = "click", _("Click")
    SCROLL = "scroll", _("Scroll")
    MOUSE_MOVE = "mouse_move", _("Mouse Move")
    FORM_SUBMIT = "form_submit", _("Form Submit")
    INPUT_CHANGE = "input_change", _("Input Change")
    PAGE_RESIZE = "page_resize", _("Page Resize")
    KEYPRESS = "keypress", _("Key Press")
    HOVER = "hover", _("Hover")
