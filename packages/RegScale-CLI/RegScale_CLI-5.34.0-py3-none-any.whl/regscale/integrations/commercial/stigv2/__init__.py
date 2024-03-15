#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale GCP Package """
from pathlib import Path
from typing import List, Iterator, Optional

import click

from regscale.integrations.commercial.stigv2.ckl_parser import (
    parse_checklist,
    get_all_components_from_checklists,
    get_all_assets_from_checklists,
    find_stig_files,
    Checklist,
    Vuln,
)
from regscale.integrations.scanner_integration import (
    logger,
    IntegrationFinding,
    ScannerIntegration,
    IntegrationAsset,
    ScannerIntegrationType,
)
from regscale.models import regscale_models
from regscale.models.regscale_models import AssetType


class StigIntegration(ScannerIntegration):
    title = "STIG Integration"
    asset_identifier_field = "fqdn"
    type = ScannerIntegrationType.CHECKLIST
    finding_status_map = {
        "NotAFinding": regscale_models.ChecklistStatus.PASS,
        "Open": regscale_models.ChecklistStatus.FAIL,
    }
    finding_severity_map = {
        "high": regscale_models.IssueSeverity.High,
        "medium": regscale_models.IssueSeverity.Moderate,
        "low": regscale_models.IssueSeverity.Low,
    }

    def fetch_findings(  # type: ignore
        self, path: Path
    ) -> Iterator[IntegrationFinding]:
        """
        Fetches GCP findings using the SecurityCenterClient

        :return: A list of parsed findings
        :rtype: List[IntegrationFinding]
        """

        logger.info("Fetching findings...")
        stig_files = find_stig_files(path)

        self.num_findings_to_process = 0
        for stig_file in stig_files:
            logger.info(f"Processing '{stig_file}'")
            checklist = parse_checklist(stig_file)
            logger.info(
                f"Found {len(checklist.stigs[0].vulns)} Vulnerabilities in '{stig_file}'"
            )
            for stig in checklist.stigs:
                for vuln in stig.vulns:
                    self.num_findings_to_process += 1
                    yield from self.process_vulnerabilities(checklist, vuln)

    def process_vulnerabilities(
        self, checklist: Checklist, vuln: Vuln
    ) -> Iterator[IntegrationFinding]:
        """
        Processes vulnerabilities for each asset in the checklist.

        Iterates through each asset in the provided checklist, extracts the asset identifier (host_fqdn),
        and yields an IntegrationFinding for each vulnerability associated with the asset.

        :param Checklist checklist: The checklist containing assets to process.
        :param Vuln vuln: The vulnerability information to be processed.
        :return: An iterator of IntegrationFinding objects.
        """
        for asset in checklist.assets:
            asset_identifier = getattr(asset, "host_fqdn", None)
            if not asset_identifier:
                self.log_error(
                    f"Failed to extract host_fqdn from Asset: {asset} and "
                    f"vuln from {vuln}"
                )
                continue

            yield self.create_integration_finding(asset_identifier, vuln)

    def create_integration_finding(
        self, asset_identifier: str, vuln: Vuln
    ) -> IntegrationFinding:
        """
        Creates an IntegrationFinding object from the provided asset identifier and vulnerability information.

        :param str asset_identifier: The identifier of the asset associated with the finding.
        :param Vuln vuln: The vulnerability information used to populate the finding.
        :return: An IntegrationFinding object populated with the provided information.
        """
        return IntegrationFinding(
            asset_identifier=asset_identifier,
            control_ids=[],  # Determine how to populate this
            title=vuln.rule_title,
            category=vuln.group_title,
            severity=self.get_finding_severity(vuln.severity),
            description=f"{vuln.check_content} {vuln.vuln_discuss} {vuln.fix_text}",
            status=self.get_finding_status(vuln.status),
            external_id=vuln.vuln_num,
            cci_ref=vuln.cci_ref,
            rule_id=vuln.rule_id,
            results=f"Vulnerability Number: {vuln.vuln_num}, Severity: {vuln.severity}, "
            f"Rule Title: {vuln.rule_title}<br><br>Check Content: {vuln.check_content}<br><br>"
            f"Fix Text: {vuln.fix_text}<br><br>STIG Reference: {vuln.stigref}<br><br>"
            f"Vulnerability Discussion: {vuln.vuln_discuss}",
            recommendation_for_mitigation=vuln.fix_text,
            comments=vuln.comments,
        )

    def fetch_assets(self, path: Optional[Path] = None) -> Iterator[IntegrationAsset]:
        """
        Fetches GCP assets using the AssetServiceClient

        :return: An iterator of parsed assets
        :rtype: Iterator[IntegrationAsset]
        """
        if not path:
            raise ValueError("Path to STIG files is required.")
        logger.info("Fetching assets...")
        stig_files = find_stig_files(path)

        self.num_assets_to_process = len(stig_files)

        loading_stig_files = self.asset_progress.add_task(
            f"[#f8b737]Loading {len(stig_files)} STIG files.",
            total=len(stig_files),
        )
        for stig_file in stig_files:
            logger.info(f"Processing '{stig_file}'")
            checklist = parse_checklist(stig_file)
            for stig_asset in checklist.assets:
                component_names = []
                for stig in checklist.stigs:
                    component_names.append(stig.component_title)

                if not stig_asset.host_name or not stig_asset.host_fqdn:
                    self.log_error(f"Failed to extract asset from {stig_asset}")
                    continue

                yield IntegrationAsset(
                    name=stig_asset.host_name,
                    identifier=stig_asset.host_fqdn,
                    asset_type=AssetType.Other,
                    asset_owner_id=self.assessor_id,
                    parent_id=self.plan_id,
                    parent_module=regscale_models.SecurityPlan.get_module_slug(),
                    asset_category="STIG",
                    component_names=component_names,
                    # TODO: Determine correct component type
                    component_type=regscale_models.ComponentType.Software,
                )
            self.asset_progress.update(loading_stig_files, advance=1)


@click.group()
def stigv2():
    """STIG Integrations"""


@stigv2.command(name="sync_findings")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "-d",
    "--stig_directory",
    type=click.Path(exists=True),
    help="The directory where STIG files are located",
    prompt="Enter STIG directory",
    required=True,
)
def sync_findings(regscale_ssp_id, stig_directory):
    """Sync GCP Findings to RegScale."""
    StigIntegration.sync_findings(plan_id=regscale_ssp_id, path=stig_directory)


@stigv2.command(name="sync_assets")
@click.option(
    "-p",
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "-d",
    "--stig_directory",
    type=click.Path(exists=True),
    help="The directory where STIG files are located",
    prompt="Enter STIG directory",
    required=True,
)
def sync_assets(regscale_ssp_id, stig_directory):
    """Sync GCP Assets to RegScale."""
    StigIntegration.sync_assets(plan_id=regscale_ssp_id, path=stig_directory)
