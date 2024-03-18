import os
import requests
import json
import logging

from functools import wraps
from .errors import AuthClientError, MissingTokenError
from typing import Tuple

from .constants import USPS_AUTHENTICATION, USPS_ADDRESS
from urllib.parse import urlencode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode="a")
py_formatter = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s"
)

py_handler.setFormatter(py_formatter)
logger.addHandler(py_handler)


def singleton(cls):
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper


def request_new_token():
    session = requests.Session()
    my_headers = {
        "Content-Type": "application/json"
    }

    resp = session.post(
        USPS_AUTHENTICATION,
        headers=my_headers,
        json={
            "grant_type": "client_credentials",
            "client_id": os.environ["USPS_CLIENT_ID"],
            "client_secret": os.environ["USPS_CLIENT_SECRET"],
        },
    )
    resp = json.loads(resp.content)
    token = resp["access_token"]
    return session, token


@singleton
class USPSAPI:
    """USPS API"""

    def __init__(self, logging=None, token=None, session=None):
        self.token = token
        self.session = session
        self.logging = logging

    """ class decorator """
    def _renew_token(foo):
        """private decorator"""

        def wrapper(self, *args, **kwargs):
            try:
                if self.logging:
                    logger.info(f"Existing token : {self.token}")
                return foo(self, *args, **kwargs)
            except (MissingTokenError, AuthClientError):
                self.session, self.token = request_new_token()
                if self.logging:
                    logger.info(f"New token : {self.token}")
                return foo(self, *args, **kwargs)

        return wrapper

    @_renew_token
    def get_token(self):
        """return the OAuth token"""
        if not self.token:
            raise MissingTokenError
        return self.token

    def get_new_token(self):
        """return a new token"""
        _, self.token = request_new_token()
        return self.token

    def construct_address(
            self,
            street_address=None,
            secondary_address=None,
            city=None,
            state=None,
            zipcode=None,
            urbanization_code=None,
    ):

        address_params = {
            'streetAddress': street_address,
            'secondaryAddress': secondary_address,
            'city': city,
            'state': state,
            'ZIPCode': zipcode,
            'urbanization': urbanization_code,
        }

        get_parameters = urlencode(address_params)
        return get_parameters

    def construct_address_from_str(self, address):
        list_address = address.split(",")
        if len(list_address) == 1:
            street_address = list_address[0]
            secondary_address = city = state = zipcode = ''
        if len(list_address) == 2:
            street_address, city = list_address
            secondary_address = state = zipcode = ''
        if len(list_address) == 3:
            street_address, city, state_zipcode = list_address
            secondary_address = ''
            try:
                state, zipcode = state_zipcode.strip().split(" ")
            except Exception as e:
                logging.error(f"construct_address_from_str : {e}")
                state = state_zipcode
                zipcode = ''
        elif len(list_address) == 4:
            street_address, secondary_address, city, state_zipcode = list_address
            state, zipcode = state_zipcode.split(" ")
        return self.construct_address(
            street_address.strip().upper() if street_address else '',
            secondary_address.strip().upper() if secondary_address else '',
            city.strip().upper() if city else '',
            state.strip().upper() if state else '',
            zipcode.strip().upper() if zipcode else ''
        )

    @_renew_token
    def _verify_address(self, address: str):
        """Verify official USPS address"""
        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token
        str_address = self.construct_address_from_str(address)
        
        resp_query = self.session.get(
            USPS_ADDRESS + str_address,
            headers={"Authorization": auth, "Accept": "application/json"},
        )

        if self.logging:
            logger.info(f"Verify address status code : {resp_query.status_code}")
            logger.info(f"Response content : {resp_query.content}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Request address 401 error.")
            raise AuthClientError

        return resp_query.status_code, resp_query

    @_renew_token
    def _official_address_usps(self, address1: str, address2: str, city: str, state: str, zipcode: str, urbanization_code: str):
        """Retrieve official USPS address"""
        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token
        str_address = self.construct_address(
            address1.strip().upper() if address1 else '',
            address2.strip().upper() if address2 else '',
            city.strip().upper() if city else '',
            state.strip().upper() if state else '',
            zipcode.strip().upper() if zipcode else '',
            urbanization_code.strip().upper() if urbanization_code else '',
        )

        resp_query = self.session.get(
            USPS_ADDRESS + str_address,
            headers={"Authorization": auth, "Accept": "application/json"},
        )

        if self.logging:
            logger.info(f"Verify address status code : {resp_query.status_code}")
            logger.info(f"Response content : {resp_query.content}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Request address 401 error.")
            raise AuthClientError

        print(f'resp_query {resp_query}')
        return resp_query
    
    @_renew_token
    def _official_address(self, address: str):
        """Retrieve official USPS address"""
        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token
        str_address = self.construct_address_from_str(address)

        resp_query = self.session.get(
            USPS_ADDRESS + str_address,
            headers={"Authorization": auth, "Accept": "application/json"},
        )

        if self.logging:
            logger.info(f"Verify address status code : {resp_query.status_code}")
            logger.info(f"Response content : {resp_query.content}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Request address 401 error.")
            raise AuthClientError

        print(f'resp_query {resp_query}')
        return resp_query

    def check_address(self, address=None):
        """Return the USPS official address"""
        _, resp = self._verify_address(address)
        return resp

    def get_offical_address_resp(self, address=None) -> Tuple[int, any]:
        resp = self._official_address(address)
        return resp

    def get_offical_address_resp_usps(self, address1=None, address2=None, city=None, state=None, zipcode=None, urbanization_code=None) -> Tuple[int, any]:
        resp = self._official_address_usps(address1, address2, city, state, zipcode, urbanization_code)
        return resp
