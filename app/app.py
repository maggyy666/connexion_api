import connexion 
from connexion import RestyResolver
from api import anomaly_detection, tenants
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware


app = connexion.App(__name__, specification_dir='.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    middleware_position=MiddlewarePosition.BEFORE_REQUEST
)


app.add_api('openapi.yaml', resolver=RestyResolver('api'), pythonic_params=True)

if __name__ == "__main__":
    app.run(port=8080)