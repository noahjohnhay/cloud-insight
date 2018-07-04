from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from packages.executor import execute

"""Manages CLI commands through the Cement Framework and executes
   cloud insight from here.
"""


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Simplifies the tracking of docker container versions, " \
                      "health and other important information across various platforms."
        arguments = [
            (['-p', '--profile'],
             dict(action='store', help='cvent-aws-cli profile to run against'))
            ]

    @expose(hide=True)
    def default(self):
        self.app.log.info('Running Cloud-insight')
        if self.app.pargs.profile:
            self.app.log.info("Running against profile: {profile}".format(profile=self.app.pargs.profile))
        execute()


class CloudInsight(CementApp):
    class Meta:
        label = 'cloud-insight'
        base_controller = 'base'
        handlers = [BaseController]


def main():
    """Runs the commands and subcommands from here. Setup.py defines
       This function as the driver method for the application.
    """
    with CloudInsight() as app:
        app.run()


if __name__ == '__main__':
    main()
