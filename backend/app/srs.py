"""Replaceable FSRS adapter: clients never calculate or submit due dates."""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from fsrs import Card, Rating, Scheduler


@dataclass(frozen=True)
class ScheduleResult:
    card: dict
    due: datetime
    log: dict


class SRSAdapter(Protocol):
    def new_card(self) -> ScheduleResult: ...
    def review(self, card: dict, rating: int, at: datetime) -> ScheduleResult: ...


class FSRSAdapter:
    def __init__(self):
        self.scheduler = Scheduler(enable_fuzzing=False)

    def new_card(self) -> ScheduleResult:
        card = Card()
        return ScheduleResult(card.to_dict(), card.due, {})

    def review(self, card: dict, rating: int, at: datetime) -> ScheduleResult:
        updated, log = self.scheduler.review_card(Card.from_dict(card), Rating(rating), review_datetime=at)
        return ScheduleResult(updated.to_dict(), updated.due, log.to_dict())


srs_adapter: SRSAdapter = FSRSAdapter()
