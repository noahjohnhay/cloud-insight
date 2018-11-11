#!/usr/bin/python

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import cloud_insight.executor as executor
import cloud_insight.api as api


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = ""
        arguments = [
            (
                ['-c', '--config'], dict(action='store', help='Path to configuration file to use')
            )
        ]

    @expose(help="This command will compare two sets of containers")
    def compare(self):
        self.app.config.parse_file(self.app.pargs.config)
        executor.main(self.app, 'compare')

    @expose(help="This command will list the containers connectivity information")
    def connectivity(self):
        self.app.config.parse_file(self.app.pargs.config)
        executor.main(self.app, 'connectivity')

    @expose(hide=True)
    def default(self):
        self.app.log.error('A namespace must be specified use "--help" to see all options')
        self.app.close(1)

    @expose(help="This command will list the containers health information")
    def health(self):
        self.app.config.parse_file(self.app.pargs.config)
        executor.main(self.app, 'health')

    @expose(help="This command will list the containers history information")
    def history(self):
        self.app.config.parse_file(self.app.pargs.config)
        executor.main(self.app, 'history')

    @expose(help="This command will list the container information")
    def list(self):
        self.app.config.parse_file(self.app.pargs.config)
        executor.main(self.app, 'list')

    @expose(help="This command will list the container information")
    def api(self):
        api.start_api(self.app)


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
