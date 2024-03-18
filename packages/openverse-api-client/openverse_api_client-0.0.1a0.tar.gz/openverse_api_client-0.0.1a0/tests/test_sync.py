import pytest

from openverse_api_client import OpenverseClient


@pytest.fixture
def client():
    return OpenverseClient()


def test_image_stats(client: OpenverseClient):
    stats = client.GET_v1_images_stats()

    assert isinstance(stats, list)
    source_names = [s["source_name"] for s in stats]
    assert "flickr" in source_names


def test_thumbnail(client):
    image_search = client.GET_v1_images(q="dogs")

    assert isinstance(image_search, dict)
    image = image_search["results"][0]

    thumbnail = client.GET_v1_images_thumbnail(identifier=image["id"])
    assert isinstance(thumbnail, bytes)
