# Essay Viewer

从前利用简陋的系统写一些东西，当时把这个简陋的系统叫做“Journal”。Journal 只支持纯文本写作，所以留下来的内容都是纯文本的，
有时我会嵌入一些链接、代码，不自觉的应用了一些 Markdown 的规则，因此这些文本可以交给 Markdown 处理。这个项目 Essay Viewer 的目的
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
这类信息默认的 logger 不记录的，需要比较多的自定义。我使用了 [https://github.com/rgs258/logging_in_django](https://github.com/rgs258/logging_in_django) 的日志方案，包含了 `logging_helpers.py` 文件，在 django 的 project 配置目录下。

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

## 期望进一步完善

- 前端打包器融合
- 自动化测试
- 完善组合

## 非必要

- 国际化
-
