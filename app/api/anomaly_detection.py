from opensearchpy import OpenSearch
from opensearchpy.helpers.query import MultiMatch, Match
from connexion.lifecycle import ConnexionRequest
import connexion
from connexion import problem
from app.models import AnomalyDetector

"""
Handles the /anomaly_detection/{tenant_id} endpoint.

Searches for anomaly detectors linked to a specific tenant using OpenSearch.
Includes structured error handling with RFC 7807-compliant responses.
"""



async def get(tenant_id: str):

    request : ConnexionRequest = connexion.context.request
    client = request.state.client

    index_name = "anomaly_detection"
    

    query = Match(tenant_id=tenant_id)

    response = client.search(index=index_name, body={'query': query.to_dict()})
    try:
            if 'hits' in response and isinstance(response['hits'], dict):
                if 'total' in response['hits'] and isinstance(response['hits']['total'], dict):
                    if 'value' in response['hits']['total'] and isinstance(response['hits']['total']['value'], int):
                        if response['hits']['total']['value'] > 0:
                            hit = response['hits']['hits'][0]
                            detector = AnomalyDetector(
                                 detector_id=hit['_source'].get('detector_id', 'Unknown'),
                                 detector_name=hit['_source'].get('name', 'Unknown'),
                                 detector_description=hit['_source'].get('description', 'Unknown')
                            )
                            return detector.model_dump()
                        else:
                            return problem(404, "Not Found", "No detectors found for this tenant")
                    else:
                        return problem(404, "Not Found", "Invalid total field")
                else:
                     return problem(404, "Not Found", "Missing total field")
            else:
                 return problem(404, "Not Found", "Invalid hits field")
    except Exception as e:
         return problem(500, "Internal Server Error", str(e))

