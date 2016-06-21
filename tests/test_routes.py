import asyncio
from aiohttp import web

from aiohttp_route_decorator import RouteCollector


def test_routes(app):
	route = RouteCollector()

	@route('GET', '/', name='index')
	@asyncio.coroutine
	def handler(request):
		yield web.Response(body=b'OK')

	@route('*', '/test/', name='test')
	@asyncio.coroutine
	def handler(request):
		yield web.Response(body=b'OK')

	route.add_to_router(app.router)

	assert app.router['index'].url() == '/'
	assert app.router['test'].url() == '/test/'
