import asyncio
from aiohttp import web

from aiohttp_route_decorator import RouteCollector


def test_routes(app):
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

	router = app.router
	route.add_to_router(router)

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
