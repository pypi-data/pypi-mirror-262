import argparse
import os

import MVC
from MVC import MvcConnection


def save_json_to_file(in_obj: dict, filename: str):
    with open(filename, mode="w", encoding="UTF-8") as f:
        f.write(MVC.pretty(in_obj))


if __name__ == '__main__':
    # Instantiate the parser and give it a description that will show before help
    parser = argparse.ArgumentParser(description='SkyhighSSEPolicyBackup')

    # Add arguments to the parser
    parser.add_argument('--username', dest='username', type=str, required=True, help='Username for Skyhigh SSE Admin')
    parser.add_argument('--password', dest='password', type=str, required=True,
                        help='Password for Skyhigh SSE Admin, can also be provided in environment variable SSEPASSWORD')
    parser.add_argument('--bps-tenant-id', dest='bps_tenant_id', type=str, required=True,
                        help='BPS Tenant ID for the tenant to connect to (looks like a uuid)')
    parser.add_argument('--backup-password', dest='backup_pass', type=str, required=True,
                        help='Password for Backup encryption')

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

    if not args.backup_pass:
        print("Error you need to supply a Backup password.")
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
    backup_files = []
    # get policy backup
    policy_backup_fname = "customer_{}_policy.zip".format(m.bps_tenantid)
    m.web_get_backup_customer_policy(export_password=args.backup_pass, target_file=policy_backup_fname)
    backup_files.append(policy_backup_fname)
    # get scp policies
    scp_policy_ids = m.web_mcp_get_policies()
    print("Found {} SCP Policies".format(len(scp_policy_ids)))
    for sp in scp_policy_ids:
        # download policy details as json files
        scp_policy_fname = "scp_policy_{}.json".format(sp["id"])
        print("Saving SCP Policy named '{}' to file '{}'".format(sp["name"], scp_policy_fname))
        save_json_to_file(in_obj=m.web_mcp_get_policy_by_id(sp["id"]), filename=scp_policy_fname)
        backup_files.append(scp_policy_fname)
        # download OPG file for this policy
        opg_binary = m.web_mcp_get_policy_opg_by_id(sp["id"])
        opg_filename = "scp_policy_{}.opg".format(sp["id"])
        print("Saving SCP Policy '{}' OPG file to '{}'".format(sp["name"], opg_filename))
        with open(opg_filename, mode="wb") as of:
                of.write(opg_binary)
        backup_files.append(opg_filename)
    # get gateway lists
    scp_gatewaylist_ids = m.web_mcp_get_gateway_lists()
    print("Found {} SCP Gateway Lists".format(len(scp_gatewaylist_ids)))
    for gwl in scp_gatewaylist_ids:
        gwl_fname = "scp_gatewaylist_{}.json".format(gwl["id"])
        print("Saving SCP Gateway List named '{}' to file '{}'".format(gwl["name"], gwl_fname))
        save_json_to_file(in_obj=m.web_mcp_get_gateway_list_by_id(gwl["id"]), filename=gwl_fname)
        backup_files.append(gwl_fname)
    print("Done, with backup, saved {} files".format(len(backup_files)))
    print(MVC.pretty(backup_files))
