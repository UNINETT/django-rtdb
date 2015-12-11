from __future__ import unicode_literals

from collections import Counter

from django.test import TestCase

import factory
from faker import Factory as Faker

from rtdb.stats import (
        get_statuses,
        get_queues,
        get_stats_for_queue,
        get_stats_for_customfield
)

from .factories import TicketFactory
from .factories import QueueFactory
from .factories import TicketCustomfieldValueFactory


STATUSES = ('open', 'resolved')


class StatusTestCase(TestCase):
    statuses = STATUSES

    def setUp(self):
        queue = QueueFactory()
        for s in self.statuses:
            TicketFactory(queue=queue, status=s)

    def test_get_statuses(self):
        statuses = get_statuses()
        self.assertEqual(set(statuses), set(self.statuses))

class QueueTestCase(TestCase):
    queues = ['alpha', 'beta', 'gamma']

    def setUp(self):
        for q in self.queues:
            QueueFactory(name=q)

    def test_get_queues(self):
        queues = get_queues()
        self.assertEqual([q.name for q in queues], self.queues)


class StatsForQueueTestCase(TestCase):
    queues = ['alpha', 'beta', 'gamma']

    def setUp(self):
        self.alpha_queue_statuses = STATUSES * 3
        self.beta_queue_statuses = STATUSES * 4
        self.gamma_queue_statuses = STATUSES * 5

        alpha = QueueFactory(name='alpha')
        for s in self.alpha_queue_statuses:
            TicketFactory(queue=alpha, status=s)
        beta = QueueFactory(name='beta')
        for s in self.beta_queue_statuses:
            TicketFactory(queue=beta, status=s)
        gamma = QueueFactory(name='gamma')
        for s in self.gamma_queue_statuses:
            TicketFactory(queue=gamma, status=s)

    def test_get_stats_for_queue_one(self):
        stats = get_stats_for_queue(['alpha'])
        self.assertEqual(type({}), type(stats))
        self.assertIn('alpha', stats)
        self.assertEqual(stats['alpha'], Counter(self.alpha_queue_statuses))

    def test_get_stats_for_queue_all(self):
        stats = get_stats_for_queue()
        self.assertIsInstance(stats, dict)
        self.assertEqual(set(stats.keys()), set(self.queues))
        self.assertEqual(stats['beta'], Counter(self.beta_queue_statuses))
        self.assertEqual(stats['gamma'], Counter(self.gamma_queue_statuses))

class StatsForCustomFieldsTestCase(TestCase):
    customfields = ['alpha', 'omega']
    statuses = ('new', 'open', 'closed')

    def setUp(self):
        queue = QueueFactory()

        self.alpha_cf = {
                'thing1': ['new'],
                'thing2': ['new', 'new', 'open'],
                'thing3': ['closed', 'new', 'open'],
        }
        self.omega_cf = {
                'thing4': ['open', 'open', 'open', 'open'],
        }
        for content, statuses in self.alpha_cf.items():
            for s in statuses:
                ticket = TicketFactory(queue=queue, status=s)
                TicketCustomfieldValueFactory(ticket=ticket, customfield__name='alpha', content=content)
        for content, statuses in self.omega_cf.items():
            for s in statuses:
                ticket = TicketFactory(queue=queue, status=s)
                TicketCustomfieldValueFactory(ticket=ticket, customfield__name='omega', content=content)

    def test_get_stats_for_customfield(self):
        stats = get_stats_for_customfield()
        self.assertIsInstance(stats, dict)
        self.assertEqual(set(stats.keys()), set(self.customfields))
        for content, data in stats['alpha'].items():
            self.assertEqual(Counter(self.alpha_cf[content]), data)
        for content, data in stats['omega'].items():
            self.assertEqual(Counter(self.omega_cf[content]), data)
