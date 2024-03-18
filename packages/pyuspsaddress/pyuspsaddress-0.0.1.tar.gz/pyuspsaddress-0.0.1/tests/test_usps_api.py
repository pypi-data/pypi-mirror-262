from pyuspsaddress import USPSAPI
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import pytest


@pytest.fixture(scope="module")
def usps_api():
    api_instance = USPSAPI(logging=True)
    return api_instance


def test_get_address(usps_api):
    resp = usps_api.check_address("664 Calle Hernandez, San Juan, PR 00907")
    assert resp.status_code == HTTP_200_OK


def test_get_offical_address_resp(usps_api):
    resp = usps_api.get_offical_address_resp(
        "664 Calle Hernandez, San Juan, PR 00907"
        )
    # print(str(code) + ", " + str(json.loads(resp)))
    assert resp.status_code == HTTP_200_OK
    # assert isinstance(resp, dict) is True
    bad_resp = usps_api.get_offical_address_resp("100")
    # print(str(code_400) + ", " + str(json.loads(bad_resp)))

    assert bad_resp.status_code == HTTP_400_BAD_REQUEST
    # assert isinstance(bad_resp, dict) is True
