"""Proactive token-per-minute pacing.

Groq's free tier caps TOKENS per minute, not requests: observed 8,000 TPM against
1,000 RPM, so the token budget binds roughly 100x earlier than the request budget.

Reacting to 429s is the wrong shape for this. Blind exponential backoff overshoots --
it sleeps 2, 4, 8, 16s regardless of when the window actually resets, and with a
60-second window that wastes most of the recovery. Worse, it makes a throttled run
indistinguishable from a hung one, which is exactly how the first n=20 attempt came
to look dead while it was in fact progressing.

So: track what has actually been spent in the trailing 60 seconds and sleep only long
enough for the next call to fit. Retry-on-429 stays in LLMAgent as a backstop for
when the estimate is wrong.
"""
from __future__ import annotations

import threading
import time
from collections import deque


class TokenPacer:
    def __init__(self, tokens_per_minute: int = 8000, window_s: float = 60.0,
                 safety: float = 0.85):
        # safety margin because the estimate for the NEXT call is necessarily a
        # guess, and overshooting the window costs a full reset
        self.budget = tokens_per_minute * safety
        self.window_s = window_s
        self._spent: deque[tuple[float, int]] = deque()
        self._lock = threading.Lock()
        self.total_waited_s = 0.0

    def _prune(self, now: float) -> None:
        while self._spent and now - self._spent[0][0] > self.window_s:
            self._spent.popleft()

    def spent_in_window(self) -> int:
        with self._lock:
            self._prune(time.monotonic())
            return sum(n for _, n in self._spent)

    def wait_for(self, estimated_tokens: int) -> float:
        """Block until `estimated_tokens` fits in the window. Returns seconds waited."""
        waited = 0.0
        while True:
            with self._lock:
                now = time.monotonic()
                self._prune(now)
                used = sum(n for _, n in self._spent)
                if used + estimated_tokens <= self.budget or not self._spent:
                    return waited
                # sleep only until the oldest entry leaves the window
                oldest_at = self._spent[0][0]
            nap = max(0.25, self.window_s - (time.monotonic() - oldest_at) + 0.1)
            time.sleep(nap)
            waited += nap
            self.total_waited_s += nap

    def record(self, tokens: int) -> None:
        with self._lock:
            self._spent.append((time.monotonic(), tokens))
