from unittest import TestCase
from src.aero_svo_api import models
from . import payload


class TestModels(TestCase):
    def test_aircraft_on_valid(self):
        valid_data = payload.AircraftPayload().model_dump()
        aircraft = models.Aircraft.model_validate(valid_data)

    def test_country_on_valid(self):
        valid_data = payload.CountryPayload().model_dump()
        country = models.Country.model_validate(valid_data)

    def test_city_on_valid(self):
        valid_data = payload.CityPayload().model_dump()
        country = models.City.model_validate(valid_data)

    def test_airport_on_valid(self):
        valid_data = payload.AirportPayload().model_dump()
        airport = models.Airport.model_validate(valid_data)

    def test_company_on_valid(self):
        valid_data = payload.CompanyPayload().model_dump()
        company = models.Company.model_validate(valid_data)

    def test_flight_on_valid(self):
        valid_data = payload.FlightPayload().model_dump()
        flight = models.Flight.model_validate(valid_data)
