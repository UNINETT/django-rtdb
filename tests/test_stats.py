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
    queues = ['alpha', 'beta', 'gamma']
    customfields = ['winter', 'spring', 'summer', 'fall']

    def setUp(self):
        self.alpha_cf_statuses = STATUSES * 1
        self.beta_cf_statuses = STATUSES * 2
        self.gamma_cf_statuses = STATUSES * 3

        alpha = QueueFactory(name='alpha')
        for s in self.alpha_cf_statuses:
            ticket = TicketFactory(queue=alpha, status=s)
            TicketCustomfieldValueFactory(ticket=ticket, customfield__name='winter')
        beta = QueueFactory(name='beta')
        for s in self.beta_cf_statuses:
            ticket = TicketFactory(queue=beta, status=s)
            TicketCustomfieldValueFactory(ticket=ticket, customfield__name='spring')
            TicketCustomfieldValueFactory(ticket=ticket, customfield__name='winter')
        gamma = QueueFactory(name='gamma')
        for s in self.gamma_cf_statuses:
            ticket = TicketFactory(queue=gamma, status=s)
            TicketCustomfieldValueFactory(ticket=ticket, customfield__name='summer')
            TicketCustomfieldValueFactory(ticket=ticket, customfield__name='fall')

    def test_get_stats_for_customfield(self):
        stats = get_stats_for_customfield()
        self.assertIsInstance(stats, dict)
        self.assertEqual(set(stats.keys()), set(self.customfields))
        for cf, stat in stats.items():
            del stat['content']
            self.assertEqual(stat, Counter(STATUSES))
