import base64
import json
import os
import re
import uuid
from copy import copy
from datetime import datetime
from datetime import timedelta
from enum import Enum
from io import BytesIO

import requests

# constants:
tsfilename = "export_incidents_example_timestamp.txt"
date_format = "%Y-%m-%dT%H:%M:%S.000+00:00"  # 2020-10-01T00:00:00.000+00:00
IAAS_CSPS = {  # known list of the three IaaS CSPs
    "aws": {"cspname": "Amazon Web Services", "cspid": 2049},
    "azure": {"cspname": "Microsoft Azure", "cspid": 4366},
    "gcp": {"cspname": "Google Cloud Platform", "cspid": 13465},
}
_REGEX_WEB_POLICY_INCLUDES = re.compile(r'(.*)INCLUDE\s*\"(.+)\".*')


def pretty(in_obj):
    if not in_obj:
        return "<Nothing>"
    return str(json.dumps(in_obj, indent=2, sort_keys=True, default=str))


def curlify_request(req):
    url = req.url
    method = req.method
    headers = dict(req.headers)
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    if req.body:
        data = " -d '" + req.body.decode("utf-8") + "'"
    else:
        data = ""
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    return (command.format(method=method, headers=header, data=data, uri=url))


class PolicyType(Enum):
    API_DLP = 0
    PROXY_DLP = 1
    LIGHTNING_LINK = 5
    CONFIG_AUDIT = 6
    MALWARE = 8
    VULNERABILITY = 9
    APPLICATION_CONTROL = 10
    FILE_INTEGRITY = 11
    WORKLOAD_HARDENING = 12
    CONTAINER_IMAGE_CONTROL = 13


