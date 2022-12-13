# Essay Viewer

从前利用简陋的系统写一些东西，当时把这个简陋的系统叫做“Journal”。Journal 只支持纯文本写作，所以留下来的内容都是纯文本的，
有时我会嵌入一些链接、代码，下意识的应用了一些 Markdown 的规则，因此这些文本可以交给 Markdown 处理。这个项目 Essay Viewer 的目的
是把这些内容通过网页展示出来，给爱人浏览一下。Essay Viewer 是一个最小可行性产品（MVP），它本身仅提供了随笔（我把每一篇内容称作随笔）
列表、查看的功能，用户认证用的是官方和第三方模块。

我选用了熟悉的 Django 开发，因为我仅打算花半天时间做好这件事情，实际也做到了。然而在部署中遇到一些麻烦，我想作为一个 MVP 项目，
这种困难是有共性的。于是我把这个项目采取的一些技术选择公布出来，以方便以后做其它 MVP 项目时减少负担。

尽管这个项目仅计划用半天时间完成，但是许多小型项目不是这样子，可能需要一周或者更长时间才能完成。
上线后也需要长时间运行。因此做代码格式化、日志记录也是有必要的。

代码格式化我选择了 black，black 会自己根据 PEP8 的规则重新排版代码，省去了样式统一的负担。
再配合 flake8 做质量检查。简单说一下它们的安装使用方法：

```
# MVP 项目我觉得用不着做 CI/CD，把这些依赖工具安装到全局就行
pip install black flake8
```

因为 black 覆盖了 flake8 的一部分职能，需要关闭一些 flake8 的选项，在项目根目录下创建 `.flake8` 文件：

```
[flake8]
max-line-length = 88
select = C,E,F,W,B,B950
ignore = W503
extend-ignore = E203, E501, E722
```

手动使用命令：

```
black .
flake8 --exclude .venv
```

项目提交前可以反复执行这两个命令，对代码做调整。平时开发时不需要这么做，交给 IDE 做更好。
可以参考 VSCode 的 workspace 文件中的配置（VSCode 需要装 Black、Flake8 相关插件）：

```
"settings": {
    "editor.formatOnPaste": true,
    "editor.formatOnSave": true,
    "python.linting.flake8Enabled": true,
    "files.associations": {
        "*.html": "django-html"
    }
}
```

上面的配置里还有 `django-html` 插件，用来高亮 django template，这里需要手动把 `*.html` 和 `django-html` 插件关联起来。

还有一个 `.prettierignore` 文件，配置忽略了 `*.html` 文件的格式化。prettier 是前端的 black，但是无法支持 django template，
因此禁止它格式化 django template 。

另外一点是日志处理。默认的日志仅打印在控制台上，我们需要在生产环境中记录程序出问题后的日志。Web 应用的日志需要包含访问者 ip 等信息。
这类信息默认的 logger 不记录的，需要比较多的自定义。我使用了 [logging_in_django](https://github.com/rgs258/logging_in_django) 的日志方案，包含了 `logging_helpers.py` 文件，在 `essay_viewer` 目录下。

需要在配置文件中加入另外的配置：

```
# %(threadName)-14s (%(pathname)s:%(lineno)d)
CONSOLE_LOGGING_FORMAT = (
    "%(hostname)s %(asctime)s %(levelname)-8s %(name)s.%(funcName)s: %(message)s"
)
CONSOLE_LOGGING_FILE_LOCATION = BASE_DIR / "logs" / "django.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "ignore_something": {
            "()": "essay_viewer.logging_helpers.SomethingFilter",
        },
    },
    "formatters": {
        "my_formatter": {
            "format": CONSOLE_LOGGING_FORMAT,
            "class": "essay_viewer.logging_helpers.HostnameAddingFormatter",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": [
                "require_debug_false",
                "ignore_something",
            ],
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "my_formatter",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": CONSOLE_LOGGING_FILE_LOCATION,
            "mode": "a",
            "encoding": "utf-8",
            "formatter": "my_formatter",
            "backupCount": 30,
            "maxBytes": 10485760,  # 10MB
        },
    },
    "loggers": {
        "": {
            # The root logger is always defined as an empty string and will pick up all logging that is not collected
            # by a more specific logger below
            "handlers": ["console", "mail_admins", "file"],
            "level": os.getenv("ROOT_LOG_LEVEL", "INFO"),
        },
        "django": {
            # The 'django' logger is configured by Django out of the box. Here, it is reconfigured in order to
            # utilize the file logger and allow configuration at runtime
            "handlers": ["console", "mail_admins", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.server": {
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "propagate": False,
            "level": "ERROR",
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
```

这份日志策略在开发环境下会打印出所有访问信息以及 django orm 生成的查询 sql，生产环境只有 WARNING 及以上日志，
所以如果要记录所有访问记录，需要配合 Web Server 的日志。日志文件保存在 logs 目录，按照 10MB 切割，保留 30 份。

对于静态文件，我选择用 [WhiteNoise](http://whitenoise.evans.io/en/latest/) 管理，Django 框架在生产环境中不会自动处理静态文件。

```
pip install whitenoise

# settings.py
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

用户登录用了 [django-allauth](https://github.com/pennersr/django-allauth) 和 [django-allauth-ui](https://github.com/danihodovic/django-allauth-ui)。
有了他们，连 UI 都不用做了。

```
pip install django-allauth django-allauth-ui django-widget-tweaks

# settings.py
INSTALLED_APPS = [
    ...(自己的 APPS)
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "widget_tweaks",
    ...(系统的 APPS)
]

# urls.py

urlpatterns = [
    path(accounts/, include("allauth.urls")),
    ...
]
```

别忘了要修改默认的时区，我在上海，用的时区是 Asia/Shanghai，语言是 zh-Hans。

```
# settings.py

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"
```

无法避免的生产环境和开发环境有些配置是不同的，我选择以开发环境配置为模板，其余环境 import \*，然后对一些选项做修改。
比如 `settings_prod.py`。然后对 `asgi.py` `wsgi.py` 以及 `manage.py` 中的 `DJANGO_SETTINGS_MODULE` 环境变量做调整。

```
# 原来
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "essay_viewer.settings")

# 现在
setting_suffix = ""
env = os.getenv("ENV")
if env:
    setting_suffix = "_" + env
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "essay_viewer.settings" + setting_suffix
)
```

其实就是把 `ENV` 环境变量的值加入到 `settings.py` 文件名做后缀。如果设置了 `ENV=prod`，就会使用 `settings_prod.py` 这个文件作为配置。
下面的 `# noqa: F401,F403` 是让 flake8 忽略检测全局导入错误。

