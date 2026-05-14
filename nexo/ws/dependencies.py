from nexo.auth.jwt import decode_token


async def authenticate_ws(token: str) -> str | None:
    if not token:
        return None
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    return payload.get("sub")
