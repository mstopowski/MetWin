from jsonmethods import JSON
from request import Request


class MeteoAPIUrl:
    """Class containig methods that are helpful for generating proper URLs for eDWIN Meteo API."""
    meteo_stations_url = 'https://edwin-meteo.apps.paas.psnc.pl/observationStation'
    meteo_data_url = 'https://edwin-meteo.apps.paas.psnc.pl/meteo/'

    @classmethod
    def get_stations_url(cls, contains: str=None, station_type: str=None, active: bool=True, page: int=0, size: int=100, sort_return: str='asc') -> str:
        """This method generates URL.
        When opened it returns json file with stations filtered using supplied parameters.

        Args:
            contains (str, optional): Select stations with with name containing supplied string. Defaults to None -> returns all.
            station_type (str, optional): Type of station - weather|rain|unknown. Defaults to None -> returns all.
            active (bool, optional): Returns only active stations (with data from last 48h). Defaults to True.
            page (int, optional): Returns selected page. Defaults to 0. Counting starts from 0.
            size (int, optional): Returns selected amount of records per page. Defaults to 100. Max 1000.
            sort_return (str, optional): Sorting order of returned stations - asc|desc. Defaults to 'asc'.

        Returns:
            str: Returns URL

        Example:
            get_stations_url(contains='35', station_type='weather', active=True, page=10, size=50, sort_return='desc') -->
            Returns url that will get you json file with stations that:
            - contain in name '35'
            - are type 'weather'
            - are active
            Additionally:
            - page no. 10 will be returned
            - containing 50 records
            - presenting them in descending order
        """
        url = (cls.meteo_stations_url + '?active=' + str(active) + '&page=' + str(page) + '&size=' + str(size) + '&sort=' + sort_return)
        if contains:
            url += '&contains=' + contains
        if station_type:
            url += '&type=' + station_type
        return url

    @classmethod
    def get_station_by_id_url(cls, id: str) -> str:
        """This method generates URL.
        When opened it returns json file with station selected by supplied id.

        Args:
            id (str): Id of a desired station

        Returns:
            str: Returns URL

        Example:
            get_station_by_id_url(id='PME34') -->
            Returns url that will get you json file with selected station.
        """        
        url = cls.meteo_stations_url + '/' + id
        return url

    @classmethod
    def get_station_by_coordinates_url(cls, latitude: float, longitude: float, active: bool=True, distance: int=50, station_type: str=None, page: int=0, size: int=100, sort_return: str='asc') -> str:
        """This method generates URL.
        When opened, it returns json file with stations that are located at supplied latitude and longitude coordinates.
        Stations returned from closest to furthest from supplied latitude and longitude coordinates.

        Args:
            latitude (float): Latitude coordinate of the station
            longitude (float): Longitude coordinate of the station
            active (bool, optional): Returns only active stations (with data from last 48h). Defaults to True.
            distance (int, optional): Maximum distance in kilometers from selected coordinates. Defaults to 50. Max 500.
            station_type (str, optional): Type of station - weather|rain|unknown. Defaults to None -> returns all.
            page (int, optional): Returns selected page. Defaults to 0. Counting starts from 0.
            size (int, optional): Returns selected amount of records per page. Defaults to 100. Max 1000.
            sort_return (str, optional): Sorting order of returned stations - asc|desc. Defaults to 'asc'.

        Returns:
            str: Returns URL

        Example:
            get_station_by_coordinates_url(latitude=51.1, longitude=21.6, active=True, distance=100, station_type='weather', page=0, size=10, sort_return='asc')
            Returns url that will get you json file with stations that:
            - latitude coordinate - 51.1
            - longitude coordinate - 21.6
            - are active
            - are within 100km from selected coordinates
            - are type 'weather'
            Additionally:
            - page no. 0 will be returned
            - containing 10 records
            - presenting them in ascending order
        """        
        url = (cls.meteo_stations_url + '/' + 'location/' + str(latitude) + '/' + str(longitude)
               + '?active=' + str(active) + '&distance=' + str(distance) + '&page=' + str(page) + '&size=' + str(size) + '&sort=' + str(sort_return))
        if station_type:
            url += '&type=' + station_type
        return url

    @classmethod
    def get_meteo_by_station_id_url(cls, id: str, after: str=None, before: str=None, page: int=0, size: int=100, sort_return: str='asc') -> str:
        """This method generates URL.
        When opened, it returns json file with meteo data for selected station filtered using supplied parameters.
        By default it returns data from the last 30 days. If only one parameter from after/before is specified that it returns data from 30 days after/before selecteed date.
        If both parameters are specified (after & before) - the maximum period is 90 days.

        Args:
            id (str): Id of a desired station
            after (str, optional): Beginning date of meteo data. UTC/Format: YYYY-MM-DDTHH:MM:SSZ. Defaults to None.
            before (str, optional): End date of meteo data. UTC/Format: YYYY-MM-DDTHH:MM:SSZ.. Defaults to None.
            page (int, optional): Returns selected page. Defaults to 0. Counting starts from 0.
            size (int, optional): Returns selected amount of records per page. Defaults to 100. Max 1000.
            sort_return (str, optional): Sorting order of returned stations - asc|desc. Defaults to 'asc'.

        Returns:
            str: Returns URL

        Example:
            get_meteo_by_station_id_url(id='PME262', after='2022-11-01T00:00:00Z', before='2022-11-03T00:00:00Z', page=0, size=10, sort_return='asc')
            Returns meteo data for:
            - station with id - PME262
            - data starts after - 2022-11-01 00:00:00
            - data ends before - 2022-11-03 00:00:00
            Additionally:
            - page no. 0 will be returned
            - containing 10 records
            - presenting them in ascending order
        """        
        url = (cls.meteo_data_url + 'station/' + str(id) + '?page=' + str(page) + '&size=' + str(size) + '&sort=' + str(sort_return))
        if after:
            url += '&after=' + after
        if before:
            url += '&before=' + before
        return url

    @classmethod
    def get_meteo_by_coordinates_url(cls, latitude: float, longitude: float, stationsCount: int, after: str=None, before: str=None, page: int=0, size: int=100, sort_return: str='asc') -> str:
        """This method generates URL.
        When opened, it returns json file with meteo data from specified number of stations closest to specified latitude and longitude coordinates.
        By default it returns data from the last 30 days. If only one parameter from after/before is specified that it returns data from 30 days after/before selecteed date.
        If both parameters are specified (after & before) - the maximum period is 90 days.

        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            stationsCount (int): Number of closest stations
            after (str, optional): Beginning date of meteo data. UTC/Format: YYYY-MM-DDTHH:MM:SSZ. Defaults to None.
            before (str, optional): End date of meteo data. UTC/Format: YYYY-MM-DDTHH:MM:SSZ.. Defaults to None.
            page (int, optional): Returns selected page. Defaults to 0. Counting starts from 0.
            size (int, optional): Returns selected amount of records per page. Defaults to 100. Max 1000.
            sort_return (str, optional): Sorting order of returned stations - asc|desc. Defaults to 'asc'.

        Returns:
            str: Returns URL

        Example:
            get_meteo_by_coordinates_url(latitude=52, longitude=21, stationsCount=1, after='2022-11-01T00:00:00Z', before='2022-11-03T00:00:00Z', page=0, size=50, sort_return='asc')
            Returns meteo data for:
            - latitude coordinate - 52
            - longitude coordinate - 21
            - number of closest stations - 1
            - data starts after - 2022-11-01 00:00:00
            - data ends before - 2022-11-03 00:00:00
            Additionally:
            - page no. 0 will be returned
            - containing 10 records
            - presenting them in ascending order
        """        
        url = (cls.meteo_data_url + 'location/' + str(latitude) + '/' + str(longitude)
               + '?stationsCount=' + str(stationsCount) + '&page=' + str(page) + '&size=' + str(size) + '&sort=' + str(sort_return))
        if after:
            url += '&after=' + after
        if before:
            url += '&before=' + before
        return url

    @staticmethod
    def url_data(url: str):
        """This method gets data from parsed url.

        Args:
            url (str): URL to get the data from

        Returns:
            Data from parsed url that can be saved as json file
        """        
        return Request.urlopen_without_ssl(url)

    @staticmethod
    def read_url_data( url: str):
        """This method reads data from parsed url.
        Use it if you want to create dict from obtained data. 

        Args:
            url (str): URL to read from

        Returns:
            Object of 'bytes' class
        """        
        return MeteoAPIUrl.url_data(url).read()


