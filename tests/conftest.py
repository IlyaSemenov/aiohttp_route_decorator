import asyncio

from aiohttp import web
import pytest


@pytest.yield_fixture
def loop():
	# Set-up
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	yield loop

	# Clean-up
	loop.close()


@pytest.yield_fixture
def app(loop):
	app = web.Application(loop=loop)
	yield app
	loop.run_until_complete(app.shutdown())
	loop.run_until_complete(app.cleanup())
	loop.close()
