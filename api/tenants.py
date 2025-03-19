import re
from opensearchpy import OpenSearch


client = OpenSearch(
    hosts=["https://localhost:9200"],
    http_auth = ('admin', 'StrongPassw0rd!'),
    use_ssl = True,
    verify_certs = False
)
async def search():
    index_name = "tenants"
    query = {"query": {"match_all": {}}}

    response = client.search(index=index_name, body=query)
    tenants = []
    for hit in response['hits']['hits']:
        description = hit['_source'].get('description','')

        #REGEX
        match = re.search(r"NAME: (.+), DATA: (.+)", description)
        name, data = match.groups() if match else ("Unknown", "Unknown")
        tenants.append({
            "id": hit['_id'],
            "name": name,
            "data": data
        })
    return tenants
