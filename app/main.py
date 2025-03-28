import connexion 
from connexion import RestyResolver
from .api import anomaly_detection, tenants
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings
import contextlib
from opensearchpy import OpenSearch
import typing

@contextlib.asynccontextmanager
async def lifespan_handler(app):
    client = OpenSearch(
        hosts=[settings.opensearch_host],
        http_auth = (settings.opensearch_user, settings.opensearch_password),
        use_ssl = True,
        verify_certs = False)
    yield {"client": client}
    client.close()


app = connexion.AsyncApp(__name__, specification_dir='../schema/',lifespan=lifespan_handler)

app.add_api(
    'openapi.yaml',
    resolver=RestyResolver('app.api'),
    pythonic_params=True,
    pass_context_arg_name='request',
    validate_responses=True
)
def main():
    app.run(host=settings.HOST, port=settings.PORT)

if __name__ == "__main__":
    main()