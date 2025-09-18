from core.models import UserModel
from customer_support.utils.zoho_desk import ZohoDeskManager

def add_zoho_desk_tickets_to_db():
    cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
    zoho_desk_manager = ZohoDeskManager(cur_users=[cur_user])
    zoho_desk_manager.get_all_tickets()

def add_zoho_desk_tickets_to_kb():
    cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
    zoho_desk_manager = ZohoDeskManager(cur_users=[cur_user])
    zoho_desk_manager.add_zoho_tickets_info_to_kb()