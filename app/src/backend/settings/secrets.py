#: configuration keeping secrets keys separately to keep them in strict
#: form

#: reduce redundant imports
from . utils import get_env_string as _get_env_string

EMAIL_HOST_PASSWORD = _get_env_string('EMAIL_HOST_PASSWORD', '')
