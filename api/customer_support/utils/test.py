from customer_support.utils.connection_config import ConnectionConfigManager
from customer_support.utils.zoho_desk import ZohoDeskManager

def test_conn_manager():
    conn_manager = ConnectionConfigManager()
    res = conn_manager.send_zoho_desk_req(zoho_endpoint=f"tickets?limit={10}&from={1}", method="GET")
    print("Connection Config Manager Test Response:", res)

def test_zoho_desk_manager():
    zoho_desk_manager = ZohoDeskManager()
    # tickets = zoho_desk_manager.get_all_tickets()
    # print("Zoho Desk Manager All Tickets:", tickets)
    # cur_ticket = zoho_desk_manager.get_ticket_details(ticket_id="852042000031219787")
    # print("Zoho Desk Manager Ticket Details:", cur_ticket)
    zoho_desk_manager._add_zoho_ticket_info_to_kb("852042000026668511")

def test_customer_support_utils():
    test_zoho_desk_manager()