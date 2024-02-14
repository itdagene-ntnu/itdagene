from vobject import vCard
from vobject.vcard import Name


def vcard_string(person) -> str:
    """Helper function for vcard views. Accepts a 'user' object with
    certain attributes (firstname, lastname, email, phone, id) and
    returns a string containing serialized vCard data.
    """
    # vobject API is a bit verbose...
    v_card = vCard()
    v_card.add("n")
    v_card.n.value = Name(family=person.last_name, given=person.first_name)
    v_card.add("fn")
    v_card.fn.value = f"{person.first_name} {person.last_name}"
    v_card.add("email")
    v_card.email.value = person.email
    v_card.add("tel")
    v_card.tel.value = str(person.phone)
    v_card.tel.type_param = "WORK"
    return v_card.serialize()
