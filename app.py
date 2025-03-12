import connexion 
from connexion import RestyResolver
from api.anomaly_detection import get_anomaly_detection
from api.tenants import get_tenants



app = connexion.App(__name__, specification_dir='.')

app.add_api('openapi.yaml', resolver=RestyResolver('api'), pythonic_params=True)

if __name__ == "__main__":
    app.run(port=8080)