from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=["https://localhost:9200"],
    http_auth = ('admin', 'StrongPassw0rd!'),
    use_ssl = True,
    verify_certs = False
)
async def get_anomaly_detection(tenant_id: str):
    index_name = "anomaly_detection"
    
    query = {
        "query":{
            "match":{
                "tenant_id": tenant_id
            }
        }
    }
    response = client.search(index=index_name, body=query)

    if response["hits"]["total"]["value"] > 0:
        hit = response["hits"]["hits"][0]
        return {
            "detector_id": hit["_source"].get("detector_id",'Unknown'),
            "detector_name":hit["_source"].get("name",'Unknown'),
            "detector_description":hit["_source"].get("description",'No description available')

        }
    else:
        return {"message": "Anomaly detection not found"}, 404