SHELL := /bin/sh

APP := rtdb

LOCALPATH := ./src
PYTHONPATH := $(LOCALPATH)/
SETTINGS := production
DJANGO_SETTINGS_MODULE = $(APP).settings.$(SETTINGS)
DJANGO_POSTFIX := --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_TEST_SETTINGS_MODULE = "tests.test_settings"
DJANGO_POSTFIX := --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
PYTHON_BIN := $(VIRTUAL_ENV)/bin

.PHONY: clean showenv coverage test bootstrap pip virtualenv sdist virtual_env_set

.DEFAULT: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $@ $(DJANGO_LOCAL_POSTFIX)

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@$(PYTHON_BIN)/python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'APP:' $(APP)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)

showenv.all: showenv showenv.virtualenv showenv.site

showenv.virtualenv: virtual_env_set
	PATH := $(VIRTUAL_ENV)/bin:$(PATH)
	export $(PATH)
	@echo 'VIRTUAL_ENV:' $(VIRTUAL_ENV)
	@echo 'PATH:' $(PATH)

showenv.site: site_set
	@echo 'SITE:' $(SITE)

cmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_POSTFIX)

rsync:
	rsync -avz --checksum --exclude-from .gitignore --exclude-from .rsyncignore . ${REMOTE_URI}

compare:
	rsync -avz --checksum --dry-run --exclude-from .gitignore --exclude-from .rsyncignore . ${REMOTE_URI}

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf build
	rm -rf dist

test: clean
	$(PYTHON_BIN)/python runtests.py

coverage: clean virtual_env_set
	-$(PYTHON_BIN)/coverage run $(PYTHON_BIN)/python runtests.py
	-$(PYTHON_BIN)/coverage html --include="$(LOCALPATH)/*" --omit="*/admin.py,*/test*"

predeploy: test

register: virtual_env_set
	python setup.py register

sdist: virtual_env_set
	python setup.py sdist

upload: sdist virtual_env_set
	python setup.py upload
	make clean

bootstrap: virtualenv pip virtual_env_set

pip: requirements/$(SETTINGS).txt virtual_env_set
	pip install -r requirements/$(SETTINGS).txt

virtualenv:
	virtualenv --no-site-packages $(VIRTUAL_ENV)
	echo $(VIRTUAL_ENV)
