provider "google" {
  project = "gfw-int-infrastructure"
}

variable "pypi_password_secret_version" {
  description = "Secret Manager version for _PYPI_PASSWORD, in projects/PROJECT/secrets/SECRET/versions/VERSION format."
  type        = string
}

variable "pypi_token_secret_version" {
  description = "Secret Manager version for _PYPI_TOKEN, in projects/PROJECT/secrets/SECRET/versions/VERSION format."
  type        = string
}

variable "pypi_token_username" {
  description = "PyPI username used with the API token."
  type        = string
  default     = "__token__"
}

resource "google_cloudbuild_trigger" "shipdataprocess_trigger_tag" {
  name     = "shipdataprocess-release"
  location = "us-central1"

  github {
    name  = "ShipDataProcess"
    owner = "GlobalFishingWatch"
    push {
      tag          = "^v?[0-9]+\\.[0-9]+\\.[0-9]+$"
      invert_regex = false
    }
  }

  service_account = "projects/global-fishing-watch/serviceAccounts/terraform-deployer@global-fishing-watch.iam.gserviceaccount.com"

  substitutions = {
    _PYPI_PASSWORD       = var.pypi_password_secret_version
    _PYPI_TOKEN          = var.pypi_token_secret_version
    _PYPI_TOKEN_USERNAME = var.pypi_token_username
  }

  build {
    step {
      id   = "FETCH TAGS"
      name = "gcr.io/cloud-builders/git"
      args = ["fetch", "--unshallow"]
    }

    step {
      id         = "BUILD WHEEL"
      name       = "python:3.12-slim"
      entrypoint = "bash"
      args = [
        "-ceu",
        <<-EOF
          apt-get update
          apt-get install -y --no-install-recommends git
          python -m pip install --no-cache-dir build==1.2.2.post1
          python -m build
        EOF
      ]
      wait_for = ["FETCH TAGS"]
    }

    step {
      id         = "push to pypi"
      name       = "python:3.12-slim"
      entrypoint = "bash"
      args = [
        "-ceu",
        <<-EOF
          python -m pip install --no-cache-dir twine==6.1.0
          python -m twine check /workspace/dist/*
          python -m twine upload /workspace/dist/* -u "$_PYPI_TOKEN_USERNAME" -p "$$TOKEN" --verbose
        EOF
      ]
      wait_for   = ["BUILD WHEEL"]
      secret_env = ["PASSWORD", "TOKEN"]
    }

    available_secrets {
      secret_manager {
        version_name = "$_PYPI_PASSWORD"
        env          = "PASSWORD"
      }

      secret_manager {
        version_name = "$_PYPI_TOKEN"
        env          = "TOKEN"
      }
    }

    options {
      logging = "CLOUD_LOGGING_ONLY"
    }

    timeout = "900s"
  }
}
