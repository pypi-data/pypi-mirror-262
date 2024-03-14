import os
import time

import pytest
import requests

from MVC import pretty, curlify_request, MvcConnection

BPS_TENANT_ID = "DCF7AD1A-C165-4994-8DC3-A5E4A5BD4855"
IAM_USER = "iaasworkshop+030@student.mvisionlabs.com"
PASSWORD = os.getenv("PASSWORD")


def get_instance():
    m = MvcConnection(username=IAM_USER, password=PASSWORD,
                      bps_tenantid=BPS_TENANT_ID)
    return m


def tenant_login():
    m = get_instance()
    res = m.authenticate()
    assert res
    return m


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_unmatched_uploads():
    m = tenant_login()
    res = m.shadow_get_unmatched_uploads_summary()
    assert (isinstance([], res))


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_gateway_categories():
    m = tenant_login()
    res = m.web_get_appcontrol_categories()
    assert (len(res) > 30)
    res = m.web_get_url_categories()
    assert (len(res.keys()) > 200)


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_gateway_ruleset_library():
    rs = "Hybrid_Policy"
    m = tenant_login()
    res = m.web_policy_get_library_rulesets()
    assert (len(res) > 10)
    res = m.web_policy_get_library_ruleset_by_id(res[4]["id"])
    assert (len(res["resources"]["content"]) > 25)


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_get_hybridstatus():
    m = tenant_login()
    res = m.web_get_hybridstatus()
    print(res)
    assert ('isHybrid' in res)


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_gateway_list_new():
    old_list = test_web_get_gateway_list_details()
    old_list["name"] = "appl {}".format(time.time())
    old_list["id"] = ""
    old_list["proxyList"][0]["hostname"] = "appl_{}.de".format(time.time())
    old_list["proxyList"][0]["httpPort"] = "9090"
    m = tenant_login()
    res = m.web_mcp_add_gateway_list(old_list)
    # print(res)
    assert (len(res["/mcp/proxies"]) == 64)


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_get_gateway_list_details():
    m = get_instance()
    p = m.web_mcp_get_gateway_lists()
    d = m.web_mcp_get_gateway_list_by_id(p[-1]['id'])
    assert (len(d.get("proxyList")) > 0)
    return d


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_web_get_gateway_lists():
    m = tenant_login()
    p = m.web_mcp_get_gateway_lists()
    # print(p)
    assert (len(p) > 0)


def test_pretty():
    assert pretty({"hey": "ho"}) == '{\n  "hey": "ho"\n}'


def test_curlify_request():
    res = requests.get(url="http://icanhazip.com", headers={"addt": "header", "User-Agent": "Hi"})
    curlified = curlify_request(res.request)
    assert curlified == 'curl -v -H "User-Agent: Hi" -H "Accept-Encoding: gzip, deflate, zstd" -H "Accept: */*" -H ' \
                        '"Connection: keep-alive" -H "addt: header"  -X GET http://icanhazip.com/'


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_get_tenants():
    m = get_instance()
    assert len(m.get_tenants()[0].get("bps-tenant-id")) == 36


@pytest.mark.skipif(not PASSWORD, reason="No PASSWORD in env")
def test_login():
    m = tenant_login()
    assert (not m.login_error)
