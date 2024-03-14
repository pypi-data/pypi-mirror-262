from typing import Optional, Literal

import requests

from buymeacoffee_api.src.constants import BASE_URL, SUBSCRIPTION_URL, SUBSCRIPTIONS_URL, SUPPORTER_URL, SUPPORTERS_URL, PURCHASE_URL, PURCHASES_URL
from buymeacoffee_api.src.types import SubscriptionResponse, SubscriptionsResponse, SupportersResponse, \
    SupporterResponse, PurchaseResponse, PurchasesResponse


class BuyMeACoffeeAPI:
    def __init__(self, api_key: str, base_url: str = BASE_URL, proxies: Optional[dict] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.proxies = proxies
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        return session

    def get_json(self, url: str, params: Optional[dict] = None) -> dict:
        response = self.session.get(url, proxies=self.proxies, params=params)
        return response.json()

    def get_subscriptions(self, status: Literal["active", "inactive", "all"] = "all") -> SubscriptionsResponse:
        url = SUBSCRIPTIONS_URL.format(base_url=self.base_url)
        return self.get_json(url, params={"status": status})

    def get_subscription(self, id_: int) -> SubscriptionResponse:
        url = SUBSCRIPTION_URL.format(base_url=self.base_url, id=id_)
        return self.get_json(url)

    def get_supporters(self) -> SupportersResponse:
        url = SUPPORTERS_URL.format(base_url=self.base_url)
        return self.get_json(url)

    def get_supporter(self, id_: int) -> SupporterResponse:
        url = SUPPORTER_URL.format(base_url=self.base_url, id=id_)
        return self.get_json(url)

    def get_purchases(self) -> PurchasesResponse:
        url = PURCHASES_URL.format(base_url=self.base_url)
        return self.get_json(url)

    def get_purchase(self, id_: int) -> PurchaseResponse:
        url = PURCHASE_URL.format(base_url=self.base_url, id=id_)
        return self.get_json(url)
