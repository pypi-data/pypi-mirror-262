import logging

# © Copyright Databand.ai, an IBM Company 2022
from typing import Dict, List, Optional

from airflow_monitor.data_fetcher.plugin_metadata import get_plugin_metadata
from airflow_monitor.shared.adapter.adapter import Adapter, Assets, ThirdPartyInfo


logger = logging.getLogger(__name__)


class AirflowAdapter(Adapter):
    def init_cursor(self) -> str:
        raise NotImplementedError()

    def init_assets_for_cursor(
        self, cursor: str, batch_size: int, next_page: str
    ) -> Assets:
        raise NotImplementedError()

    def get_assets_data(self, to_update: List[str]) -> Dict[str, object]:
        raise NotImplementedError()

    def get_third_party_info(self) -> Optional[ThirdPartyInfo]:
        metadata = get_plugin_metadata()
        metadata_dict = metadata.as_safe_dict() if metadata else {}

        from airflow_monitor.adapter.validations import (
            get_all_errors,
            get_tracking_validation_steps,
        )

        errors_list = get_all_errors(get_tracking_validation_steps())

        return ThirdPartyInfo(metadata=metadata_dict, error_list=errors_list)