class MeteoAPIDataReader:

    @classmethod
    def get_number_of_active_stations(cls) -> int:
        stations_url = MeteoAPIUrl.get_stations_url()
        stations_data = MeteoAPIUrl.read_url_data(stations_url)
        stations_data_dict = JSON.load_data_to_dict(stations_data)
        number_of_active_stations = stations_data_dict['page']['totalElements']
        return number_of_active_stations

    @classmethod
    def get_number_of_active_stations_by_type(cls, station_type: str) -> int:
        stations_url = MeteoAPIUrl.get_stations_url(station_type=station_type)
        stations_data = MeteoAPIUrl.read_url_data(stations_url)
        stations_data_dict = JSON.load_data_to_dict(stations_data)
        number_of_active_stations = stations_data_dict['page']['totalElements']
        return number_of_active_stations

    @classmethod
    def get_number_of_pages(cls, url: str) -> int:
        data = MeteoAPIUrl.read_url_data(url)
        data_dict = JSON.load_data_to_dict(data)
        number_of_pages = data_dict['page']['totalPages']
        return number_of_pages


class MeteoAPIFileDownloader:
    
    @classmethod
    def get_all_stations(cls):
        url = MeteoAPIUrl.get_stations_url()
        number_of_pages = MeteoAPIDataReader.get_number_of_pages(url)
        for page in range(number_of_pages + 1):
            url = MeteoAPIUrl.get_stations_url(page=page)
            data = MeteoAPIUrl.url_data(url)
            JSON.save_file('data/stations/', f'active stations page_{page}.json', data)

    @classmethod
    def get_weather_locations(cls):
        url = MeteoAPIUrl.get_stations_url(station_type='weather')
        number_of_pages = MeteoAPIDataReader.get_number_of_pages(url)
        for page in range(number_of_pages + 1):
            page_url = MeteoAPIUrl.get_stations_url(station_type='weather', page=page)
            page_data = MeteoAPIUrl.read_url_data(page_url)
            page_dict = JSON.load_data_to_dict(page_data)
            for station in page_dict['content']:
                station_url = MeteoAPIUrl.get_station_by_id_url(station['id'])
                station_data = MeteoAPIUrl.url_data(station_url)
                id = station['id']
                JSON.save_file('data/stations/weather/', f'{id}.json', station_data)

    @classmethod
    def get_rain_locations(cls):
        url = MeteoAPIUrl.get_stations_url(station_type='rain')
        number_of_pages = MeteoAPIDataReader.get_number_of_pages(url)
        for page in range(number_of_pages + 1):
            page_url = MeteoAPIUrl.get_stations_url(station_type='rain', page=page)
            page_data = MeteoAPIUrl.read_url_data(page_url)
            page_dict = JSON.load_data_to_dict(page_data)
            for station in page_dict['content']:
                station_url = MeteoAPIUrl.get_station_by_id_url(station['id'])
                station_data = MeteoAPIUrl.url_data(station_url)
                id = station['id']
                JSON.save_file('data/stations/rain/', f'{id}.json', station_data)

    @classmethod
    def get_unknown_locations(cls):
        url = MeteoAPIUrl.get_stations_url(station_type='unknown')
        number_of_pages = MeteoAPIDataReader.get_number_of_pages(url)
        for page in range(number_of_pages + 1):
            page_url = MeteoAPIUrl.get_stations_url(station_type='unknown', page=page)
            page_data = MeteoAPIUrl.read_url_data(page_url)
            page_dict = JSON.load_data_to_dict(page_data)
            for station in page_dict['content']:
                station_url = MeteoAPIUrl.get_station_by_id_url(station['id'])
                station_data = MeteoAPIUrl.url_data(station_url)
                id = station['id']
                JSON.save_file('data/stations/unknown/', f'{id}.json', station_data)


if __name__ == '__main__':
    MeteoAPIFileDownloader().get_unknown_locations()