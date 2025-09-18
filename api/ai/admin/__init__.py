from django.contrib import admin

from ai.models import AiCostModel
from ai.admin import ai_cost

admin.site.register(AiCostModel, ai_cost.AiCostAdmin)
