from fastapi import Header, HTTPException


async def current_user_id(x_user_id: str = Header(..., alias="X-User-Id")) -> int:
    """El gateway pone X-User-Id tras validar el JWT."""
    try:
        return int(x_user_id)
    except (TypeError, ValueError):
        raise HTTPException(401, "X-User-Id inválido o ausente")


async def current_user_role(
    x_user_role: str = Header("STUDENT", alias="X-User-Role"),
) -> str:
    return x_user_role.upper()


async def require_admin(role: str = Header("STUDENT", alias="X-User-Role")) -> str:
    if role.upper() != "ADMIN":
        raise HTTPException(403, "Solo administradores")
    return role.upper()
