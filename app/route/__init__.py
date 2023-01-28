from .auth import auth_router
from .competition import comp_router
from .gym import gym_router
from .search import search_router
from .user import user_router

__all__ = ["auth_router", "search_router", "gym_router", "comp_router", "user_router"]
