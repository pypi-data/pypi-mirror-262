

try:
    from .manager import version, Tools
    DIFFUSER_ACTIVE = True
except ImportError as e:
    DIFFUSER_ACTIVE = e

Name = "diffuser"
Version = version
# private = True
