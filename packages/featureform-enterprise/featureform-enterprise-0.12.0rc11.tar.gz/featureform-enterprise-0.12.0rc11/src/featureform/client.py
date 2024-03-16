import featureform.resources
from typing import Union, Optional
from datetime import datetime
from typing import Union, List, Optional

import pandas as pd
from featureform.proto import metadata_pb2 as pb
from google.protobuf.timestamp_pb2 import Timestamp
from typeguard import typechecked

from .constants import NO_RECORD_LIMIT
from .register import (
    ResourceClient,
    SourceRegistrar,
    SubscriptableTransformation,
    FeatureColumnResource,
    register_user,
)
from .serving import ServingClient
from .enums import ResourceType
from .lib import auth


class Client(ResourceClient, ServingClient):
    """
    Client for interacting with Featureform APIs (resources and serving)

    **Using the Client:**
    ```py title="definitions.py"
    import featureform as ff
    from featureform import Client

    client = Client()

    # Example 1: Get a registered provider
    redis = client.get_provider("redis-quickstart")

    # Example 2: Compute a dataframe from a registered source
    transactions_df = client.dataframe("transactions", "quickstart")
    ```
    """

    def __init__(
        self,
        host=None,
        local=False,
        insecure=False,
        cert_path=None,
        dry_run=False,
        debug=False,
    ):
        if local:
            raise Exception(
                "Local mode is not supported in this version. Use featureform <= 1.12.0 for localmode"
            )

        if host is not None:
            self._validate_host(host)

        ResourceClient.__init__(
            self,
            host=host,
            local=local,
            insecure=insecure,
            cert_path=cert_path,
            dry_run=dry_run,
            debug=debug,
        )
        ServingClient.__init__(
            self,
            host=host,
            local=local,
            insecure=insecure,
            cert_path=cert_path,
            debug=debug,
        )

        if not dry_run:
            # We configure authentication here to ensure the default owner is set prior to any calls to apply.
            # If authentication is enabled, the default owner will be set to the authenticated user; otherwise,
            # it is set to "default_owner".
            auth_config = self.get_auth_config()
            subject = auth.singleton.get_subject(auth_config, insecure, host)
        else:
            subject = "default_owner"
        register_user(subject).make_default_owner()

    def dataframe(
        self,
        source: Union[SourceRegistrar, SubscriptableTransformation, str],
        variant: Optional[str] = None,
        limit=NO_RECORD_LIMIT,
        asynchronous=False,
        verbose=False,
    ):
        """
        Return a dataframe from a registered source or transformation

        **Example:**
        ```py title="definitions.py"
        transactions_df = client.dataframe("transactions", "quickstart")

        avg_user_transaction_df = transactions_df.groupby("CustomerID")["TransactionAmount"].mean()
        ```

        Args:
            source (Union[SourceRegistrar, SubscriptableTransformation, str]): The source or transformation to compute the dataframe from
            variant (str): The source variant; can't be None if source is a string
            limit (int): The maximum number of records to return; defaults to NO_RECORD_LIMIT
            asynchronous (bool): Flag to determine whether the client should wait for resources to be in either a READY or FAILED state before returning. Defaults to False to ensure that newly registered resources are in a READY state prior to serving them as dataframes.

        Returns:
            df (pandas.DataFrame): The dataframe computed from the source or transformation

        """
        self.apply(asynchronous=asynchronous, verbose=verbose)
        if isinstance(source, (SourceRegistrar, SubscriptableTransformation)):
            name, variant = source.name_variant()
        elif isinstance(source, str):
            name = source
            if variant is None:
                raise ValueError("variant must be specified if source is a string")
            if variant == "":
                raise ValueError("variant cannot be an empty string")
        else:
            raise ValueError(
                f"source must be of type SourceRegistrar, SubscriptableTransformation or str, not {type(source)}\n"
                "use client.dataframe(name, variant) or client.dataframe(source) or client.dataframe(transformation)"
            )
        return self.impl._get_source_as_df(name, variant, limit)

    def nearest(self, feature, vector, k):
        """
        Query the K nearest neighbors of a provider vector in the index of a registered feature variant

        **Example:**

        ```py title="definitions.py"
        # Get the 5 nearest neighbors of the vector [0.1, 0.2, 0.3] in the index of the feature "my_feature" with variant "my_variant"
        nearest_neighbors = client.nearest("my_feature", "my_variant", [0.1, 0.2, 0.3], 5)
        print(nearest_neighbors) # prints a list of entities (e.g. ["entity1", "entity2", "entity3", "entity4", "entity5"])
        ```

        Args:
            feature (Union[FeatureColumnResource, tuple(str, str)]): Feature object or tuple of Feature name and variant
            vector (List[float]): Query vector
            k (int): Number of nearest neighbors to return

        """
        if isinstance(feature, tuple):
            name, variant = feature
        elif isinstance(feature, FeatureColumnResource):
            name = feature.name
            variant = feature.variant
        else:
            raise Exception(
                f"the feature '{feature}' of type '{type(feature)}' is not support."
                "Feature must be a tuple of (name, variant) or a FeatureColumnResource"
            )

        if k < 1:
            raise ValueError(f"k must be a positive integer")
        return self.impl._nearest(name, variant, vector, k)

    @typechecked
    def write_feature(
        self,
        name_variant: tuple,
        entity: str,
        value: Union[str, int, float, bool, List[float]],
    ):
        name, variant = name_variant

        ts = Timestamp()
        # consider allowing user to pass in timestamp
        ts.GetCurrentTime()

        feature = pb.StreamingFeatureVariant(
            name=name,
            variant=variant,
            entity=entity,
            value=str(value),
            ts=ts,
        )

        features = iter([feature])
        # TODO: add retry logic
        self._stub.WriteFeatures(features)

    @typechecked
    def write_label(
        self,
        name_variant: tuple,
        entity: str,
        value: Union[str, int, float, bool, List[float]],
        timestamp: Optional[datetime] = None,
    ):
        name, variant = name_variant

        ts = Timestamp()
        if timestamp is None:
            ts.GetCurrentTime()
        else:
            ts.FromDatetime(timestamp)

        label = pb.StreamingLabelVariant(
            name=name,
            variant=variant,
            entity=entity,
            value=str(value),
            ts=ts,
        )

        labels = iter([label])
        self._stub.WriteLabels(labels)

    def location(
        self,
        source: Union[SourceRegistrar, SubscriptableTransformation, str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
    ):
        """
        Returns the location of a registered resource. For SQL resources, it will return the table name
        and for file resources, it will return the file path.

        **Example:**
        ```py title="definitions.py"
        transaction_location = client.location("transactions", "quickstart", ff.SOURCE)
        ```

        Args:
            source (Union[SourceRegistrar, SubscriptableTransformation, str]): The source or transformation to compute the dataframe from
            variant (str): The source variant; can't be None if source is a string
            resource_type (ResourceType): The type of resource; can be one of ff.SOURCE, ff.FEATURE, ff.LABEL, or ff.TRAINING_SET
        """
        if isinstance(source, (SourceRegistrar, SubscriptableTransformation)):
            name, variant = source.name_variant()
            resource_type = ResourceType.SOURCE
        elif isinstance(source, featureform.resources.TrainingSetVariant):
            name = source.name
            variant = source.variant
            resource_type = ResourceType.TRAINING_SET
        elif isinstance(source, str):
            name = source
            if variant is None:
                raise ValueError("variant must be specified if source is a string")
            if variant == "":
                raise ValueError("variant cannot be an empty string")

            if resource_type is None:
                raise ValueError(
                    "resource_type must be specified if source is a string"
                )

        else:
            raise ValueError(
                f"source must be of type SourceRegistrar, SubscriptableTransformation or str, not {type(resource)}\n"
                "use client.dataframe(name, variant) or client.dataframe(source) or client.dataframe(transformation)"
            )

        location = self.impl.location(name, variant, resource_type)
        return location

    def close(self):
        """
        Closes the client, closes channel for hosted mode
        """
        self.impl.close()

    def columns(
        self,
        source: Union[SourceRegistrar, SubscriptableTransformation, str],
        variant: Optional[str] = None,
    ):
        """
        Returns the columns of a registered source or transformation

        **Example:**
        ```py title="definitions.py"
        columns = client.columns("transactions", "quickstart")
        ```

        Args:
            source (Union[SourceRegistrar, SubscriptableTransformation, str]): The source or transformation to get the columns from
            variant (str): The source variant; can't be None if source is a string

        Returns:
            columns (List[str]): The columns of the source or transformation
        """
        if isinstance(source, (SourceRegistrar, SubscriptableTransformation)):
            name, variant = source.name_variant()
        elif isinstance(source, str):
            name = source
            if variant is None:
                raise ValueError("variant must be specified if source is a string")
            if variant == "":
                raise ValueError("variant cannot be an empty string")
        else:
            raise ValueError(
                f"source must be of type SourceRegistrar, SubscriptableTransformation or str, not {type(source)}\n"
                "use client.columns(name, variant) or client.columns(source) or client.columns(transformation)"
            )
        return self.impl._get_source_columns(name, variant)

    @staticmethod
    def _validate_host(host):
        if host.startswith("http://") or host.startswith("https://"):
            raise ValueError("Invalid Host: Host should not contain http or https.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
