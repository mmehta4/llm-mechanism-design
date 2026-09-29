"""A server refusing a request is not the model failing.

Both behaviours below were wrong on the Gemini practice round: daily-quota errors
were retried five times each, and the resulting failures were logged as the model
giving an unreadable answer.
"""
from agents.llm import _is_transient, infra_kind


class FakeAPIError(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code


def test_daily_quota_is_not_retried():
    e = FakeAPIError(429, "You exceeded your current quota, please check your plan")
    assert infra_kind(e) == "quota"
    assert _is_transient(e) is False


def test_per_minute_rate_limit_is_retried():
    e = FakeAPIError(429, "Rate limit reached for requests per minute")
    assert infra_kind(e) == "rate_limit"
    assert _is_transient(e) is True


def test_overload_is_infrastructure_and_retried():
    e = FakeAPIError(503, "This model is currently experiencing high demand")
    assert infra_kind(e) == "overloaded"
    assert _is_transient(e) is True


def test_a_real_model_error_is_not_infrastructure():
    e = FakeAPIError(400, "Failed to generate JSON")
    assert infra_kind(e) is None
