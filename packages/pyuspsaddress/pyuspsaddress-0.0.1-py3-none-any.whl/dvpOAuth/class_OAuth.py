import requests 
import json
import os
import logging
import re, pdb

from functools import wraps
from .error import AuthClientError, MissingTokenError

from .util import SEARCH_PAR, RETRIEVE_PAR, USAGE_PAR
from collections import defaultdict

from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode="a")
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

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
    session.proxies = {
        "http": os.environ["QUOTAGUARDSTATIC_URL"],
        "https": os.environ["QUOTAGUARDSTATIC_URL"],
    }

    my_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {"grant_type": "client_credentials"}

    resp = session.post(
        os.environ["Authentication"],
        params=params,
        headers=my_headers,
        data={
            "client_id": os.environ["client_id"],
            "client_secret": os.environ["client_secret"],
        },
    )

    a = json.loads(resp.content)
    token = a["access_token"]
    return session, token


@singleton
class DVPOAuth:
    """OAuth API for dvp app"""

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
            except (MissingTokenError, AuthClientError) as e:
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

    @_renew_token
    def call_eligibility(self, account=None):
        """check if the account is eligible"""
        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token
        eligibility_params = {
            "ContractAccountID": "'" + account + "'",
            "DUNSNumber": "'" + os.environ["DUNSNumber"] + "'",
            "$format": "json",
        }

        resp_query = self.session.get(
            os.environ["Eligibility"],
            params=eligibility_params,
            headers={"Authorization": auth},
        )

        if self.logging:
            logger.info(f"Eligibiity status code : {resp_query.status_code}")
            logger.info(f"Response content : {resp_query.content}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Eligibility 401 error.")
            raise AuthClientError

        resp = json.loads(resp_query.content)
        if self.logging:
            logger.info(f'Response : {resp["d"]["ZDSMInquiry"]}')
        return resp_query.status_code, resp

    def check_eligibility(self, account=None):
        """return the account eligibility"""
        _, resp = self.call_eligibility(account)
        return True if resp["d"]["ZDSMInquiry"]["RejectionReasonDsm"] == "" else False

    def convert_account_retrieve_from_oauth_to_soap(self, status_code=None, resp=None):
        """convert the response to the old soap format"""
        data = resp['d']['results'][0]
        res = {
            'AccountNumber': data['BillAccount'],
            'AccountStatusCode': data['RETRACCTData']['BillAccountStatusCode'],
            'AccountType': data['RETRACCTData']['AccountType'],
            'BusinessName': None,
            'FirstName': data['RETRACCTData']['NameCustFirst'],
            'Header': {
                'DateTimeStamp': datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f"),
                'MessageText': data['ReturnMessageText'],
                'Result': data['InternetReturnCode'],
                'ReturnCode': data['ErrorCode']
            },
            'LastName': data['RETRACCTData']['NameCustLast'],
            'LastSmartCoolCreditAmt': None,
            'LastSmartCoolCreditDate': None,
            'Latitude': None,
            'Longitude': None,
            'MailingAddressCity': data['RETRACCTData']['MailAddrCity'],
            'MailingAddressLine1': data['RETRACCTData']['MailAddrStreetName'],
            'MailingAddressState': data['RETRACCTData']['MailAddrState'],
            'MailingAddressZipCode': data['RETRACCTData']['MailAddrZipcode'],
            'MedicalFlag': None,
            'MiddleName': data['RETRACCTData']['NameCustMiddle'],
            'NameSuffix': None,
            'NonStandardAddressLine1': None,
            'NonStandardAddressLine2': None,
            'NonStandardAddressLine3': None,
            'OfficeCode': data['RETRACCTData']['TownCode'],
            'OpenAccess': None,
            'OptOut': None,
            'OtherAccountNames': None,
            'PremiseId': data['RETRACCTData']['PremiseId'],
            'PremisePhoneAreaCode': data['RETRACCTData']["PhoneAreaCode"],
            'PremisePhoneNumber': data['RETRACCTData']["Phone"],
            'ServiceAddressLine1': None,
            'ServiceCity': data['RETRACCTData']['SvcAddrCity'],
            'ServicePoint': {
                'ServicePoint': [
                    {
                        'AmiMeter': None,
                        'MeterNumber': None,
                        'RateCode': data['RETRACCTData']['RateCode'],
                    }
                ]
            },
            'ServiceState': data['RETRACCTData']["SvcAddrSt"],
            'ServiceZipCode': data['RETRACCTData']["SvcAddrZip"],
            'SwitchActive': None,
            'SwitchInstalled': None
        }
        return res

    def convert_eligibility_json_from_oauth_to_soap(self, status_code=None, resp=None):
        """convert the oauth return the the soap format"""
        data = resp["d"]["ZDSMInquiry"]
        
        res = {
            "AccountNumber": data["AccountNumber"],
            "AccountStatusCode": data["AccountStatus"],
            "AccountType": data["AccountClass"],
            "BusinessName": data["BusinessName"],
            "FirstName": data["CustomerFirstName"],
            "Header": {
                "DateTimeStamp": datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f"),
                "MessageText": data["RejectionReasonDsm"],
                "Result": "S" if data["RejectionReasonDsm"] == "" else "N",
                "ReturnCode": status_code,
            },
            "LastName": data["CustomerLastName"],
            "LastSmartCoolCreditAmt": ".00",
            "LastSmartCoolCreditDate": None,
            "Latitude": data["LatitudeOfPremise"],
            "Longitude": data["LongitudeOfPremise"],
            "MailingAddressCity": data["MailingAddressCity"],
            "MailingAddressLine1": data["MailingAddressStreet"],
            "MailingAddressState": data["MailingAddressState"],
            "MailingAddressZipCode": data["MailingAddressZipCode"],
            "MedicalFlag": data.get("LifeSupportFlag", 'Y'),
            "MiddleName": data["CustomerMiddleName"],
            "NameSuffix": data["NameSuffix"],
            "NonStandardAddressLine1": data["MailingAddressStreet1"],
            "NonStandardAddressLine2": data["MailingAddressStreet2"],
            "NonStandardAddressLine3": data["MailingAddressStreet3"],
            "OfficeCode": data["OfficeId"],
            "OpenAccess": data.get("ChoiceEnrolledFlag", ''),
            "OptOut": data["OptOutFlag"],
            "OtherAccountNames": data["BpRelation1"]["FullName"],
            "PremiseId": data["PremiseId"],
            "PremisePhoneAreaCode": data["AreaCode"],
            "PremisePhoneNumber": data["PhoneNumber"],
            "ServiceAddressLine1": data["ServiceStreetAddress"],
            "ServiceCity": data["ServiceAddressCity"],
            "ServicePoint": {
                "ServicePoint": [
                    {
                        "AmiMeter": data["MeterData1"]["AmiFlag"],
                        "MeterNumber": data["MeterData1"]["MeterId"],
                        "RateCode": [data["MeterData1"]["RateCode"]],
                    }
                ]
            },
            "ServiceState": data["ServiceAddressState"],
            "ServiceZipCode": data["ServiceAddressZipCode"],
            "SwitchActive": "N",
            "SwitchInstalled": "N",
        }
        return res

    def soap_U_format(self, resp=None):
        return_dict = {
            'AccountSearchSequence': {
                'AccountSearchSequence': []
            },
            'Header': {
                'DateTimeStamp': datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f"),
                'MessageText': resp.get('ReturnMessageText',''),
                'Result': resp.get('InternetReturnCode', ''),
                'ReturnCode': resp.get('ErrorCode', '')
            },
            'MoreData': resp.get('MoreData', ''),
            'RowsReturned': resp.get('RowsReturned', '')
        }
        return return_dict

    def convert_account_search_json_from_oauth_to_soap(
        self, status_code=None, resp=None
    ):
        """convert the search result json to the soap format"""
        if not resp["d"]["results"]:
            return None

        if resp['d']['results'][0]['InternetReturnCode'] == 'U':
            return self.soap_U_format(resp['d']['results'][0])

        resp_parent = resp["d"]["results"][0]
        list_data = []
        for data in resp['d']['results'][0]['ZAcctSearchNav']['results']:
            list_data.append(
                {
                    "AccountFirstName": data["CustomerFirstName"],
                    "AccountLastName": data["CustomerLastName"],
                    "AccountMiddleName": data["CustomerMiddleName"],
                    "AccountName": data["CustomerName"],
                    "AccountNameSuffix": data["CustomerSuffix"],
                    "AccountNumber": data["IdBa"],
                    "AccountStatus": data["BillingAccountStat"],
                    "AccountStatusDesc": data["AcctStatusDescription"],
                    "AdditionalAddressInfo": data.get("AdditionalAddr", ''),
                    "Address": data["AddressLine1"],
                    "City": data["City"],
                    "CompanyNumber": "",
                    "State": data["State"],
                    "ZipCode": data["Zip"],
                    "Premise": data["Premise"],
                    "Meter": data["MeterId"],
                    "AccountCloseDate": data["AccountCloseDate"]
                }
            )
        
        return_dict = {
            "AccountSearchSequence": {
                "AccountSearchSequence": list_data
            },
            "Header": {
                "DateTimeStamp": datetime.fromtimestamp(
                    eval(re.findall(r"\(.*?\)", resp_parent["ActiveTimeStamp"])[0])
                    / 1000
                ).strftime(
                    "%Y-%m-%d-%H.%M.%S.%f"
                ),  # ??? need parse the timestamp /Date(1672174552000)/
                "MessageText": resp_parent[
                    "ReturnMessageText"
                ],  
                "Result": resp_parent["InternetReturnCode"],
                "ReturnCode": resp_parent["ErrorCode"],  
            },
            "MoreData": resp_parent["MoreData"],
            "RowsReturned": str(resp_parent["RowsReturned"]),
        }
        return return_dict

    @_renew_token
    def account_search(self, *args, **kwargs):
        """search account based on the account number, first and last name, meter number and premise number"""
        SEARCH_BASE_URL = os.environ["SEARCH_BASE_URL"]
        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token

        # search API

        dict = defaultdict(str, args[0])
        try:
            if dict["account"]:
                account = dict["account"] if dict["account"] else None
                filter = (
                    SEARCH_PAR
                    + "SearchType eq 'ACC' and BillAccount eq '"
                    + account
                    + "' and CallingApplication eq 'DSM' and ActiveBaOnly eq 'N' and QuantityRowsRequested eq 10 "
                )
            elif dict["first_name"] and dict["last_name"]:
                filter = (
                    SEARCH_PAR
                    + "SearchType eq 'NAM' and CustomerFirstName eq '"
                    + dict["first_name"]
                    + "' and CustomerLastName eq '"
                    + dict["last_name"]
                    + "' and ActiveBaOnly eq 'N'"
                )
            elif dict["meter_number"]:
                filter = (
                    SEARCH_PAR
                    + "SearchType eq 'MTR' and Meter eq '"
                    + dict["meter_number"]
                    + "' and ActiveBaOnly eq 'Y' and QuantityRowsRequested eq 50"
                )
            elif dict["premise_number"]:
                filter = (
                    SEARCH_PAR
                    + "SearchType eq 'PRE' and Premise eq '"
                    + dict["premise_number"]
                    + "' and ActiveBaOnly eq 'N'"
                )
            elif dict["house_number"] and dict["street_name"] and dict["street_type"] and dict["city"] and dict["state"]:
                filter = (
                    SEARCH_PAR
                    + "SearchType eq 'ADR' and HouseNumber eq '"
                    + dict["house_number"] + "' and StreetName eq '"
                    + dict["street_name"] + "' and StreetType eq '"
                    + dict["street_type"] + "' and City eq'"
                    + dict["city"] + "' and State eq'"
                    + dict["state"] + "' and ActiveBaOnly eq 'Y'"
                )

            else:
                raise ValueError
        except:
            pass
            """handle exception here"""

        search_params = {
            "$format": "json",
            "$filter": filter,
            "$expand": "ZAcctSearchNav",
        }

        resp_query = requests.get(
            SEARCH_BASE_URL, params=search_params, headers={"Authorization": auth}
        )

        if self.logging:
            logger.info(f"Search status code : {resp_query.status_code}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Account search error.")
            raise AuthClientError

        resp = json.loads(resp_query.content)
        if self.logging:
            logger.info(f"Search response : {resp}")

        return resp_query.status_code, resp


    @_renew_token
    def account_retrieve(self, *args, **kwargs):
        """retrieve account based on the account number"""
        SEARCH_BASE_URL = os.environ["SEARCH_BASE_URL"]

        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token

        # retrieve API

        dict = defaultdict(str, args[0])
        try:
            if dict["account"]:
                account = dict["account"] if dict["account"] else None
                filter = (
                    RETRIEVE_PAR
                    + "BillAccount eq '"
                    + account
                    + "'"
                )
            else:
                raise ValueError
        except:
            pass
            """handle exception here"""

        search_params = {
            "$format": "json",
            "$filter": filter,
            "$expand": "ZAcctSearchNav",
        }

        resp_query = requests.get(
            SEARCH_BASE_URL, params=search_params, headers={"Authorization": auth}
        )

        if self.logging:
            logger.info(f"Search status code : {resp_query.status_code}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Account search error.")
            raise AuthClientError

        resp = json.loads(resp_query.content)
        if self.logging:
            logger.info(f"Search response : {resp}")

        return resp_query.status_code, resp


    @_renew_token
    def account_usage(self, *args, **kwargs):
        """retrieve account usage info based on the account number"""
        USAGE_BASE_URL = os.environ["USAGE_BASE_URL"]

        if not self.token:
            raise MissingTokenError

        auth = "Bearer " + self.token

        # Usage API

        dict = defaultdict(str, args[0])
        try:
            if dict["account"]:
                account = dict["account"] if dict["account"] else None
                start_date = dict["start_date"] if dict["start_date"] else None
                end_date = dict["end_date"] if dict["end_date"] else None
                filter = (
                    USAGE_PAR
                    + account
                    + "' and Action eq '5' and DateRange/StartDate eq datetime'"
                    + start_date
                    + "' and DateRange/EndDate eq datetime'"
                    + end_date
                    + "'"
                )
            else:
                raise ValueError
        except:
            pass
            """handle exception here"""

        usage_params = {
            "$format": "json",
            "$filter": filter,
            "$expand": "ZUsageStatement",
        }

        headers = {
            'Accept-Encoding':'gzip,deflate',
            "Authorization": auth
        }

        resp_query = requests.get(
            USAGE_BASE_URL, params=usage_params, headers=headers
        )

        if self.logging:
            logger.info(f"Usage status code : {resp_query.status_code}")

        if resp_query.status_code == 401:
            if self.logging:
                logger.exception("Account usage error.")
            raise AuthClientError

        resp = json.loads(resp_query.content)
        if self.logging:
            logger.info(f"Usage response : {resp}")
        return resp_query.status_code, resp

    def convert_account_usage_json_from_oauth_to_soap(
        self, status_code=None, resp=None
    ):
        """convert the usage result json to the soap format"""
        if not resp["d"]["results"]:
            return None

        resp_parent = resp["d"]["results"][0]
        list_data = []
        for data in resp_parent['ZUsageStatement']['results']:
            MRDate = data['MRDate']
            list_data.append(
                {
                    "AccountNumber": data["ContractAccount"],
                    "RateCode": data["RateCode"],
                    "MeterReadDate": datetime.fromtimestamp(eval(re.findall(r"\((.*?)\)", MRDate)[0])/ 1000).strftime("%Y-%m-%d-%H.%M.%S.%f"),  # ??? need parse the timestamp /Date(1672174552000)/
                    "RateCodeDescription": data["RateCodeDescription"],
                    "BillingDays": data["BillingDays"],
                    "TotalBilledAmount": data["TotalBilledAmount"],
                    "MeterStatus": data["MeterStatus"],
                    "MRMethod": data["MRMethod"],
                    "MeterRead": data["MeterRead"],
                    "Usage": data["Usage"],
                    "Demand": data["Demand"],
                    "AvgDailyUse": data["AvgDailyUse"],
                    "Meter": data["MeterID"],
                }
            )
        
        return_dict = {
            "AccountUsageSequence": {
                "AccountUsageSequence": list_data
            },
            'Header': {
                'DateTimeStamp': datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f"),
                'MessageText': resp_parent['ReturnMessage'],
                'ReturnCode': resp_parent['ResultCode']
            },
        }
        return return_dict