from datetime import datetime, timedelta

import requests


class Energidataservice:
    @staticmethod
    def dayahead_prices(area, start_date=datetime(2020, 1, 1), end_date=datetime(2030, 12, 31)):
        filters = f'{{"PriceArea":"{area}"}}'
        start_date_str = start_date.strftime("%Y-%m-%dT00:00")
        end_date_str = (end_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00")
        base_url = f"https://api.energidataservice.dk/dataset/Elspotprices?offset=0"
        url = f"{base_url}&start={start_date_str}&end={end_date_str}&filter={filters}&sort=HourUTC ASC"
        indata_json = requests.get(url, verify=True).json()['records']
        for d in indata_json:
            d.update((k, datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')) for k, v in d.items() if k in ['HourUTC', 'HourDK'])
        return indata_json

    @staticmethod
    def production_consumption(area, start_date=datetime(2020, 1, 1), end_date=datetime(2030, 12, 31)):
        filters = f'{{"PriceArea":"{area}"}}'
        start_date_str = start_date.strftime("%Y-%m-%dT00:00")
        end_date_str = (end_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00")
        base_url = f"https://api.energidataservice.dk/dataset/ProductionConsumptionSettlement?offset=0"
        url = f"{base_url}&start={start_date_str}&end={end_date_str}&filter={filters}&sort=HourUTC ASC"
        indata_json = requests.get(url, verify=True).json()['records']
        for d in indata_json:
            d.update((k, datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')) for k, v in d.items() if k in ['HourUTC', 'HourDK'])
        return indata_json

    @staticmethod
    def transmission_lines(area, start_date=datetime(2020, 1, 1), end_date=datetime(2030, 12, 31)):
        start_date_str = start_date.strftime("%Y-%m-%dT00:00")
        end_date_str = (end_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00")
        base_url = f"https://api.energidataservice.dk/dataset/Transmissionlines?offset=0&sort=HourUTC ASC"
        url = f"{base_url}&start={start_date_str}&end={end_date_str}"
        indata_json = requests.get(url, verify=True).json()['records']
        indata_json = [obs for obs in indata_json if obs['PriceArea'] == area]
        for d in indata_json:
            d.update((k, datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')) for k, v in d.items() if
                     (k in ['HourUTC', 'HourDK'] and v))
        return indata_json

    @staticmethod
    def forecasts(area, start_date=datetime(2020, 1, 1), end_date=datetime(2030, 12, 31)):
        start_date_str = start_date.strftime("%Y-%m-%dT00:00")
        end_date_str = (end_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00")
        base_url = f"https://api.energidataservice.dk/dataset/Forecasts_Hour?offset=0"
        url = f"{base_url}&start={start_date_str}&end={end_date_str}"
        indata_json = requests.get(url, verify=True).json()['records']
        indata_json = [obs for obs in indata_json if obs['PriceArea'] == area]
        for d in indata_json:
            d.update((k, datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')) for k, v in d.items() if
                     (k in ['HourUTC', 'HourDK'] and v))
        return indata_json
