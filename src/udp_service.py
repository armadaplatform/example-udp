import json
import os

import web


class Health(object):
    def GET(self):
        return 'ok'


class Env(object):
    def GET(self):
        return json.dumps(dict(os.environ), sort_keys=True, indent=4)


def main():
    urls = (
        '/health', Health.__name__,
        '/', Env.__name__,
    )
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    main()
