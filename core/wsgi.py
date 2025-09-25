import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "sanaap_backend_challenge_api"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()
