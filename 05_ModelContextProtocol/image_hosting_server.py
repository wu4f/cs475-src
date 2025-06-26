from fastmcp import FastMCP
import requests
from typing import Dict

mcp = FastMCP(
    name="Image Hosting Service",
)


@mcp.tool()
def is_admin(id: str) -> Dict[str, bool]:
    """
    Check if the user with the given ID is an admin for the image hosting service.
    Returns a dictionary with the user's ID and admin status.
    """
    id = id.strip().lower()

    try:
        r = requests.get(
            f"https://viking-images.up.railway.app/api/admin/isadmin/{id}", timeout=5
        )
        is_admin = r.status_code == 200
    except requests.RequestException:
        is_admin = False  # Fail closed on error

    return {"id": id, "admin": is_admin}


@mcp.tool()
def is_registered(id: str) -> Dict[str, bool]:
    """
    Check if the user with the given ID is registered for the image hosting service.
    Returns a dictionary with the user's ID and registration status.
    """
    id = id.strip().lower()

    try:
        headers = {"Authorization": id}
        r = requests.get(
            "https://viking-images.up.railway.app/api/key/check",
            timeout=5,
            headers=headers,
        )
        is_registered = r.status_code == 200
    except requests.RequestException:
        is_registered = False  # Fail closed on error

    return {"id": id, "exists": is_registered}


@mcp.tool()
def register() -> Dict[str, bool]:
    """
    Register a user for the image hosting hosting service.
    Returns a dictionary with the ID and success status.
    """
    try:
        r = requests.post(
            "https://viking-images.up.railway.app/api/key/create", timeout=5
        )
        if r.status_code != 200:
            return {"id": None, "success": False}
        else:
            r = r.json()
            return {"id": r["Key"], "success": True}
    # Global exception so we can handle a JSON decode failure, normally
    # I don't like doing this but it's fine.
    except:
        return {"id": None, "success": False}


@mcp.tool()
def get_image_count_per_user(id: str) -> int:
    """
    Get an image count for a user. If the user doesn't exist the returned
    count will be -1.
    """
    headers = {"Authorization": id}
    try:
        r = requests.get(
            "https://viking-images.up.railway.app/api/user/images", headers=headers
        )
        if r.status_code != 200:
            return -1
        else:
            return len(r.json())
    except:
        return -1


if __name__ == "__main__":
    mcp.run(transport="stdio")
