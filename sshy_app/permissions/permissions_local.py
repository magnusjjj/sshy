import os
import getpass

class PermissionsLocal:
    @staticmethod
    def chmod(filename, mode):
        if os.name == 'nt':
            sanitized_path = filename.replace("/", "\\")
            username = getpass.getuser()
            os.system("Icacls " + sanitized_path + " /inheritancelevel:r")
            os.system("Icacls " + sanitized_path + " /c /t /Remove:g Administrator \"Authenticated Users\" BUILTIN\\Administrators BUILTIN Everyone System Users")
            os.system("Icacls " + sanitized_path + " /grant:r \"" + username + "\":\"(R)\"")
        else:
            os.chmod(filename, mode)