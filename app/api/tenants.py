import re
from opensearchpy import OpenSearch
from opensearchpy.helpers.query import MultiMatch
from opensearchpy.exceptions import NotFoundError, TransportError
import connexion
from connexion.lifecycle import ConnexionRequest
from connexion import problem
from app.models import Tenant
"""
Handles the /tenants endpoint.

Performs tenant search operations using OpenSearch and parses tenant descriptions
using regular expressions. Responses follow RFC 7807 via Connexion's `problem()` function.
"""


async def search():

    request: ConnexionRequest = connexion.context.request
    client = request.state.client
    index_name = "tenants"

    # Prints all data that matches the query
    

    tenants = []
    query = MultiMatch(query='NAME',fields=['description'], operator='and') 

    try:
        
        response = client.search(index=index_name, body={'query': query.to_dict()})


        if 'hits' in response and isinstance(response['hits'], dict):
            if 'hits' in response['hits'] and isinstance(response['hits']['hits'],list):
                    hits = response['hits']['hits']
                    if not hits:
                        return problem(404, "Not Found", "No tenants found")
                    for hit in hits:
                        description = hit['_source'].get('description','')

                        #REGEX
                        
                        match = re.search(r"NAME: (.+), DATA: (.+)", description) if description else None
                        name, data = match.groups() if match else ("Unknown", "Unknown")

                        tenant = Tenant(
                            id=hit['_source'].get('id', 'Unknown'),
                            name=name,
                            data=data
                        )
                        tenants.append(tenant.model_dump())
                    
                    return tenants
                        

            else:
                return problem(404, "Not Found", "Invalid hits field")
        else:
            return problem(404, "Not Found", "Invalid hits field")

    
    except NotFoundError as e:
        return problem(404, "Not Found", "Index 'tenants' does not exist in OpenSearch")
    
    except TransportError as e:
        return problem(500, "OpenSearch Transport Error", f"Error: {str(e)}")
    
    except Exception as e:
        return problem(500, "Internal Server Error", str(e))
    

    
    
