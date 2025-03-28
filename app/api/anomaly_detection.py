from opensearchpy import OpenSearch
from opensearchpy.helpers.query import MultiMatch
from connexion.lifecycle import ConnexionRequest
import connexion

async def get(tenant_id: str):

    request = ConnexionRequest = connexion.context.request
    client = request.state.client

    index_name = "anomaly_detection"
    
    query = {
        "query":{
            "match":{
                "tenant_id": tenant_id
            }
        }
    }

    response = client.search(index=index_name, body=query)
    try:
            if 'hits' in response and isinstance(response['hits'], dict):
                if 'total' in response['hits'] and isinstance(response['hits']['total'], dict):
                    if 'value' in response['hits']['total'] and isinstance(response['hits']['total']['value'], int):
                        if response['hits']['total']['value'] > 0:
                            hit = response['hits']['hits'][0]
                            return {
                                "detector_id": hit['_source'].get('detector_id','Unknown'),
                                "detector_name": hit['_source'].get('name','Unknown'),
                                "detector_description": hit['_source'].get('description','No description available')
                            }
                        else:
                            return {"message": "No data found"}, 404
                    else:
                        return {"message": "Invalid value field"}, 404
                else:
                     return {"message": "Missing total field"}, 404
            else:
                 return {"message": "Missing hits field"}, 404
    except Exception as e:
         return {"message": str(e)}, 500

