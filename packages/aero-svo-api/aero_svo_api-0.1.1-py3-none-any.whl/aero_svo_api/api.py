import urllib.parse
import pydantic
from typing import Literal, Any
from aiohttp import ClientSession
from datetime import datetime
from logging import getLogger
from functools import cached_property

from . import (
    urls,
    models,
    utils,
)

svo_logger = getLogger('svo-api')


class AsyncSvoApi:
    def __init__(self, session: ClientSession | None = None) -> None:
        self._session = session

    @cached_property
    def session(self):
        if self._session is None:
            self._session = ClientSession()
        return self._session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()

    async def _request(self, url: str, params: dict, _session: ClientSession | None = None, **kwargs: Any) -> dict:
        response = await (_session or self.session).get(url, params=params, **kwargs)
        response.raise_for_status()
        return await response.json()

    async def get_schedule(self,
                           direction: Literal['arrival', 'departure'],
                           date_start: datetime,
                           date_end: datetime,
                           per_page: int = 99999,
                           page: int = 0,
                           locale: str = 'ru',
                           **kwargs
                           ) -> models.Schedule:

        response = await self._request(
            url=urls.timetable,
            params=dict(
                direction=direction,
                dateStart=utils.format_date(date_start),
                dateEnd=utils.format_date(date_end),
                perPage=per_page,
                page=page,
                locale=locale,
            ),
            **kwargs,
        )

        schedule = models.Schedule()

        for item in response['items']:
            try:
                flight = models.Flight.model_validate(item)
                schedule.flights.append(flight)
            except pydantic.ValidationError as err:
                svo_logger.warning(f'Skip flight id={item.get("i_id")}\n' + str(err))

        return schedule

    async def get_flight(self,
                         flight_id: int,
                         locale: str = 'ru',
                         **kwargs
                         ) -> models.Flight:

        response = await self._request(
            url=urllib.parse.urljoin(urls.timetable, f'{flight_id}/'),
            params=dict(
                locale=locale,
            ),
            **kwargs
        )
        return models.Flight.model_validate(response)
