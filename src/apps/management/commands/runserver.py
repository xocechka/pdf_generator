from django.core.management.commands.runserver import Command as RunServer
import uvicorn
import asyncio


class Command(RunServer):

    def inner_run(self, **options):
        from config.asgi import application
        config = uvicorn.Config(application, host=self.addr, port=int(self.port), log_level="info")
        server = uvicorn.Server(config)
        asyncio.run(server.serve())
