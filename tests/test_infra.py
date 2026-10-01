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


def test_groq_daily_token_cap_is_quota_not_rate_limit():
    e = FakeAPIError(429, "Rate limit reached for model `openai/gpt-oss-120b` "
                          "on tokens per day (TPD): Limit 200000, Used 199500")
    assert infra_kind(e) == "quota"
    assert _is_transient(e) is False


def test_google_per_minute_cap_is_rate_limit_not_daily_quota():
    """Google words both caps 'exceeded your current quota'; the quotaId differs."""
    e = FakeAPIError(429, "You exceeded your current quota ... 'quotaId': "
                          "'GenerateRequestsPerMinutePerProjectPerModel-FreeTier'")
    assert infra_kind(e) == "rate_limit"
    assert _is_transient(e) is True


def test_google_per_day_cap_is_quota():
    e = FakeAPIError(429, "You exceeded your current quota ... 'quotaId': "
                          "'GenerateRequestsPerDayPerProjectPerModel-FreeTier'")
    assert infra_kind(e) == "quota"


def test_request_pacer_spaces_calls():
    import time
    from agents.pacer import TokenPacer
    p = TokenPacer(requests_per_minute=600, safety=1.0)    # 0.1s apart
    t = time.monotonic()
    for _ in range(4):
        p.wait_for(1)
    assert time.monotonic() - t >= 0.29


def test_empty_reply_is_infrastructure_and_retried():
    """An empty reply is the endpoint failing, not the model answering badly."""
    from agents.llm import EmptyResponse
    e = EmptyResponse("the endpoint returned an empty reply")
    assert infra_kind(e) == "empty_response"
    assert _is_transient(e) is True


def test_access_refused_is_infrastructure():
    """403s were once scored as unreadable answers: ~4,450 of them in ten minutes."""
    assert infra_kind(FakeAPIError(403, "Authorization failed")) == "auth"
    assert infra_kind(FakeAPIError(401, "Unauthorized")) == "auth"


def test_any_failure_before_a_reply_is_infrastructure():
    assert infra_kind(FakeAPIError(418, "something unexpected")) == "api_error"
    assert infra_kind(ValueError("boom")) == "api_error"
