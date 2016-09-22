====
Serp
====

Serp is a web-based ERP aplication for direct debit transactions 
management following SEPA rules

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "serp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'serp',
    ]

2. Include the serp URLconf in your project urls.py like this::

    url(r'^serp/', include('serp.urls')),

3. Run `python manage.py migrate` to create the serp models.

4. Run `python manage.py collectstatic` to collect the static data.

5. Visit http://127.0.0.1:8000/serp/ to test the website.

