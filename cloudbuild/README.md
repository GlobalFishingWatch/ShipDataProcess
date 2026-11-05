# Cloud Build configuration

Terraform manages the `shipdataprocess-release` trigger in
`gfw-int-infrastructure`, in `us-central1`, following the `bigquery-udfs`
configuration. State is stored in the shared GCS bucket under the separate
`cloudbuild-shipdataprocess` prefix.

The trigger publishes releases for tags such as `0.8.6` and `v0.8.7` (three
numeric components, with an optional `v` prefix). The complete build is defined
inline in `main.tf`, including its steps, secrets, Cloud Logging configuration
and 900-second timeout. No `cloudbuild.yaml` is needed in the source revision.

Packaging and publishing use the official `python:3.12-slim` image, with
`build==1.2.2.post1` and `twine==6.1.0`, respectively. The packaging step installs
Git for Versioneer and waits for the repository history fetch before building.
`python -m build` produces a source distribution and a Python 3 wheel; Twine
checks their metadata before publishing. The build needs network access to
Docker Hub, Debian package repositories and PyPI.

From this directory, initialize and review the configuration:

```sh
terraform init
terraform plan
terraform apply
```

Set the existing PyPI secret version paths in a local `terraform.tfvars` file
(excluded from Git):

```hcl
pypi_password_secret_version = "projects/PROJECT/secrets/PASSWORD_SECRET/versions/latest"
pypi_token_secret_version    = "projects/PROJECT/secrets/TOKEN_SECRET/versions/latest"
pypi_token_username          = "__token__"
```

These variables contain Secret Manager resource names, not secret values.
The PyPI token username defaults to `__token__` and can be overridden with
`pypi_token_username`. Review the plan before applying. Changes to the build
configuration take effect after `terraform apply`, including for existing tags.

The GitHub repository must already be connected to Cloud Build. The build uses
`terraform-deployer@global-fishing-watch.iam.gserviceaccount.com`, which must
have access to the build images, Secret Manager secret versions, and Cloud
Logging. The identity applying Terraform must be allowed to use that service
account. This configuration does not create secrets or change IAM permissions.
