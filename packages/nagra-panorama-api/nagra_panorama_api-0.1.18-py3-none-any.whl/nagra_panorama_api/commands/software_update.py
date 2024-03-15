"""
This example will download and install the latest version of the software.

Python requirements:
- ping3
"""

import logging
import os
from multiprocessing.pool import ThreadPool
from pathlib import Path

import click
import requests
import urllib3
import yaml

# from nagra_network_misc_utils.logger import set_default_logger
from rich.logging import RichHandler

# from ping3 import ping  # Ping
import nagra_panorama_api
from nagra_panorama_api.utils import wait

# set_default_logger()
logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)


def wait_availability(client, fw_host, logger=None):
    if logger is None:
        logger = logging
    logger.info(
        f"Waiting for firewall '{fw_host}' availability. Repeating until success or timeout"
    )
    for _ in wait():
        try:
            versions = client.get_versions()
            current = next(v for v in versions if v.current)
            if current is None:
                logger.warning("Device is not not answering")
            else:
                return current
        except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
            logger.warning(f"Firewall {fw_host} is still not responding")
        except Exception as e:
            logger.debug(
                f"Unexpected error of type {type(e)} occured on firewall {fw_host}"
            )
            logger.error(f"Firewall {fw_host} is still not responding: {e}")
    raise Exception(f"Timeout while waiting for availability of firewall {fw_host}")


def getenv(*varnames, exit_on_failure=True, default=None):
    for var in varnames:
        val = os.environ.get(var)
        if val is not None:
            return val.strip()
    logging.error(
        f"None of the following environment variables are defined: {', '.join(varnames)}"
    )
    if exit_on_failure:
        exit(1)
    return default


def check_availability(client, fw_host, logger=None):
    if logger is None:
        logger = logging
    ## Wait for the FW to respond
    version = wait_availability(client, fw_host, logger=logger)
    if not version:
        logger.error(f"Device {fw_host} never responded")
        return False
    logger.info(f"Firewall {fw_host} is available")
    return True


def check_panorama_connection(panorama_client, fw_host, logger=None):
    if logger is None:
        logger = logging
    ## Check that the device is connected to Panorama
    devices = panorama_client.get_devices()
    device = next((d for d in devices if d.ip_address == fw_host), None)
    if device is None:
        logger.error(f"Device with IP {fw_host} is not detected AT ALL to panorama")
        return False
    if not device.connected:
        logger.error(
            f"Device with IP {fw_host} is not detected as connected to panorama"
        )
        return False
    logger.info(f"Firewall {fw_host} is detected has connected to panorama")
    return True


def run_checks(panorama_client, client, fw_host, logger=None):
    if logger is None:
        logger = logging
    if not check_availability(client, fw_host, logger=logger):
        return False
    if not check_panorama_connection(panorama_client, fw_host, logger=logger):
        return False
    return True


################################################################################
DEFAULT_LOGGER_FORMAT = "%(message)s"


