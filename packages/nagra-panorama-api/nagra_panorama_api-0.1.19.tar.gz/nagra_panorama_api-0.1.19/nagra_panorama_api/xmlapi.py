import logging
from itertools import chain, product
from multiprocessing.pool import ThreadPool as Pool
from typing import Optional

import requests

from . import types
from .constants import SUCCESS_CODE
from .utils import (
    clean_url_host,
    detach,
    diff_patch,
    el2dict,
    etree_fromstring,
    etree_tostring,
    extend_element,
    map_dicts,
    wait,
)


def get_tree(
    host, api_key, remove_blank_text=True, verify=False, timeout=None, logger=None
):
    if logger is None:
        logger = logging
    res = requests.get(
        f"{host}/api?type=config&action=show&xpath=/config",
        headers={"X-PAN-KEY": api_key},
        verify=verify,
        timeout=timeout,
    )
    root_tree = etree_fromstring(res.content, remove_blank_text=remove_blank_text)
    try:
        tree = root_tree.xpath("/response/result/config")[0]
    except Exception:
        logger.warning("Response doesn't contains the config tag. Response:")
        logger.warning(etree_tostring(root_tree, pretty_print=True).decode()[:1000])
        raise Exception("Response doesn't contains the config tag. Check the logs")
    detach(tree)  # Remove the /response/result part
    return tree


def parse_msg_result(result):
    # sometimes, there is <line> elements inside of msg
    msg = "".join(result.xpath("./msg/text()"))
    if not msg:
        msg = "".join(result.xpath("./result/msg/text()"))
    if msg:
        return msg
    return "\n".join(result.xpath("./msg/line/text()"))


def _get_rule_use_cmd(device_group, position, rule_type, start_index, number):
    # positions = ("pre", "post")
    return f"""<show><policy-app>
        <mode>get-all</mode>
        <filter>(rule-state eq 'any')</filter>
        <vsysName>{device_group}</vsysName>
        <position>{position}</position>
        <type>{rule_type}</type>
        <anchor>{start_index}</anchor>
        <nrec>{number}</nrec>
        <pageContext>rule_usage</pageContext>
    </policy-app></show>"""


def raw_request(
    url,
    type,
    method="GET",
    vsys=None,
    params=None,
    headers=None,
    remove_blank_text=True,
    verify=False,
    logger=None,
):
    if logger is None:
        logger = logging
    query_params = {"type": type}
    if params:
        query_params = {**query_params, **params}
    if vsys is not None:
        query_params["vsys"] = vsys

    res = requests.request(
        method=method,
        url=url,
        params=query_params,
        headers=headers,
        verify=verify,
    )
    content = res.content.decode()
    tree = etree_fromstring(content, remove_blank_text=remove_blank_text)
    status = tree.attrib["status"]
    code = int(tree.get("code", SUCCESS_CODE))
    msg = parse_msg_result(tree)
    if status == "error" or code < SUCCESS_CODE:
        logger.debug(content[:500])
        raise Exception(msg)
    if msg:
        return msg
    return tree


