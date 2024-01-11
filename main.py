from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import (
    Body,
    FastAPI,
    Request,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()


app = FastAPI(lifespan=lifespan)


async def make_hc_ping_request(url: str, request: Request, payload: Any = Body(None)):
    requests_client: httpx.AsyncClient = request.app.requests_client

    headers: dict = dict()
    for header_name in ("Content-Type", "User-Agent"):
        if header_name in request.headers:
            headers["User-Agent"] = request.headers["User-Agent"]

    request_kwargs: dict = dict(
        method=request.method,
        url=url,
        headers=headers,
    )

    if request.method == "POST":
        request_kwargs["data"] = payload
    response = await requests_client.request(**request_kwargs)

    return response.content


@app.get("/ping/{uuid}")
@app.head("/ping/{uuid}")
@app.post("/ping/{uuid}")
async def ping_uuid_success(
    request: Request,
    uuid: str,
    payload: Any = Body(None),
):
    proxy_url = f"https://hc-ping.com/{uuid}"
    return await make_hc_ping_request(url=proxy_url, request=request, payload=payload)


@app.get("/ping/{uuid}/start")
@app.head("/ping/{uuid}/start")
@app.post("/ping/{uuid}/start")
async def ping_uuid_start(
    request: Request,
    uuid: str,
    payload: Any = Body(None),
):
    proxy_url = f"https://hc-ping.com/{uuid}/start"
    return await make_hc_ping_request(url=proxy_url, request=request, payload=payload)


@app.get("/ping/{uuid}/fail")
@app.head("/ping/{uuid}/fail")
@app.post("/ping/{uuid}/fail")
async def ping_uuid_fail(
    request: Request,
    uuid: str,
    payload: Any = Body(None),
):
    proxy_url = f"https://hc-ping.com/{uuid}/fail"
    return await make_hc_ping_request(url=proxy_url, request=request, payload=payload)


@app.get("/ping/{uuid}/log")
@app.head("/ping/{uuid}/log")
@app.post("/ping/{uuid}/log")
async def ping_uuid_log(
    request: Request,
    uuid: str,
    payload: Any = Body(None),
):
    proxy_url = f"https://hc-ping.com/{uuid}/log"
    return await make_hc_ping_request(url=proxy_url, request=request, payload=payload)


@app.get("/ping/{uuid}/{exit-status}")
@app.head("/ping/{uuid}/{exit-status}")
@app.post("/ping/{uuid}/{exit-status}")
async def ping_uuid_exit_status(
    request: Request,
    uuid: str,
    exit_status: str,
    payload: Any = Body(None),
):
    proxy_url = f"https://hc-ping.com/{uuid}/{exit_status}"
    return await make_hc_ping_request(url=proxy_url, request=request, payload=payload)
