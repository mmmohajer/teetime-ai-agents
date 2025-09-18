from celery import shared_task

from core.models import UserModel, ProfileModel
from ai.models import AiCostModel

@shared_task
def apply_cost_task(user_ids, cost, service):
    if cost > 0:
        if user_ids:
            for user_id in user_ids:
                cur_profile = ProfileModel.objects.filter(user_id=user_id).first()
                cur_profile.credit = cur_profile.credit - (cost / len(user_ids))
                cur_profile.save()
                
                cur_cost = AiCostModel()
                cur_cost.user_id = user_id
                cur_cost.cost = cost / len(user_ids)
                cur_cost.service = service
                cur_cost.save()
        else:
            cur_cost = AiCostModel()
            cur_cost.cost = cost
            cur_cost.service = service
            cur_cost.save()