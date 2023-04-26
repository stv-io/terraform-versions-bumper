import glob
import fileinput
import os
import sys
import logging
import pygohcl
import httpx
import json

# log_format = "%(asctime)s %(levelname)s: %(message)s"
log_format = "%(levelname)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(log_level)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(log_level)
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(log_level)

# TODO: Configure this from an input parameter
replace = True

# TODO: cater for when we don't have matching terraform files, or we don't find the terraform block


def main():
    # Terraform versions
    logging.info(f'Searching for "required_version" in terraform files ..')
    tf_required_filename = find_file_with_string("required_version", "*.tf")
    logging.info(f"Processing {tf_required_filename}..")
    tf_required_block = load_terraform_block(tf_required_filename)
    current_tf_version_string = resolve_tf_version(tf_required_block)
    # print(f"current_tf_version_string {current_tf_version_string}")
    current_tf_version = resolve_version(current_tf_version_string)
    logging.info(f"current_tf_version {current_tf_version}")
    latest_terraform_release = get_latest_terraform_release()
    latest_terraform_version = latest_terraform_release.replace("v", "")
    # print(f"latest_terraform_version {latest_terraform_version}")
    # print(f"tf_required_filename {tf_required_filename}")
    # print(f"current_tf_version {current_tf_version}")
    # print(f"latest_terraform_version {latest_terraform_version}")

    if replace:
        logging.info(f"Replacing terraform required_version in {tf_required_filename}")
        bump_version_latest(
            tf_required_filename, current_tf_version, latest_terraform_version
        )

    # # Providers versions
    logging.info(f'Searching for "required_providers" in terraform files ..')
    providers_required_filename = find_file_with_string("required_providers", "*.tf")
    providers_required_block = load_terraform_block(providers_required_filename)
    provider_map = resolve_providers(providers_required_block)
    logging.debug(f"found {len(provider_map)} providers\n{json.dumps(provider_map)}")
    for provider_name, provider_config in provider_map.items():
        source = provider_config["source"]
        version = provider_config["version"]
        logging.info(f"Processing provider {source}")
        latest_provider_version = get_latest_provider(source)
        logging.info(
            f"Current defined versions - {version}; latest available version for provider {source}: {latest_provider_version}"
        )
        provider_version = resolve_version(version)
        if replace:
            logging.info(
                f"Replacing required_providers in {providers_required_filename}"
            )
            bump_version_latest(
                providers_required_filename, provider_version, latest_provider_version
            )


def bump_version_latest(file_name, search_string, replace_string):
    logging.info(
        f"Replacing version {search_string} with {replace_string} in {file_name}"
    )
    with fileinput.FileInput(file_name, inplace=True, backup=".bak") as file:
        for line in file:
            print(line.replace(search_string, replace_string), end="")


def find_file_with_string(string, extension):
    files = glob.glob(extension)
    for line in fileinput.input(files):
        if string in line:
            logging.debug(f"Matched {string} in {files}")
    if len(files) != 1:
        logging.error(
            f'The string "{string}" was found in {len(files)} files: {files}.'
        )
        logging.error('Please run "terraform validate", fix, and try again')
        sys.exit(1)
    return files[0]


def load_terraform_block(file):
    with open(file) as f:
        terraform_block = pygohcl.loads(f.read())
    return terraform_block


def resolve_tf_version(content):
    current_tf_version = None
    if "terraform" in content:
        terraform = content["terraform"]
        if "required_version" in terraform:
            current_tf_version = terraform["required_version"]
    return current_tf_version


def resolve_providers(content):
    provider_map = {}
    if "terraform" in content:
        terraform = content["terraform"]
        if "required_providers" in terraform:
            required_providers = terraform["required_providers"]
            for provider_name, provider_config in required_providers.items():
                if "source" in provider_config and "version" in provider_config:
                    provider_map[provider_name] = {
                        "source": provider_config["source"],
                        "version": provider_config["version"],
                    }
    return provider_map


def get_latest_terraform_release():
    url = "https://api.github.com/repos/hashicorp/terraform/releases/latest"
    with httpx.Client() as client:
        response = httpx.get(url)
        logging.debug(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()["tag_name"]
    else:
        print(f"{response.status_code} error querying {url}:\n {response.text}")
    return data


def get_latest_provider(source):
    url = f"https://registry.terraform.io/v2/providers/{source}/provider-versions"
    with httpx.Client() as client:
        response = httpx.get(url)
        logging.debug(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()["data"]
        for version in data:
            latest_version = data[-1]["attributes"]["version"]
    else:
        print(f"{response.status_code} error querying {url}:\n {response.text}")

    return latest_version


def resolve_version(version_string):
    # print(f"version_string {version_string}")
    version_parts = version_string.split(" ")
    # print(f"version_parts {version_parts}")
    if len(version_parts) == 2:
        version = version_parts[1]
        print(f"version {version}")
    elif len(version_parts) == 1:
        print("lenght is 1")
        if version_parts[0].isnumeric() or isfloat(version_parts[0]):
            version = version_parts[0]
    else:
        logging.error(f"Version {version_string} not supported")
        sys.exit(1)
    # logging.debug(version)
    return version


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
