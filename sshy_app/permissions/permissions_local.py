import os
import getpass

# This class contains methods helping out with permission changes locally
# TODO: Error checking?

class PermissionsLocal:
    @staticmethod
    def chmod_special(filename, mode) -> None:
        """This function changes the permissions of a file.
        Under unix-like operating systems, this sets the standard chmod settings.
        Under Windows, this goes further, changing the owner, removing all access rights for every other user.
        This function is used to make openssh not freak out about having other users have access to the encryption keys"""
        if os.name == 'nt':
            sanitized_path = filename.replace("/", "\\") # This needs to be in the windows format
            username = getpass.getuser()
            os.system("Icacls " + sanitized_path + " /inheritancelevel:r") # Remove filesystem permission inheritance
            os.system("Icacls " + sanitized_path + " /c /t /Remove:g Administrator \"Authenticated Users\" BUILTIN\\Administrators BUILTIN Everyone System Users") # Remove all other common users.
            os.system("Icacls " + sanitized_path + " /grant:r \"" + username + "\":\"(R)\"") # Re-add your own user.
        else:
            os.chmod(filename, mode) # Just call the unix version.