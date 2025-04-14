from pydantic import BaseModel

class AnomalyDetector(BaseModel):
    detector_id: str
    detector_name: str
    detector_description: str

class Tenant(BaseModel):
    id: str
    name: str
    data: str


#TO-DO: Add @classmethod to map from OpenSearch _source.
