# -*- encoding: utf-8 -*-
"""

"""

import os
# import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
# sys.path.append('/home/nirmal/projects/studyblogs/')
application = get_wsgi_application()















