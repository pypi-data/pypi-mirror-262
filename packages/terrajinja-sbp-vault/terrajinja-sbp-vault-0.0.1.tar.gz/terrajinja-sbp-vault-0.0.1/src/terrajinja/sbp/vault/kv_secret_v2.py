from cdktf import Fn
from cdktf_cdktf_provider_vault.kv_secret_v2 import KvSecretV2
from constructs import Construct
from password_generator import PasswordGenerator


class SbpVaultKvSecretV2(KvSecretV2):
    """SBP version of vault.kv_secret_v2"""

    def __init__(self, scope: Construct, ns: str, data: dict, **kwargs):
        """Enhances the original vault.kv_secret_v2

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource
            data (dict): a dictionary with the key/values of the secret to store

        Original:
            https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/kv_secret_v2
        """

        # convert passwords with the string "random" to a random string
        for key in data.keys():
            if data[key] == "random":
                pwo = PasswordGenerator()
                pwo.minlen = 30
                pwo.maxlen = 30
                pwo.minuchars = 3  # (Optional)
                pwo.minlchars = 3  # (Optional)
                pwo.minnumbers = 3  # (Optional)
                pwo.minschars = 3  # (Optional)
                pwo.excludeschars = "%$@[]}{()}|`'\",<>?#"
                data[key] = pwo.generate()

            # fix for multi-line values
            # if isinstance(data[key], str):
            #     data[key] = Fn.replace(data[key], "\n", r'\\n')

        # call the original resource
        super().__init__(
            scope=scope,
            id_=ns,
            data_json=Fn.jsonencode(data),
            lifecycle={'ignore_changes': "all"},
            **kwargs,
        )
