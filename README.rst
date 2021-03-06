aiohttp_route_decorator
=======================

The library provides ``@route`` decorator for `aiohttp.web`_, resembling the contract of Flask_ ``@app.route``.

.. _aiohttp.web: https://aiohttp.readthedocs.io/en/latest/web.html
.. _Flask: http://flask.pocoo.org/docs/0.11/quickstart/#routing

The imaginary ``aiohttp`` ``@app.route`` decorator is discouraged_ for multiple_ reasons_; this one tries to solve part of those problems (the ``app`` doesn't need to be global at the very least).

.. _discouraged: http://aiohttp.readthedocs.io/en/stable/faq.html
.. _multiple: https://github.com/KeepSafe/aiohttp/issues/428
.. _reasons: https://github.com/KeepSafe/aiohttp/pull/195


Deprecation warning
-------------------

This package was created for older aiohttp releases. As of aiohttp 2.3, there is built-in RouteTableDef_ class which works pretty much the same way.

.. _RouteTableDef: https://docs.aiohttp.org/en/latest/web_reference.html#aiohttp-web-route-table-def


Installation
============

::

        pip install aiohttp_route_decorator


Usage
=====

Create a ``route`` object in each of your handler modules, and decorate the handlers:

.. code:: python

	# myapp/handlers.py

	from aiohttp_route_decorator import RouteCollector

	route = RouteCollector()

	@route('/')
	async def index(request):
		return web.Response(body=b'OK')

	@route('/publish', method='POST')
	async def publish(request):
		return web.Response(body=b'OK')

	@route('/login', methods=['GET', 'POST'], name='login')
	async def login(request):
		if request.method == 'POST':
			return web.Response(body=b'OK')
		return web.Response(body=b'Login')
		

When you init the application, push the collected ``routes`` into ``app.router``:

.. code:: python

	from aiohttp import web
	from myapp import handlers

	def run():
		app = web.Application()
		handlers.route.add_to_router(app.router)
		web.run_app(app)


Non-decorator use
-----------------

If you prefer to keep your routes together, you can construct the list manually after your handers:

.. code:: python

	from aiohttp_route_decorator import RouteCollector, Route

	async def index(request):
		return web.Response(body=b'OK')

	async def publish(request):
		return web.Response(body=b'OK')

	async def login(request):
		if request.method == 'POST':
			return web.Response(body=b'OK')
		return web.Response(body=b'Login')

	routes = RouteCollector([
		Route('/', index),
		Route('/publish', publish, method='POST'),
		Route('/login', login, methods=['GET', 'POST'], name='login'),
	])


Prefixed routes
---------------

You can provide common route prefix that will be prepended to all routes:

.. code:: python

	from aiohttp_route_decorator import RouteCollector

	routes = RouteCollector(prefix='/app')

	@route('/')
	async def index(request):
		return web.Response(body=b'OK')

	@route('/publish', method='POST')
	async def publish(request):
		return web.Response(body=b'OK')

	...

	handlers.route.add_to_router(app.router)
	# /app/ -> index
	# /app/publish -> publish


You can also provide the prefix within ``add_to_router()`` call instead:

.. code:: python

	from aiohttp_route_decorator import RouteCollector

	routes = RouteCollector()

	@route('/')
	async def index(request):
		return web.Response(body=b'OK')

	@route('/publish', method='POST')
	async def publish(request):
		return web.Response(body=b'OK')

	...

	handlers.route.add_to_router(app.router, prefix='/app')
	# /app/ -> index
	# /app/publish -> publish


...or use both:

.. code:: python

	from aiohttp_route_decorator import RouteCollector

	routes = RouteCollector(prefix='/app')

	@route('/')
	async def index(request):
		return web.Response(body=b'OK')

	@route('/publish', method='POST')
	async def publish(request):
		return web.Response(body=b'OK')

	...

	handlers.route.add_to_router(app.router, prefix='/project')
	# /project/app/ -> index
	# /project/app/publish -> publish


The non-decorator version of ``RouteCollector`` can also accept prefix:

.. code:: python

	from aiohttp_route_decorator import RouteCollector, Route

	async def index(request):
		return web.Response(body=b'OK')

	async def publish(request):
		return web.Response(body=b'OK')

	routes = RouteCollector(prefix='/app', routes=[
		Route('/', index),
		Route('/publish', publish, method='POST'),
	])


Parameters reference
--------------------

``route(path, *, method='GET', methods=None, name=None, **kwargs)``

- **path** (*str*) — route path. Should be started with slash (``'/'``).
- **method** (*str*) — HTTP method for route. Should be one of ``'GET'``, ``'POST'``, ``'PUT'``, ``'DELETE'``, ``'PATCH'``, ``'HEAD'``, ``'OPTIONS'`` or ``'*'`` for any method.
- **methods** (*List[str]*) — optional shortcut for creating several routes with different HTTP methods at once. If used, should be a list of acceptable values for ``method`` argument.
- **name** (*str*) — optional route name.
- **kwargs** — other parameters to be passed to ``aiohttp.web.Resource.add_route()``.
