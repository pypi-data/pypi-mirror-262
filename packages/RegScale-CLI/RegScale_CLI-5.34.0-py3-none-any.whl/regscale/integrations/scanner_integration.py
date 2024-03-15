#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Scanner Integration Class """

import concurrent.futures
import dataclasses
import enum
import logging
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Optional, Any, Iterator, Union

from rich.progress import Progress, TaskID

from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.utils.app_utils import (
    get_current_datetime,
    create_progress_object,
)
from regscale.core.utils.date import date_str, days_from_today
from regscale.models import regscale_models

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class IntegrationAsset:
    """
    Dataclass for integration assets.

    Represents an asset to be integrated, including its metadata and associated components.
    If a component does not exist, it will be created based on the names provided in ``component_names``.

    :param name: The name of the asset.
    :param identifier: A unique identifier for the asset.
    :param asset_type: The type of the asset.
    :param asset_category: The category of the asset.
    :param component_type: The type of the component, defaults to ``ComponentType.Hardware``.
    :param parent_id: The ID of the parent asset, defaults to None.
    :param parent_module: The module of the parent asset, defaults to None.
    :param status: The status of the asset, defaults to "Active (On Network)".
    :param date_last_updated: The last update date of the asset, defaults to the current datetime.
    :param asset_owner_id: The ID of the asset owner, defaults to None.
    :param mac_address: The MAC address of the asset, defaults to None.
    :param fqdn: The Fully Qualified Domain Name of the asset, defaults to None.
    :param ip_address: The IP address of the asset, defaults to None.
    :param component_names: A list of strings that represent the names of the components associated with the asset,
    components will be created if they do not exist.
    """

    name: str
    identifier: str
    asset_type: str
    asset_category: str
    component_type: str = regscale_models.ComponentType.Hardware
    parent_id: Optional[int] = None
    parent_module: Optional[str] = None
    status: str = "Active (On Network)"
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    asset_owner_id: Optional[str] = None
    mac_address: Optional[str] = None
    fqdn: Optional[str] = None
    ip_address: Optional[str] = None
    component_names: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class IntegrationFinding:
    """
    Dataclass for integration findings.

    :param control_ids: A list of control IDs associated with the finding.
    :param title: The title of the finding.
    :param category: The category of the finding.
    :param severity: The severity of the finding, based on regscale_models.IssueSeverity.
    :param description: A description of the finding.
    :param status: The status of the finding, based on regscale_models.ControlTestResultStatus.
    :param priority: The priority of the finding, defaults to "Medium".
    :param issue_title: The title of the issue, defaults to an empty string.
    :param issue_type: The type of issue, defaults to "Risk".
    :param date_created: The creation date of the finding, defaults to the current datetime.
    :param date_last_updated: The last update date of the finding, defaults to the current datetime.
    :param external_id: An external identifier for the finding, defaults to an empty string.
    :param gaps: A description of any gaps identified, defaults to an empty string.
    :param observations: Observations related to the finding, defaults to an empty string.
    :param evidence: Evidence supporting the finding, defaults to an empty string.
    :param identified_risk: The risk identified by the finding, defaults to an empty string.
    :param impact: The impact of the finding, defaults to an empty string.
    :param recommendation_for_mitigation: Recommendations for mitigating the finding, defaults to an empty string.
    """

    control_ids: List[int]
    title: str
    category: str
    severity: regscale_models.IssueSeverity
    description: str
    status: Union[
        regscale_models.ControlTestResultStatus, regscale_models.ChecklistStatus
    ]
    priority: str = "Medium"

    # Issues
    issue_title: str = ""
    issue_type: str = "Risk"
    date_created: str = dataclasses.field(default_factory=get_current_datetime)
    date_last_updated: str = dataclasses.field(default_factory=get_current_datetime)
    external_id: str = ""
    gaps: str = ""
    observations: str = ""
    evidence: str = ""
    identified_risk: str = ""
    impact: str = ""
    recommendation_for_mitigation: str = ""
    asset_identifier: str = ""
    cci_ref: Optional[str] = None
    rule_id: str = ""
    results: str = ""
    comments: Optional[str] = None


