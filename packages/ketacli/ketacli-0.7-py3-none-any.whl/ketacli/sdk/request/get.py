from ..util import is_fuzzy_key

ASSET_MAP = {
    # key 都小写
    "repos": {
        "path": "repos",
    },
    "sourcetype": {
        "path": "sourcetype",
    },
    "targets": {
        "path": "metric/targets",
    },
    "bizsystems": {
        "path": "target/bizSystems"
    },
    "metrics": {
        "path": "metric/metrics"
    }
}


def get_asset_by_id_request(asset_type, asset_id, **kwargs):
    path = asset_type
    key = is_fuzzy_key(asset_type, value_map=ASSET_MAP)
    if key != None:
        path = ASSET_MAP.get(key)["path"] + "/" + asset_id
    else:
        path = f"{asset_type}/{asset_id}"

    return {
        "path": path,
        "query_params": {},
        # list 操作用不到的内容
        "method": "get",
        "data": {},
        "custom_headers": {},
    }
