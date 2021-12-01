from sshy_app.user_interfaces.gui import GuiRunner
from sshy_app.user_interfaces.cli import CLI
import argparse

#TODO: Automatic dependency installation + pipenv

parser = argparse.ArgumentParser(description="Connect to an SSH server and adds your key. Generates a new ssh key and fixes permissions if needed. Call without parameters to launch gui.")
parser.add_argument("--host", default=None)
parser.add_argument("--user", default=None)
parser.add_argument("--password", default=None)
args = parser.parse_args()

# Allright, so, if we get *any* arguments, don't launch the gui, instead, use the console interface.

for arg in args.__dict__:
    if args.__dict__[arg] is not None:
        CLI(args.host, args.user, args.password)
        exit()

GuiRunner().run()