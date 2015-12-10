from __future__ import unicode_literals

import factory
from faker import Factory as Faker

from rtdb.models import Customfield
from rtdb.models import Queue
from rtdb.models import Ticket
from rtdb.models import TicketCustomfieldValue

__all__ = [
    'QueueFactory',
    'TicketFactory',
]


fake = Faker.create()

class QueueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Queue

    name = factory.LazyAttribute(lambda t: fake.name())
    initialpriority = 0
    finalpriority = 0
    defaultduein = 0
    creator = 0
    lastupdatedby = 0
    disabled = 0


class TicketFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Ticket

    effectiveid = 0
    queue = factory.SubFactory(QueueFactory)
    issuestatement = 0
    resolution = 0
    owner = 0
    initialpriority = 0
    finalpriority = 0
    priority = 0
    timeestimated = 0
    timeworked = 0
    status = factory.LazyAttribute(lambda t: fake.tld())
    timeleft = 0
    lastupdatedby = 0
    creator = 0
    disabled = 0


class CustomfieldFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Customfield

    name = factory.LazyAttribute(lambda t: fake.tld())
    sortorder = 0
    creator = 0
    lastupdatedby = 0
    disabled = 0
    lookuptype = 'RT::Queue-RT::Ticket'


class TicketCustomfieldValueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TicketCustomfieldValue

    ticket = factory.SubFactory(TicketFactory)
    customfield = factory.SubFactory(CustomfieldFactory)
    content = factory.LazyAttribute(lambda t: fake.domain_name())
    creator = 0
    lastupdatedby = 0
    objecttype = 'RT::Ticket'
    sortorder = 0
    disabled = 0