def get_logger(name, file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.handlers.clear()

    formatter = logging.Formatter(DEFAULT_LOGGER_FORMAT)
    stream_handler = RichHandler()
    logger.addHandler(stream_handler)
    if file is not None:
        file = Path(file).resolve()
        file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file, mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    logger.propagate = False  # Prevent calling the root logger
    return logger


@click.command(
    "upgrade",
    help="Upgrade a group of devices to a different softare version",
)
@click.argument(
    "file",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    # help="Configuration file containing the upgrade groups"
)
@click.argument("group")  # help="Upgrade group from the configuration to run"
@click.option(
    "--apikey",
    help="Panorama & Firewall api key (must be the same for both). Use one of the following environment variables: PANORAMA_APIKEY, PANO_APIKEY",
)
@click.option(
    "--download-only",
    is_flag=True,
    default=False,
    help="Only download the software version without installing it",
)
@click.option("--test-only", is_flag=True, default=False, help="Only runs the checks")
@click.option("--logs-output", help="Destination folder where to put the logs")
def upgrade_cmd(file, group, apikey, download_only, test_only, logs_output):
    if download_only and test_only:
        logging.error(
            "You cannot not use --download-only and --test-only flags at the same time"
        )
        exit(1)
    file = Path(file).resolve()
    if not apikey:
        apikey = getenv("PANORAMA_APIKEY", "PANO_APIKEY")
    if not apikey:
        logging.error(
            "PANORAMA_APIKEY not provided, please check the environment variables"
        )
        exit(1)
    if file.suffix not in (".yml", ".yaml"):
        logging.error("File must be in yaml format")
        exit(1)
    if logs_output is not None:
        logs_output = Path(logs_output).resolve()
        if logs_output.is_file():
            logging.error(f"{logs_output} is a file, it must be a folder or not exists")
    try:
        data = yaml.safe_load(file.read_text())
        groups = data["groups"]
        group_data = groups.get(group)
        if not group_data:
            logging.error(f"Group '{group}' does not exist ini file {file}")
            defined_groups = groups.keys()
            if defined_groups:
                defined_groups = ", ".join(sorted(defined_groups))
                logging.info(f"Possible groups are: {defined_groups}")
            exit(1)
    except Exception as e:
        logging.debug(e)
        logging.error(
            f"An error occured when parsing the file '{file}' and/or retrieving the data of group '{group}'",
            "Make sure that the file is formatted correctly and that the group exists",
        )
        exit(1)

    panorama_ip = group_data["panorama_ip"]
    version = group_data.get("version")
    devices = group_data["devices"]

    if not test_only:
        if not version:
            logging.warning(
                "version not defined, the script will default to the latest version for each devices"
            )
        else:
            logging.info(f"Starting upgrade to version {version}")

    def worker(args):
        try:
            (
                group,
                panorama_host,
                fw_name,
                fw_host,
                apikey,
                version,
                download_only,
                test_only,
                logs_output,
            ) = args

            logfile = logs_output / Path(group) / fw_host if logs_output else None
            logger = get_logger(f"Device {fw_name}", logfile)

            panorama_client = nagra_panorama_api.XMLApi(
                panorama_host, apikey, logger=logger
            )
            client = nagra_panorama_api.XMLApi(fw_host, apikey, logger=logger)

            fw_sys_info = client.system_info()
            serial_number = fw_sys_info.xpath(".//serial/text()")[0]
            current_version = fw_sys_info.xpath(".//sw-version/text()")[0]
            logger.info(
                f"Device with IP {fw_host} (S/N: {serial_number}) is currently on version '{current_version}'"
            )
            if not test_only:
                version = client.automatic_software_upgrade(
                    version, install=(not download_only)
                )

            # Tests
            res = run_checks(panorama_client, client, fw_host, logger=logger)
            if download_only:
                logger.info(
                    f"Done dowloading version { version.version } on device {fw_name} ({fw_host}) "
                )
            elif not test_only:
                logger.info(
                    f"Done upgrading device {fw_name} ({fw_host}) to version { version.version }"
                )
            return res
        except Exception as e:
            logger.error(
                f"""\
An unexpected error occured
Worker args: {args}
{e}
"""
            )
            return False

    pool_data = [
        (
            group,
            panorama_ip,
            d["hostname"],
            d["ip_address"],
            apikey,
            version,
            download_only,
            test_only,
            logs_output,
        )
        for d in devices
    ]
    failed_upgrades = 0
    with ThreadPool(len(pool_data)) as pool:
        for i, upgrade_res in enumerate(pool.imap_unordered(worker, pool_data), 1):
            logging.info(f"Upraded {i}/{len(pool_data)}")
            if not upgrade_res:
                failed_upgrades += 1
    if failed_upgrades > 0:
        logging.error(f"There was {failed_upgrades} failed upgrades")
    else:
        logging.info("All upgrades went successfuly")


@click.command(
    "generate-apikey",
    help="This command generate the configuration file boilerplate using all devices connected to panorama",
)
@click.option(
    "--panorama-host",
    "host",
    envvar="PANORAMA_HOST",
    required=True,
    help="Panorama host/ip. Use PANORAMA_HOST environment variable",
)
@click.option(
    "--username",
    envvar="PANORAMA_USERNAME",
    required=True,
    help="Username password to access Panorama (envvar: PANORAMA_USERNAME)",
)
@click.option(
    "--password",
    envvar="PANORAMA_PASSWORD",
    prompt=True,
    hide_input=True,
    required=True,
    help="User password to access Panorama (envvar: PANORAMA_PASSWORD)",
)
def generate_apikey_cmd(host, username, password):
    client = nagra_panorama_api.XMLApi(host, "dummykey")
    print(client.generate_apikey(username, password))


@click.command(
    "generate-config",
    help="This command generate the configuration file boilerplate using all devices connected to panorama",
)
@click.option(
    "--panorama-host",
    "host",
    help="Panorama host/ip. Use PANORAMA_HOST environment variable",
)
@click.option(
    "--apikey",
    help="Panorama api key. Use one of the following environment variables: PANORAMA_APIKEY, PANO_APIKEY",
)
@click.option(
    "--sw-version",
    "version",
)
@click.option(
    "-o",
    "--out",
    help="Output file for the configuration containing the upgrade groups (default to stdin)",
)
def generate_configuration_file_cmd(host, apikey, version, out):
    if not host:
        host = getenv("PANORAMA_HOST")
    if not host:
        logging.error("Missing Panorama host")
        exit(1)
    if not apikey:
        apikey = getenv("PANORAMA_APIKEY", "PANO_APIKEY")
    if not apikey:
        logging.error("Missing Panorama API Key")
        exit(1)
    panorama_client = nagra_panorama_api.XMLApi(host, apikey)
    connected_devices = panorama_client.get_devices(connected=True)
    data = {
        "groups": {
            "all": {
                "panorama_ip": host,
                "version": version,
                "devices": [
                    {
                        "hostname": d.hostname,
                        "ip_address": d.ip_address,
                    }
                    for d in connected_devices
                ],
            }
        },
    }

    content = yaml.dump(data, sort_keys=False, explicit_start=True, indent=2)
    if not out:
        print(content)
    else:
        output = Path(out)
        output.write_text(content)


# client = nagra_panorama_api.XMLApi(os.environ["PANO_HOST"], os.environ["PANO_APIKEY"])
# fw_sys_info = client.system_info()

# vpn_flows = client.get_vpn_flows()
# template_status = list(panorama_client.get_templates_sync_status())
