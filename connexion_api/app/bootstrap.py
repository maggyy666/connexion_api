import connexion 
from connexion import RestyResolver
from app.settings import settings
from app.api import tenants, anomaly_detection
from opensearchpy import OpenSearch
import contextlib
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from connexion.middleware import MiddlewarePosition

"""
Initializes and configures the Connexion application.

Defines the lifespan handler for managing the OpenSearch client lifecycle,
and sets up the API using an OpenAPI specification.
"""


@contextlib.asynccontextmanager
async def lifespan_handler(app):
    client = OpenSearch(
        hosts=[settings.opensearch_host],
        http_auth = (settings.opensearch_user, settings.opensearch_password),
        use_ssl = True,
        verify_certs = False)
    yield {"client": client}
    client.close()

def run():
    app = connexion.AsyncApp(
        __name__,
        specification_dir='../schema/',
        lifespan=lifespan_handler
    )

    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_EXCEPTION,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],

    )

    app.add_api(
        'openapi.yaml',
        resolver=RestyResolver('app.api'),
        pythonic_params=True,
        pass_context_arg_name='request',
        validate_responses=True
    )


    app.run(host=settings.HOST, port=settings.PORT)
