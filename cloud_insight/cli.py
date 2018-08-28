#!/usr/bin/python

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import cloud_insight.executor as executor


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Simplifies the tracking of docker container versions, " \
                      "health and other important information across various platforms."
        arguments = [
            (['-c', '--config'],
             dict(action='store', help='Path to configuration file to use'))
            ]

    @expose(hide=True)
    def default(self):
        executor.default_command(self.app)

    @expose(help="This command will list the container information")
    def list(self):
        executor.list_command(self.app)

    @expose(help="This command will compare two sets of containers")
    def compare(self):
        executor.compare_command(self.app)


class CloudInsight(CementApp):
    class Meta:
        base_controller = 'base'
        config_handler = 'json'
        extensions = ['colorlog', 'json']
        handlers = [BaseController]
        label = 'cloud-insight'
        log_handler = 'colorlog'


def main():
    with CloudInsight() as app:
        app.run()


if __name__ == '__main__':
    main()
