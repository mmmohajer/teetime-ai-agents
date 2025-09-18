from fabric import task

from config.utils.role_based import build_group_list
from core.utils.test import test_core_utils
from ai.utils.test import test_ai_manager
from customer_support.utils.test import test_customer_support_utils
from customer_support.utils.knowledge_base import add_zoho_desk_tickets_to_db, add_zoho_desk_tickets_to_kb
from customer_support.utils.teetime_agent_manager import TeeTimeSupportAgent

@task
def buildgrouplist(ctx):
    """Build the group list for role-based tasks."""
    build_group_list()

@task
def addzohodesktodb(ctx):
    """Add Zoho Desk tickets to the database."""
    add_zoho_desk_tickets_to_db()

@task
def addzohodesktokb(ctx):
    """Add Zoho Desk tickets to the knowledge base."""
    add_zoho_desk_tickets_to_kb()

@task
def buildpredfinedmessages(ctx):
    """Build predefined messages for the TeeTimeSupportAgent."""
    agent = TeeTimeSupportAgent(session_id="")
    agent.build_pre_defined_messages()

# --------------------------------------------
# Testing Tasks Beginning
# --------------------------------------------
@task
def testaimanager(ctx):
    test_ai_manager()

@task
def testcoreutils(ctx):
    test_core_utils()

@task
def testcustomersupportutils(ctx):
    test_customer_support_utils()
# --------------------------------------------
# Testing Tasks Ending
# --------------------------------------------