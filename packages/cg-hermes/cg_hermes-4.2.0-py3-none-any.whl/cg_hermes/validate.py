"""Code for validating files from different sources."""
import logging
from typing import FrozenSet

from cg_hermes.config.tags import COMMON_TAG_CATEGORIES
from cg_hermes.config.workflows import AnalysisType
from cg_hermes.constants.workflow import Workflow
from cg_hermes.deliverables import Deliverables
from cg_hermes.models.tags import TagMap

LOG = logging.getLogger(__name__)


def get_deliverables_obj(
    deliverables: dict[str, list[dict[str, str]]],
    workflow: Workflow,
    analysis_type: AnalysisType | None = None,
) -> Deliverables:
    if Workflow.BALSAMIC in workflow and not analysis_type:
        LOG.error(f"Please specify analysis type for {workflow}")
        raise SyntaxError
    return Deliverables(deliverables=deliverables, workflow=workflow, analysis_type=analysis_type)


def validate_common_tags() -> bool:
    """Validate the common tags"""
    for category in COMMON_TAG_CATEGORIES:
        tag_map: dict[str, dict[str, str]] = COMMON_TAG_CATEGORIES[category]
        for tag_name, value in tag_map.items():
            try:
                assert isinstance(tag_map[tag_name], dict)
            except AssertionError as err:
                LOG.warning("Tag %s in %s is on the wrong format", tag_name, category.upper())
                raise err
            try:
                assert "description" in value
            except AssertionError as err:
                LOG.warning("Tag %s in %s does not have a description", tag_name, category.upper())
                raise err
    return True


def validate_tag_map(tag_map: dict[FrozenSet[str], dict]) -> bool:
    """Validate if a tag map is on the correct format."""
    for workflow_tags, value in tag_map.items():
        assert isinstance(workflow_tags, frozenset)
        TagMap.validate(value)
    return True
