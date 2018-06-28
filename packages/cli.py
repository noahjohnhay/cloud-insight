<<<<<<< HEAD
#!/usr/bin/python

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import packages.executor as executor
=======
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from packages.executor import execute
>>>>>>> Adding CLI support through the cement framework; Added setup.py to package cloud-insight

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
<<<<<<< HEAD
             dict(action='store', help='aws profile to run against'))
=======
             dict(action='store', help='cvent-aws-cli profile to run against'))
>>>>>>> Adding CLI support through the cement framework; Added setup.py to package cloud-insight
            ]

    @expose(hide=True)
    def default(self):
<<<<<<< HEAD
        executor.default_command(self.app)

    @expose(help="This command will list the container information")
    def list(self):
        executor.list_command(self.app)

    @expose(help="This command will compare two sets of containers")
    def compare(self):
        executor.compare_command(self.app)
=======
        self.app.log.info('Running Cloud-insight')
        if self.app.pargs.profile:
            self.app.log.info("Running against profile: {profile}".format(profile=self.app.pargs.profile))
        execute()
>>>>>>> Adding CLI support through the cement framework; Added setup.py to package cloud-insight


class CloudInsight(CementApp):
    class Meta:
<<<<<<< HEAD
        base_controller = 'base'
        config_handler = 'json'
        extensions = ['json']
        handlers = [BaseController]
        label = 'cloud-insight'
=======
        label = 'cloud-insight'
        base_controller = 'base'
        handlers = [BaseController]
>>>>>>> Adding CLI support through the cement framework; Added setup.py to package cloud-insight


def main():
    """Runs the commands and subcommands from here. Setup.py defines
       This function as the driver method for the application.
    """
    with CloudInsight() as app:
        app.run()


if __name__ == '__main__':
    main()
