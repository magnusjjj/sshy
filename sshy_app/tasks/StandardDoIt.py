from . import TaskBase
from fabric import Connection

# This tasks connects, and adds the key.
class StandardDoIt(TaskBase.TaskBase):
    runDefault = True
    needsSFTP = True
    def run(self):
        super().run()
        
        self.log("Time to get going")

        # TODO: We are assuming we are in the users home directory upon login

        # Check if the .ssh folder exists, create it if not, warn that the folder has the wrong permissions if it does
        if ".ssh" not in  self.client.listdir():
            self.log(".ssh folder did not exist. Creating.")
            self.client.mkdir(".ssh", 0o700)
        else:
            self.assertServerPermissions(".ssh", "700")

        # Check if the authorized_keys exists in the right directory. If not, create it.
        if "authorized_keys" not in self.client.listdir(".ssh"):
            self.log(".ssh/authorized_keys file did not exist. Creating.")
            f = self.client.file(".ssh/authorized_keys", "w")
            f.write(self.publickey)
            f.close()
            self.client.chmod(".ssh/authorized_keys", 0o600)
        else:
            # Now, if the authorized keys *does* exist, check if the permissions are correct
            self.assertServerPermissions(".ssh/authorized_keys", "600")

            # Read the authorized key file, with the possibility of adding to it
            f = self.client.file(".ssh/authorized_keys", "r+")
            content = f.read()

            # Check if our key already exists..
            if self.publickey in content:
                self.log("Key already exists on server. Not doing anything, you are all set :)")
            else:
                # It doesn't, so first check if we are on a new line, otherwise add a new line..
                if content[-1] != b'\n'[0]:
                    f.write(b'\n')
                
                # Write our key.
                f.write(self.publickey)
            
            # Clean up!
            f.close()

        self.log("All done!")