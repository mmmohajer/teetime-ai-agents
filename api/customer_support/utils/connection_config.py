from django.conf import settings
from django.core.cache import cache
import psycopg2
from psycopg2.extras import RealDictCursor
import requests


class ConnectionConfigManager:

    def connect_to_prod_app_db(self, query):
        """
        Executes a SELECT query on the production app database and returns the results.

        Args:
            query (str): SQL SELECT query to execute.

        Returns:
            dict: {"success": bool, "data": list} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().connect_to_prod_app_db("SELECT * FROM users;")
            if result["success"]:
                print(result["data"])
        """
        db_config = {
            'host': settings.PROD_APP_DB_HOST,
            'user': settings.PROD_APP_DB_USER,
            'password': settings.PROD_APP_DB_PASSWORD,
            'database': settings.PROD_APP_DB_DATABASE,
        }
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(
                host=db_config['host'],
                dbname=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query)
            return {"success": True, "data": cur.fetchall()}
        except Exception as e:
            print(f"❌ {e}")
            return {"success": False, "message": f"❌ {e}"}
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def connect_to_prod_app_db_update(self, query):
        """
        Executes an UPDATE/INSERT/DELETE query on the production app database.

        Args:
            query (str): SQL query to execute (UPDATE, INSERT, or DELETE).

        Returns:
            dict: {"success": True} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().connect_to_prod_app_db_update("UPDATE users SET active=TRUE;")
            if result["success"]:
                print("Update successful!")
        """
        db_config = {
            'host': settings.PROD_APP_DB_HOST,
            'user': settings.PROD_APP_DB_USER,
            'password': settings.PROD_APP_DB_PASSWORD,
            'database': settings.PROD_APP_DB_DATABASE,
        }
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(
                host=db_config['host'],
                dbname=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return {"success": True}
        except Exception as e:
            print(f"❌ {e}")
            return {"success": False, "message": f"❌ {e}"}
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_zoho_access_token(self):
        """
        Retrieves a Zoho OAuth access token, using cache if available, otherwise requests a new one.

        Returns:
            dict: {"success": True, "data": {"access_token": str}} on success, or {"success": False, "message": str} on failure.

        Example:
            token_data = ConnectionConfigManager().get_zoho_access_token()
            if token_data["success"]:
                print(token_data["data"]["access_token"])
        """
        access_token = cache.get("ZOH_ACCESS_TOKEN")
        if access_token:
            return {"success": True, "data": {"access_token": access_token}}

        url = "https://accounts.zoho.com/oauth/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": settings.ZOHO_CLIENT_ID,
            "client_secret": settings.ZOHO_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": settings.ZOHO_REFRESH_TOKEN
        }

        response = requests.post(url, headers=headers, data=data)
        if not response:
            return {"success": False, "message": "❌ No response!"}
        if response.status_code != 200:
            return {"success": False, "message": f"❌ {response.text}"}

        data = response.json()
        access_token = data["access_token"]
        expires_in = int(data.get("expires_in", 3600))
        cache.set("ZOH_ACCESS_TOKEN", access_token, timeout=expires_in - 60)
        return {"success": True, "data": {"access_token": access_token}}

    def _handle_response(self, response):
        """
        Centralized handler for all HTTP responses from Zoho/RevenueCat APIs.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            dict: {"success": True, "data": ...} on success, or {"success": False, "message": str} on failure.

        Example:
            response = requests.get(url)
            result = ConnectionConfigManager()._handle_response(response)
        """
        if not response:
            return {"success": False, "message": "❌ No response object"}

        if not response.ok:
            return {"success": False, "message": f"❌ {response.status_code} {response.text}"}

        if response.status_code == 204 or not response.content:
            return {"success": False, "message": "No content found"}

        try:
            data = response.json()
        except ValueError:
            return {"success": True, "data": response.text}

        if isinstance(data, dict) and "data" in data:
            return {"success": True, "data": data["data"]}

        return {"success": True, "data": data}

    def send_zoho_crm_req(self, zoho_endpoint, method="GET", payload=None, headers={}):
        """
        Sends a request to the Zoho CRM API with the given endpoint and method.

        Args:
            zoho_endpoint (str): CRM API endpoint (e.g., 'Leads').
            method (str): HTTP method ('GET', 'POST', 'PUT'). Default is 'GET'.
            payload (dict, optional): Data to send in the request body for POST/PUT.
            headers (dict, optional): Additional headers.

        Returns:
            dict: {"success": True, "data": ...} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().send_zoho_crm_req('Leads', method='GET')
            if result["success"]:
                print(result["data"])
        """
        access_token_data = self.get_zoho_access_token()
        if not access_token_data["success"]:
            return access_token_data

        access_token = access_token_data["data"]["access_token"]
        url = f"https://www.zohoapis.com/crm/v2/{zoho_endpoint}"
        ZOHO_HEADERS = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json",
            **headers,
        }

        if method == "GET":
            response = requests.get(url, headers=ZOHO_HEADERS)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=ZOHO_HEADERS)
        elif method == "PUT":
            response = requests.put(url, json=payload, headers=ZOHO_HEADERS)
        else:
            return {"success": False, "message": f"Unsupported method {method}"}

        return self._handle_response(response)

    def send_zoho_desk_req(self, zoho_endpoint, method="GET", payload=None, headers={}):
        """
        Sends a request to the Zoho Desk API with the given endpoint and method.

        Args:
            zoho_endpoint (str): Desk API endpoint (e.g., 'tickets', 'tickets/{id}/threads').
            method (str): HTTP method ('GET', 'POST', 'PUT'). Default is 'GET'.
            payload (dict, optional): Data to send in the request body for POST/PUT.
            headers (dict, optional): Additional headers.

        Returns:
            dict: {"success": True, "data": ...} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().send_zoho_desk_req('tickets', method='GET')
            if result["success"]:
                print(result["data"])
        """
        access_token_data = self.get_zoho_access_token()
        if not access_token_data["success"]:
            return access_token_data

        access_token = access_token_data["data"]["access_token"]
        url = f"https://desk.zoho.com/api/v1/{zoho_endpoint}"
        ZOHO_HEADERS = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json",
            **headers,
        }

        if method == "GET":
            response = requests.get(url, headers=ZOHO_HEADERS)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=ZOHO_HEADERS)
        elif method == "PUT":
            response = requests.put(url, json=payload, headers=ZOHO_HEADERS)
        else:
            return {"success": False, "message": f"Unsupported method {method}"}

        return self._handle_response(response)

    def send_revenue_cat_req(self, rc_endpoint, use_endpoint_as_main_url=False, method="GET"):
        """
        Sends a request to the RevenueCat API.

        Args:
            rc_endpoint (str): RevenueCat API endpoint or full URL if use_endpoint_as_main_url is True.
            use_endpoint_as_main_url (bool): If True, rc_endpoint is treated as the full URL. Default is False.
            method (str): HTTP method ('GET'). Default is 'GET'.

        Returns:
            dict: {"success": True, "data": ...} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().send_revenue_cat_req('subscribers')
            if result["success"]:
                print(result["data"])
        """
        ACCESS_TOKEN = f"Bearer {settings.REVENUE_CAT_SECRET_KEY}"
        REVENUE_CAT_HEADERS = {
            "Authorization": ACCESS_TOKEN,
            "Content-Type": "application/json",
        }

        if not use_endpoint_as_main_url:
            url = f"https://api.revenuecat.com/v2/projects/{settings.REVENUE_CAT_PROJECT_ID}/{rc_endpoint}"
        else:
            url = rc_endpoint

        if method == "GET":
            response = requests.get(url, headers=REVENUE_CAT_HEADERS)
        else:
            return {"success": False, "message": f"Unsupported method {method}"}

        return self._handle_response(response)

    def send_zoho_campaign_req(self, zoho_campaign_endpoint, method="GET", payload=None, is_response_json_format=True, headers={}):
        """
        Sends a request to the Zoho Campaign API.

        Args:
            zoho_campaign_endpoint (str): Campaign API endpoint (e.g., 'getmailinglists').
            method (str): HTTP method ('GET', 'POST', 'PUT'). Default is 'GET'.
            payload (dict, optional): Data to send in the request body for POST/PUT.
            is_response_json_format (bool): If True, expects JSON response. Default is True.
            headers (dict, optional): Additional headers.

        Returns:
            dict: {"success": True, "data": ...} on success, or {"success": False, "message": str} on failure.

        Example:
            result = ConnectionConfigManager().send_zoho_campaign_req('getmailinglists', method='GET')
            if result["success"]:
                print(result["data"])
        """
        access_token_data = self.get_zoho_access_token()
        if not access_token_data["success"]:
            return access_token_data

        access_token = access_token_data["data"]["access_token"]
        url = f"https://campaigns.zoho.com/api/v1.1/{zoho_campaign_endpoint}"
        ZOHO_HEADERS = {"Authorization": f"Zoho-oauthtoken {access_token}", **headers}

        if method == "GET":
            response = requests.get(url, headers=ZOHO_HEADERS)
        elif method == "POST":
            response = requests.post(url, data=payload, headers=ZOHO_HEADERS)
        elif method == "PUT":
            response = requests.put(url, data=payload, headers=ZOHO_HEADERS)
        else:
            return {"success": False, "message": f"Unsupported method {method}"}

        if not is_response_json_format:
            return {"success": True, "data": response.text if response.ok else response.text}

        return self._handle_response(response)
