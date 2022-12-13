from essay_viewer.settings import *  # noqa: F401,F403
from essay_viewer.settings_utils import with_url_prefix

DEBUG = False

# 部署到其它域名时要修改这里
ALLOWED_HOSTS = ["coffeepi.top"]

# FORCE_SCRIPT_NAME 有局限性，实际使用时有各种各样的问题，这个作用是相同的
URL_PREFIX = "essay-viewer"

SESSION_COOKIE_NAME = "essay_viewer_sessionid"
SESSION_COOKIE_PATH = with_url_prefix(URL_PREFIX, "")

CSRF_COOKIE_NAME = "essay_viewer_csrftoken"
CSRF_COOKIE_PATH = with_url_prefix(URL_PREFIX, "")

STATIC_URL = with_url_prefix(URL_PREFIX, "static/")
