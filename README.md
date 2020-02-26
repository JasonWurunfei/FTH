# Free Tech Hub

## Requirements
---

- Python 3.8
- Django 3.0
- mistletoe 0.7.2
- django-crispy-forms 1.8.1
---
## Installation

**0. It is suggested that you use a vertual environment**

to do this run ` python -m venv [name ofyour vertual environment]` in cmd or terminal

- windows

  - run `[path to your vertual environment]\Scripts\activate` to activate your virtual environment

- Linux/Mac

  - run `source [path to your vertual environment]\bin\activate` to activate your virtual environment

**1.  run `pip install requirements.txt` to install requirements**

**2. run `python manage.py collectstatic`**

**3. `python manage.py makemigrations`**

**4. `python manage.py migrate`**

---
## To have better markdown code block

**It is suggested that you use mistletoe as your markdown coverter**

go to `python3.5/site-packages/markdownx/utils.py`
 Find function `markdownify`

which would look like this:

```python
def markdownify(content):
    md = markdown(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
    )
    return md
```

Change this to:

```python
def markdownify(content):
    import mistletoe
    rendered = mistletoe.markdown(str(content))
    return rendered 
```

---

## Run

In your activate your virtual environment and run `python manage.py runserver`