class MvcConnection:
    session = None
    tenants = None
    username = None
    password = None
    bps_tenantid = None
    env = None
    lastauthdate = None
    token_lifetime = None
    iam_token = None
    tenantid = None
    authinfo = None
    mpops = None
    iam_user_details = None
    CSPID_AWS = 2049
    _web_get_etag = False
    login_error = None
    _DEFAULT_SCOPES = "shn.con.r web.adm.x web.rpt.x web.rpt.r web.lst.x web.plc.x web.xprt.x web.cnf.x uam:admin" \
                      " udlp.cl.f"

    def __init__(self, username, password, bps_tenantid=None, env="www.myshn.net"):
        self.username = username
        self.password = password
        self.bps_tenantid = bps_tenantid
        self.env = "https://" + env
        self.session = requests.session()

    @property
    def bps_tenantid_web(self):
        # a special version of the bpsid for the web policy, lowercase and with underscore instead of dashes
        if self.bps_tenantid:
            return self.bps_tenantid.lower().replace('-', '_')
        return None

    def set_web_get_etag(self, get_etag):
        self._web_get_etag = get_etag

    def authenticate(self, bps_tenantid=None, addl_scopes=None):
        if not self.bps_tenantid and not bps_tenantid:
            raise SyntaxError(
                "Error, can't authenticate unless you supply a tenant id from this list: {}".format(self.get_tenants()))
        if bps_tenantid and not self.bps_tenantid:
            self.bps_tenantid = bps_tenantid
        # 1. Get IAM token
        iam_url = "https://iam.mcafee-cloud.com/iam/v1.1/token"  # hard coded
        client_id = os.getenv("MVC_OAUTH_CLIENT_ID")
        if not client_id:
            raise LookupError("You need to set the OAuth Client ID in environment variable named MVC_OAUTH_CLIENT_ID")
        if addl_scopes:
            scopes = self._DEFAULT_SCOPES + " " + addl_scopes
        else:
            scopes = self._DEFAULT_SCOPES
        payload = {
            "client_id": client_id,
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": scopes,
            "tenant_id": self.bps_tenantid
        }
        res = self.session.post(iam_url, data=payload)  # handling directly here

        if res.status_code != 200:
            print("Could not get IAM token: " + res.text)
            raise RuntimeError("Exception, can't authenticate: {}".format(res.text))
        self.iam_token = res.json().get("access_token")
        # 2. Get Skyhigh Cloud tokens
        #    Now we can use the IAM token to get our session tokens for Skyhigh Cloud
        url = self.env + "/neo/neo-auth-service/oauth/token?grant_type=iam_token"
        heads = {'x-iam-token': self.iam_token}
        r = self.session.post(url, headers=heads)
        if r.status_code != 200:
            print("Could not authenticate to Skyhigh Cloud: {}".format(r.text))
            raise RuntimeError("Could not authenticate to Skyhigh Cloud: {}".format(r.text))
        self.lastauthdate = datetime.now()
        mvc_authinfo = r.json()
        self.tenantid = int(mvc_authinfo.get("tenantID"))
        self.authinfo = {
            'x-access-token': mvc_authinfo.get("access_token"),
            'x-refresh-token': mvc_authinfo.get("refresh_token"),
            'tenant-id': int(self.tenantid),
            'tenant-name': str(mvc_authinfo.get('tenantName')),
            'user-id': int(mvc_authinfo.get("userId")),
            'user-email': str(mvc_authinfo.get("email")),
            'user-name': str(mvc_authinfo.get("user")),
        }
        self.token_lifetime = mvc_authinfo.get("expires_in")
        session_headers = {'x-access-token': mvc_authinfo.get("access_token"),
                           'x-refresh-token': mvc_authinfo.get("refresh_token")}
        self.session.headers.update(session_headers)
        # print("Authenticated successfully")
        return True

    @property
    def tenantname(self):
        return self.authinfo.get("tenant-name")

    def check_password(self):
        # check if the password is ok
        try:
            res = self.authenticate(bps_tenantid=self.bps_tenantid)
            if res:
                self.login_error = None
                return res
        except Exception as e:
            self.login_error = e
            pass
        return False

    def get_tenants(self):
        if not self.tenants:
            # we handle this one direct as its so special
            url = self.env + "/shnapi/rest/external/api/v1/groups?source=shn.ec.x"
            res = self.session.get(url, auth=(self.username, self.password))
            if res.status_code != 200:
                raise PermissionError("Could not get associated tenants", res)
            self.tenants = res.json()
        return self.tenants

    def comm_dlp(self, method, url, params=None, jsondata=None, rawresponse=False):
        if self.needs_new_auth():
            self.authenticate()
        dlpapi_hostname = self.env.replace('www.', 'cmmw.')
        url = "{}/jsonapi/{}".format(dlpapi_hostname, url)
        dlpheaders = self.session.headers.copy()
        dlpheaders.update({"Authorization": "Bearer {}".format(self.iam_token)})
        try:
            res = self.session.request(method, url, json=jsondata, params=params, headers=dlpheaders)
        except requests.exceptions.ConnectionError as e:
            print("   ConnectionError during comm to url '{}', trying again".format(url), e)
            res = self.session.request(method, url, json=jsondata, params=params, headers=dlpheaders)
        if rawresponse:
            return res
        if res.status_code != 200:
            return {"error": res.text, "status_code": res.status_code}
        ret = res.json()
        return ret

    def comm_web(self, method, url, jsondata=None, rawresponse=False, with_etag="undef", extra_headers=None):
        if extra_headers is None:
            extra_headers = []
        if self.needs_new_auth():
            self.authenticate()
        if with_etag == "undef":  # if it's not explicitly set but set on a class level
            if self._web_get_etag:
                with_etag = True
        url = url.replace("##CID##", "customer_{}".format(self.bps_tenantid_web))
        url = "https://webpolicy.cloud.mvision.skyhigh.cloud/api{}".format(url)
        webheaders = self.session.headers.copy()
        webheaders.update({"Authorization": "Bearer {}".format(self.iam_token)})
        if extra_headers:
            for e in extra_headers:
                webheaders.update(e)
        try:
            res = self.session.request(method, url, json=jsondata, headers=webheaders)
        except requests.exceptions.ConnectionError as e:
            print("   ConnectionError during comm to url '{}', trying again".format(url), e)
            res = self.session.request(method, url, json=jsondata, headers=webheaders)
        if rawresponse:
            return res
        if res.status_code != 200:
            return {"error": res.text, "status_code": res.status_code}
        ret = res.json()
        if with_etag == True:
            ret = {"etag": res.headers.get("etag"), "payload": ret}
        return ret

    def comm(self, method, url, jsondata=None, trace=False, remove_iam_token_header=False):
        url = "{}{}".format(self.env, url)
        if self.needs_new_auth():
            self.authenticate()
        # since november the iam token header needs to be removed, otherwise the response will always be a 500 complianing that a redis server was not found
        # mohan babu tries to figure out why
        if "/neo/web-analytics-service/" in url:
            remove_iam_token_header = True
        iam_token_header = None
        if remove_iam_token_header and self.session.headers.get("x-iam-token"):
            # store and remove this header temporarily from the session
            iam_token_header = self.session.headers["x-iam-token"]
            del (self.session.headers["x-iam-token"])
        try:
            res = self.session.request(method, url, json=jsondata)
        except requests.exceptions.ConnectionError as e:
            print("   ConnectionError during comm to url '{}', trying again".format(url), e)
            res = self.session.request(method, url, json=jsondata)
        if remove_iam_token_header and iam_token_header:
            # add it again
            self.session.headers["x-iam-token"] = iam_token_header
        req = {"url": url, "data": jsondata}
        if trace:
            with open(str(round(datetime.now().timestamp(), 0)) + ".json", "w") as f:
                f.write("request:\n")
                f.write(pretty(req))
                f.write("\n")
                f.write("curlified:\n")
                f.write(curlify_request(res.request))
                f.write("\n")
                if res:
                    f.write("response:\n")
                    f.write(pretty(res.text))
        if res.status_code != 200:
            return {"error": res.text, "status_code": res.status_code}
        if res.text == "":  # sometimes an API call returns an empty string on OK
            return {}
        return res.json()

    def needs_new_auth(self):
        if not self.lastauthdate:
            return True
        since = datetime.now() - self.lastauthdate
        if since.total_seconds() >= self.token_lifetime:
            return True
        else:
            return False

    def call_iam_api(self, endpoint, verb="GET", payload=None):
        headers = {'authorization': "Bearer {}".format(self.iam_token)}
        url = "https://uam.api.trellix.com/prod/api{}".format(endpoint)
        if payload:
            res = self.session.request(verb, url, headers=headers, json=payload)
        else:
            res = self.session.request(verb, url, headers=headers)
        if res.status_code not in (200, 202):
            raise ConnectionAbortedError("Error {} while calling API endpoint: {}".format(res.status_code, res.text),
                                         res)
        return res.json()

    def get_iam_user_details(self):
        if self.iam_user_details:
            return self.iam_user_details
        res = self.call_iam_api("/v1/user")
        self.iam_user_details = res
        return self.iam_user_details

    def change_iam_password(self, new_password):
        # 1. get user details
        ud = self.get_iam_user_details()
        # patch verb .... nice
        payload = {"type": {"id": ud["type"].get("id")},
                   "profile": {
                       "firstName": ud["profile"].get("firstName"),
                       "lastName": ud["profile"].get("lastName"),
                       "primaryPhone": ud["profile"].get("primaryPhone"),
                       "tenantId": ud["profile"].get("tenantId"),
                       "locale": ud["profile"].get("locale"),
                       "login": ud["profile"].get("login"),
                       "email": ud["profile"].get("email")
                   },
                   "credentials": {"password": {"value": "{}".format(new_password)}}}
        res = self.call_iam_api("/v1/user", "PATCH", payload)
        # successfully changed the password. logout
        self.session.get(
            "https://iam.mcafee-cloud.com/iam/v1.0/logout?redirect_uri=https://auth.ui.trellix.com/email.html")
        self.session.close()
        print("Please kill this object and login again")
        return ("Please kill this object and login again")

    @staticmethod
    def parse_policy(pol):
        # parse the content of the policy into a dict
        rules = None
        try:
            rules = json.loads(pol.get('content'))
        except:
            pass
        pol["rules"] = rules
        pol["content"] = "<see rules>"
        return pol

    def get_config_audit_policies_count(self):
        # Request URL: Request URL: https://www.myshn.net/neo/config-audit/v1/getPoliciesCount
        data = {"searchRequest": {"policyStatus": [], "policyType": [], "policyIds": [], "policyCategory": [],
                                  "cisLevels": [], "cspIds": [], "start": 0, "limit": 500, "sortOrder": "desc",
                                  "sortBy": "edittime"}}
        ep = '/neo/config-audit/v1/getPoliciesCount'
        al = self.comm("POST", ep, data)
        print("Retrieved a count of {} config audit policies".format(str(al)))
        return al

    def list_config_audit_policies(self):
        ep = "https://{{fabric}}/neo/config-audit/v1/getPolicies"
        data = {"searchRequest": {"policyStatus": ["0"], "policyCategory": [], "cisLevels": [], "cspIds": [],
                                  "start": 0, "limit": 5, "sortOrder": "desc", "sortBy": "edittime"
                                  }}
        al = self.comm("POST", ep, data)
        print("Found a count of {} matching config audit policies".format(len(al)))
        return al

    def search_config_audit_policies(self, search_term):
        ep = "/neo/config-audit/v1/searchPolicies"
        data = {"searchParam": str(search_term)}
        al = self.comm("POST", ep, data)
        print("Found a count of {} matching config audit policies for term '{}'".format(len(al[0].get("items")),
                                                                                        search_term))
        return al[0].get("items")

    def search_DLP_policies(self, search_term):
        ep = "/neo/shndlpapi/v3/{}/policies/suggest".format(self.tenantid)
        data = {"search_param": str(search_term), "search_request": None, "type_id": None}
        al = self.comm("POST", ep, data)
        if al:
            print("Found a count of {} matching policies for term '{}'".format(len(al[0].get("items")), search_term))
            return al[0].get("items")
        return []

    def list_cwpp_policies(self, policy_types=None):
        ep = "/neo/shndlpapi/v1/{}/policies/search".format(self.tenantid)
        if not policy_types or not isinstance(policy_types, list):
            policy_types = list(PolicyType)
        policy_types = [str(e.value) for e in policy_types]
        data = {
            "type_id": None,
            "search_param": None,
            "search_request": {
                "policy_statuses": [],
                "policy_types": policy_types,
                "policy_ids": [],
                "csp_ids": [],
                "instance_ids": [],
                "start": 0,
                "limit": 1500,
                "sort_order": "desc",
                "sort_by": "name",
                "enabled": True,
                "metadata": {"policy_mode": [], "platform": []}
            }
        }
        al = self.comm("POST", ep, data)
        print("Found a count of {} matching config audit policies".format(len(al)))
        return al

    def get_config_audit_policy_by_id(self, policy_id):
        ep = "/neo/shndlpapi/v1/{}/policies/details/{}".format(self.tenantid, str(policy_id))
        return self.comm("GET", ep)

    def get_cwpp_policy_by_id(self, policy_id):
        ep = "/neo/config-audit/cwpp/ui/v1/loadPolicy/{}".format(str(policy_id))
        return self.comm("GET", ep)

    def save_config_audit_policy(self, policy_id, policy):
        ep = "/neo/shndlpapi/v1/{}/policies/details/{}".format(self.tenantid, policy_id)
        al = self.comm("PUT", ep, policy)
        print("Result from saving policy was {}".format(al['status']))
        return al['status']

    def save_cwpp_policy(self, policy_id, policy):
        ep = "/neo/config-audit/cwpp/ui/v1/savePolicy"
        al = self.comm("POST", ep, policy)
        print("Result from saving policy was {}".format(al['message']))
        return al['message']

    def get_policy_count(self, policy_types):
        filter = {"type_id": None, "search_param": None,
                  "search_request": {"policy_statuses": [], "policy_types": policy_types, "policy_ids": [],
                                     "csp_ids": [],
                                     "instance_ids": [], "start": 0, "limit": 1500, "sort_order": "desc",
                                     "sort_by": "edittime", "enabled": True,
                                     "metadata": {"policy_mode": [], "platform": []}}}
        ep = '/neo/shndlpapi/v1/{}/policies/count'.format(self.tenantid)
        al = self.comm("POST", ep, jsondata=filter)
        print("Retrieved a count of {} policies for policy types {}".format(al, policy_types))
        return int(al)

    def get_number_of_resources(self):
        # Request URL: Request URL: https://www.myshn.net/neo/config-audit/resource/v1/resourceCount
        data = {"iaaSResourcesFilterParams": [],
                "type": "AND",
                "sortInfo": {"sortColumn": "risk_score", "sortOrder": "desc"},
                "pageInfo": {"limit": 100, "offset": 0},
                "payload": {
                    "searchExpression": {"type": "and", "expressions": []},
                    "dateCriteria": {"datasetId": None, "fromTime": None, "toTime": None, "presetRange": "DEFAULT",
                                     "userPreferenceDateId": None},
                    "sortCriteria": {"sortColumn": "risk_score", "sortAscending": False},
                    "pageCriteria": {"startIndex": 0, "numRecords": 40}
                }
                }
        ep = '/neo/config-audit/resource/v1/resourceCount'
        rc = self.comm("POST", ep, jsondata=data, remove_iam_token_header=True)
        # only continue if we have a count, not a error message
        try:
            return int(rc)
        except:
            return None

    def get_all_instances(self):
        instance_url = "/neo/shndlpapi/v1/service-management/{}/all-instance-configs".format(self.tenantid)
        instances = self.comm("GET", url=instance_url)
        res_instances = []
        for k, v in instances.items():
            if isinstance(v, dict):
                res_instances.append(v)
        # print("Retrieved {} instances".format(len(res_instances)))
        return res_instances

    def disable_api_instance(self, ins):
        instance_id = ins.get("tenantInstanceInfo").get("id")
        cspid = ins.get("tenantInstanceInfo").get("cspId")
        # del "/neo/zeus/v1/80243/deregister-webhooks/2049/17970"
        res = self.comm("DELETE",
                        "/neo/zeus/v1/{}/deregister-webhooks/{}/{}".format(self.tenantid, cspid, instance_id))
        res = self.comm("DELETE",
                        "/neo/zeus/v1/{}/deregister-webhooks/{}".format(self.tenantid, cspid))
        # GET https://www.myshn.net/neo/shndlpapi/v1/dlp/oauth/revoke?tid=80243&cspid=2049&instanceid=17970
        res = self.comm("GET",
                        "/neo/shndlpapi/v1/dlp/oauth/revoke?tid={}&cspid={}&instanceid={}".format(self.tenantid, cspid,
                                                                                                  instance_id))

        # https://www.myshn.net/neo/zeus/v1/80243/csp-health/errors/2049/17970
        res = self.comm("DELETE", "/neo/zeus/v1/{}/csp-health/errors/{}/{}".format(self.tenantid, cspid, instance_id))

        # get https://www.myshn.net/neo/config-audit/v2/apiConfig/2049
        apiconfig = self.comm("GET", "/neo/config-audit/v2/apiConfig/{}".format(cspid))
        # POST https://www.myshn.net/neo/config-audit/v1/realTimeConfig/cleanup/2049/13731 {"api_config":{"accountId":"969816421732","supportedFeatures":["CONFIG_AUDIT","DLP"],"awsExternalId":"9022081","awsMultiAccounts":[{"accountId":"348422998519","hasErrors":false,"accountName":"mcafeelab","ownerEmails":[],"assumedRole":"arn:aws:iam::348422998519:role/McAfeeServiceRole","awsBucketNames":[]}],"realTimeConfig":null,"configMode":"MANUAL_ENTRY","policyAttachedAt":1582739708653,"sessionId":"9HdgI5udTs+9HUGI!@#$%IDneq/r4Up9T7hXQ9NdG9wTQz8/JinOiPAqZdeSGCpb30opuM8o+Yi1LEGhCOrSbILiZZ+9GGOLxkXkMprveipUxZG1E1PP+1Pr1tqosew=="},"delete_user":true,"type":"aws_real_time_cleanup_request"}
        if apiconfig and apiconfig.get("additionalDetails"):
            del_req = {"api_config": apiconfig.get("additionalDetails"),
                       "delete_user": True, "type": "aws_real_time_cleanup_request"}
            res = self.comm("POST", "/neo/config-audit/v1/realTimeConfig/cleanup/{}/{}".format(cspid, instance_id),
                            data=del_req)
        # del  https://www.myshn.net/neo/config-audit/v1/cleanup/iaasConfigs/2049/17970
        res = self.comm("DELETE", "/neo/config-audit/v1/cleanup/iaasConfigs/{}/{}".format(cspid, instance_id))
        if res:
            print("deleted iaasConfig")

        print("Disabled instance {}".format(ins))
        return

    def get_all_users_raw(self):
        url = '/neo/tenant-onboarding/v1/useradmin/searchUser'
        data = {"pageCriteria": {"startIndex": 0, "numRecords": 100},
                "sortCriteria": {"sortColumn": "lastLoginDate", "sortAscending": False}, "searchString": "",
                "tenantId": self.tenantid, "userRole": None}
        res = self.comm("POST", url, data)
        return res

    def get_mvc_audit_log(self, hours=4, event_categories=[]):
        # Request URL: https://www.myshn.net/neo/shnadmin-service/v1/auditService/auditEventsSummary
        now_ts = int(datetime.utcnow().timestamp()) * 1000
        # we need to add another 2 hours here, not sure why, otherwise we are 2 hours early to GMT
        now_ts = now_ts + (2 * 60 * 60 * 1000)
        four_hours_ago = now_ts - (hours * 60 * 60 * 1000)
        data = {"pageCriteria": {"startIndex": 0, "numRecords": 100},
                "sortCriteria": {"sortColumn": "timestamp", "sortAscending": False},
                "dateCriteria": {"fromTime": four_hours_ago, "toTime": now_ts, "presetRange": "CUSTOM"},
                "searchString": "", "eventCategories": event_categories, "events": [], "userIds": []}
        ep = '/neo/shnadmin-service/v1/auditService/auditEventsSummary'
        al = self.comm("POST", ep, data)
        print("Retrieved {} audit log entries for last {} hours".format(len(al), hours))
        return al

    def get_mvc_audit_log_count_by_user(self, hours=4, event_categories=[], userids=[]):
        # Request URL: https://www.myshn.net/neo/shnadmin-service/v1/auditService/auditEventsCount
        now_ts = int(datetime.utcnow().timestamp()) * 1000
        # we need to add another 2 hours here, not sure why, otherwise we are 2 hours early to GMT
        now_ts = now_ts + (2 * 60 * 60 * 1000)
        four_hours_ago = now_ts - (hours * 60 * 60 * 1000)
        data = {"pageCriteria": {"startIndex": 0, "numRecords": 100},
                "sortCriteria": {"sortColumn": "timestamp", "sortAscending": False},
                "dateCriteria": {"fromTime": four_hours_ago, "toTime": now_ts, "presetRange": "CUSTOM"},
                "searchString": "", "eventCategories": event_categories, "events": [], "userIds": userids}
        ep = '/neo/shnadmin-service/v1/auditService/auditEventsCount'
        al = self.comm("POST", ep, data)
        print(
            "Retrieved count of {} audit log entries for user {} during last {} hours".format(al.get("count"), userids,
                                                                                              hours))
        return al.get("count")

    def get_policy_templates(self, searchExpression=None):
        if not searchExpression:
            searchExpression = {"type": "and", "expressions": []}
        query = {
            "searchQuery": {"searchExpression": searchExpression,
                            "sortCriteria": {"ascending": False, "field": "last_modified_date"},
                            "pageCriteria": None}}
        url = "/neo/shndlpapi/v1/policy-templates/search"
        res = self.comm("POST", url, jsondata=query)
        templates = res.get("policy_templates")
        print("Retrieved {} policy templates for this filter".format(len(templates)))
        return templates

    def get_policy_template_facets(self, searchExpression=None):
        if not searchExpression:
            searchExpression = {"type": "and", "expressions": []}
        query = {
            "searchQuery": {"searchExpression": searchExpression,
                            "sortCriteria": {"ascending": False, "field": "last_modified_date"},
                            "pageCriteria": None}}
        url = "/neo/shndlpapi/v1/policy-templates/facets"
        res = self.comm("POST", url, jsondata=query)
        print("Retrieved {} policy terms_facets for this filter".format(len(res)))
        return res

    def dlp_get_policies(self, policy_types=[]):
        pol = {}  # array holding all policies
        pagesize = 300
        offset = 0
        req_count = 0

        search_filter = {"type_id": None, "search_param": None,
                         "search_request": {"policy_statuses": [], "policy_types": policy_types, "policy_ids": [],
                                            "csp_ids": [],
                                            "instance_ids": [], "start": 0, "limit": None, "sort_order": "asc",
                                            "sort_by": "name", "enabled": True}}

        # get first page
        # https://www.myshn.net/neo/shndlpapi/v3/77231/policies/search
        url = "/neo/shndlpapi/v3/{}/policies/search".format(self.tenantid)
        self.session.headers.update({'x-iam-token': self.iam_token})
        res = self.comm("POST", url, jsondata=search_filter)
        req_count += 1
        rescount = len(res)
        # map to a dict indexed by the policy id
        for p in res:
            pol[str(p.get('id'))] = self.parse_policy(p)
        print(
            "received {} policies".format(rescount))

        # now we can see what else we need to do
        # iterate / page as long as the result size is a big as the offset
        while rescount == pagesize:
            offset += pagesize
            # modify th filter
            search_filter['searchRequest']['start'] = offset
            # send another page
            res = self.comm("POST", url, jsondata=search_filter)
            req_count += 1
            rescount = len(res)
            print("received another {} policies in this page".format(rescount))
            # map to a dict indexed by the policy id
            for p in res:
                pol[str(p.get('id'))] = self.parse_policy(p)

        print("It took {} requests to fetch all {} policies".format(req_count, len(pol)))
        return pol

    def dlp_delete_policies(self, policy_ids: list):
        api_url = "/neo/shndlpapi/v3/{}/policies/delete/false".format(self.tenantid);
        res = self.comm("POST", api_url, policy_ids)
        return res

    def dlp_evaluate_policy(self, source_file=None, policy_ids="", number_of_times=1):
        # https://www.myshn.net/neo/shndlpapi/v1/policy-evaluation/77231/1
        filename = os.path.basename(source_file)
        form_data = {'file': (filename, open(source_file, "br"), 'application/octet-stream', {'Expires': '0'})}
        params = {"policy_ids": policy_ids, "numOfTimes": number_of_times}

        url = "/neo/shndlpapi/v1/policy-evaluation/{}/{}".format(self.tenantid, number_of_times)
        # handling the comms here directly as we need to build a multipart POST
        url = "{}{}".format(self.env, url)
        if self.needs_new_auth():
            self.authenticate()
        headers = dict(self.session.headers)
        if headers.get("x-iam-token"):
            del (headers["x-iam-token"])
        try:
            res = self.session.request("POST", url, params=params, files=form_data, headers=headers)
        except requests.exceptions.ConnectionError as e:
            print("   ConnectionError during comm to url '{}', trying again".format(url), e)
            res = self.session.request("POST", url, params=params, files=form_data, headers=headers)
        if res.status_code != 200:
            raise RuntimeError(res.text)
        return res.json()

    def dlp_get_classifications(self, addl_fields=None):
        fields = "name,category,precanned"
        if addl_fields:
            fields += " " + addl_fields
        params = {"sort": "name", "fields[classification]": fields}
        res = self.comm_dlp("GET", "classification", params=params)
        return res["data"]

    def dlp_is_classificationInUse(self, id):
        params = {"include": "policyReferences", "fields[classificationInUse]": "policyReferences",
                  "fields[policyReference]": "name,url,serviceType"}
        api_url = "classificationInUse/{}".format(id)
        res = self.comm_dlp("GET", api_url, params=params)
        if res.get("data") and len(res.get("data")) > 0:
            return res.get("data")
        return False

    def dlp_delete_classification(self, id):
        api_url = "classification/{}".format(id)
        res = self.comm_dlp("DELETE", api_url, rawresponse=True)
        if res.status_code != 204:
            raise RecursionError('Couldn\'t delete the classification {} "{}"'.format(res.status_code, res.text))
        return True

    def dlp_get_classificationCategories(self):
        fields = "name,precanned"
        params = {"sort": "name", "fields[classificationCategory]": fields}
        res = self.comm_dlp("GET", "classificationCategory", params=params)
        return res["data"]

    def dlp_delete_classificationCategory(self, id):
        api_url = "classificationCategory/{}".format(id)
        res = self.comm_dlp("DELETE", api_url, rawresponse=True)
        if res.status_code == 204:
            return True
        return False

    def dlp_get_classificationTextPatterns(self, addl_fields=None):
        fields = "name,precanned,classifications"
        if addl_fields:
            fields += " " + addl_fields
        params = {"sort": "name", "fields[classificationTextPattern]": fields}
        res = self.comm_dlp("GET", "classificationTextPattern", params=params)
        return res["data"]

    def dlp_delete_classificationTextPattern(self, id):
        api_url = "classificationTextPattern/{}".format(id)
        res = self.comm_dlp("DELETE", api_url, rawresponse=True)
        if res.status_code == 204:
            return True
        return False

    def dlp_get_fingerprint_definitions(self):
        ep = '/neo/shndlpapi/v1/dcube/definitions'
        res = self.comm("GET", ep)
        return res

    def dlp_delete_fingerprint_definition(self, definition_id):
        ep = '/neo/shndlpapi/v1/dcube/edit/{}/1/DELETE'.format(definition_id)
        res = self.comm("POST", ep, jsondata={})
        return res

    def update_incident_status(self, incident_id, old_status, new_status):
        # PUT https://www.myshn.net/neo/watchtower/ui/v1/77231/bulk/incident
        url = "/neo/watchtower/ui/v1/{}/bulk/incident".format(self.tenantid)
        payload = [{"tenant_id": self.tenantid,
                    "incident_id": incident_id,
                    "user_info": {"id": self.authinfo.get('user-id'), "name": self.authinfo.get('user-name'),
                                  "email": self.authinfo.get('user-email'),
                                  "user_type": "ADMIN"},
                    "update_fields": [
                        {"name": "status_id", "new_value": str(new_status), "old_value": str(old_status)}]}]
        r = self.comm("PUT", url, jsondata=payload)
        return r

    def get_workflow_statuses(self):
        return self.comm("GET", '/neo/watchtower/ui/v1/{}/workflow-statuses-v2'.format(self.tenantid))

    def quarantine_restore(self, incident_id):
        url = "/neo/watchtower/ui/v1/{}/remediation/remediate/{}/Quarantined%20Restore".format(self.tenantid,
                                                                                               incident_id)
        payload = {"remediatorId": self.authinfo.get('user-id'), "collaborators": None, "remediatorType": "ADMIN",
                   "remediatorEmail": self.authinfo.get('user-email'), "remediatorName": self.authinfo.get('user-name')}
        r = self.comm("POST", url, jsondata=payload)
        return r

    def add_incident_note(self, incident_id, incident_note):
        # first get the incident details, to get the latest version
        inc = self.get_incident_details(incident_id)
        last_note_version = 0
        if inc.get("notes_detail"):
            last_note_version = int(inc["notes_detail"]["version"])
        url = "/neo/watchtower/ui/v1/{}/incident/{}/note".format(self.tenantid, incident_id)
        ts = int(datetime.now().timestamp() * 1000)
        payload = {"type": "incident_note_request",
                   "incident_note": {"type": "incident_note", "note_id": None, "note": incident_note,
                                     "user_name": self.authinfo.get('user-name'),
                                     "user_id": self.authinfo.get('user-id'),
                                     "user_email": self.authinfo.get('user-email'),
                                     "is_external": False, "created_on_date": ts,
                                     "modified_on_date": ts}, "version": last_note_version}
        r = self.comm("POST", url, jsondata=payload)
        return r

    def get_incident_details(self, incident_id):
        url = "/neo/watchtower/ui/v1/{}/incident/{}".format(self.tenantid, incident_id)
        return self.comm("GET", url)

    def get_ui_deeplink(self, incident):
        return "{}/dlp-incidents/#/policy/incidents?incidentId={}".format(self.env, incident["workflow"]["id"])

    def get_inline_incidents(self, last=500, since_days=1):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=since_days)).isoformat()[:10]
        data = {"query_request": {
            "sort_dimensions": [{"field": "created_on_date", "order": "desc"}],
            "pagination": {"offset": 0, "limit": last},
            "search_query": {
                "type": "and_search_query", "queries": [
                    {"type": "equal_search_query", "value": "1", "field": "incident_detail.dev_ops_scan_mode"},
                    {"type": "between_search_query", "field": "created_on_date",
                     "lower_bound": since + "T00:00:00.000+00:00",
                     "upper_bound": today + "T23:59:59.000+00:00"
                     }
                ]
            }, "timezone": "UTC"},
            "add_default_filters": False,
            "incident_types": [0, 3, 4, 6, 7]
        }
        ep = '/neo/watchtower/ui/v1/{}/incident/search'.format(self.tenantid)
        incidents = self.comm("POST", ep, data).get("results")
        print("Found {} inline incidents".format(len(incidents)))
        return incidents

    def get_incident_facets(self, days=7):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {
            "search_query": {
                "type": "between_search_query",
                "field": "created_on_date",
                "lower_bound": since + "T00:00:00.000+00:00",
                "upper_bound": today + "T23:59:59.000+00:00"
            },
            "incident_types": ["policy_violation", "audit_violation", "cloud_access_policy_violation",
                               "malware_policy_violation", "connected_apps_violation", "vulnerability_violation",
                               "file_integrity_incident", "image_hardening_violation", "epo_violation"],
            "filter_type": "Policy",
            "selected_facets": []
        }
        url = '/neo/watchtower/ui/v1/{}/incident/facets'.format(self.tenantid)
        r = self.comm("POST", url, jsondata=filter)
        print("Found {} incident facets".format(len(r)))
        return r

    def get_incidents_since(self, incident_search_time_from, username=None):
        pvs = []  # array holding all policy violations
        pagesize = 1000
        offset = 0
        req_count = 0
        incomplete = False

        # build date strings
        from_ts = incident_search_time_from
        to_time = datetime.utcnow() - timedelta(
            hours=1)  # go one hour back to avoid incidents that are still in progress
        to_ts = to_time.strftime(date_format)  # now
        # build initial filter

        search_filter = {"query_request": {"sort_dimensions": [{"field": "created_on_date", "order": "asc"}],
                                           "pagination": {"offset": offset, "limit": pagesize},
                                           "search_query": {
                                               "type": "and_search_query", "queries":
                                                   [
                                                       {
                                                           "type": "equal_search_query",
                                                           "value": "policy_violation",
                                                           "field": "type"
                                                       },
                                                       {
                                                           "type": "between_search_query",
                                                           "field": "created_on_date",
                                                           "lower_bound": from_ts,  # the date filter
                                                           "upper_bound": to_ts
                                                       },
                                                       {  # type query: Open and new incidents only
                                                           "type": "in_search_query",
                                                           "field": "workflow.status_id",
                                                           "values": ["2001", "2002"]
                                                       }
                                                   ]
                                           }, "timezone": "UTC"},
                         "add_default_filters": False,
                         "incident_types": [0, 3, 4, 5, 6, 7, 8]
                         }

        # add username filter is needed:
        if username:
            search_filter['query_request']['search_query']['queries'].append(
                {"type": "equal_search_query",
                 "value": username,
                 "field": "incident_detail.user.name"}
            )
        # get first page
        url = "/neo/watchtower/ui/v1/{}/incident/search".format(self.tenantid)
        res = self.comm("POST", url, jsondata=search_filter)
        req_count += 1
        total_matching = res["total"]
        pvs.extend(res["results"])
        print(
            "received {} policy violations/incidents from {} matching the filter".format(len(pvs), total_matching))

        # now we can see what else we need to do
        # in this case we count to the total_matching (assuming it does not change)
        while len(pvs) < total_matching:
            offset += pagesize
            if offset >= 10000:
                incomplete = True
                print("we downloaded {} incidents, but we cannot download more than 10k incidents in one go".format(
                    len(pvs)))
                break
            # modify th filter
            search_filter['query_request']['pagination']['offset'] = offset
            # send another page
            res = self.comm("POST", url, jsondata=search_filter)
            req_count += 1
            print("received another {} policy violations in this page".format(len(res["results"])))
            pvs.extend(res["results"])

        print("It took {} requests to fetch all {} incidents matching the filter".format(req_count, len(pvs)))
        last_incident_ts = None
        if len(pvs) > 0:
            last_incident_ts = pvs[-1].get('created_on_date')
        result = {"pvs": pvs, "total_matching": total_matching, "result_incomplete": incomplete,
                  "last_incident_created_on_date": last_incident_ts}
        return result

    def get_all_incidents(self, incident_search_time_from, username=None):
        # we need to apply special pagination methods as the search API stops after responding with 10.000 incidents
        all_incidents = []
        incomplete = True
        while incomplete:
            res = self.get_incidents(incident_search_time_from, username=username)
            # check if the first incident is the same as the last incident from previous iteration
            if len(all_incidents) > 0 and res['pvs'][0].get('incident_id') == all_incidents[-1].get('incident_id'):
                del res['pvs'][0]  # then delete the first incident from the result
            all_incidents.extend(res['pvs'])
            incomplete = res['result_incomplete']
            incident_search_time_from = res["last_incident_created_on_date"]
            if incomplete:
                print("we have more than 10k incidents matching, so starting the next search from:{}".format(
                    incident_search_time_from))
        return all_incidents

    def get_users(self):
        url = "/neo/tenant-onboarding/v1/useradmin/searchUser"
        search = {"pageCriteria": {"startIndex": 0, "numRecords": 2500},
                  "sortCriteria": {"sortColumn": "lastLoginDate", "sortAscending": False}, "searchString": "",
                  "tenantId": 80285, "userRole": None}
        res = self.comm("POST", url, jsondata=search)
        return res

    def get_mpop_deployment_package(self, filename=None):
        url = "/neo/cwpp-updater-service/v1/pop-creation/pkg"
        url = "{}{}".format(self.env, url)
        if self.needs_new_auth():
            self.authenticate()
        # we need the IAM token for this call, too.
        self.session.headers.update({'x-iam-token': self.iam_token})
        res = self.session.get(url)
        if res.status_code != 200 or len(res.content) < 10000:
            print("ERROR: status code was {}".format(res.status_code))
            print("ERROR: response was: {}".format(res.text))
            print("ERROR: request was: {}".format(res.request))
            print("ERROR: request url was: {}".format(url))
            raise ConnectionAbortedError("Error downloading package: {}".format(res.text))
        if filename:
            with open(filename, 'wb') as f:
                f.write(res.content)
            print("Wrote package to file {}".format(filename))
        return res.content

    def get_list_of_mpops(self):
        url = "/neo/cwpp-pop-management-service/v1/popdata"
        res = self.comm("GET", url)
        self.mpops = res.get("popInfo")
        return self.mpops

    def get_mpop_id_by_name(self, mpopname):
        if not self.mpops:
            self.get_list_of_mpops()
        for p in self.mpops:
            if str(p.get("popName")) == str(mpopname):
                return p.get("id")
        return None

    def get_cwpp_client_deployment_package(self, mpopid, filename=None):
        url = "/neo/cwpp-updater-service/v1/cicd-config/pkg"
        url = "{}{}".format(self.env, url)
        if self.needs_new_auth():
            self.authenticate()
        params = {'popId': mpopid}
        res = self.session.get(url, params=params)
        if res.status_code != 200:
            raise ConnectionAbortedError("Error downloading package")
        if filename:
            with open(filename, 'wb') as f:
                f.write(res.content)
            print("Wrote package to file {}".format(filename))
        return res.content

    def do_mvc_graphql(self, data):
        return self.comm('POST', url='/neo/shndlpapi/v2/graphql', jsondata=data)

    def get_ods_status(self, scanConfigId):
        data = {
            "operationName": "ScanStatusQuery",
            "variables": {
                "scanConfigIds": [scanConfigId]
            },
            "query": "query ScanStatusQuery($scanConfigIds: [Int]!) {\n  getScanStatusByScanConfig(scanConfigIds: $scanConfigIds)\n}\n"
        }
        res = self.do_mvc_graphql(data)
        status = {}
        try:
            status = res.get('data').get('getScanStatusByScanConfig').get(str(scanConfigId))
        except:
            print("Could not get status for ods scan with scanConfigId {}".format(scanConfigId))
        return status

    def start_ods_scan(self, scanConfigId):
        data = {
            "operationName": "PerformActionMutation",
            "variables": {
                "dlpScanConfigId": scanConfigId,
                "action": "START"
            },
            "query": "mutation PerformActionMutation($dlpScanConfigId: Int!, $action: DlpScanActionInput!) {\n  performScanAction(dlpScanConfigId: $dlpScanConfigId, action: $action) {\n    statusId\n    scanId\n    scanConfigId\n    startTime\n    __typename\n  }\n}\n"
        }
        res = self.do_mvc_graphql(data)
        return res.get('data').get('performScanAction').get('statusId') == 0

    def get_ods_scans(self, type_filter=None):
        data = {
            "operationName": "ODSSummaryPageQuery",
            "variables": {
                "queryRequest": []
            },
            "query": "query ODSSummaryPageQuery($queryRequest: [OmnibarPillContainerInput], $sortColumn: SortColumnInput, $sortOrder: SortOrderInput) {\n  getScanOverview(scanFilter: {queryRequest: $queryRequest, sortOrder: $sortOrder, sortColumn: $sortColumn}) {\n    description\n    estimationSupported\n    scanId\n    scanConfigId\n    scanMode\n    scanName\n    scanType\n    scanPolicyType\n    schedule\n    status\n    runDate\n    readOnlyConfig\n    numErrors\n    numIncidents\n    scanInstanceCount\n    cspId\n    __typename\n  }\n}\n"
        }
        res = self.do_mvc_graphql(data)
        scans = []
        if res and res.get('data') and res['data'].get('getScanOverview'):
            for scan in res['data']['getScanOverview']:
                if type_filter and str(scan.get('scanType')) not in type_filter:
                    continue  # skip if filter did not match
                scans.append(scan)
            print("Retrieved {} ODS scans".format(len(scans)))
        else:
            print("Retrieved no ODS scans, response was: {}".format(res))
        return scans

    def shadow_get_service_groups(self):
        url = "/neo/events-analytics-service/v1/serviceGroups/serviceGroupGrid"
        filter = {"searchExpression": {"type": "and", "expressions": []},
                  "dateCriteria": {"datasetId": None, "fromTime": None, "toTime": None, "presetRange": "DEFAULT",
                                   "userPreferenceDateId": None},
                  "sortCriteria": {"sortColumn": "serviceGroupName", "sortAscending": True},
                  "pageCriteria": {"startIndex": 0, "numRecords": 100}}
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        return r

    def shadow_get_service_details(self, cspid: str):
        url = "/neo/service-workflow/servicedetails/{}".format(cspid)
        r = self.comm("GET", url)
        return r

    def shadow_get_unmatched_uploads_summary(self, sort_column="uploadData", num_records=100):
        """
        shadow_get_unmatched_uploads_summary gets the Shadow IT unmatched uploads information
        :param sort_column: The name of the field to sort descending.
                            Default 'uploadData' other examples 'uploadCount', 'LastDay'
        :param num_records: default 100, can be increased to query more rows
        :return: Array of entries as shown in the UI, up the 'num_records'
        """
        url = "/neo/events-analytics-service/v1/unmatcheduploads/summary"
        filter = {"searchExpression": {"type": "and", "expressions": []},
                  "dateCriteria": {"datasetId": None, "fromTime": None, "toTime": None, "presetRange": "LAST_MONTH",
                                   "userPreferenceDateId": None},
                  "sortCriteria": {"sortColumn": sort_column, "sortAscending": False},
                  "pageCriteria": {"startIndex": 0, "numRecords": num_records}}
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        return r

    def get_aws_auth_config(self):
        url = "/neo/config-audit/v1/authConfig/{}".format(self.CSPID_AWS)
        res = self.comm("GET", url)
        return res

    def web_get_customer_rootca(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/Customer_CA"
        res = self.comm_web("GET", url)
        return res

    def web_get_mpa_connector_groups(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/Connector_Group"
        connectors = self.comm_web("GET", url)
        details = {}
        if connectors and isinstance(connectors, list):
            for c in connectors:
                url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/Connector_Group/{}".format(c.get("id"))
                res = self.comm_web("GET", url)
                details[c.get("id")] = res
        return {"connector_groups": connectors, "details": details}

    def web_get_customerid(self):
        ctm = self.web_get_customer_tenant_map()
        return ctm.get("value")

    def web_get_customer_tenant_map(self):
        res = self.comm_web("GET", "/policy/v1/gps/content/product/Web/CustomerTenantMap/{}".format(self.bps_tenantid))
        return res

    def web_mcp_get_settings(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp"
        res = self.comm_web("GET", url)
        return res

    def web_mcp_get_gateway_lists(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp/proxies"
        res = self.comm_web("GET", url)
        return res

    def web_mcp_get_gateway_list_by_id(self, gateway_list_id):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp/proxies/{}".format(gateway_list_id)
        res = self.comm_web("GET", url)
        return res

    def web_mcp_get_gateway_list_by_name(self, gateway_list_name):
        for l in self.web_mcp_get_gateway_lists():
            if l["name"] == gateway_list_name:
                return self.web_mcp_get_gateway_list_by_id(l["id"])

    def web_policy_get_library_rulesets(self):
        url = "/policy/v2/RuleSetLibrary/list"
        res = self.comm_web("GET", url)
        return res["rulesetGroups"]

    def web_policy_get_library_ruleset_by_id(self, library_ruleset_id: str):
        url = "/policy/v2/RuleSetLibrary/id/{}".format(library_ruleset_id)
        res = self.comm_web("GET", url)
        return res

    def web_mcp_add_gateway_list(self, gateway_list):
        if not isinstance(gateway_list, dict) or not gateway_list.get("proxyList"):
            raise ConnectionAbortedError(
                "entry must be a dict in the style of a gateway list")

        # get current collection with hash:
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp/proxies"
        res = self.comm_web("GET", url, with_etag=True)
        gateway_lists_hash = res["etag"]
        proxy_coll = res["payload"].copy()

        # 2. append the new value
        gateway_list["id"] = str(uuid.uuid4())
        proxy_coll.append({"name": gateway_list["name"], "id": gateway_list["id"]})

        data = [{"op": "mcp/proxies.single.create",
                 "name": gateway_list["name"],
                 "path": "/mcp/proxies/{}".format(gateway_list["id"]),
                 "absolute": False,
                 "content": gateway_list,
                 "hash": "0"},
                {"op": "mcp/proxies.collection.update", "path": "/mcp/proxies",
                 "content": proxy_coll,
                 "hash": gateway_lists_hash}]
        url = "/policy/v1/commit"
        res = self.comm_web("POST", url, jsondata=data, rawresponse=True)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Didn't get a 200 for the commit", res)
        response = res.json()
        return response["hashes"]

    def web_mcp_get_policies(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp/policies"
        res = self.comm_web("GET", url)
        return res

    def web_mcp_get_policy_by_id(self, mcp_policy_id):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/mcp/policies/{}".format(mcp_policy_id)
        res = self.comm_web("GET", url)
        return res

    def web_mcp_get_policy_opg_by_id(self, mcp_policy_id):
        url = "/gps/v1/revision/latest/content/product/Web/Policy/##CID##/Policy/mcp/policies/{}/opg".format(
            mcp_policy_id)
        res = self.comm_web("GET", url, with_etag=False)  # etag would break this
        # result is the value in base64
        bin = base64.b64decode(res.get("value"))
        return bin

    def web_mcp_get_installer_bundle_by_id(self, mcp_policy_id, os="windows"):
        url_meta = "/mcpArchive/export/{}?os={}&bits=64".format(mcp_policy_id, os)
        res_meta = self.comm_web("GET", url_meta)
        cv = res_meta.get("cacheValue")
        if not cv:
            print("Could not download mcp installer bundle, no cacheValue")
            return None
        url_package = "/mcpArchive/download/{}".format(cv)
        # we handle the download of the package here completely separately as its multi MB, so we use streaming downloads
        if self.needs_new_auth():
            self.authenticate()
        url = "https://webpolicy.cloud.mvision.skyhigh.cloud/api{}".format(url_package)
        webheaders = self.session.headers.copy()
        webheaders.update({"Authorization": "Bearer {}".format(self.iam_token)})
        cs = 10240
        retbytes = bytes()
        f = BytesIO()
        try:
            r = self.session.get(url, headers=webheaders, stream=True)
            t = 0
            for chunk in r.iter_content(chunk_size=cs):
                t += cs
                f.write(chunk)
            f.seek(0)
            retbytes = f.read()
            f.close()
        except:
            print("Error downloading the package file")
        return retbytes

    def web_policy_lists_customer(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/lists"
        res = self.comm_web("GET", url)
        return res

    def web_policy_list_by_id(self, list_id):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/{}".format(list_id)
        res = self.comm_web("GET", url, rawresponse=True)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Could not get list detail", res)
        list = res.json()
        list.update({"hash": res.headers.get("ETag")})
        return list

    def web_policy_list_add_entry(self, list_id, entry):
        if not isinstance(entry, dict) or not entry.get("value"):
            raise ConnectionAbortedError(
                "entry must be a dict with at least the filed 'value'. Field 'comment' is optional")
        if not entry.get("comment"):
            entry["comment"] = ""
        # get current list:
        current = self.web_policy_list_by_id(list_id)

        # 1. create a copy
        newlist = current.copy()
        # 2 remove the hash code
        del (newlist["hash"])
        # 3 set the type if needed:
        if not newlist.get("type"):
            # we also need to figure out the type reliably
            lists = self.web_policy_lists_customer()
            for l in lists:
                if l["id"] == current["id"]:
                    newlist["type"] = l["type"]
                    break
        # 4 append the new value
        newlist["entries"].append(entry)
        # 5 append the new value
        if not newlist.get("listFeature"):
            newlist["listFeature"] = "User defined"

        data = [{"op": "lists.single.update",
                 "name": current.get("name"),
                 "path": "/{}".format(current.get("id")),
                 "absolute": False,
                 "content": newlist,
                 "hash": current.get("hash")}]
        url = "/policy/v1/commit"
        res = self.comm_web("POST", url, jsondata=data, rawresponse=True)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Didn't get a 200 for the commit", res)
        response = res.json()
        return response["hashes"]["/" + current.get("id")]

    def web_get_policy_lists(self, with_content=False):
        """ get the current tenant's lists and all content of those"""
        # .../Web/Policy/customer_1e76a680_3161_49b9_94db_faee9c049b68/Policy/lists
        p = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/lists",
                          with_etag=True)
        lists_root = {}
        if p.get("status_code") == 502:
            # sometimes we get a 502... then let's simply try again once more
            p = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/lists",
                              with_etag=True)
        if not p.get("payload"):
            raise KeyError("Did not receive a payload alongside the answer: '{}'".format(str(p)))
        lists_root["lists"] = copy(p["payload"])
        lists_root["etag"] = p["etag"]
        # print("Found {} lists for this tenant".format(len(lists_root["lists"])))
        if with_content and isinstance(lists_root["lists"], list):
            for list_entry in lists_root["lists"]:
                list_id = list_entry["id"]
                # print("getting list {}".format(list_id))
                r = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/{}".format(list_id),
                                  with_etag=True)
                if r.get("error"):
                    continue
                etag = r.get("eTag")  # sometimes in camelCase... sometimes not ... what a mess
                if not etag:
                    etag = r.get("etag")
                list_entry["etag"] = etag
                list_entry["payload"] = r["payload"]
        return lists_root

    def web_policy_list_replace_entries(self, list_id, entries):
        if not isinstance(entries, list) or not isinstance(entries[0], dict) or not entries[0].get("value"):
            raise SyntaxError("entry must be a list of dicts with at least the field 'value'. Field 'comment' "
                              "is optional")

        # get current list:
        current = self.web_policy_list_by_id(list_id)

        # 1. create a copy
        newlist = current.copy()
        # 2 remove the hash code
        del (newlist["hash"])
        # 3 set the type if needed:
        if not newlist.get("type"):
            # we also need to figure out the type reliably
            lists = self.web_policy_lists_customer()
            for l in lists:
                if l["id"] == current["id"]:
                    newlist["type"] = l["type"]
                    break
        # 4 replace the entries
        newlist["entries"] = entries
        # 5 set list type
        if not newlist.get("listFeature"):
            newlist["listFeature"] = "User defined"

        data = [{"op": "lists.single.update",
                 "name": current.get("name"),
                 "path": "/{}".format(current.get("id")),
                 "absolute": False,
                 "content": newlist,
                 "hash": current.get("hash")}]
        url = "/policy/v1/commit"
        res = self.comm_web("POST", url, jsondata=data, rawresponse=True)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Didn't get a 200 for the commit", res)
        response = res.json()
        return response["hashes"]["/" + current.get("id")]

    def web_policy_commit(self, data: list, clear_userchanges=False):
        """
        Commits changes to the web policy
        :param data: data is the list / array of ops to be committed
        :param clean_userchanges: if this is set to True all other outstanding userchanges will be cleaned before the commit
        :return: returns the json response as dict
        """
        if clear_userchanges:
            # not implemented, needs more sophisticated approach
            # res = self.session.request("PUT", "https://webpolicy.cloud.mvision.mcafee.com/api/userchanges", json={})
            pass
        url = "/policy/v1/commit"
        res = self.comm_web("POST", url, jsondata=data, rawresponse=True)
        if res.status_code == 409:
            raise KeyError("Web Policy Commit failed: {}".format(res.text), res)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Didn't get a 200 for the commit: {}".format(res.text), res)
        response = res.json()
        return response

    def web_get_traffic_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0",
                  "table_name": "WEB_TRAFFIC", "logSource": location,
                  "select_expression": {"field_names": ["siteName", "reputationName", "categoryId", "serviceId"],
                                        "aliases": [
                                            {"alias": "total_bytes", "field": "totalBytes", "isAggregate": True,
                                             "aggregateFunction": "sum"},
                                            {"alias": "request_hits", "field": "requestHits", "isAggregate": True,
                                             "aggregateFunction": "sum"},
                                            {"alias": "allowed_count", "field": "allowedCount", "isAggregate": True,
                                             "aggregateFunction": "sum"},
                                            {"alias": "denied_count", "field": "deniedCount", "isAggregate": True,
                                             "aggregateFunction": "sum"},
                                            {"alias": "bytes_uploaded", "field": "bytesUploaded", "isAggregate": True,
                                             "aggregateFunction": "sum"},
                                            {"alias": "bytes_downloaded", "field": "bytesDownloaded",
                                             "isAggregate": True, "aggregateFunction": "sum"},
                                            {"alias": "malware_count", "field": "malwareName", "isAggregate": True,
                                             "aggregateFunction": "COUNT_DISTINCT"},
                                            {"alias": "protection_area_id", "field": "protectionAreaId",
                                             "isAggregate": True, "aggregateFunction": "ARRAY_AGG"},
                                            {"alias": "protection_area_count", "field": "protectionAreaId",
                                             "isAggregate": True, "aggregateFunction": "COUNT_DISTINCT"},
                                            {"alias": "isolation_type", "field": "isolationType", "isAggregate": True,
                                             "aggregateFunction": "ARRAY_AGG"},
                                            {"alias": "isolated_count", "field": "isolationType", "isAggregate": True,
                                             "aggregateFunction": "COUNT"},
                                            {"alias": "user_count", "field": "userName", "isAggregate": True,
                                             "aggregateFunction": "COUNT_DISTINCT"}]}, "limit": 1000, "offset": 0,
                  "group_by": ["siteName", "reputationName", "categoryId", "serviceId"], "sql_template": "Site",
                  "use_r_cache": True, "search_expression": {"type": "and", "expressions": [
                {"type": "notEq", "filter_name": "isolationType", "values": ["3"]}]},
                  "sort_criteria": [{"sortAscending": False, "sortColumn": "siteName"}]}
        url = '/neo/web-analytics-service/v1/webanalytics/queries/webtraffic'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        res = []
        if r.get("list"):
            res = r["list"]
        print("Found {} web traffic sites".format(len(res)))
        return res

    def web_get_user_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0", "table_name": "WEB_USER",
                  "logSource": location, "select_expression": {"field_names": ["userName"], "aliases": [
                {"alias": "site_count", "field": "siteName", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "reputation_name", "field": "reputationName", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "reputation_count", "field": "reputationName", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "application_name", "field": "serviceId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "application_name_count", "field": "serviceId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "application_category", "field": "categoryId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "application_category_count", "field": "categoryId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "total_bytes", "field": "totalBytes", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "request_hits", "field": "requestHits", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "allowed_count", "field": "allowedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "denied_count", "field": "deniedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "bytes_uploaded", "field": "bytesUploaded", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "bytes_downloaded", "field": "bytesDownloaded", "isAggregate": True,
                 "aggregateFunction": "sum"}, {"alias": "malware_count", "field": "malwareName", "isAggregate": True,
                                               "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "protection_area_id", "field": "protectionAreaId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "protection_area_count", "field": "protectionAreaId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "isolation_type", "field": "isolationType", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "isolated_count", "field": "isolationType", "isAggregate": True,
                 "aggregateFunction": "COUNT"}]}, "limit": 1000, "offset": 0, "group_by": ["userName"],
                  "sql_template": "User", "use_r_cache": True, "search_expression": {"type": "and", "expressions": [
                {"type": "notEq", "filter_name": "isolationType", "values": ["3"]}]},
                  "sort_criteria": [{"sortAscending": True, "sortColumn": "userName"}]}
        url = '/neo/web-analytics-service/v1/webanalytics/queries/webuser'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        res = []
        if r.get("list"):
            res = r["list"]
        print("Found {} web traffic sites".format(len(res)))
        return res

    def web_get_malware_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0", "table_name": "MALWARE",
                  "logSource": location, "select_expression": {"field_names": ["malwareName"], "aliases": [
                {"alias": "total_bytes", "field": "totalBytes", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "request_hits", "field": "requestHits", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "allowed_count", "field": "allowedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "denied_count", "field": "deniedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "bytes_uploaded", "field": "bytesUploaded", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "bytes_downloaded", "field": "bytesDownloaded", "isAggregate": True,
                 "aggregateFunction": "sum"}, {"alias": "user_count", "field": "userName", "isAggregate": True,
                                               "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "user_name", "field": "userName", "isAggregate": True, "aggregateFunction": "ARRAY_AGG"},
                {"alias": "ip_address", "field": "ipAdddress", "isAggregate": True, "aggregateFunction": "ARRAY_AGG"},
                {"alias": "ip_address_count", "field": "ipAdddress", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "site_count", "field": "siteName", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "application_name", "field": "serviceId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "application_name_count", "field": "serviceId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "application_category", "field": "categoryId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "application_category_count", "field": "categoryId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "protection_area_id", "field": "protectionAreaId", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "protection_area_count", "field": "protectionAreaId", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "mcp_enabled", "field": "mcpEnabled", "isAggregate": True, "aggregateFunction": "ARRAY_AGG"},
                {"alias": "url_category", "field": "urlCategory", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"}]}, "limit": 1000, "offset": 0, "group_by": ["malwareName"],
                  "sql_template": None, "use_r_cache": True, "search_expression": {"type": "and", "expressions": []},
                  "sort_criteria": [{"sortAscending": False, "sortColumn": "malwareName"}]}
        url = '/neo/web-analytics-service/v1/webanalytics/queries/malware'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)

        res = []
        if r.get("list"):
            res = r["list"]
        print("Found {} malware stats".format(len(res)))
        return res

    def web_get_private_access_usage_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {
            "begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0",
            "table_name": "PRIVATE_ACCESS_TRAFFIC",
            "logSource": location,
            "select_expression": {"field_names": ["paApplicationName"], "aliases": [
                {"alias": "total_bytes", "field": "totalBytes", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "request_hits", "field": "requestHits", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "allowed_count", "field": "allowedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "denied_count", "field": "deniedCount", "isAggregate": True, "aggregateFunction": "sum"},
                {"alias": "requested_host_count", "field": "requestedHost", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "requested_host_name", "field": "requestedHost", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "app_group_count", "field": "appGroupName", "isAggregate": True,
                 "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "app_group_name", "field": "appGroupName", "isAggregate": True,
                 "aggregateFunction": "ARRAY_AGG"},
                {"alias": "lastactivity", "field": "requestTimestamp", "isAggregate": True,
                 "aggregateFunction": "MAX_FIELD"}, {"alias": "user_count", "field": "userName", "isAggregate": True,
                                                     "aggregateFunction": "COUNT_DISTINCT"},
                {"alias": "user_name", "field": "userName", "isAggregate": True, "aggregateFunction": "ARRAY_AGG"}]},
            "limit": 100,
            "offset": 0,
            "group_by": ["paApplicationName"],
            "sql_template": None,
            "use_r_cache": True,
            "search_expression": {"type": "and", "expressions": []},
            "sort_criteria": [{"sortAscending": False, "sortColumn": "lastActivity"}],
            "selected_time_zone": None
        }
        url = '/neo/web-analytics-service/v1/private-access/privatetraffic'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        if r.get("list"):
            pa_list = r["list"]
        else:
            pa_list = []
        print("Found {} private access traffic entries".format(len(pa_list)))
        return pa_list

    def web_get_isolated_traffic_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0",
                  "table_name": "ISOLATED_TRAFFIC", "logSource": location, "select_expression": {
                "field_names": ["userName", "siteName", "timeSpent", "reputationName", "urlCategory", "isolationType",
                                "isolatedRequestTime"], "aliases": []}, "limit": 1000, "offset": 0, "group_by": [""],
                  "sql_template": None, "use_r_cache": False, "search_expression": {"type": "and", "expressions": []},
                  "sort_criteria": [{"sortAscending": False, "sortColumn": "isolatedRequestTime"}]}
        url = '/neo/web-analytics-service/v1/webanalytics/queries/isolatedtraffic'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        print("Found {} isolated traffic sites".format(len(r)))
        return r

    def web_get_isolated_filetransfer_stats(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0",
                  "table_name": "FILE_TRANSFER_ACTIVITY", "logSource": location, "select_expression": {
                "field_names": ["userName", "siteName", "fileName", "fileSize", "direction", "requestURL",
                                "isolationType", "isolatedRequestTime", "statusCode"], "aliases": []}, "limit": 1000,
                  "offset": 0, "group_by": None, "sql_template": None, "use_r_cache": True,
                  "search_expression": {"type": "and", "expressions": [
                      {"type": "notEq", "filter_name": "isolationType", "values": ["3", "0"]},
                      {"type": "notEq", "filter_name": "fileName", "values": [None]}]},
                  "sort_criteria": [{"sortAscending": False, "sortColumn": "isolatedRequestTime"}]}
        url = '/neo/web-analytics-service/v1/webanalytics/queries/filetransfer'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True)
        res = []
        if r.get("list"):
            res = r["list"]
        print("Found {} isolated filetransfer stats".format(len(res)))
        return res

    def web_get_traffic_by_action(self, days=7, location="NA"):
        today = datetime.utcnow().isoformat()[:10]
        since = (datetime.now() - timedelta(days=days)).isoformat()[:10]
        filter = {"begin_date": since + " 00:00:00+0", "end_date": today + " 23:59:59+0", "table_name": "WEB_TRAFFIC",
                  "facet_name": "actionTaken", "logSource": location, "search_expression": {"type": "and",
                                                                                            "expressions": [
                                                                                                {"type": "notEq",
                                                                                                 "filter_name": "isolationType",
                                                                                                 "values": ["3"]}]},
                  "category_type_id": "ACTION_TAKEN", "category_type_name": "Action Taken", "use_r_cache": True}
        url = '/neo/web-analytics-service/v1/webanalytics/facet'
        r = self.comm("POST", url, jsondata=filter, remove_iam_token_header=True, trace=False)
        res = []
        if r.get("list"):
            res = r["list"]
        print("Found {} web traffic actions".format(len(res)))
        # reformat the dict
        by_action = {}
        for l in res:
            by_action[l["facetName"]] = l["usageCount"]
        # mandatory fields:
        for i in ["Allowed", "Denied"]:
            if not by_action.get(i):
                by_action[i] = 0
        return by_action

    def web_settings_locations(self):
        # https://webpolicy.cloud.mvision.mcafee.com/api/policy/v1/gps/content/product/Web/Policy/customer_b...9/Policy/locations
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/locations"
        res = self.comm_web("GET", url, with_etag=True)
        return res

    def web_get_hybridstatus(self):
        # https://webpolicy.cloud.mvision.skyhigh.cloud/api/hybridstatus
        url = "/hybridstatus"
        res = self.comm_web("GET", url)
        return res

    def web_get_url_categories(self):
        url = "/policy/v1/gps/content/product/Web/UI/URLCategories"
        res = self.comm_web("GET", url)
        return res

    def web_get_appcontrol_categories(self):
        url = "/policy/v1/gps/content/product/Web/UI/ApplicationControl/Categories"
        res = self.comm_web("GET", url)
        return res

    def web_get_appcontrol_applications(self):
        url = "/policy/v1/gps/content/product/Web/UI/ApplicationControl/Applications"
        res = self.comm_web("GET", url)
        return res

    def web_get_appcontrol_activities(self):
        url = "/policy/v1/gps/content/product/Web/UI/ApplicationControl/Activities"
        res = self.comm_web("GET", url)
        return res

    def web_get_appcontrol_genericactivities(self):
        url = "/policy/v1/gps/content/product/Web/UI/ApplicationControl/GenericActivities"
        res = self.comm_web("GET", url)
        return res

    @staticmethod
    def web_get_list_of_included_part_ids(part_in):
        # static methos
        includes = []
        if part_in.get("value"):
            mowgli_source = part_in.get("value")
        elif part_in.get("payload"):
            mowgli_source = part_in.get("payload")["value"]
        else:
            raise SyntaxError("Can't get payload value from part")
        for mowgli_line in mowgli_source.split("\n"):
            mowgli_line = mowgli_line.strip()
            m = _REGEX_WEB_POLICY_INCLUDES.match(mowgli_line)
            if m and len(m.groups()) > 1:
                if "//" in m.group(1):  # if this line is commented out
                    continue
                inc_id = m.group(2).strip()
                includes.append(inc_id)
        return includes

    def web_get_policy_settings(self):
        """ get the current tenant's settings and all content of those"""
        # .../Web/Policy/customer_1e76a680_3161_49b9_94db_faee9c049b68/Policy/settings
        p = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/settings",
                          with_etag=True)
        settings_root = {}
        settings_root["settings"] = copy(p["payload"])
        settings_root["etag"] = p["etag"]
        # print("Found {} settings for this tenant".format(len(settings_root["settings"])))
        for setting in settings_root["settings"]:
            setting_id = setting["id"]
            if setting_id == "Customer_CA":
                continue
            # print("getting setting {}".format(setting_id))
            r = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/{}".format(setting_id),
                              with_etag=True)
            setting["etag"] = r["etag"]
            setting["payload"] = r["payload"]
        return settings_root

    def get_policy_child_node(self, parent_node, child_node_id, with_ui=True, recursive=False):
        child_node_path = parent_node.get("path") + "/" + child_node_id
        # build the skeleton
        child_node = {"id": child_node_id, "name": None, "value": None, "ui": {}, "etag": None,
                      "path": child_node_path,
                      "children": []}
        # print("Getting policy node: {}".format(child_node_path))
        resp = self.comm_web("GET",
                             "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy{}".format(child_node_path),
                             with_etag=True)
        if resp.get("error") and resp.get("status_code") != 200:
            child_node["error"] = True
            child_node["error_detail"] = str(resp)
            return child_node
        # add flesh
        child_node["etag"] = resp.get("etag")
        child_node["name"] = resp["payload"].get("name")
        child_node["value"] = resp["payload"].get("value")
        child_node["ui"] = {"name": resp["payload"].get("ui"), "etag": None, "path": None, "payload": {}}
        if with_ui and child_node["ui"].get("name"):
            child_ui_node_path = parent_node.get("path") + "/" + child_node["ui"]["name"]
            child_node["ui"]["path"] = child_ui_node_path
            resp_ui = self.comm_web("GET",
                                    "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy{}".format(
                                        child_ui_node_path),
                                    with_etag=True)
            if resp_ui.get("etag"):
                child_node["ui"]["etag"] = resp_ui["etag"]
                child_node["ui"]["payload"] = resp_ui["payload"]
        if recursive:
            # dive in recursively into the family tree
            grandchildren_ids = self.web_get_list_of_included_part_ids(child_node)
            # now dive into recursive mode
            for grandchild_node_id in grandchildren_ids:
                grandchild_node = self.get_policy_child_node(child_node, grandchild_node_id, recursive=True)
                child_node["children"].append(grandchild_node)
        return child_node

    def web_get_web_policy_part(self, path):
        """convenience function to get only a part fo a web policy, always with etag. e.g. '/device-profiles'"""
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy{}"
        return self.comm_web("GET", url=url.format(path), with_etag=True)

    def web_get_full_web_policy(self):
        """ getting the full web proxy policy in jsTree format
        https://www.jstree.com/docs/json/
        """
        # get policy root
        p = self.comm_web("GET", "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy", with_etag=True)
        if p.get("error"):
            raise InterruptedError("Error in web_get_full_web_policy during comm_web", p)
        policy_root = copy(p["payload"])
        policy_root["etag"] = p["etag"]
        policy_root["path"] = ""
        policy_root["children"] = []
        # parse INCLUDE statements of the root node

        children_ids = self.web_get_list_of_included_part_ids(p)
        # add Private Access child even if not referenced in the root policy
        # children_ids.append("Private_Access")
        # now dive into recursive mode
        for child_node_id in children_ids:
            child_node = self.get_policy_child_node(policy_root, child_node_id, recursive=True)
            policy_root["children"].append(child_node)
        return policy_root

    def web_get_backup_customer_policy(self, export_password: str, target_file: str = None):
        # https://webpolicy.cloud.mvision.skyhigh.cloud/api/policy/v2/PolicyMigrator/backup_customer_policy
        extra_headers = [{"x-auth": export_password}]
        p = self.comm_web("GET", "/policy/v2/PolicyMigrator/backup_customer_policy",
                          extra_headers=extra_headers, rawresponse=True)
        if p.status_code != 200:
            raise AssertionError("Could not load policy backup for tenant, non 200 received", p)
        print("Downloaded a backup with {} bytes".format(len(p.content)))
        if target_file:
            with open(target_file, 'wb') as f:
                f.write(p.content)
            print("Wrote package to file {}".format(target_file))
        return p

    def web_set_policy_restore_default(self):
        # https://webpolicy.cloud.mvision.skyhigh.cloud/api/policy/v2/PolicyMigrator/reset
        p = self.comm_web("POST", "/policy/v2/PolicyMigrator/reset")
        return p

    def web_set_policy_restore_backup_file(self, data=None, source_file=None):
        # https://webpolicy.cloud.mvision.skyhigh.cloud/api/policy/v2/PolicyMigrator/restore_customer_policy
        if not data:
            with open(source_file, 'r') as f:
                data = f.read()
            print("Read {} bytes from file {}".format(len(data), source_file))
        # doing the comms here directly so no need to add binary upload to comm_web
        url = "https://webpolicy.cloud.mvision.skyhigh.cloud/api/policy/v2/PolicyMigrator/restore_customer_policy"
        res = self.session.request("POST", url, data=data)
        return res.json()
