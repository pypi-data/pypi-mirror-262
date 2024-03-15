import os
from json import JSONDecodeError

import httpx
import pytest

from .utils import get_supported_media_types


def pytest_collection_modifyitems(items):
    # Run the collected test functions in order of conformance test number
    items[:] = sorted(items, key=lambda item: int(item.name.replace("test_ct", "")))


try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass


@pytest.fixture(scope="session")
def instance_url() -> str:
    try:
        load_dotenv()
    except NameError:
        pass
    return os.environ.get("INSTANCE_URL", "")


if os.getenv("CLIENT_OVERRIDDEN") != "True":

    @pytest.fixture(scope="session")
    def http_client(instance_url: str) -> httpx.Client:
        with httpx.Client() as client:
            client.base_url = instance_url
            yield client


@pytest.fixture(scope="session", autouse=True)
def suite_props(record_testsuite_property, instance_url):
    record_testsuite_property("instance-url", instance_url)


@pytest.fixture(scope="session")
def implemented_media_types() -> set:
    return {"application/geo+json", ...}


@pytest.fixture(scope="session")
def collections(http_client) -> list[dict]:
    response = http_client.get("/collections", headers={"Accept": "application/json"})
    try:
        collections = response.json().get("collections", [])
    except JSONDecodeError:
        collections = []
    return collections


@pytest.fixture(scope="session")
def filterable_resources(
    collections: list[dict], http_client: httpx.Client, implemented_media_types: set
) -> list[dict]:
    resources = []
    for collection in collections:
        # Check for supported media types
        response = http_client.get(f"/collections/{collection['id']}/items")
        supported_media_types = get_supported_media_types(response)
        media_types = supported_media_types.intersection(implemented_media_types)
        if media_types:
            media_type = (
                media_types.pop()
            )  # Only keep one of the supported media types for testing
        else:
            raise Exception(
                f"None of the media types supported at {collection['id']} have been implemented in this test suite."
            )
        resource = dict()
        resource["id"] = collection["id"]
        resource["url"] = f"/collections/{collection['id']}/items"
        resource["media_type"] = media_type
        resources.append(resource)
    return resources
