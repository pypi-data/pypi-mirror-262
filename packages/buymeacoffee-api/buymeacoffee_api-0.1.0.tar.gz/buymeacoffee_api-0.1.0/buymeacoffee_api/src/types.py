from typing import TypedDict, Optional, Literal, TypeVar

_T = TypeVar("_T")

PageResponse = TypedDict("PageResponse", {"data": _T, "from": int, "current_page": int, "first_page_url": str, "last_page": int,
                                          "last_page_url": str, "next_page_url": Optional[str], "path": str,
                                          "per_page": int, "prev_page_url": Optional[str], "to": int, "total": int})


class SubscriptionResponse(TypedDict):
    subscription_id: int
    subscription_cancelled_on: Optional[str]
    subscription_created_on: str
    subscription_updated_on: str
    subscription_current_period_start: str
    subscription_current_period_end: str
    subscription_coffee_price: str
    subscription_coffee_num: int
    subscription_is_cancelled: Optional[bool]
    subscription_is_cancelled_at_period_end: Optional[bool]
    subscription_currency: str
    subscription_message: Optional[str]
    message_visibility: int
    subscription_duration_type: Literal["month", "year"]
    referer: Optional[str]
    country: Optional[str]
    transaction_id: str
    payer_email: str
    payer_name: str


SubscriptionsResponse = PageResponse[SubscriptionResponse]


class SupporterResponse(TypedDict):
    support_id: int
    support_note: Optional[str]
    support_coffees: int
    transaction_id: str
    support_visibility: int
    support_created_on: str
    support_updated_on: str
    transfer_id: Optional[str]
    supporter_name: Optional[str]
    support_coffee_price: str
    support_email: str
    is_refunded: Optional[bool]
    support_currency: str
    support_note_pinned: int
    referer: Optional[str]
    country: Optional[str]
    payer_email: str
    payment_platform: str
    payer_name: str


SupportersResponse = PageResponse[SupporterResponse]


class Extra(TypedDict):
    reward_id: int
    reward_title: str
    reward_description: str
    reward_confirmation_message: str
    reward_question: str
    reward_used: int
    reward_created_on: str
    reward_updated_on: str
    reward_deleted_on: Optional[str]
    reward_is_active: int
    reward_image: str
    reward_slots: int
    reward_coffee_price: str
    reward_order: int


class PurchaseResponse(TypedDict):
    purchase_id: int
    purchased_on: str
    purchase_updated_on: str
    purchase_is_revoked: int
    purchase_amount: str
    purchase_currency: str
    purchase_question: str
    payer_email: str
    payer_name: str
    extra: Extra


PurchasesResponse = PageResponse[PurchaseResponse]
