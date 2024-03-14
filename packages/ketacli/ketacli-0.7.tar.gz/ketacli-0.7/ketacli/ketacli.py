from mando import command, main
from datetime import datetime

from ketacli.sdk.base.client import *
from ketacli.sdk.base.search import search_spl
from ketacli.sdk.request.list import list_assets_request
from ketacli.sdk.request.get import get_asset_by_id_request

from ketacli.sdk.output.output import list_output, describe_output, get_asset_output
from ketacli.sdk.output.output import search_result_output
import json
from ketacli.sdk.output.format import format_table


@command
def login(name="keta", endpoint="http://localhost:9000", token=""):
    """Login to ketadb, cache authentication info to ~/.keta/config.yaml

    :param repository: Repository to push to.
    :param -n, --name: The login account name. Defaults to "keta".
    :param -e, --endpoint: The ketadb endpoint. Defaults to "http://localhost:9000".
    :param -t, --token: Your keta api token, create from ketadb webui. Defaults to "".
    """
    do_login(name=name, endpoint=endpoint, token=token)


@command
def logout():
    """Logout from ketadb, clear authentication info"""
    do_logout()


@command
def list(asset_type, groupId=-1, order="desc", pageNo=1, pageSize=10, prefix="", sort="updateTime", fields="", format=None):
    """List asset (such as repo,sourcetype,metric...) from ketadb

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param -l, --pageSize: Limit the page size.
    :param --pageNo: Limit the page number.
    :param --prefix: Fuzzy query filter.
    :param --sort: The field used to order by
    :param --order: The sort order, desc|asc
    :param --fields: The fields to display. Separate by comman, such as "id,name,type"
    :param -f, --format: The output format, text|json|csv|html|latex
    :param --groupId: The resource group id.
    """
    req = list_assets_request(
        asset_type, groupId, order, pageNo, pageSize, prefix, sort)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    output_fields = []
    if len(fields.strip()) > 0:
        output_fields = fields.strip().split(",")
    table = list_output(asset_type, output_fields=output_fields, resp=resp)
    if table is None:
        print(f"we cannot find any {asset_type}")
    else:
        print(format_table(table, format))


@command
def get(asset_type, asset_id, fields="", format=None):
    """Get asset detail info from ketadb

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param asset_id: The unique id of asset. (such as id or name...)
    :param --fields: The fields to display. Separate by comman, such as "id,name,type"
    :param -f, --format: The output format, text|json|csv|html|latex
    """
    req = get_asset_by_id_request(asset_type=asset_type, asset_id=asset_id)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    output_fields = []
    if len(fields.strip()) > 0:
        output_fields = fields.strip().split(",")
    table = get_asset_output(output_fields=output_fields, resp=resp)
    table.align = "l"
    if table is None:
        print(f"we cannot find any {asset_type}")
    else:
        print(format_table(table, format))


@command
def describe(asset_type, format=None):
    """Describe the schema of asset type

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param -f, --format: The output format, text|json|csv|html|latex
    """

    req = list_assets_request(asset_type)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    table = describe_output(asset_type, resp=resp)
    if table is None:
        print(f"we cannot find any {asset_type}")
    else:
        print(format_table(table, format))


@command
def search(spl, start=None, end=None, limit=100, format=None):
    """Search spl from ketadb

    :param spl: The spl query 
    :param --start: The start time. Time format "2024-01-02 10:10:10"
    :param --end: The start time. Time format "2024-01-02 10:10:10"
    :param -l, --limit: The limit size of query result
    :param -f, --format: The output format, text|json|csv|html|latex
    """
    if start != None:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    if end != None:
        end = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    resp = search_spl(spl=spl, start=start, end=end, limit=limit)
    table = search_result_output(resp)
    if table is None:
        print(f"we cannot find any data")
    else:
        print(format_table(table, format))


@command
def insert(repo="default", data=None, file=None):
    """Upload data to specified repo

    :param --repo: The target repo
    :param --data: The json string data [{"raw":"this is text", "host": "host-1"}]
    :param --file: Upload json text from file path.
    """
    if repo is None:
        print(f"Please specify target repo with --repo")
        return
    if data is None and file is None:
        print(f"Please use --data or --file to specify data to upload")
        return

    if file is not None:
        f = open(file)
        data = f.read()

    query_params = {
        "repo": repo,
    }
    resp = request_post("data", json.loads(data), query_params).json()
    print(resp)


if __name__ == "__main__":
    main()
