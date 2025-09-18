from django.conf import settings

from ai.utils.open_ai_manager import OpenAIManager
from customer_support.models import ZohoDeskTicketModel, CustomerSupportKnowledgeBaseModel, CustomerSupportKnowledgeBaseChunkModel
from customer_support.utils.connection_config import ConnectionConfigManager


class ZohoDeskManager:
    def __init__(self, cur_users=[]):
        """
        Initializes the ZohoDeskManager with a connection manager and OpenAI manager.

        Example:
            manager = ZohoDeskManager()
        """
        self.conn_manager = ConnectionConfigManager()
        self.open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY, cur_users=cur_users)

    def _get_paginated_tickets(self, limit=10, from_record=0):
        """
        Fetches a paginated list of ticket metadata from Zoho Desk.

        Args:
            limit (int): Number of tickets to fetch per page.
            from_record (int): Offset for pagination.

        Returns:
            list: List of ticket metadata dictionaries.

        Example:
            tickets = self._get_paginated_tickets(limit=50, from_record=0)
        """
        endpoint = f"tickets?limit={limit}&from={from_record}"
        res = self.conn_manager.send_zoho_desk_req(zoho_endpoint=endpoint, method="GET")
        if not res["success"]:
            print(f"❌ {res['message']}")
            return []
        return res["data"]

    def _get_threads_list(self, ticket_id):
        """
        Fetches thread metadata (summary, ids) for a given ticket.

        Args:
            ticket_id (str): The ID of the ticket.

        Returns:
            list: List of thread metadata dictionaries.

        Example:
            threads = self._get_threads_list(ticket_id="123456789")
        """
        endpoint = f"tickets/{ticket_id}/threads"
        res = self.conn_manager.send_zoho_desk_req(zoho_endpoint=endpoint, method="GET")
        if not res["success"]:
            print(f"❌ {res['message']}")
            return []
        return res["data"]

    def _get_thread_details(self, ticket_id, thread_id):
        """
        Fetches full details for a single thread, including content and attachments.

        Args:
            ticket_id (str): The ID of the ticket.
            thread_id (str): The ID of the thread.

        Returns:
            dict or None: Thread details dictionary, or None if not found.

        Example:
            thread = self._get_thread_details(ticket_id="123", thread_id="456")
        """
        endpoint = f"tickets/{ticket_id}/threads/{thread_id}"
        res = self.conn_manager.send_zoho_desk_req(zoho_endpoint=endpoint, method="GET")
        if not res["success"]:
            print(f"❌ Failed to fetch thread {thread_id}: {res['message']}")
            return None
        return res["data"]

    def _get_ticket_details(self, ticket_id):
        """
        Fetches all threads for a ticket, including full content and attachments for each thread.

        Args:
            ticket_id (str): The ID of the ticket.

        Returns:
            list: List of thread detail dictionaries for the ticket.

        Example:
            details = self._get_ticket_details(ticket_id="123456789")
        """
        threads = self._get_threads_list(ticket_id)
        full_threads = []
        for t in threads:
            thread_id = t.get("id")
            if not thread_id:
                continue
            full_thread = self._get_thread_details(ticket_id, thread_id)
            if full_thread:
                full_threads.append(full_thread)
        return full_threads

    def get_all_tickets(self, limit=100, from_record=0):
        """
        Fetches all tickets (paginated) and saves their full thread details to the database.

        Args:
            limit (int): Number of tickets to fetch per page. Default is 2.
            from_record (int): Offset for pagination. Default is 0.

        Returns:
            set: Set of processed ticket IDs.

        Example:
            ticket_ids = self.get_all_tickets(limit=10)
        """
        ticket_ids = set()
        round = 0
        while True:
            round += 1
            print(f"Fetching tickets, round {round} ...")
            tickets = self._get_paginated_tickets(limit=limit, from_record=from_record)
            if not tickets:
                break
            for idx, ticket in enumerate(tickets, start=1):
                print(f"Processing ticket {idx}/{len(tickets)} in this round ...")
                ticket_id = str(ticket.get("id"))
                if not ticket_id or ticket_id in ticket_ids:
                    continue
                ticket_ids.add(ticket_id)
                ticket_details = self._get_ticket_details(ticket_id=ticket_id)
                if ticket_details:
                    cur_ticket = ZohoDeskTicketModel.objects.filter(ticket_id=ticket_id).first()
                    if not cur_ticket:
                        cur_ticket = ZohoDeskTicketModel(ticket_id=ticket_id)
                    cur_ticket.details = ticket_details
                    cur_ticket.save()
            from_record += limit
            if len(tickets) < limit:
                break
        return ticket_ids
    
    def _add_zoho_ticket_info_to_kb(self, ticket_id):
        """
        Uses OpenAI to generate a complete explanation/summary of a Zoho Desk ticket's issue and how it was handled.
        The summary is intended for future retrieval and similarity search, so similar issues can be quickly found and referenced for new customer requests.

        Args:
            ticket_id (str): The ID of the Zoho Desk ticket.

        Example:
            self._add_zoho_tickets_to_db(ticket_id="123456789")
        """
        system_prompt = (
            "You are an expert customer support analyst. You will receive a Zoho Desk ticket's full details. "
            "Please generate a complete, clear, and concise explanation/summary of what the customer's issue was and how the issue was handled or resolved. "
            "This summary will be stored for future use, so that if a customer comes with a similar issue, we can search for the most relevant past tickets and use the most similar one to help reply. "
            "Focus on clarity, completeness, and relevance for future retrieval."
        )
        self.open_ai_manager.add_message(role="system", text=system_prompt)
        response = self.open_ai_manager.generate_response()
        if response:
            CustomerSupportKnowledgeBaseModel.objects.filter(url=f"zoho_ticket_{ticket_id}").delete()
            cur_kb = CustomerSupportKnowledgeBaseModel()
            cur_kb.url = f"zoho_ticket_{ticket_id}"
            cur_kb.description = response
            cur_kb.save()
            chunks = self.open_ai_manager.build_materials_for_rag(text=response, max_chunk_size=2000)
            for index, chunk in enumerate(chunks):
                print(f"Saving chunk {index+1}/{len(chunks)} to database...")
                cur_text = chunk['text']
                cur_embedding = chunk['vector']
                cur_kb_chunk = CustomerSupportKnowledgeBaseChunkModel()
                cur_kb_chunk.kb = cur_kb
                cur_kb_chunk.chunk_text = cur_text
                cur_kb_chunk.embedding = cur_embedding
                cur_kb_chunk.save()
        return response
    
    def add_zoho_tickets_info_to_kb(self):
        """ Fetches all Zoho Desk tickets from the database and processes each to generate and store summaries in the knowledge base.
        Example:
            self.add_zoho_tickets_info_to_kb()
        """
        ticket_ids = ZohoDeskTicketModel.objects.all().order_by('created_at').values_list('ticket_id', flat=True)
        for idx, ticket_id in enumerate(ticket_ids):
            print(f"Processing ticket {idx+1}/{len(ticket_ids)} with ID {ticket_id} ...")
            self._add_zoho_ticket_info_to_kb(ticket_id=ticket_id)
