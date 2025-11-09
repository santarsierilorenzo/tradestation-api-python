from src.base_client import BaseAPIClient
from typing import Dict


class Brokerage(BaseAPIClient):
    """
    Provides access to TradeStation Brokerage API endpoints.

    This class handles requests related to user brokerage data such as
    account information, balances, and trading permissions.
    It inherits from `BaseAPIClient` to leverage the shared
    HTTP request and token management logic.

    Attributes
    ----------
    token_manager : TokenManager
        Object responsible for providing and refreshing OAuth tokens.
    """

    def __init__(
        self,
        *,
        token_manager
    ) -> None:
        """
        Initialize a Brokerage API client.

        Parameters
        ----------
        token_manager : TokenManager
            Instance managing authentication tokens for API requests.
        """
        self.token_manager = token_manager

    def get_accounts(self) -> Dict:
        """
        Retrieve the list of brokerage accounts associated with the
        authenticated user.

        Returns
        -------
        dict
            JSON response containing available accounts, each typically
            including:
              - `AccountID`: Unique account identifier
              - `AccountType`: Account category (e.g., Individual, IRA)
              - `Description`: Human-readable name or label
              - `Status`: Current account status (Active, Closed, etc.)

        Raises
        ------
        requests.exceptions.RequestException
            If the HTTP request fails or the API returns an error response.

        Notes
        -----
        - Requires a valid access token.
        - Data returned may vary based on account type and permissions.
        """
        url = "https://api.tradestation.com/v3/brokerage/accounts"
        token = self.token_manager.get_token()
        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_request(
            url=url,
            headers=headers,
            params={}
        )

        return response
