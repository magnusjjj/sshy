from fabric import Connection
from sshy_app.permissions.permissionhelper import PermissionHelper
from sshy_app.lib.certificate import Certificate
import stat
import traceback
import paramiko

# All tasks inherit this. Has helper functions for connecting to the ssh server.
class TaskBase:
    runDefault = False
    log = None
    client = None
    loggableclass = None
    host = ""
    username = ""
    password = ""
    publickey = ""

    def __init__(self, loggableclass, sftpclient=None, host="", username="", password="") -> None:
        self.loggableclass = loggableclass
        self.client = sftpclient
        self.host = host
        self.username = username
        self.password = password

    def runDefaults(self, sftpclient=None) -> None:
        """Load all classes that extend TaskBase, and run them."""
        self.log("Running")
        try:
            for theclass in TaskBase.__subclasses__():
                theinstance = theclass(self.loggableclass, sftpclient, host=self.host, username=self.username, password=self.password)
                if theinstance.runDefault:
                    theinstance.run()
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            self.log(str(e))
        except Exception as e:
            self.log(traceback.format_exc())
            raise(e)
    
    def log(self, message) -> None:
        """Just simple shortcut to the default log"""
        self.loggableclass.log(message)

    def run(self) -> None:
        # TODO: Error handling
        if self.needsSFTP:
            self.publickey = Certificate().loadOrCreateCertificate()
            self.log("Connecting to: " + self.host)
            # TODO: Don't repeatedly do this in case we have more tasks.
            # TODO: If we get more tasks, handle using an existing certificate
            self.client = Connection(host=self.host,
                                user=self.username,
                                connect_kwargs={"password": self.password}
                                ).sftp() # Connect! :3
        
    def assertServerPermissions(self, filename, chmod) -> bool:
        """Check that the correct permission settings exists for a file or directory on the server."""
        # TODO: Raise a question if we want to change the chmod..
        mode = self.client.stat(filename).st_mode
        type = "folder" if stat.S_ISDIR(mode) else "file"
        if PermissionHelper.NumberToChmod(mode) == str(chmod):
            self.log("The "+ filename + " " + type + " exists, and has the right permissions")
            return True
        else:
            self.log("WARNING! The " + filename + " " + type + " exists, but has the wrong permission. Should be chmod " + str(chmod) + ", or openssh will not allow you to use the certificate")
            return False