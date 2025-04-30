"""                                             
Implementation of the v1 router.
Using these notation, in the future it will be possible to manage multiple versions of the API at once.
"""

from fastapi import APIRouter

from .routes import profits
from .routes import what_if

# Create router with v1 prefix
router = APIRouter(prefix="/v1")

# Add the router
router.include_router(profits.router)
router.include_router(what_if.router)
