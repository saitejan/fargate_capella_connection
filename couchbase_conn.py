from datetime import timedelta
import os
# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

import logging
from couchbase import configure_logging
# from config import Settings, temp
configure_logging(__name__, logging.DEBUG)

temp = {
    "endpoint" : "",
    "username" : "",
    "password" : "",
    "bucket_name" : "",
    "cb_scope" : "",
    # "cb_scope" : "",
    # "cb_collection" : "",
    "cb_collection" : "",
}

# Update this to your cluster
endpoint = temp["endpoint"]
username = temp["username"]
password = temp["password"]
bucket_name = temp["bucket_name"]
cb_scope = temp["cb_scope"]
cb_collection = temp["cb_collection"]
# User Input ends here.
# print(endpoint)
# Connect options - authentication
auth = PasswordAuthenticator(username, password)

# Connect options - global timeout opts
timeout_opts = ClusterTimeoutOptions(connect_timeout=timedelta(seconds=20), 
                                     kv_timeout=timedelta(seconds=20))

# get a reference to our cluster
cluster = Cluster('couchbases://'+str(endpoint),
                  ClusterOptions(auth, timeout_options=timeout_opts))

# Wait until the cluster is ready for use.
cluster.wait_until_ready(timedelta(seconds=5))

# get a reference to our bucket
cb = cluster.bucket(bucket_name)

cb_coll = cb.scope(cb_scope).collection(cb_collection)

def upsert_document(doc):
    try:
        key = doc["_type"] + "_" + str(doc["id"])
        result = cb_coll.upsert(key, doc)
        print(result.cas)
    except Exception as e:
        print(e)

# get document function
def get_rows_by_key(key):
    print("\nGet Result: ")
    try:
        result = cb_coll.get(key)
        print(result.content_as[str])
        return dict(result.value)
        # sql_query = f"SELECT VALUE id FROM {bucket_name}.{cb_scope}.{cb_collection} WHERE id = $1"
        # row_iter = cluster.query(
        #     sql_query,
        #     QueryOptions(positional_parameters=[key]))
        # return [row for row in row_iter]
    except Exception as e:
        print(e)

# query for new document by callsign
def lookup_by_column(ky, vl):
    print("\nLookup Result: ")
    try:
        sql_query = f"SELECT VALUE name FROM `{bucket_name}`.{cb_scope}.{cb_collection} WHERE {ky} = $1"
        row_iter = cluster.query(
            sql_query,
            QueryOptions(positional_parameters=[vl]))
        for row in row_iter:
            print(row)
    except Exception as e:
        print(e)

# airline = {
#     "type": "airline",
#     "id": 8091,
#     "callsign": "CBS",
#     "iata": None,
#     "icao": None,
#     "name": "Couchbase Airways",
# }

cust = {
    "id": 4,
    "_type": "customer",
    "crypto_rank": 0,
    "debit_rank": 0,
    "wallet_rank": 0,
    "opted_for_crypto": False,
    "opted_for_debit": False,
    "opted_for_wallet": False
}

upsert_document(cust)

# get_airline_by_key("airline_8091")

# lookup_by_callsign("CBS")