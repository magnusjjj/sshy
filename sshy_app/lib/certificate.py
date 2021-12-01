from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
from pathlib import Path
from sshy_app.permissions.permissions_local import PermissionsLocal

# In this file:
# We are dealing with finding, or generating, ssh certificates

class Certificate:
    # The paths to where we find the different ssh files.
    ssh_directory = str(Path.home()) +  "/.ssh"
    public_key_path = str(Path.home()) + "/.ssh/id_rsa.pub"
    private_key_path = str(Path.home()) + "/.ssh/id_rsa"

    # The name says it all. We try to load a certificate, and if we can't find one, we create it.
    # We return a string containing the public key.
    def loadOrCreateCertificate(self) -> str:
        # TODO: More error checking.
        # - What happens if we can't create the directory, or change permissions.
        # TODO: Raise permission change question x 2
        # TODO: We assume that if id_rsa.pub or id_rsa does not exist, then both don't
        # TODO: What happens if we can't write the file

        # We check if the local ssh directory exists, and if not we create it
        if not os.path.exists(self.ssh_directory):
            self.log("Have to create the .ssh folder..")
            os.mkdir(self.ssh_directory)
            self.chmod(self.ssh_directory, "700")

        # If we can't find the private or public key, we generate a new one.
        if (not os.path.exists(self.private_key_path)) or (not os.path.exists(self.public_key_path)):
            self.log("Need to generate a new key")

            # We use the cryptographic libraries to generate new keys.
            key = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=2048
            )

            private_key = key.private_bytes(
                crypto_serialization.Encoding.PEM,
                crypto_serialization.PrivateFormat.PKCS8,
                crypto_serialization.NoEncryption()
            )

            public_key = key.public_key().public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH
            )

            # Write the new keys to disk
            f = open(self.private_key_path, "wb")
            f.write(private_key)
            f.close()
            f = open(self.public_key_path, "wb")
            f.write(public_key)
            f.close()

            # Fix the permissions
            PermissionsLocal.chmod(self.private_key_path, "600")
            PermissionsLocal.chmod(self.public_key_path, "600")

        # Read the file, and return it's contents.
        f = open(self.public_key_path, "rb")
        content = f.read()
        f.close()
        return content