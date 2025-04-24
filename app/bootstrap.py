import connexion 
from connexion import RestyResolver
from app.settings import settings
from app.api import tenants, anomaly_detection
from opensearchpy import OpenSearch, exceptions
import contextlib
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from connexion.middleware import MiddlewarePosition
import time
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
    for attempt in range(10):
        try:
            if client.ping():
                print("[OpenSearch] Ping successful")
                break
            else:
                print(f"[OpenSearch] Ping failed, attempt {attempt + 1}/10")
        except Exception as e:
            print(f"[OpenSearch] Connection failed on attempt {attempt + 1}/10, retrying in 3s... ({e})")
        time.sleep(3)
    else:
        print("[OpenSearch] ERROR: Could not connect after 10 attempts")

    ensure_index_exists(client, "tenants")
    ensure_index_exists(client, "anomaly_detection")
    yield {"client": client}
    client.close()

def ensure_index_exists(client: OpenSearch, index_name: str, retries: int = 5, delay: int = 3):
    for attempt in range(retries):
        try:
            if not client.indices.exists(index=index_name):
                if index_name == "tenants":
                    body = {
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0
                        },
                        "mappings": {
                            "properties": {
                                "name": {"type": "text"},
                                "description": {"type": "text"},
                            }
                        }
                    }
                elif index_name == "anomaly_detection":
                    body = {
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0
                        },
                        "mappings": {
                            "properties": {
                                "tenant_id": {"type": "keyword"},
                                "detection_id": {"type": "keyword"},
                                "name": {"type": "text"},
                                "description": {"type": "text"}
                            }
                        }
                    }
                else:
                    body = {}
                client.indices.create(index=index_name, body=body)
                print(f"[OpenSearch] Created index: {index_name}")
            else:
                print(f"[OpenSearch] Index already exists: {index_name}")
            return  # <--- DODAJ TO, jeśli sukces
        except exceptions.ConnectionError as e:
            print(f"[OpenSearch] Connection failed on attempt {attempt + 1}/{retries}, retrying in {delay}s...")
            time.sleep(delay)
        except exceptions.OpenSearchException as e:
            print(f"[OpenSearch] Error creating index {index_name}: {e}")
            break
        except Exception as e:
            print(f"[OpenSearch] Unexpected error: {e}")
            break





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
        validate_responses=False
    )


    app.run(host=settings.HOST, port=settings.PORT)