class XMLApi:
    def __init__(self, host, api_key, verify=False, logger=None):
        if not host:
            raise Exception("Missing Host")
        host, _, _ = clean_url_host(host)

        self._host = host
        self._api_key = api_key
        self._url = f"{host}/api"
        self._verify = verify
        self.logger = logger or logging

    def _request(
        self,
        type,
        method="GET",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if verify is None:
            verify = self._verify
        headers = {"X-PAN-KEY": self._api_key}
        return raw_request(
            self._url,
            type,
            method,
            vsys=vsys,
            params=params,
            headers=headers,
            remove_blank_text=remove_blank_text,
            verify=verify,
            logger=self.logger,
        )

    def _conf_request(
        self,
        xpath,
        action="get",
        method="GET",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"action": action, "xpath": xpath, **params}
        return self._request(
            "config",
            method=method,
            vsys=vsys,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def _op_request(
        self,
        cmd,
        method="POST",
        vsys=None,
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"cmd": cmd, **params}
        return self._request(
            "op",
            method=method,
            vsys=vsys,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def _commit_request(
        self,
        cmd,
        method="POST",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        if params is None:
            params = {}
        params = {"cmd": cmd, **params}
        return self._request(
            "commit",
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key
    def generate_apikey(self, username, password, verify=None):
        params = {"user": username, "password": password}
        return self._request(
            "keygen",
            method="POST",
            params=params,
            verify=verify,
        ).xpath(".//key/text()")[0]

    # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/get-version-info-api
    def api_version(self, verify=None):
        return el2dict(
            self._request(
                "version",
                method="POST",
                verify=verify,
            ).xpath(".//result")[0]
        )["result"]

    def configuration(
        self,
        xpath,
        action="get",
        method="GET",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        return self._conf_request(
            xpath,
            action=action,
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def operation(
        self,
        cmd,
        method="POST",
        params=None,
        remove_blank_text=True,
        verify=None,
    ):
        return self._op_request(
            cmd,
            method=method,
            params=params,
            remove_blank_text=remove_blank_text,
            verify=verify,
        )

    def get_tree(self, extended=False, verify=None):
        if verify is None:
            verify = self._verify
        tree = get_tree(self._host, self._api_key, verify=verify, logger=self.logger)
        if extended:
            self._extend_tree_information(tree, verify=verify)
        return tree

    def _get_rule_use(self, device_group, position, rule_type, number=200, verify=None):
        results = []
        for i in range(100):
            cmd = _get_rule_use_cmd(
                device_group,
                position,
                rule_type,
                i * number,
                number,
            )
            res = self._op_request(cmd, verify=verify).xpath("result")[0]
            total_count = int(res.attrib["total-count"])
            results.extend(res.xpath("entry"))
            if len(results) >= total_count:
                break
        return results

    def get_rule_use(self, tree=None, max_threads=None, verify=None):
        if tree is None:
            tree = self.get_tree(verify=verify)
        device_groups = tree.xpath("devices/*/device-group/*/@name")
        positions = ("pre", "post")
        # rule_types = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*"
        # "/*[self::post-rulebase or self::pre-rulebase]/*")})
        rule_types = ("security", "pbf", "nat", "application-override")
        args_list = list(product(device_groups, positions, rule_types))

        def func(args):
            return self._get_rule_use(*args, verify=verify)

        threads = len(args_list)
        threads = min(max_threads or threads, threads)
        with Pool(len(args_list)) as pool:
            data = pool.map(func, args_list)
        return [entry for entry_list in data for entry in entry_list]

    def _get_rule_hit_count(self, device_group, rulebase, rule_type, verify=None):
        cmd = (
            "<show><rule-hit-count><device-group>"
            f"<entry name='{device_group}'><{rulebase}><entry name='{rule_type}'>"
            f"<rules><all/></rules></entry></{rulebase}></entry>"
            "</device-group></rule-hit-count></show>"
        )
        res = self._op_request(cmd, verify=verify)
        entries = res.xpath(".//rules/entry") or []
        # return entries
        return [(device_group, rulebase, rule_type, e) for e in entries]

    def get_rule_hit_count(self, tree=None, max_threads=None, verify=None):
        if tree is None:
            tree = self.get_tree(verify=verify)
        device_groups = tree.xpath("devices/*/device-group/*/@name")
        # rulebases = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*/*")})
        rulebases = ("pre-rulebase", "post-rulebase")
        # rule_types = tuple({x.tag for x in tree.xpath(
        # "devices/*/device-group/*"
        # "/*[self::post-rulebase or self::pre-rulebase]/*")})
        rule_types = ("security", "pbf", "nat", "application-override")
        args_list = list(product(device_groups, rulebases, rule_types))

        def func(args):
            return self._get_rule_hit_count(*args, verify=verify)

        threads = len(args_list)
        threads = min(max_threads or threads, threads)
        with Pool(len(args_list)) as pool:
            data = pool.map(func, args_list)
        return [entry for entry_list in data for entry in entry_list]

    def _extend_tree_information(
        self,
        tree,
        extended=None,
        max_threads=None,
        verify=None,
    ):
        if extended is None:
            extended = self.get_rule_use(tree, max_threads=max_threads, verify=verify)
        rules = tree.xpath(
            ".//device-group/entry/"
            "*[self::pre-rulebase or self::post-rulebase]/*/rules/entry[@uuid]",
        )
        ext_dict = {x.attrib.get("uuid"): x for x in extended}
        rules_dict = {x.attrib["uuid"]: x for x in rules}
        for ext, rule in map_dicts(ext_dict, rules_dict):
            extend_element(rule, ext)
            # rule.extend(ext) # This is causing duplicates entries
        return tree, extended

    def get(self, xpath, verify=None):
        """
        This will retrieve the xml definition based on the xpath
        The xpath doesn't need to be exact
        and can select multiple values at once.
        Still, it must at least speciy /config at is begining
        """
        return self._conf_request(xpath, action="show", method="GET", verify=verify)

    def delete(self, xpath, verify=None):
        """
        This will REMOVE the xml definition at the provided xpath.
        The xpath must be exact.
        """
        return self._conf_request(
            xpath,
            action="delete",
            method="DELETE",
            verify=verify,
        )

    def create(self, xpath, xml_definition, verify=None):
        """
        This will ADD the xml definition
        INSIDE the element at the provided xpath.
        The xpath must be exact.
        """
        # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration
        params = {"element": xml_definition}
        return self._conf_request(
            xpath,
            action="set",
            method="POST",
            params=params,
            verify=verify,
        )

    def update(self, xpath, xml_definition, verify=None):
        """
        This will REPLACE the xml definition
        INSTEAD of the element at the provided xpath
        The xpath must be exact.
        Nb: We can pull the whole config, update it locally,
        and push the final result
        """
        # https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration
        params = {"element": xml_definition}
        return self._conf_request(
            xpath,
            action="edit",
            method="POST",
            params=params,
            verify=verify,
        )

    def revert_changes(self, skip_validated=False, verify=None):
        skip = "<skip-validate>yes</skip-validate>" if skip_validated else ""
        cmd = f"<revert><config>{skip}</config></revert>"
        return self._op_request(cmd, verify=verify)

    def validate_changes(self, verify=None):
        cmd = "<validate><full></full></validate>"
        return self._op_request(cmd, verify=verify)

    def raw_get_push_scope(self, admin=None, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        filter = f"<admin><member>{admin}</member></admin>" if admin else ""
        cmd = f"<show><config><push-scope>{filter}</push-scope></config></show>"
        return self._op_request(cmd, verify=verify)

    def get_push_scope_devicegroups(self, admin=None, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        # TODO
        scope = self.raw_get_push_scope(admin=admin, verify=verify)
        return list(set(scope.xpath(".//objects/entry[@loc-type='device-group']/@loc")))

    def uncommited_changes(self, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        cmd = "<show><config><list><changes></changes></list></config></show>"
        return self._op_request(cmd, verify=verify)

    def uncommited_changes_patch(self, verify=None):
        """
        Gives detailed information about pending changes
        (e.g. xpath, owner, action, ...)
        """
        candidate = self.candidate_config(verify=verify)
        running = self.running_config(verify=verify)
        return diff_patch(running, candidate)

    def uncommited_changes_summary(self, admin=None, verify=None):
        """
        Only gives the concern device groups
        """
        admin = (
            f"<partial><admin><member>{admin}</member></admin></partial>"
            if admin
            else ""
        )
        cmd = f"<show><config><list><change-summary>{admin}</change-summary></list></config></show>"
        return self._op_request(cmd, verify=verify)

    def pending_changes(self, verify=None):
        """
        Result content is either 'yes' or 'no'
        """
        cmd = "<check><pending-changes></pending-changes></check>"
        return self._op_request(cmd, verify=verify)

    def candidate_config(self, verify=None):
        """
        Get the confirmation with pending changes
        """
        cmd = "<show><config><candidate></candidate></config></show>"
        return self._op_request(cmd, remove_blank_text=False, verify=verify)

    def running_config(self, verify=None):
        """
        Get the running configuration
        """
        cmd = "<show><config><running></running></config></show>"
        return self._op_request(cmd, remove_blank_text=False, verify=verify)

    def raw_get_jobs(self, job_id=None, verify=None):
        cmd = "<show><jobs>{}</jobs></show>".format(
            f"<id>{job_id}</id>" if job_id else "<all></all>",
        )
        return self._op_request(cmd, verify=verify)

    def raw_get_versions(self, verify=None):
        cmd = "<request><system><software><check></check></software></system></request>"
        return self.operation(cmd, verify=verify)

    def get_versions(self):
        res = self.raw_get_versions()
        return [
            types.SoftwareVersion.from_xml(entry)
            for entry in res.xpath(".//sw-updates/versions/entry")
        ]

    def get_jobs(self, job_id=None, verify=None):
        job_xmls = self.raw_get_jobs(job_id, verify=verify).xpath(".//job")
        res = [types.Job.from_xml(x) for x in job_xmls]
        if job_id:  # We want one specific ID
            return res[0]
        return res

    def wait_job_completion(self, job_id, waiter=None):
        if not waiter:
            waiter = wait()
        for _ in waiter:
            job = self.get_jobs(job_id)
            if job.progress >= 100:
                return job
            self.logger.info(f"Job {job_id} progress: {job.progress}")
        raise Exception("Timeout while waiting for job completion")

    def get_pending_jobs(self, verify=None):
        cmd = "<show><jobs><pending></pending></jobs></show>"
        return self._op_request(cmd, verify=verify)

    def commit_changes(self, force=False, verify=None):
        # force = "<force></force>"  # We don't want to support force option
        cmd = "<commit>{}</commit>".format("<force></force>" if force else "")
        return self._commit_request(cmd, verify=verify)

    def _lock_cmd(self, cmd, vsys, no_exception=False, verify=None):
        try:
            result = "".join(self._op_request(cmd, vsys=vsys, verify=verify).itertext())
            self.logger.debug(result)
        except Exception as e:
            if no_exception:
                self.logger.error(e)
                return False
            raise
        return True

    # https://github.com/PaloAltoNetworks/pan-os-python/blob/a6b018e3864ff313fed36c3804394e2c92ca87b3/panos/base.py#L4459
    def add_config_lock(
        self, comment=None, vsys="shared", no_exception=False, verify=None
    ):
        comment = f"<comment>{comment}</comment>" if comment else ""
        cmd = f"<request><config-lock><add>{comment}</add></config-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def remove_config_lock(self, vsys="shared", no_exception=False, verify=None):
        cmd = "<request><config-lock><remove></remove></config-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def add_commit_lock(
        self, comment=None, vsys="shared", no_exception=False, verify=None
    ):
        comment = f"<comment>{comment}</comment>" if comment else ""
        cmd = f"<request><commit-lock><add>{comment}</add></commit-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def remove_commit_lock(self, vsys="shared", no_exception=False, verify=None):
        cmd = "<request><commit-lock><remove></remove></commit-lock></request>"
        return self._lock_cmd(cmd, vsys=vsys, no_exception=no_exception, verify=verify)

    def get_panorama_status(self, verify=None):
        cmd = "<show><panorama-status></panorama-status></show>"
        return self.operation(cmd, verify=verify).xpath(".//result")

    def raw_get_devices(self, connected=False, verify=None):
        # This only works on Panorama, not the FW
        filter = "<connected></connected>" if connected else "<all></all>"
        cmd = f"<show><devices>{filter}</devices></show>"
        return self.operation(cmd, verify=verify)

    def get_devices(self, connected=False, verify=None):
        entries = self.raw_get_devices(connected=connected, verify=verify).xpath(
            ".//devices/entry"
        )
        return [types.Device.from_xml(e) for e in entries]

    def raw_get_dg_hierarchy(self, verify=None):
        cmd = "<show><dg-hierarchy></dg-hierarchy></show>"
        return self.operation(cmd, verify=verify)

    def get_plan_dg_hierarchy(self, recursive=False, verify=None):
        devicegroups = {}  # name: children
        hierarchy = self.raw_get_dg_hierarchy(verify=verify).xpath(".//dg-hierarchy")[0]
        xpath = ".//dg" if recursive else "./dg"
        for dg in hierarchy.xpath(".//dg"):
            devicegroups[dg.attrib["name"]] = [
                x.attrib["name"] for x in dg.xpath(xpath)
            ]
        return devicegroups

    def raw_get_devicegroups(self, verify=None):
        cmd = "<show><devicegroups></devicegroups></show>"
        return self.operation(cmd, verify=verify)

    def get_devicegroups_name(
        self, parents=None, with_connected_devices=None, verify=None
    ):
        """
        This returns the names of the devicegroups:
        - parents: the returned list will only contain children of the provided parents (parents included)
        - with_devices: the returned list will only contain devicegroups that have direct devices under them
        """
        devicegroups = self.raw_get_devicegroups(verify=verify).xpath(
            ".//devicegroups/entry"
        )
        if with_connected_devices:
            names = [
                dg.attrib["name"]
                for dg in devicegroups
                if dg.xpath("./devices/entry/connected[text() = 'yes']")
            ]
        else:
            names = [dg.attrib["name"] for dg in devicegroups]
        if parents:
            hierarchy = self.get_plan_dg_hierarchy(recursive=True)
            tokeep = set(chain(*(hierarchy.get(p, []) for p in parents))) | set(parents)
            names = list(set(names) & tokeep)
        return names

    def raw_get_templates(self, name=None, verify=None):
        # This only works on Panorama, not the FW
        filter = f"<name>{name}</name>" if name else ""
        cmd = f"<show><templates>{filter}</templates></show>"
        return self.operation(cmd, verify=verify)

    def get_templates_sync_status(self, verify=None):
        res = self.raw_get_templates(verify=verify)
        for entry in res.xpath("./result/templates/entry"):
            template_name = entry.attrib["name"]
            for device in entry.xpath("./devices/entry"):
                device_name = device.attrib["name"]
                template_status = next(device.xpath("./template-status/text()"), None)
                yield (template_name, device_name, template_status)

    def raw_get_vpn_flows(self, name=None, verify=None):
        # This only works on Panorama, not the FW"
        filter = f"<name>{name}</name>" if name else "<all></all>"
        cmd = f"<show><vpn><flow>{filter}</flow></vpn></show>"
        return self.operation(cmd, verify=verify)

    def get_vpn_flows(self, name=None, verify=None):
        entries = self.raw_get_vpn_flows(name=name, verify=verify).xpath(
            ".//IPSec/entry"
        )
        return [types.VPNFlow.from_xml(e) for e in entries]

    def system_info(self, verify=None):
        cmd = "<show><system><info></info></system></show>"
        return self.operation(cmd, verify=verify)

    def raw_system_resources(self, verify=None):
        cmd = "<show><system><resources></resources></system></show>"
        return self.operation(cmd, verify=verify)

    def system_resources(self, verify=None):
        res = self.raw_system_resources(verify=verify)
        text = res.xpath(".//result/text()")[0]
        return text.split("\n\n")[0]

    def raw_download_software(self, version, verify=None):
        """
        version is the software version to download
        """
        cmd = f"<request><system><software><download><version>{version}</version></download></software></system></request>"
        return self.operation(cmd, verify=verify)

    def download_software(self, version, verify=None):
        """
        version is the software version to download
        """
        res = self.raw_download_software(version, verify=verify)
        try:
            return res.xpath(".//job/text()")[0]
        except Exception:
            self.logger.debug("Download has not started")
        return None

    def raw_install_software(self, version, verify=None):
        """
        version is the software version to install
        """
        cmd = f"<request><system><software><install><version>{version}</version></install></software></system></request>"
        return self.operation(cmd, verify=verify)

    def install_software(self, version, verify=None):
        """
        version is the software version to install
        """
        if isinstance(version, types.SoftwareVersion):
            version = version.version
        res = self.raw_install_software(version, verify=verify)
        try:
            return res.xpath(".//job/text()")[0]
        except Exception:
            self.logger.debug("Download has not started")
        return None

    def raw_restart(self, verify=None):
        cmd = "<request><restart><system></system></restart></request>"
        return self.operation(cmd, verify=verify)

    def restart(self, verify=None):
        return "".join(self.raw_restart(verify=verify).xpath(".//result/text()"))

    def automatic_download_software(self, version: Optional[str] = None):
        version_str = version
        versions = self.get_versions()
        if not version_str:
            version = next((v for v in versions if v.latest), None)
        else:
            version = next((v for v in versions if v.version == version_str), None)
        if not version:
            self.logger.error(f"Version {version_str} not found")
            return exit(1)

        # Already downloaded: Nothing to do
        if version.downloaded:
            self.logger.info(f"Version {version.version} already downloaded")
            return version

        # Download minor version first (required)
        base_version = next(
            (v for v in versions if v.version == version.base_minor_version), None
        )
        if not base_version.downloaded:
            self.logger.info(
                f"Launching download of minor version {base_version.version}"
            )
            job_id = self.download_software(base_version.version)
            if not job_id:
                raise Exception("Download has not started")
            job = self.wait_job_completion(job_id)
            if job.result != "OK":
                self.logger.debug(job)
                raise Exception(job.details)
            print(job.details)

        # Actually download the wanted version
        self.logger.info(f"Launching download of version {version.version}")
        job_id = self.download_software(version.version)
        if not job_id:
            raise Exception("Download has not started")
        job = self.wait_job_completion(job_id)
        if job.result != "OK":
            self.logger.debug(job)
            raise Exception(job.details)
        self.logger.info(job.details)
        return version

    def automatic_software_upgrade(
        self, version: Optional[str] = None, install=True, restart=True
    ):
        version = self.automatic_download_software(version)
        if version.current:
            self.logger.info(f"Version {version.version} is already installed")
            return version
        if not install:
            return version
        # We may get the following error:
        # "Error: Upgrading from 10.2.4-h10 to 11.1.2 requires a content version of 8761 or greater and found 8638-7689."
        # This should never happen, we decided to report the error and handle this manually
        self.logger.info(f"Launching install of version {version.version}")

        job_id = self.install_software(version.version)
        if not job_id:
            self.logger.error("Install has not started")
            exit(1)
        job = self.wait_job_completion(job_id)
        self.logger.info(job.details)

        if restart:
            self.logger.info("Restarting the device")
            restart_response = self.restart()
            self.logger.info(restart_response)
        return version
