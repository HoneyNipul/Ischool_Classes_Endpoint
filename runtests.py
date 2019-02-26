#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.sys.path.insert(0, os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = 'ischool_classes.settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["ischool_classes"])
sys.exit(bool(failures))