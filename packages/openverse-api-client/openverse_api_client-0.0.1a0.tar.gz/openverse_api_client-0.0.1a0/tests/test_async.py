import pytest

from openverse_api_client import AsyncOpenverseClient


@pytest.fixture
def client():
    return AsyncOpenverseClient()


@pytest.mark.asyncio
async def test_image_stats(client):
    stats = await client.GET_v1_images_stats()

    assert isinstance(stats, list)
    source_names = [s["source_name"] for s in stats]
    assert "flickr" in source_names

@pytest.mark.asyncio
async def test_thumbnail(client):
    image_search = await client.GET_v1_images(q="dogs")

    assert isinstance(image_search, dict)
    image = image_search["results"][0]

    thumbnail = await client.GET_v1_images_thumbnail(identifier=image["id"])
    assert isinstance(thumbnail, bytes)
