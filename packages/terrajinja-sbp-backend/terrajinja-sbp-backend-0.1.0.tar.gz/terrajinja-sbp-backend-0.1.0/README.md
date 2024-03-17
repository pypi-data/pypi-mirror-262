# terrajinja-sbp-backend

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.backend.s3_backend
Original provider: [backend.s3_backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3)

This custom provider adds the following:
- adds the s3 backend provider to terrajinja

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | - | there are no new parameters |

This resource is an interface for the backend providers,
as the concept of backend is not an resource, this is the intermediate to support it.

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This created both the hashicorp vault with the name `generic`, and adds a secret in it in the path `application` with key `admin` that contains a random password
```
terraform:
  resources:
    - task: s3-backend
      module: sbp.backend.s3_backend
      parameters:
        bucket: "terraform-state"
        key: {{  terraform.state_file }}
        endpoint: "https://s3.endpoint.url"
        encrypt: True
        region: eu-nl-prod01
        skip_region_validation: True
        skip_credentials_validation: True
        skip_metadata_api_check: True
```

