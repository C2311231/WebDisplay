from src.system_modules.web import web_module
## Used for running webserver independently
class NullObject:
    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return None


server = web_module(NullObject())
server.start(cancel_run=True)
server._threaded_run(debug=True)