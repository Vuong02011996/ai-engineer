from odmantic import Model


class PersonImage(Model):
    person_id: str
    url: str
    name: str
