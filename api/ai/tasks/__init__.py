from celery import shared_task

from core.models import ProfileModel

@shared_task
def apply_cost_task(user_id, cost):
    profile = ProfileModel.objects.filter(user_id=user_id).first()
    profile.credit = profile.credit - cost
    profile.save()