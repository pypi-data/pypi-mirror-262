import argparse
import csv
import os
from copy import copy
from datetime import datetime

import requests


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
    _web_get_etag = False
    login_error = None

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

    def authenticate(self, bps_tenantid=None):
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
        payload = {
            "client_id": client_id,
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "shn.con.r web.adm.x web.rpt.x web.rpt.r web.lst.x web.plc.x web.xprt.x web.cnf.x uam:admin",
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

    def get_tenants(self):
        if not self.tenants:
            # we handle this one direct as its so special
            url = self.env + "/shnapi/rest/external/api/v1/groups?source=shn.ec.x"
            res = self.session.get(url, auth=(self.username, self.password))
            if res.status_code != 200:
                raise PermissionError("Could not get associated tenants", res)
            self.tenants = res.json()
        return self.tenants

    def comm_web(self, method, url, jsondata=None, rawresponse=False, with_etag="undef", extra_headers=[]):
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

    def web_get_customerid(self):
        ctm = self.web_get_customer_tenant_map()
        return ctm.get("value")

    def web_policy_lists_customer(self):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/lists"
        res = self.comm_web("GET", url)
        return res

    def web_policy_list_by_id(self, list_id):
        url = "/policy/v1/gps/content/product/Web/Policy/##CID##/Policy/{}".format(list_id)
        res = self.comm_web("GET", url, rawresponse=True)
        if not res.status_code == 200:
            raise ConnectionAbortedError("Could not get list detail, no such list with id {}".format(list_id), res)
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
                etag = r.get("eTag")  # sometimes in camelCase... sometimes not
                if not etag: etag = r.get("etag")
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


if __name__ == '__main__':
    # Instantiate the parser and give it a description that will show before help
    parser = argparse.ArgumentParser(description='SkyhighSSEListUpdate')

    # Add arguments to the parser
    parser.add_argument('--username', dest='username', type=str, required=True, help='Username for Skyhigh SSE Admin')
    parser.add_argument('--password', dest='password', type=str, required=True, help='Password for Skyhigh SSE Admin')
    parser.add_argument('--bps-tenant-id', dest='bps_tenant_id', type=str, required=True,
                        help='BPS Tenant ID for the tenant to connect to (looks like a uuid)')
    parser.add_argument('--list-id', dest='list_id', type=str, required=True, help='The ID of the list to replace')
    parser.add_argument('--input-file', dest='input_file', type=str, required=True,
                        help='The full path to the input file')

    # Run method to parse the arguments
    args = parser.parse_args()

    password_env = os.getenv("SSEPASSWORD", None)
    if not args.password and not password_env:
        print("Error you need to supply a password. Either though argument --password "
              "or in the env variable SSEPASSWORD")
        exit(1)

    if not args.username:
        print("Error you need to supply a username.")
        exit(1)

    if not args.bps_tenant_id:
        print("Error you need to supply a BPS Tenant ID.")
        exit(1)

    if not args.list_id:
        print("Error you need to supply a List ID.")
        exit(1)

    if password_env and not args.password:
        password = password_env
        print("Using password from env variable")
    else:
        password = args.password

    # Connect and authenticate
    m = MvcConnection(username=args.username, password=password,
                      bps_tenantid=args.bps_tenant_id)
    res = m.authenticate()
    if not res:
        print("Could not authenticate")
        exit(2)

    # read input file to entries dict:
    new_entries = []
    with open(args.input_file, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            new_entries.append(row)
    print("Read {} entries from file {}".format(len(new_entries), args.input_file))
    res = m.web_policy_list_replace_entries(list_id=args.list_id, entries=new_entries)
    print("Done, commit etag was {}".format(res))
