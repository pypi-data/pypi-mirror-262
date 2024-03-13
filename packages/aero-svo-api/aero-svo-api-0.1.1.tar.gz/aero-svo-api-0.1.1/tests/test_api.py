from src.aero_svo_api.api import AsyncSvoApi, svo_logger
from src.aero_svo_api import urls
from src.aero_svo_api import models
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock
from datetime import datetime, timedelta

from . import payload


class TestAsyncSvoApi(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = AsyncSvoApi()
        self.mock_response = AsyncMock(raise_for_status=Mock)
        self.api.session.get = AsyncMock(return_value=self.mock_response)

    async def asyncTearDown(self) -> None:
        await self.api.session.close()

    async def test_request(self):
        response = await self.api._request(urls.timetable, proxy='https://example.com', params={'param': 'val'})
        self.api.session.get.assert_called_with(urls.timetable, proxy='https://example.com', params={'param': 'val'})

    async def test_request_inject_session(self):
        json_mock = AsyncMock(return_value=payload.FlightPayload().model_dump())
        mock_session = AsyncMock(get=AsyncMock(return_value=Mock(json=json_mock)))

        response = await self.api.get_flight(flight_id=12345, _session=mock_session)
        mock_session.get.assert_called()

    async def test_session_injection_does_not_create_session(self):
        api = AsyncSvoApi()
        mock_session = AsyncMock(get=AsyncMock(return_value=AsyncMock(raise_for_status=Mock)))

        response = await api._request(urls.timetable, params={}, _session=mock_session)

        self.assertIsNone(api._session)

    async def test_context_manager(self):
        async with AsyncSvoApi() as api:
            self.assertFalse(api.session.closed)
        self.assertTrue(api.session.closed)

    async def test_get_schedule(self):
        data = {'items': [payload.FlightPayload().model_dump() for _ in range(10)]}
        self.mock_response.json.return_value = data

        schedule = await self.api.get_schedule(
            direction='arrival',
            date_start=datetime.now() - timedelta(hours=4),
            date_end=datetime.now(),
        )

        self.assertEqual(len(schedule.flights), 10)

    async def test_get_schedule_logging(self):
        self.mock_response.json.return_value = models.Schedule.model_construct(
            items=[
                payload.FlightPayload(i_id='string').model_dump(),      # invalid
                payload.FlightPayload().model_dump(),                   # valid
            ]
        ).model_dump(by_alias=True)

        with self.assertLogs(svo_logger, level='WARNING') as log:
            schedule = await self.api.get_schedule(
                direction='arrival',
                date_start=datetime.now() - timedelta(hours=4),
                date_end=datetime.now()
            )
            self.assertIn('validation error', log.output[0])
            self.assertEqual(len(schedule.flights), 1)

    async def test_get_flight(self):
        self.mock_response.json.return_value = payload.FlightPayload(i_id='12345').model_dump()
        flight = await self.api.get_flight(flight_id=12345)

        self.assertEqual(flight.id, 12345)

