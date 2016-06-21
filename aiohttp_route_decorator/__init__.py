"""
Usage:

route = RouteCollector()

@route('GET', '/')
async def handler(request):
	return web.Response(body=b'OK')

...

app = Application()
route.add_to_router(app.router)
"""


class RouteCollector(list):
	def __call__(self, *args, **kwargs):
		def wrapper(handler):
			self.append((args, kwargs, handler))
			return handler

		return wrapper

	def add_to_router(self, router):
		for args, kwargs, handler in self:
			router.add_route(*args, handler=handler, **kwargs)
