import asyncio
from aiohttp import web

from aiohttp_route_decorator import RouteCollector, Route


def test_route_decorator(app):
	route = RouteCollector()

	@route('/')
	async def handler(request):
		return web.Response(body=b'OK')

	@route('/test', method='PUT', name='test')
	async def handler(request):
		return web.Response(body=b'OK')

	@route('/test_methods', methods=['GET', 'POST'], name='test_methods')
	async def handler(request):
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
		Route('/test', handler2, method='PUT', name='test'),
		Route('/test_methods', handler3, methods=['GET', 'POST'], name='test_methods'),
	])

	routes.add_to_router(app.router)
	assert_router_configured(app.router)


def assert_router_configured(router):
	expected_routes = [
		('/', 'GET'),
		('/test', 'PUT'),
		('/test_methods', 'GET'),
		('/test_methods', 'POST'),
	]

	assert len(router.routes()) == len(expected_routes)
	assert len(router.named_resources()) == 2

	for route, (path, method) in zip(router.routes(), expected_routes):
		assert route.resource.url() == path
		assert route.method == method

	assert router['test'].url() == '/test'
