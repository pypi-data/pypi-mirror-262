import json
from base64 import b64encode
import pytest
from cdktf import Testing
from src.terrajinja.sbp.kubernetes.secret_v1 import SbpKubernetesSecretV1
from .helper import stack, has_resource, has_resource_count, has_resource_path_value

class TestSbpKubernetesSecretV1:

    def test_resource(self, stack):
        username = "username"
        password = "password"
        secret = SbpKubernetesSecretV1(
            scope=stack,
            ns="test",
            metadata={
                'namespace': 'test_ns',
                'name': 'test_name'
            },
            data={
                '.dockerconfigjson': {
                    'auths': {
                        'test_registry': {
                            'username': username,
                            'password': password
                        }
                    }
                }
            }
        )

        print(dir(secret.metadata.name))
        synthesized = Testing.synth(stack)

        # Test synth output
        has_resource(synthesized, "kubernetes_secret_v1")
        has_resource_count(synthesized, "kubernetes_secret_v1", 1)

        # Test specific .dockerconfig
        has_resource_path_value(synthesized, "kubernetes_secret_v1", "test", "metadata", "name", "test_name")
        has_resource_path_value(synthesized, "kubernetes_secret_v1", "test", "data", ".dockerconfigjson",
                                json.dumps(separators=(',', ':'), obj={
                                    "auths": {
                                        "test_registry": {
                                            "username": username,
                                            "password": password,
                                            "auth": b64encode(f"{username}:{password}".encode("ascii")).decode("ascii")
                                        }
                                    }
                                }))

if __name__ == "__main__":
    pytest.main()
