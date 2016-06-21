aiohttp_route_decorator
=======================

The library provides `@route` decorator for `aiohttp.web`_.

.. _aiohttp.web: https://aiohttp.readthedocs.io/en/latest/web.html

The imaginary `@app.route` decorator is discouraged_ for multiple_ reasons_; this one tries to solve part of those problems (the `app` doesn't need to be global at the very least).

.. _discouraged: http://aiohttp.readthedocs.io/en/stable/faq.html
.. _multiple: https://github.com/KeepSafe/aiohttp/issues/428
.. _reasons: https://github.com/KeepSafe/aiohttp/pull/195

Usage
=====

Create a `route` object in each of your handler modules, and decorate the handlers:

.. code:: python

	from aiohttp_route_decorator import RouteCollector

	route = RouteCollector()


	@route('GET', '/', name='index')
	async def handler(request):
		return web.Response(body=b'OK')
		
When you init the application, push the collected `routes` into `app.router`:

.. code:: python

	from aiohttp import web

	from myapp import handlers


	def run():
		app = web.Application()
		handlers.route.add_to_router(app.router)
		web.run_app(app)
