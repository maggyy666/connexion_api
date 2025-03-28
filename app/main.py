import connexion 
from connexion import RestyResolver
from .api import anomaly_detection, tenants
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings

app = connexion.AsyncApp(__name__, specification_dir='../schema/')


app.add_api(
    'openapi.yaml',
    resolver=RestyResolver('app.api'),
    pythonic_params=True,
    validate_responses=True
)
def main():
    app.run(host=settings.HOST, port=settings.PORT)

if __name__ == "__main__":
    main()