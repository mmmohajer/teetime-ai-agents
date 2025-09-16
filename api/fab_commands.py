from fabric import task

from config.utils.role_based import build_group_list
from core.utils.test import test_core_utils
from ai.utils.test import test_ai_manager

@task
def buildgrouplist(ctx):
    build_group_list()


# --------------------------------------------
# Testing Tasks Beginning
# --------------------------------------------
@task
def testaimanager(ctx):
    test_ai_manager()

@task
def testcoreutils(ctx):
    test_core_utils()
# --------------------------------------------
# Testing Tasks Ending
# --------------------------------------------