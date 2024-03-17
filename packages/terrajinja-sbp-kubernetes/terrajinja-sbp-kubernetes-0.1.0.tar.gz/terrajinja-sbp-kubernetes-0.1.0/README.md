# terrajinja-sbp-kubernetes

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.kubernetes.secret_v1
Original provider: [kubernetes.secret_v1](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/secret_v1)

This custom provider adds the following:
- automaticly create auth string using a base64 encoded value of username and password

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| parameters.data.dockerconfigjson.auths.name.auth | - | base64 auth header is no longer required |

while this provider does not have any additional parameters, you no longer have to create the base64 authentication string. this is done for you. see the example below where the auth header is not provided compared to the original documentation

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This created the secret that allows kubernetes to connect to a private repository to fetch images
```
terraform:
  resources:
    - task: custom-repository-secret
      module: sbp.kubernetes.secret_v1
      parameters:
        metadata: {
          namespace: "my-namespace",
          name: "repository-token-auth"
        }
        data:
          .dockerconfigjson:
            auths:
              "registry.gitlab.schubergphilis.com":
                username: "username"
                password: "{{ env['gitlab_pat_token'] }}"
                email: "username@email.com"
        type: "kubernetes.io/dockerconfigjson"
```

