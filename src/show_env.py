import os

import yaml

import web


class Health(object):
    def GET(self):
        return 'ok'


class Env(object):
    def GET(self):
        return yaml.dump(dict(os.environ), default_flow_style=False)


def main():
    urls = (
        '/health', Health.__name__,
        '/', Env.__name__,
    )
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    main()
