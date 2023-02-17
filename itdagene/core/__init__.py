import vobject


def vcard_string(person):
    """
    Helper function for vcard views. Accepts a 'person' object
    with certain attributes (firstname, lastname, email, phone, id)
    and returns a string containing serialized vCard data.
    """
    # vobject API is a bit verbose...
    v = vobject.vCard()
    v.add("n")
    v.n.value = vobject.vcard.Name(family=person.last_name, given=person.first_name)
    v.add("fn")
    v.fn.value = "%s %s" % (person.first_name, person.last_name)
    v.add("email")
    v.email.value = person.email
    v.add("tel")
    v.tel.value = person.phone
    v.tel.type_param = "WORK"
    output = v.serialize()
    return output
