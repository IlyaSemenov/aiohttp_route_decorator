import asyncio

from aiohttp import web
from aiohttp_route_decorator import RouteCollector, Route
import pytest


def test_route_decorator(app):
	route = RouteCollector()

	@route('/')
	async def handler1(request):
		return web.Response(body=b'OK')

	@route('/test', method='POST', name='test')
	async def handler2(request):
		return web.Response(body=b'OK')

	@route('/test_methods', methods=['GET', 'POST'], name='test_methods')
	async def handler3(request):
		return web.Response(body=b'OK')

	route.add_to_router(app.router)
	assert_router_configured(app.router)


def test_route_list(app):
	async def handler1(request):
		return web.Response(body=b'OK')

	async def handler2(request):
		return web.Response(body=b'OK')

	async def handler3(request):
		return web.Response(body=b'OK')

	routes = RouteCollector([
		Route('/', handler1),
		Route('/test', handler2, method='POST', name='test'),
		Route('/test_methods', handler3, methods=['GET', 'POST'], name='test_methods'),
	])

	routes.add_to_router(app.router)
	assert_router_configured(app.router)


def assert_router_configured(router):
	expected_routes = [
		('/', 'GET'),
		('/test', 'POST'),
		('/test_methods', 'GET'),
		('/test_methods', 'POST'),
	]

	assert len(router.routes()) == len(expected_routes)
	assert len(router.named_resources()) == 2

	for route, (path, method) in zip(router.routes(), expected_routes):
		assert route.resource.url() == path
		assert route.method == method

	assert router['test'].url() == '/test'


def test_route_collector_prefix(app):
	route = RouteCollector(prefix='/app')

	@route('/', name='root')
	async def handler1(request):
		return web.Response(body=b'OK')

	@route('/test', name='test')
	async def handler2(request):
		return web.Response(body=b'OK')

	route.add_to_router(app.router)

	assert app.router['root'].url() == '/app/'
	assert app.router['test'].url() == '/app/test'


def test_add_to_router_prefix(app):
	route = RouteCollector()

	@route('/', name='root')
	async def handler1(request):
		return web.Response(body=b'OK')

	@route('/test', name='test')
	async def handler2(request):
		return web.Response(body=b'OK')

	route.add_to_router(app.router, prefix='/app')

	assert app.router['root'].url() == '/app/'
	assert app.router['test'].url() == '/app/test'


def test_route_list_prefix(app):

	async def handler1(request):
		return web.Response(body=b'OK')

	async def handler2(request):
		return web.Response(body=b'OK')

	routes = RouteCollector(prefix='/app', routes=[
		Route('/', handler1, name='root'),
		Route('/test', handler2, name='test'),
	])
	routes.add_to_router(app.router)

	assert app.router['root'].url() == '/app/'
	assert app.router['test'].url() == '/app/test'


def test_double_prefix(app):
	route = RouteCollector(prefix='/app')

	@route('/', name='root')
	async def handler1(request):
		return web.Response(body=b'OK')

	@route('/test', name='test')
	async def handler2(request):
		return web.Response(body=b'OK')

	route.add_to_router(app.router, prefix='/project')

	assert app.router['root'].url() == '/project/app/'
	assert app.router['test'].url() == '/project/app/test'


def test_route_collector_double_argument(app):
	async def handler1(request):
		return web.Response(body=b'OK')

	async def handler2(request):
		return web.Response(body=b'OK')

	with pytest.raises(ValueError):
		routes = RouteCollector([
			Route('/', handler1, name='root'),
		], routes=[
			Route('/test', handler2, name='test'),
		])