class ScannerIntegrationType(str, enum.Enum):
    """
    Enumeration for scanner integration types.
    """

    CHECKLIST = "checklist"
    CONTROL_TEST = "control_test"


class ScannerIntegration(ABC):
    """
    Abstract class for scanner integrations.

    :param int plan_id: The ID of the security plan
    """

    type = ScannerIntegrationType.CONTROL_TEST
    title = "Scanner Integration"
    asset_identifier_field = ""
    component_map: dict[Any, Any] = {}
    components: list[Any] = []
    asset_map: dict[Any, Any] = {}
    asset_progress: Progress
    finding_progress: Progress
    num_assets_to_process: Optional[int] = None
    num_findings_to_process: Optional[int] = None
    asset_map_by_identifier: dict[str, regscale_models.Asset] = {}
    existing_issues_map: dict[int, List[regscale_models.Issue]] = defaultdict(list)
    checklist_asset_map: dict[int, List[regscale_models.Checklist]] = defaultdict(list)
    finding_status_map: dict[Any, regscale_models.ChecklistStatus] = {}
    finding_severity_map: dict[Any, regscale_models.IssueSeverity] = {}
    errors: List[str] = []

    # Locks
    checklist_asset_map_lock = threading.Lock()
    existing_issues_map_lock = threading.Lock()

    def __init__(self, plan_id):
        """
        Initializes the scanner integration

        :param int plan_id: The ID of the security plan
        """
        self.plan_id = plan_id
        self.control_implementation_map = (
            regscale_models.ControlImplementation.get_control_map_by_plan(
                plan_id=plan_id
            )
        )
        self.control_map = {v: k for k, v in self.control_implementation_map.items()}
        self.assessment_map = {}
        self.assessor_id = self.get_assessor_id()
        self.asset_progress = create_progress_object()
        self.finding_progress = create_progress_object()
        self.asset_map_by_identifier = regscale_models.Asset.get_map(
            plan_id=self.plan_id, key_field=self.asset_identifier_field
        )

    @staticmethod
    def get_assessor_id() -> str:
        """
        Gets the ID of the assessor

        :return: The ID of the assessor
        :rtype: str
        """

        api_handler = APIHandler()
        return api_handler.get_user_id()

    @abstractmethod
    def fetch_findings(self, *args, **kwargs) -> List[IntegrationFinding]:
        """
        Fetches findings from the integration

        :return: A list of findings
        :rtype: List[IntegrationFinding]
        """
        pass

    @abstractmethod
    def fetch_assets(self, *args, **kwargs) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from the integration

        :return: A list of assets
        :rtype: List[IntegrationAsset]
        """
        pass

    def get_finding_status(
        self, status: Optional[str]
    ) -> regscale_models.ChecklistStatus:
        """
        Gets the RegScale checklist status based on the integration finding status

        :param Optional[str] status: The status of the finding
        :return: The RegScale checklist status
        :rtype: regscale_models.ChecklistStatus
        """
        return self.finding_status_map.get(
            status, regscale_models.ChecklistStatus.NOT_REVIEWED
        )

    def get_finding_severity(
        self, severity: Optional[str]
    ) -> regscale_models.IssueSeverity:
        """
        Gets the RegScale issue severity based on the integration finding severity

        :param Optional[str] severity: The severity of the finding
        :return: The RegScale issue severity
        :rtype: regscale_models.IssueSeverity
        """
        return self.finding_severity_map.get(
            severity, regscale_models.IssueSeverity.NotAssigned
        )

    def get_or_create_assessment(
        self, control_implementation_id: int
    ) -> regscale_models.Assessment:
        """
        Gets or creates a RegScale assessment

        :param int control_implementation_id: The ID of the control implementation
        :return: The assessment
        :rtype: regscale_models.Assessment
        """
        logger.info(
            f"Getting or creating assessment for control implementation {control_implementation_id}"
        )
        assessment: Optional[regscale_models.Assessment] = self.assessment_map.get(
            control_implementation_id
        )
        if assessment:
            logger.debug(
                f"Found cached assessment {assessment.id} for control implementation {control_implementation_id}"
            )
        else:
            logger.debug(
                f"Assessment not found for control implementation {control_implementation_id}"
            )
            assessment = regscale_models.Assessment(
                plannedStart=get_current_datetime(),
                plannedFinish=get_current_datetime(),
                status=regscale_models.AssessmentStatus.COMPLETE.value,
                assessmentResult=regscale_models.AssessmentResultsStatus.FAIL.value,
                actualFinish=get_current_datetime(),
                leadAssessorId=self.assessor_id,
                parentId=control_implementation_id,
                parentModule=regscale_models.ControlImplementation.get_module_string(),
                title=f"{self.title} Assessment",
                assessmentType=regscale_models.AssessmentType.QA_SURVEILLANCE.value,
            ).create()
        self.assessment_map[control_implementation_id] = assessment
        return assessment

    def create_issue_from_finding(
        self,
        title: str,
        parent_id: int,
        parent_module: str,
        finding: IntegrationFinding,
    ) -> regscale_models.Issue:
        """
        Creates a RegScale issue from a finding

        :param str title: The title of the issue
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :param IntegrationFinding finding: The finding data
        :return: The Issue create from the finding
        :rtype: regscale_models.Issue
        """
        issue_status = (
            regscale_models.IssueStatus.Closed
            if finding.status == regscale_models.ControlTestResultStatus.PASS
            else regscale_models.IssueStatus.Open
        )

        return regscale_models.Issue(
            parentId=parent_id,
            parentModule=parent_module,
            title=title,
            dateCreated=finding.date_created,
            status=issue_status,
            severityLevel=finding.severity,
            issueOwnerId=self.assessor_id,
            securityPlanId=self.plan_id,
            identification="Vulnerability Assessment",
            dateFirstDetected=finding.date_created,
            dueDate=date_str(days_from_today(30)),
            description=finding.description,
            sourceReport="STIG",
            recommendedActions=finding.recommendation_for_mitigation,
        ).create()

    @staticmethod
    def update_issues_from_finding(
        issue: regscale_models.Issue, finding: IntegrationFinding
    ) -> regscale_models.Issue:
        """
        Updates RegScale issues based on the integration findings

        :param regscale_models.Issue issue: The issue to update
        :param IntegrationFinding finding: The integration findings
        :return: The updated issue
        :rtype: regscale_models.Issue
        """
        issue_status = (
            regscale_models.IssueStatus.Closed
            if finding.status == regscale_models.ControlTestResultStatus.PASS
            else regscale_models.IssueStatus.Open
        )
        if issue.status != issue_status:
            issue.status = issue_status
            issue.severityLevel = finding.severity
            issue.dateLastUpdated = finding.date_last_updated
            issue.description = finding.description
            return issue.save()
        return issue

    def handle_passing_finding(
        self,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        parent_id: int,
        parent_module: str,
    ) -> None:
        """
        Handles findings that have passed by closing any open issues associated with the finding.

        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has passed
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :return: None
        """
        logger.info(f"Handling passing finding {finding.external_id} for {parent_id}")
        for issue in existing_issues:
            if (
                issue.identification == finding.external_id
                and issue.status != regscale_models.IssueStatus.Closed
            ):
                if (
                    parent_module
                    == regscale_models.ControlImplementation.get_module_string()
                ):
                    logger.info(
                        f"Closing issue {issue.id} for control {self.control_map[parent_id]}"
                    )
                else:
                    logger.info(f"Closing issue {issue.id} for asset {parent_id}")
                issue.status = regscale_models.IssueStatus.Closed
                issue.dateCompleted = finding.date_last_updated
                issue.save()

    def handle_failing_finding(
        self,
        issue_title: str,
        existing_issues: List[regscale_models.Issue],
        finding: IntegrationFinding,
        parent_id: int,
        parent_module: str,
    ) -> None:
        """
        Handles findings that have failed by updating an existing open issue or creating a new one.

        :param str issue_title: The title of the issue
        :param List[regscale_models.Issue] existing_issues: The list of existing issues to check against
        :param IntegrationFinding finding: The finding data that has failed
        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :return: None
        """
        # logger.info(f"Handling failing finding {finding.external_id} for {parent_id}")

        # Determine the parent type based on the parent module
        parent_type = (
            "control"
            if parent_module
            == regscale_models.ControlImplementation.get_module_string()
            else "asset"
        )
        # Attempt to find an existing open issue that matches the finding's external ID.
        if found_issue := next(
            (
                issue
                for issue in existing_issues
                if issue.identification == finding.external_id
                and issue.status != regscale_models.IssueStatus.Closed
            ),
            None,
        ):
            # If an existing open issue is found, update it with the new finding data.
            logger.info(
                f"Updating issue {found_issue.id} for {parent_type} {parent_id}"
            )
            self.update_issues_from_finding(issue=found_issue, finding=finding)
        else:
            # If no existing open issue is found, create a new one.
            logger.info(f"Creating issue for {parent_type} {parent_id}")
            self.create_issue_from_finding(
                title=issue_title,
                parent_id=parent_id,
                parent_module=parent_module,
                finding=finding,
            )

    def update_regscale_checklists(self, findings: List[IntegrationFinding]) -> None:
        """
        Process checklists from IntegrationFindings in a threaded manner.

        :param IntegrationFinding findings: The findings to process
        """
        logger.info("Updating RegScale checklists...")
        loading_findings = self.finding_progress.add_task(
            f"[#f8b737]Creating and updating checklists from {self.title}.",
        )
        progress_lock = threading.Lock()

        # Set concurrency to 3 to avoid overloading the API
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_finding = {
                executor.submit(self.process_checklist, finding): finding
                for finding in findings
            }
            for future in concurrent.futures.as_completed(future_to_finding):
                finding = future_to_finding[future]
                try:
                    # Accessing the result of the future will raise any exceptions that occurred
                    future.result()
                    with progress_lock:
                        # Wait until self.num_findings_to_process is set to set task total.
                        if self.num_findings_to_process and self.finding_progress.tasks[
                            loading_findings
                        ].total != float(self.num_findings_to_process):
                            self.finding_progress.update(
                                loading_findings,
                                total=self.num_findings_to_process,
                                description=f"[#f8b737]Creating and updating {self.num_findings_to_process} checklists from {self.title}.",
                            )
                        self.finding_progress.advance(loading_findings, 1)
                except Exception as exc:
                    self.log_error(
                        f"An error occurred when processing asset {finding.asset_identifier} "
                        f"for finding {finding.external_id}: {exc}"
                    )
        APIHandler().log_api_summary()

    def process_checklist(self, finding: IntegrationFinding) -> None:
        """
        Processes a single checklist item based on the provided finding.

        This method checks if the asset related to the finding exists, updates or creates a checklist item,
        and handles the finding based on its status (pass/fail).

        :param IntegrationFinding finding: The finding to process
        :return: None
        """
        logger.info(f"Processing checklist {finding.external_id}")
        asset = self.asset_map_by_identifier.get(finding.asset_identifier)
        if not asset:
            self.log_error(
                f"Asset not found for identifier {finding.asset_identifier}, skipping finding"
            )
            return

        asset_module_string = regscale_models.Asset.get_module_string()

        with self.checklist_asset_map_lock:
            # Clear the cache if it grows too large to prevent memory issues
            if len(self.checklist_asset_map) > 30:
                self.checklist_asset_map.clear()

            # Check if the asset's checklists are already in the cache
            if not (checklists := self.checklist_asset_map.get(asset.id)):
                # If not, fetch and cache the checklists
                self.checklist_asset_map[asset.id] = (
                    regscale_models.Checklist.get_all_by_parent(
                        parent_id=asset.id, parent_module=asset_module_string
                    )
                )
                # Now, checklists will always fetch from the cache, avoiding unnecessary database calls
                checklists = self.checklist_asset_map[asset.id]

        found_checklist = next(
            (
                checklist
                for checklist in checklists
                if checklist.vulnerabilityId == finding.external_id
                and checklist.tool == regscale_models.ChecklistTool.STIGs
            ),
            None,
        )

        if not found_checklist:
            regscale_models.Checklist(
                status=finding.status,
                assetId=asset.id,
                tool=regscale_models.ChecklistTool.STIGs,
                baseline="baseline",
                vulnerabilityId=finding.external_id,
                results=finding.results,
                check=finding.title,
                cci=finding.cci_ref,
                ruleId=finding.rule_id,
                version="Your version here",
                comments=finding.comments,
            ).create()
        else:
            found_checklist.status = finding.status
            found_checklist.results = finding.results
            found_checklist.comments = finding.comments
            found_checklist.save()

        with self.existing_issues_map_lock:
            # Check if the asset's issues are already in the cache
            if asset.id not in self.existing_issues_map:
                # If not, fetch and cache the issues
                self.existing_issues_map[asset.id] = (
                    regscale_models.Issue.get_all_by_parent(
                        parent_id=asset.id, parent_module=asset_module_string
                    )
                )
            # Now, existing_issues will always fetch from the cache, avoiding unnecessary database calls
            existing_issues = self.existing_issues_map[asset.id]

            # Optionally clear the cache if it grows too large
            if len(self.existing_issues_map) > 30:
                self.existing_issues_map.clear()

        if finding.status == regscale_models.ChecklistStatus.PASS:
            self.handle_passing_finding(
                existing_issues, finding, asset.id, asset_module_string
            )
        else:
            self.handle_failing_finding(
                issue_title=f"Vulnerability {finding.external_id} failed on {asset.fqdn}",
                existing_issues=existing_issues,
                finding=finding,
                parent_id=asset.id,
                parent_module=asset_module_string,
            )

    def update_regscale_findings(self, findings: List[IntegrationFinding]) -> None:
        """
        Updates RegScale findings based on the integration findings

        :param List[IntegrationFinding] findings: The integration findings
        :return: None
        """
        for finding in findings:
            if finding:
                for control_implementation_id in finding.control_ids:
                    assessment = self.get_or_create_assessment(
                        control_implementation_id
                    )
                    control_test = regscale_models.ControlTest(
                        uuid=finding.external_id,
                        parentControlId=control_implementation_id,
                        testCriteria=finding.description,
                    ).get_or_create()
                    regscale_models.ControlTestResult(
                        parentTestId=control_test.id,
                        parentAssessmentId=assessment.id,
                        uuid=finding.external_id,
                        result=finding.status,  # type: ignore
                        dateAssessed=finding.date_created,
                        assessedById=self.assessor_id,
                        gaps=finding.gaps,
                        observations=finding.observations,
                        evidence=finding.evidence,
                        identifiedRisk=finding.identified_risk,
                        impact=finding.impact,
                        recommendationForMitigation=finding.recommendation_for_mitigation,
                    ).create()
                    logger.info(
                        f"Created or Updated assessment {assessment.id} for control "
                        f"{self.control_map[control_implementation_id]}"
                    )
                    existing_issues: list[regscale_models.Issue] = (
                        regscale_models.Issue.get_all_by_parent(
                            parent_id=control_implementation_id,
                            parent_module=regscale_models.ControlImplementation.get_module_string(),
                        )
                    )
                    if finding.status == regscale_models.ControlTestResultStatus.PASS:
                        self.handle_passing_finding(
                            existing_issues=existing_issues,
                            finding=finding,
                            parent_id=control_implementation_id,
                            parent_module=regscale_models.ControlImplementation.get_module_string(),
                        )
                    else:
                        self.handle_failing_finding(
                            issue_title=f"Finding {finding.external_id} failed",
                            existing_issues=existing_issues,
                            finding=finding,
                            parent_id=control_implementation_id,
                            parent_module=regscale_models.ControlImplementation.get_module_string(),
                        )

    def get_components(self) -> List[regscale_models.Component]:
        """
        Get all components from the integration

        :return: A dictionary of components
        :rtype: dict
        """
        if any(self.components):
            return self.components
        self.components = regscale_models.Component.get_all_by_parent(
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_string(),
        )
        return self.components

    def get_component_by_title(self) -> dict:
        """
        Get all components from the integration

        :return: A dictionary of components
        :rtype: dict
        """
        return {component.title: component for component in self.get_components()}

    def set_asset_defaults(self, asset):
        """
        Set default values for the asset

        :param IntegrationAsset asset: The integration asset
        :return: The asset with which defaults should be set
        :rtype: IntegrationAsset
        """
        if not asset.asset_owner_id:
            asset.asset_owner_id = self.get_assessor_id()
        if not asset.status:
            asset.status = "Active (On Network)"
        return asset

    def update_regscale_assets(self, assets: Iterator[IntegrationAsset]) -> None:
        """
        Updates RegScale assets based on the integration assets

        :param Iterator[IntegrationAsset] assets: The integration assets
        :return: None
        """

        self.asset_map_by_identifier = regscale_models.Asset.get_map(
            plan_id=self.plan_id, key_field=self.asset_identifier_field
        )

        logger.info("Updating RegScale assets...")
        loading_assets = self.asset_progress.add_task(
            f"[#f8b737]Creating and updating assets from {self.title}.",
        )
        progress_lock = threading.Lock()
        # Look up Component by title
        components_by_title = self.get_component_by_title()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_asset = {
                executor.submit(
                    self.process_asset,
                    asset,
                    components_by_title,
                    loading_assets,
                    progress_lock,
                ): asset
                for asset in assets
            }
            for future in concurrent.futures.as_completed(future_to_asset):
                asset = future_to_asset[future]
                try:
                    future.result()
                except Exception as exc:
                    self.log_error(
                        f"An error occurred when processing asset {asset.name}: {exc}"
                    )

    def process_asset(
        self,
        asset: IntegrationAsset,
        components_by_title: dict,
        loading_assets: TaskID,
        progress_lock,
    ) -> None:
        """
        Processes an asset

        :param IntegrationAsset asset: The integration asset
        :param dict components_by_title: The components by title
        :param int loading_assets: The loading assets task
        :param threading.Lock progress_lock: The progress lock
        :return: None
        """

        asset = self.set_asset_defaults(asset)
        for component_name in asset.component_names:
            logger.info(f"Checking for existing assets under {component_name}...")
            if not (component := components_by_title.get(component_name)):
                component = regscale_models.Component(
                    title=component_name,
                    componentType=asset.component_type,
                    securityPlansId=self.plan_id,
                    description=component_name,
                    componentOwnerId=self.get_assessor_id(),
                ).create()
                self.components.append(component)
                if component.securityPlansId:
                    regscale_models.ComponentMapping(
                        componentId=component.id,
                        securityPlanId=component.securityPlansId,
                    ).get_or_create()
            components_by_title[component_name] = component
            existing_assets = self.asset_map.get(
                component.id
            ) or regscale_models.Asset.get_all_by_parent(
                parent_id=component.id,
                parent_module=regscale_models.Component.get_module_string(),
            )
            self.asset_map[component.id] = existing_assets
            self.update_or_create_asset(asset, component)
            with progress_lock:
                # Wait until self.num_assets_to_process is set to set task total.
                if self.num_assets_to_process and self.asset_progress.tasks[
                    loading_assets
                ].total != float(self.num_assets_to_process):
                    self.asset_progress.update(
                        loading_assets, total=self.num_assets_to_process
                    )
                self.asset_progress.advance(loading_assets, 1)

    def update_or_create_asset(
        self,
        asset: IntegrationAsset,
        component: regscale_models.Component,
    ) -> None:
        """
        Updates an existing asset or creates a new one

        :param IntegrationAsset asset: The integration asset
        :param regscale_models.Component component: The component
        :return: None
        """
        if existing_or_new_asset := self.find_existing_asset(asset):
            self.update_asset_if_needed(asset, existing_or_new_asset)
        else:
            existing_or_new_asset = self.create_new_asset(asset, component=component)

        # Create Asset Mapping
        regscale_models.AssetMapping(
            assetId=existing_or_new_asset.id,
            componentId=component.id,
        ).get_or_create()

    def find_existing_asset(
        self, asset: IntegrationAsset
    ) -> Optional[regscale_models.Asset]:
        """
        Finds an existing asset that matches the integration asset

        :param IntegrationAsset asset: The integration asset
        :return: The matching existing asset, or None if no match is found
        :rtype: Optional[regscale_models.Asset]
        """
        return self.asset_map_by_identifier.get(asset.identifier)

    @staticmethod
    def update_asset_if_needed(
        asset: IntegrationAsset, existing_asset: regscale_models.Asset
    ) -> None:
        """
        Updates an existing asset if any of its fields differ from the integration asset

        :param IntegrationAsset asset: The integration asset
        :param regscale_models.Asset existing_asset: The existing asset
        :return: None
        """
        is_updated = False
        if asset.asset_owner_id and existing_asset.assetOwnerId != asset.asset_owner_id:
            existing_asset.assetOwnerId = asset.asset_owner_id
            is_updated = True
        if asset.parent_id and existing_asset.parentId != asset.parent_id:
            existing_asset.parentId = asset.parent_id
            is_updated = True
        if asset.parent_module and existing_asset.parentModule != asset.parent_module:
            existing_asset.parentModule = asset.parent_module
            is_updated = True
        if existing_asset.assetType != asset.asset_type:
            existing_asset.assetType = asset.asset_type
            is_updated = True
        if existing_asset.status != asset.status:
            existing_asset.status = asset.status
            is_updated = True
        if existing_asset.assetCategory != asset.asset_category:
            existing_asset.assetCategory = asset.asset_category
            is_updated = True

        if is_updated:
            existing_asset.dateLastUpdated = asset.date_last_updated
            existing_asset.save()
            logger.info(f"Updated asset {asset.identifier}")
        else:
            logger.info(f"Asset {asset.identifier} is already up to date")

    def create_new_asset(
        self, asset: IntegrationAsset, component: regscale_models.Component
    ) -> regscale_models.Asset:
        """
        Creates a new asset based on the integration asset

        :param IntegrationAsset asset: The integration asset
        :param regscale_models.Component component: The component
        :return: None
        """
        new_asset = regscale_models.Asset(
            name=asset.name,
            assetOwnerId=asset.asset_owner_id or "Unknown",
            parentId=component.id,
            parentModule=regscale_models.Component.get_module_string(),
            assetType=asset.asset_type,
            dateLastUpdated=asset.date_last_updated,
            status=asset.status,
            assetCategory=asset.asset_category,
        )
        if self.asset_identifier_field:
            setattr(new_asset, self.asset_identifier_field, asset.identifier)
        new_asset = new_asset.create()
        self.asset_map_by_identifier[asset.identifier] = new_asset
        logger.info(f"Created asset {asset.identifier}")
        return new_asset

    def log_error(self, error: str, exc_info=True) -> None:
        """
        Logs an error along with the stack trace.

        :param str error: The error message
        :param bool exc_info: If True, includes the stack trace of the current exception in the log.
        :return: None
        """
        self.errors.append(error)
        logger.error(error, exc_info=exc_info)

    @classmethod
    def sync_findings(cls, plan_id: int, **kwargs) -> None:
        """
        Syncs findings from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :return: None
        """
        logger.info(f"Syncing {cls.title} findings...")
        instance = cls(plan_id)
        instance.finding_progress = create_progress_object()
        with instance.finding_progress:
            if cls.type == ScannerIntegrationType.CHECKLIST:
                instance.update_regscale_checklists(
                    findings=instance.fetch_findings(**kwargs)
                )
            else:
                instance.update_regscale_findings(
                    findings=instance.fetch_findings(**kwargs)
                )
            if instance.errors:
                logger.error("Summary of errors encountered:")
                for error in instance.errors:
                    logger.error(error)
            else:
                logger.info("All findings have been processed successfully.")

    @classmethod
    def sync_assets(cls, plan_id: int, **kwargs) -> None:
        """
        Syncs assets from the integration to RegScale

        :param int plan_id: The ID of the security plan
        :return: None
        """
        logger.info(f"Syncing {cls.title} assets...")
        instance = cls(plan_id)
        instance.asset_progress = create_progress_object()
        with instance.asset_progress:
            instance.update_regscale_assets(assets=instance.fetch_assets(**kwargs))

        if instance.errors:
            logger.error("Summary of errors encountered:")
            for error in instance.errors:
                logger.error(error)
        else:
            logger.info("All assets have been processed successfully.")
