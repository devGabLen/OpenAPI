import json
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/llm", tags=["llm"])

class Question(BaseModel):
    prompt: str
SERVICE_FILE = Path.home() / ".local" / "state" / "opencode" / "service.json"


MODEL = {"providerID": "opencode", "id": "mimo-v2.6-flash-free"}


def opencode_service() -> tuple[str, str]:
    """Devuelve (url, password) del servicio de OpenCode."""
    try:
        data = json.loads(SERVICE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        raise HTTPException(
            status_code=503,
            detail="No hay servicio de OpenCode corriendo (abri opencode una vez)",
        )
    return data["url"], data["password"]


def _check(response: httpx.Response) -> httpx.Response:
    """Si OpenCode devolvio error, lo convierte en un HTTPException."""
    if response.is_error:
        try:
            detail = response.json().get("message") or response.text
        except ValueError:
            detail = response.text
        raise HTTPException(status_code=502, detail=f"OpenCode: {detail}")
    return response


@router.post("/ask")
async def ask(question: Question):
    base_url, password = opencode_service()

    try:
        async with httpx.AsyncClient(
            base_url=base_url,
            auth=("opencode", password),
            timeout=600,
        ) as client:

            session = _check(
                await client.post(
                    "/api/session",
                    json={"location": {"directory": str(Path.cwd())}},
                )
            )
            session_id = session.json()["data"]["id"]

            try:
                _check(
                    await client.post(
                        f"/api/session/{session_id}/model",
                        json={"model": MODEL},
                    )
                )
                response = _check(
                    await client.post(
                        f"/api/session/{session_id}/generate",
                        json={"prompt": question.prompt},
                    )
                )
            finally:
                try:
                    await client.delete(f"/api/session/{session_id}")
                except httpx.HTTPError:
                    pass
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Sin conexion con OpenCode: {exc}")

    return {"answer": response.json()["data"]["text"]}