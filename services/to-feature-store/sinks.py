import hopsworks
import pandas as pd
from quixstreams.sinks.base import BatchingSink, SinkBackpressureError, SinkBatch
from datetime import datetime, timezone
from loguru import logger


class HopsworksFeatureStoreSink(BatchingSink):
    """
    Some sink writing data to a database
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_event_time: str,
        feature_group_candle_seconds: int,
        feature_group_materialization_interval_minutes: int,
    ):
        """
        Stablish connection to the Hopsworks Feature Store
        """
        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version
        self.candle_seconds = feature_group_candle_seconds
        self.materialization_interval_minutes = (
            feature_group_materialization_interval_minutes
        )
        # Establish connection to the Hopsworks Feature Store
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()

        # Get the feature group
        self._feature_group = self._fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
        )

        # set the materialization interval
        try:
            self._feature_group.materialization_job.schedule(
                cron_expression=f"0 0/{self.materialization_interval_minutes} * ? * * *",
                start_time=datetime.now(tz=timezone.utc),
            )
        # TODO: handle the FeatureStoreException
        except Exception as e:
            logger.error(f"Failed to schedule materialization job: {e}")

        # Call constructor of the parent class to make sure the batches are initialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Transform the data to a pandas DataFrame
        data = [item.value for item in batch]
        data = pd.DataFrame(data)

        breakpoint()

        try:
            # Try to write data to the db
            self._feature_group.insert(data)
        except Exception as err:  # capture the error
            # In case of timeout, tell the app to wait for 30s
            # and retry the writing later

            breakpoint()

            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err  # Chain the error to the exception
