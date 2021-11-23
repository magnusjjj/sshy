from sshy_app.gui.gui import GuiRunner
from sshy_app.cli import CLI
import argparse

parser = argparse.ArgumentParser(description="Connect to an SSH server and adds your key. Generates a new ssh key and fixes permissions if needed. Call without parameters to launch gui.")
parser.add_argument("--host", default=None)
parser.add_argument("--user", default=None)
parser.add_argument("--password", default=None)
args = parser.parse_args()

for arg in args.__dict__:
    if args.__dict__[arg] is not None:
        CLI(args.host, args.user, args.password)
        exit()

GuiRunner().run()