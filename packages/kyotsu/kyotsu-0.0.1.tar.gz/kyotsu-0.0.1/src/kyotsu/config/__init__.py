"""Danger:
Only modify these classes if you are completely certain of the implications, as numerous core settings
in external services are dependent on them.
"""

from .base import BaseSettings
from .services import GrpcService, HttpGrpcService, HttpService
