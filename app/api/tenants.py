import re
from opensearchpy import OpenSearch
from opensearchpy.helpers.query import MultiMatch
import connexion
from connexion.lifecycle import ConnexionRequest



async def search():

    request: ConnexionRequest = connexion.context.request
    client = request.state.client
    index_name = "tenants"
    query = {
        "query": {
            "match_all": {}
        }
    }


    response = client.search(index=index_name, body=query)
    tenants = []
    try:
        if 'hits' in response and isinstance(response['hits'], dict):
            if 'hits' in response['hits'] and isinstance(response['hits']['hits'],list):
                    for hit in response['hits']['hits']:
                        description = hit['_source'].get('description','')

                        #REGEX
                        
                        match = re.search(r"NAME: (.+), DATA: (.+)", description) if description else None
                        name, data = match.groups() if match else ("Unknown", "Unknown")
                        
                        tenants.append({
                        "id": hit['_id'],
                        "name": name,
                        "data": data
                        })

                        return tenants
            else:
                return {"message": "Invalid hits field"}, 404
        else:
            return {"message": "Invalid response"}, 404
    except Exception as e:
        return {"message": str(e)}, 500
    
    
