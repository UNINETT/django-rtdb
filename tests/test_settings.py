from __future__ import unicode_literals

from django.test.runner import DiscoverRunner

# Virtual tables: views, multiple django models for one underlying table, etc.
VIRTUAL_TABLES = []


class UnManagedModelTestRunner(DiscoverRunner):
    '''
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run.
    Many thanks to the Caktus Group: http://bit.ly/1N8TcHW
    '''

    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        self.unmanaged_models = [m for m in apps.get_models()
                if not m._meta.managed and m.__name__ not in VIRTUAL_TABLES]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'rtdb',
    'tests',
]

TEST_RUNNER = 'tests.test_settings.UnManagedModelTestRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
