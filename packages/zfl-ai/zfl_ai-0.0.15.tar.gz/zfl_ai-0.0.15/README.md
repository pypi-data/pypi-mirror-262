# zfl-ai

[![PyPI - Version](https://img.shields.io/pypi/v/django-hatch.svg)](https://pypi.org/project/django-hatch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-hatch.svg)](https://pypi.org/project/django-hatch)

![zfl-ai_1](https://github.com/kenno-warise/zfl-ai/assets/51676019/8ed643a6-140f-447d-89cd-932da3f462b9)

-----

**目次**

- [詳細](#詳細)
- [インストールとDjangoプロジェクト作成](#インストールとDjangoプロジェクト作成)
- [Djangoプロジェクトにプラグイン](#Djangoプロジェクトにプラグイン)
- [License](#license)

## 詳細

djangoプロジェクトでインストールできるDjangoアプリです。

使用方法は以下からご覧ください。

## インストールとDjangoプロジェクト作成

実行環境は「Python3.7」、「Django2.2.5」です。

```console
$ python3 --version
Python 3.7.0
```

Djangoアプリはpipでインストールします。

```console
$ pip install zfl-ai
```

Djangoプロジェクトを作成

```console
$ django-admin startproject myproject .
```

言語を設定します。

`myproject/settings.py`

```python
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True
```

## Djangoプロジェクトにプラグイン

Djangoアプリを設定します。

`myproject/settings.py`

```python
INSTALLED_APPS = [
    ...,
    "ai",
]
```

プロジェクト直下のtemplatesを読み込むように設定。

```python
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

`myproject/urls.py`

```python
...
from django.urls import path, include

urlpatterns = [
    ...,
    path('', include('ai.urls')),
]
```

zfl-aiのテンプレートである「index.html」ではテンプレートタグ「{% extends '...' %}」で「base.html」を読み込むように設定しているので、「templates/base.html」を作成する必要があります。

```console
$ mkdir templates && touch templates/base.html
```

base.htmlの内容

```html
{% load static %}
<html lang="ja" prefix="og: http://ogp.me/ns#">
  <head>

    <!-- BootStrap CSS Link -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">


    <!-- StaticFiles CSS -->
    {% block ai-style %}{% endblock %}

  </head>
  <body>

    <!-- Djangoテンプレートタグ -->

    {% block content %}
    {% endblock %}

    <!-- BootStrap jQuery -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

  </body>
</html>
```


サーバーを起動します。

```console
$ python3 manage.py runserver
```

`127.0.0.1:8000/ai/`にアクセスします。

## License

`zfl-ai` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
