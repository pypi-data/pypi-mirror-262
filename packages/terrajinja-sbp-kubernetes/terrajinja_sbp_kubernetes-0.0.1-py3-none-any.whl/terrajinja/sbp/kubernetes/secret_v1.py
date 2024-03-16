from dataclasses import dataclass
from constructs import Construct
from cdktf_cdktf_provider_kubernetes.secret_v1 import SecretV1
from json import dumps as json_dump
from cdktf import Fn
import base64


class SbpKubernetesSecretV1(SecretV1):
    def __init__(self, scope: Construct, ns: str, data: dict, **kwargs):
        dockerconfig = data.get('.dockerconfigjson')
        if dockerconfig:
            for k in data['.dockerconfigjson']['auths'].keys():
                username = data['.dockerconfigjson']['auths'][k]['username']
                password = data['.dockerconfigjson']['auths'][k]['password']
                credentials = f'{username}:{password}'
                data['.dockerconfigjson']['auths'][k]['auth'] = base64.b64encode(
                    credentials.encode("ascii")).decode("ascii")
            data['.dockerconfigjson'] = json_dump(separators=(',', ':'), obj=dockerconfig)

        super().__init__(
            scope=scope,
            id_=ns,
            data=data,
            **kwargs,
        )