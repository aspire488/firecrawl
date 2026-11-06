import pytest
from firecrawl.v2.types import CrawlParamsRequest
from firecrawl.v2.methods.aio import crawl as aio_crawl


@pytest.mark.asyncio
async def test_crawl_params_request_validation():
    with pytest.raises(ValueError):
        await aio_crawl.crawl_params_preview(None, CrawlParamsRequest(url="", prompt="x"))
    with pytest.raises(ValueError):
        await aio_crawl.crawl_params_preview(None, CrawlParamsRequest(url="https://x", prompt=""))



@pytest.mark.asyncio
async def test_crawl_params_preview_converts_nested_scrape_options():
    from unittest.mock import AsyncMock, Mock

    response = Mock(status_code=200)
    response.json.return_value = {
        "success": True,
        "data": {
            "scrapeOptions": {
                "includeTags": ["main", "article"],
                "excludeTags": ["nav", "footer"],
                "onlyMainContent": False,
                "waitFor": 250,
                "skipTlsVerification": True,
                "removeBase64Images": False,
                "headers": {"X-Test": "value"},
            }
        },
    }
    client = Mock()
    client.post = AsyncMock(return_value=response)

    result = await aio_crawl.crawl_params_preview(
        client, CrawlParamsRequest(url="https://example.com", prompt="Find articles")
    )

    assert result.scrape_options.include_tags == ["main", "article"]
    assert result.scrape_options.exclude_tags == ["nav", "footer"]
    assert result.scrape_options.only_main_content is False
    assert result.scrape_options.wait_for == 250
    assert result.scrape_options.skip_tls_verification is True
    assert result.scrape_options.remove_base64_images is False
    assert result.scrape_options.headers == {"X-Test": "value"}


@pytest.mark.asyncio
async def test_crawl_params_preview_preserves_null_scrape_options():
    from unittest.mock import AsyncMock, Mock

    response = Mock(status_code=200)
    response.json.return_value = {
        "success": True,
        "data": {"scrapeOptions": None},
    }
    client = Mock()
    client.post = AsyncMock(return_value=response)

    result = await aio_crawl.crawl_params_preview(
        client, CrawlParamsRequest(url="https://example.com", prompt="Find articles")
    )

    assert result.scrape_options is None
