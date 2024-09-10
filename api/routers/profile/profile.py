
from typing import Dict, Any, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.handler.firestore_handler import FirestoreHandler

from src.enum.available_os import AvailableOS

from api.routers.profile.model.profile import Profile

router = APIRouter()

firestore_handler = FirestoreHandler()


def get_user_profile(os: AvailableOS, device_uid: str) -> Optional[Dict[str, Any]]:
    profile_os = f"PROFILE_{os.value}"
    profile_doc = firestore_handler.get_colletion(
        profile_os).document(device_uid).get()

    if profile_doc.exists:
        return profile_doc.to_dict()
    else:
        return None


def update_user_profile(profile: Profile):
    profile_os = f"PROFILE_{profile.os.value}"
    device_uid = profile.device_uid
    firestore_handler.get_colletion(profile_os).document(device_uid).set(
        profile.model_dump(mode="json"))
    return {"status": "success"}


@router.get("/{os}/{device_uid}")
async def get_profile(os: str, device_uid: str):
    if AvailableOS(os) == AvailableOS.UNKNOWN:
        return JSONResponse(content={"message": f"os {os} not found"}, status_code=400)

    profile_doc = get_user_profile(AvailableOS(os), device_uid)

    if profile_doc is None:
        profile = Profile(os=AvailableOS(os), device_uid=device_uid)
        update_user_profile(profile)
        return get_user_profile(AvailableOS(os), device_uid)

    return profile_doc


@router.post("/update", status_code=200)
async def update_profile(profile: Profile):
    return update_user_profile(profile)