```
# settings_prod.py
from essay_viewer.settings import *  # noqa: F401,F403

...
```

我选择使用 [uvicorn](https://www.uvicorn.org/) 作为 Web Server。重新配置了 log，让它的策略和上面改的 Django 的策略类似。
配置在 `uvicorn-log-config.json` 文件里。

使用 [supervisor](http://supervisord.org/index.html) 做进程管理，以前我喜欢用 systemd，后来发现 supervisor 更简单一点。
参考 `supervisor.conf` 配置。使用时把内容贴进系统的 supervisord 的配置文件（默认是 `/etc/supervisord.conf`）中即可。
这份配置文件中的 `command` 指令也体现了如何启动 uvicorn。

一个简单的项目可能实际上会运行在现有的服务器上，利用现有的域名以及 SSL 证书，以 URL 前缀作为区分，比如：

```
# 开发环境
http://127.0.0.1:8000/essay/050b4a71-6389-49cb-9f68-42dee20374bc/

# 生产环境
https://coffeepi.top/essay-viewer/essay/050b4a71-6389-49cb-9f68-42dee20374bc/
```

上面的 `essay-viewer` 就是 URL 前缀。然而 Django 中直接设置 FORCE_SCRIPT_NAME 达不到理想效果，会有
静态资源问题，以及 CSRF 校验失败问题。于是我在 URL 上硬编码了 prefix，并且登录的 URL 做了相应的配置。

```
# settings.py
URL_PREFIX = ""

SESSION_COOKIE_NAME = "essay_viewer_sessionid"
SESSION_COOKIE_PATH = (
    "/" if (not URL_PREFIX) or URL_PREFIX == "/" else "/" + URL_PREFIX.strip("/") + "/"
)

CSRF_COOKIE_NAME = "essay_viewer_csrftoken"
CSRF_COOKIE_PATH = (
    "/" if (not URL_PREFIX) or URL_PREFIX == "/" else "/" + URL_PREFIX.strip("/") + "/"
)

# urls.py
def _prefixed(pattern):
    if not settings.URL_PREFIX or settings.URL_PREFIX.strip() == "/":
        return pattern
    url_prefix = settings.URL_PREFIX.lstrip("/")
    if not url_prefix.endswith("/"):
        url_prefix += "/"
    return url_prefix + pattern


urlpatterns = [
    path(_prefixed(""), lambda r: redirect("essay:index"), name="root"),
    path(_prefixed("accounts/"), include("allauth.urls")),
    path(_prefixed("admin/"), admin.site.urls),
    path(_prefixed("essay/"), include("essay.urls")),
]
```

`URL_PREFIX` 可以配置成任意的前缀名，可以设置为 `""` 或者 `None`。

## 开发环境指南

```
# 需要 python3.8+
# python --version

git clone https://github.com/lixulun/essay-viewer
cd essay-viewer
python -m venv .venv
source .venv/bin/activate # Linux/MacOS
& .\.venv\Scripts\Activate.ps1 # PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 生产环境指南

```
# 需要 python3.8+
# python --version
# 以 Ubuntu 20 为例


mkdir /opt/essay-viewer && cd /opt/essay-viewer
git clone https://github.com/lixulun/essay-viewer .
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ENV=prod
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

# 安装 supervisor，把 supervisor.conf 文件的内容拷贝到系统 supervisor 配置中
# 注意修改 user 字段，user 改成当前文件夹的拥有者
# 重启 supervisord
# supervisorctl status essay-viewer

# 配置带有 url prefix 的 Nginx/Caddy proxy
# Nginx
http {
    ...
    server {
        ...
        location /essay-viewer/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        ...
    }
    ...
}

# Caddy Caddyfile
coffeepi.top {
	...
	reverse_proxy /essay-viewer/* 127.0.0.1:8000
	...
}
```

## 期望进一步完善

- 前端打包器融合
- 自动化测试
- 压测
- Base Template 移动端优化
- 自定义登录 Template 也支持移动端
- 容器打包

## 非必要

- 国际化
