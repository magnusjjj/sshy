from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
from pathlib import Path
from sshy_app.permissions.permissions_local import PermissionsLocal

class Certificate:
    ssh_directory = str(Path.home()) +  "/.ssh"
    public_key_path = str(Path.home()) + "/.ssh/id_rsa.pub"
    private_key_path = str(Path.home()) + "/.ssh/id_rsa"


    def createOrLoadCertificate(self):
        # TODO: More error checking
        if not os.path.exists(self.ssh_directory):
            self.log("Have to create the .ssh folder..")
            os.mkdir(self.ssh_directory)
            self.chmod(self.ssh_directory, "700")

        if (not os.path.exists(self.private_key_path)) or (not os.path.exists(self.public_key_path)):
            # TODO: We assume that if id_rsa.pub or id_rsa does not exist, then both don't
            self.log("Need to generate a new key")
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

            f = open(self.private_key_path, "wb")
            f.write(private_key)
            f.close()
            f = open(self.public_key_path, "wb")
            f.write(public_key)
            f.close()

            PermissionsLocal.chmod(self.private_key_path, "600")
            PermissionsLocal.chmod(self.public_key_path, "600")

        f = open(self.public_key_path, "rb")
        content = f.read()
        f.close()
        return content