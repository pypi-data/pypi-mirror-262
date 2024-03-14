from abc import ABC, abstractmethod
import logging
import pathlib
import re
from typing import Dict, List, Optional, Tuple
import uuid

import requests

from anyscale.authenticate import AuthenticationBlock, get_auth_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi as InternalApi
from anyscale.client.openapi_client.models import (
    ArchiveStatus,
    CloudDataBucketFileType,
    CloudDataBucketPresignedUploadInfo,
    CloudDataBucketPresignedUploadRequest,
    ComputeTemplateConfig,
    ComputeTemplateQuery,
    CreateComputeTemplate,
    DecoratedComputeTemplate,
)
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as ExternalApi
from anyscale.sdk.anyscale_client.configuration import Configuration
from anyscale.sdk.anyscale_client.models import (
    ApplyServiceModel,
    Cloud,
    Cluster,
    ClusterCompute,
    ClusterComputeConfig,
    ClusterEnvironment,
    ClusterEnvironmentBuild,
    ClusterEnvironmentBuildStatus,
    Project,
    RollbackServiceModel,
    ServiceEventCurrentState,
    ServiceModel,
)
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
)
from anyscale.sdk.anyscale_client.models.create_cluster_environment_build import (
    CreateClusterEnvironmentBuild,
)
from anyscale.sdk.anyscale_client.rest import ApiException
from anyscale.util import (
    get_cluster_model_for_current_workspace,
    get_endpoint,
    is_anyscale_workspace,
)
from anyscale.utils.runtime_env import (
    is_workspace_dependency_tracking_disabled,
    WORKSPACE_REQUIREMENTS_FILE_PATH,
    zip_local_dir,
)
from anyscale.utils.workspace_notification import (
    WORKSPACE_NOTIFICATION_ADDRESS,
    WorkspaceNotification,
)


logger = logging.getLogger(__name__)

# TODO(edoakes): figure out a sane policy for this.
# Maybe just make it part of the release process to update it, or fetch the
# default builds and get the latest one. The best thing to do is probably
# to populate this in the backend.
DEFAULT_RAY_VERSION = "2.9.2"
DEFAULT_PYTHON_VERSION = "py310"
RUNTIME_ENV_PACKAGE_FORMAT = "pkg_{content_hash}.zip"

# All workspace cluster names should start with this prefix.
WORKSPACE_CLUSTER_NAME_PREFIX = "workspace-cluster-"

OPENAPI_NO_VALIDATION = Configuration()
OPENAPI_NO_VALIDATION.client_side_validation = False


class AnyscaleClientWrapper(ABC):
    @abstractmethod
    def get_service_ui_url(self, service_id: str) -> str:
        """Get a URL to the webpage for a service."""
        raise NotImplementedError

    @abstractmethod
    def inside_workspace(self) -> bool:
        """Returns true if this code is running inside a workspace."""
        raise NotImplementedError

    @abstractmethod
    def get_workspace_requirements_path(self) -> Optional[str]:
        """Returns the path to the workspace-managed requirements file.

        Returns None if dependency tracking is disable or the file does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_current_workspace_cluster(self) -> Optional[Cluster]:
        """Get the cluster model for the workspace this code is running in.

        Returns None if not running in a workspace.
        """
        raise NotImplementedError

    def send_workspace_notification(self, notification: WorkspaceNotification):
        """Send a workspace notification to be displayed to the user.

        This is a no-op if called from outside a workspace.
        """
        raise NotImplementedError

    @abstractmethod
    def get_project_id(self) -> str:
        """Get the default project ID for this user.

        If running in a workspace, returns the workspace project ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cloud_id(
        self, *, cloud_name: Optional[str] = None, compute_config_id: Optional[str]
    ) -> Optional[str]:
        """Get the cloud ID for the provided cloud name or compute config ID.

        If both arguments are None:
            - if running in a workspace, get the workspace's cloud ID.
            - else, get the user's default cloud ID.
        """
        raise NotImplementedError

    @abstractmethod
    def create_anonymous_compute_config(self, config: ComputeTemplateConfig) -> str:
        """Create an anonymous compute config and return its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_compute_config_id(
        self, compute_config_name: Optional[str] = None
    ) -> Optional[str]:
        """Get the compute config ID for the provided name.

        If compute_config_name is None:
            - if running in a workspace, get the workspace's compute config ID.
            - else, get the user's default compute config ID.

        Returns None if the compute config name does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_compute_config(
        self, compute_config_id: str
    ) -> Optional[DecoratedComputeTemplate]:
        """Get the compute config for the provided ID.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_build_id(self) -> str:
        """Get the default build id.

        If running in a workspace, it will return the workspace's cluster environment build ID.
        Else it will return the default cluster environment build ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_build_id(
        self, image_uri: str,
    ):
        """Get the cluster env build ID for the provided name.

        If cluster_env_name is None:
            - if running in a workspace, get the workspace's cluster env build ID.
            - else, get the user's default cluster env build ID.

        Returns None if the cluster env name does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_name(self, cluster_env_build_id: str) -> Optional[str]:
        """Get the cluster env name for the provided build ID.

        The returned name will include the revision, e.g., "env-name:1".

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_service(self, name: str) -> Optional[ServiceModel]:
        """Get a service by name.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def rollout_service(self, model: ApplyServiceModel) -> ServiceModel:
        """Deploy or update the service to use the provided config.

        Returns the service ID.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback_service(
        self, service_id: str, *, max_surge_percent: Optional[int] = None
    ):
        """Roll the service back to the primary version.

        This can only be used during an active rollout.
        """
        raise NotImplementedError

    @abstractmethod
    def terminate_service(self, service_id: str):
        """Mark the service to be terminated asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def upload_local_dir_to_cloud_storage(
        self, local_dir: str, *, cloud_id: str, excludes: Optional[List[str]] = None
    ) -> str:
        """Upload the provided directory to cloud storage and return a URI for it.

        The directory will be zipped and the resulting URI can be in a Ray runtime_env.

        The upload is preformed using a pre-signed URL fetched from Anyscale, so no
        local cloud provider authentication is required.
        """
        raise NotImplementedError


class FakeAnyscaleClient(AnyscaleClientWrapper):
    BASE_UI_URL = "http://fake.com"
    CLOUD_BUCKET = "s3://fake-bucket/{cloud_id}"
    DEFAULT_CLOUD_ID = "fake-default-cloud-id"
    DEFAULT_PROJECT_ID = "fake-default-project-id"
    DEFAULT_CLUSTER_COMPUTE_ID = "fake-default-cluster-compute-id"
    DEFAULT_CLUSTER_ENV_BUILD_ID = "fake-default-cluster-env-build-id"

    WORKSPACE_CLOUD_ID = "fake-workspace-cloud-id"
    WORKSPACE_CLUSTER_ID = "fake-workspace-cluster-id"
    WORKSPACE_PROJECT_ID = "fake-workspace-project-id"
    WORKSPACE_CLUSTER_COMPUTE_ID = "fake-workspace-cluster-compute-id"
    WORKSPACE_CLUSTER_ENV_BUILD_ID = "fake-workspace-cluster-env-build-id"

    def get_service_ui_url(self, service_id: str) -> str:
        return f"{self.BASE_UI_URL}/services/{service_id}"

    def __init__(self):
        self._image_uri_to_build_id: Dict[str, str] = {}
        self._build_id_to_image_uri: Dict[str, str] = {}
        self._compute_config_name_to_id: Dict[str, str] = {}
        self._compute_config_id_to_cloud_id: Dict[str, str] = {}
        self._compute_configs: Dict[str, ClusterCompute] = {}
        self._workspace_cluster: Optional[Cluster] = None
        self._workspace_dependency_tracking_enabled: bool = False
        self._services: Dict[str, ServiceModel] = {}
        self._rolled_out_model: Optional[ApplyServiceModel] = None
        self._sent_workspace_notifications: List[WorkspaceNotification] = []
        self._rolled_back_service: Optional[Tuple[str, Optional[int]]] = None
        self._terminated_service: Optional[str] = None

    def set_inside_workspace(
        self,
        inside_workspace: bool,
        *,
        requirements_path: Optional[str] = None,
        cluster_name: Optional[str] = None,
    ):
        self._requirements_path = requirements_path
        if inside_workspace:
            self._workspace_cluster = Cluster(
                id=self.WORKSPACE_CLUSTER_ID,
                name=cluster_name
                if cluster_name is not None
                else WORKSPACE_CLUSTER_NAME_PREFIX + "test",
                project_id=self.WORKSPACE_PROJECT_ID,
                cluster_compute_id=self.WORKSPACE_CLUSTER_COMPUTE_ID,
                cluster_environment_build_id=self.WORKSPACE_CLUSTER_ENV_BUILD_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        else:
            self._workspace_cluster = None

    def inside_workspace(self) -> bool:
        return self.get_current_workspace_cluster() is not None

    def get_workspace_requirements_path(self) -> Optional[str]:
        return self._requirements_path

    def get_current_workspace_cluster(self) -> Optional[Cluster]:
        return self._workspace_cluster

    @property
    def sent_workspace_notifications(self) -> List[WorkspaceNotification]:
        return self._sent_workspace_notifications

    def send_workspace_notification(self, notification: WorkspaceNotification):
        if self.inside_workspace():
            self._sent_workspace_notifications.append(notification)

    def get_project_id(self) -> str:
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.project_id

        return self.DEFAULT_PROJECT_ID

    def set_compute_config_id_to_cloud_id_mapping(
        self, compute_config_id: str, cloud_id: str
    ):
        self._compute_config_id_to_cloud_id[compute_config_id] = cloud_id

    def get_cloud_id(
        self,
        *,
        cloud_name: Optional[str] = None,
        compute_config_id: Optional[str] = None,
    ) -> Optional[str]:
        assert not (cloud_name and compute_config_id)
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return self.WORKSPACE_CLOUD_ID

        if compute_config_id is not None:
            return self._compute_config_id_to_cloud_id.get(compute_config_id)

        if cloud_name is None:
            return self.DEFAULT_CLOUD_ID

        # TODO(edoakes): uncomment the below once non-default cloud is supported.
        # return f"{cloud_name}-fake-id"
        raise NotImplementedError("Only default cloud is currently implemented.")

    def add_compute_config(self, compute_config: DecoratedComputeTemplate):
        self._compute_configs[compute_config.id] = compute_config
        self._compute_config_name_to_id[compute_config.name] = compute_config.id

    def create_anonymous_compute_config(self, config: ComputeTemplateConfig) -> str:
        compute_config_id = f"compute-config-id-{str(uuid.uuid4())}"
        self.add_compute_config(
            DecoratedComputeTemplate(
                id=compute_config_id,
                name=f"compute-config-{str(uuid.uuid4())}",
                config=config,
                anonymous=True,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )
        return compute_config_id

    def get_compute_config(
        self, compute_config_id: str
    ) -> Optional[DecoratedComputeTemplate]:
        return self._compute_configs.get(compute_config_id, None)

    def get_compute_config_id(
        self, compute_config_name: Optional[str] = None
    ) -> Optional[str]:
        if compute_config_name is not None:
            return self._compute_config_name_to_id.get(compute_config_name)

        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.cluster_compute_id

        return self.DEFAULT_CLUSTER_COMPUTE_ID

    def set_image_uri_mapping(self, image_uri: str, build_id: str):
        self._image_uri_to_build_id[image_uri] = build_id
        self._build_id_to_image_uri[build_id] = image_uri

    def get_default_build_id(self) -> str:
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.cluster_environment_build_id

        return self.DEFAULT_CLUSTER_ENV_BUILD_ID

    def get_cluster_env_build_id(self, image_uri: str) -> str:
        if image_uri in self._image_uri_to_build_id:
            return self._image_uri_to_build_id[image_uri]
        else:
            raise ValueError(f"The image_uri '{image_uri}' does not exist.")

    def get_cluster_env_name(self, cluster_env_build_id: str) -> Optional[str]:
        return self._build_id_to_image_uri.get(cluster_env_build_id, None)

    def update_service(self, model: ServiceModel):
        self._services[model.id] = model

    def get_service(self, name: str) -> Optional[ServiceModel]:
        for service in self._services.values():
            if service.name == name:
                return service

        return None

    @property
    def rolled_out_model(self) -> Optional[ApplyServiceModel]:
        return self._rolled_out_model

    def rollout_service(self, model: ApplyServiceModel) -> ServiceModel:
        self._rolled_out_model = model
        existing_service = self.get_service(model.name)
        if existing_service is not None:
            service_id = existing_service.id
        else:
            service_id = f"service-id-{str(uuid.uuid4())}"

        service = ServiceModel(
            id=service_id,
            name=model.name,
            current_state=ServiceEventCurrentState.RUNNING,
            base_url="http://fake-service-url",
            auth_token="fake-auth-token",
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )

        self.update_service(service)
        return service

    @property
    def rolled_back_service(self) -> Optional[Tuple[str, Optional[int]]]:
        return self._rolled_back_service

    def rollback_service(
        self, service_id: str, *, max_surge_percent: Optional[int] = None
    ):
        self._rolled_back_service = (service_id, max_surge_percent)

    @property
    def terminated_service(self) -> Optional[str]:
        return self._terminated_service

    def terminate_service(self, service_id: str):
        self._terminated_service = service_id

    def upload_local_dir_to_cloud_storage(
        self,
        local_dir: str,  # noqa: ARG002
        *,
        cloud_id: str,
        excludes: Optional[List[str]] = None,  # noqa: ARG002
    ) -> str:
        bucket = self.CLOUD_BUCKET.format(cloud_id=cloud_id)
        return f"{bucket}/fake_pkg_{uuid.uuid4()}.zip"


class RealAnyscaleClient(AnyscaleClientWrapper):
    # Number of entries to fetch per request for list endpoints.
    LIST_ENDPOINT_COUNT = 50

    def __init__(
        self,
        *,
        api_clients: Optional[Tuple[ExternalApi, InternalApi]] = None,
        workspace_requirements_file_path: str = WORKSPACE_REQUIREMENTS_FILE_PATH,
    ):
        if api_clients is None:
            auth_block: AuthenticationBlock = get_auth_api_client(
                raise_structured_exception=True
            )
            api_clients = (auth_block.anyscale_api_client, auth_block.api_client)

        self._external_api_client, self._internal_api_client = api_clients
        self._workspace_requirements_file_path = workspace_requirements_file_path

        # Cached IDs and models to avoid duplicate lookups.
        self._default_project_id: Optional[str] = None
        self._cloud_id_cache: Dict[Optional[str], str] = {}
        self._current_workspace_cluster: Optional[Cluster] = None

    def get_service_ui_url(self, service_id: str) -> str:
        return get_endpoint(f"/services/{service_id}")

    def inside_workspace(self) -> bool:
        return self.get_current_workspace_cluster() is not None

    def get_workspace_requirements_path(self) -> Optional[str]:
        if (
            not self.inside_workspace()
            or is_workspace_dependency_tracking_disabled()
            or not pathlib.Path(self._workspace_requirements_file_path).is_file()
        ):
            return None

        return self._workspace_requirements_file_path

    def get_current_workspace_cluster(self) -> Optional[Cluster]:
        # Checks for the existence of the ANYSCALE_EXPERIMENTAL_WORKSPACE_ID env var.
        if not is_anyscale_workspace():
            return None

        if self._current_workspace_cluster is None:
            # Picks up the cluster ID from the ANYSCALE_SESSION_ID env var.
            self._current_workspace_cluster = get_cluster_model_for_current_workspace(
                self._external_api_client
            )

        return self._current_workspace_cluster

    def get_project_id(self) -> str:
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.project_id

        if self._default_project_id is None:
            default_project: Project = self._external_api_client.get_default_project().result
            self._default_project_id = default_project.id

        return self._default_project_id

    def _get_cloud_id_for_compute_config_id(self, compute_config_id: str) -> str:
        cluster_compute: ClusterCompute = self._external_api_client.get_cluster_compute(
            compute_config_id
        ).result
        cluster_compute_config: ClusterComputeConfig = cluster_compute.config
        return cluster_compute_config.cloud_id

    def get_cloud_id(
        self, cloud_name: Optional[str] = None, compute_config_id: Optional[str] = None
    ) -> Optional[str]:
        if cloud_name is not None:
            raise NotImplementedError("Only default cloud is currently implemented.")

        if compute_config_id is not None:
            return self._get_cloud_id_for_compute_config_id(compute_config_id)

        if cloud_name in self._cloud_id_cache:
            return self._cloud_id_cache[cloud_name]

        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            # NOTE(edoakes): the Cluster model has a compute_config_config model that includes
            # its cloud ID, but it's not always populated.
            # TODO(edoakes): add cloud_id to the Cluster model to avoid a second RTT.
            cloud_id = self._get_cloud_id_for_compute_config_id(
                workspace_cluster.cluster_compute_id
            )
        else:
            result: Cloud = self._external_api_client.get_default_cloud().result
            cloud_id = result.id

        self._cloud_id_cache[cloud_name] = cloud_id
        return cloud_id

    def create_anonymous_compute_config(self, config: ComputeTemplateConfig) -> str:
        return self._internal_api_client.create_compute_template_api_v2_compute_templates_post(
            create_compute_template=CreateComputeTemplate(
                config=config, anonymous=True,
            )
        ).result.id

    def get_compute_config(
        self, compute_config_id: str
    ) -> Optional[DecoratedComputeTemplate]:
        try:
            cluster_compute: ClusterCompute = self._internal_api_client.get_compute_template_api_v2_compute_templates_template_id_get(
                compute_config_id
            ).result
            return cluster_compute
        except ApiException as e:
            if e.status == 404:
                return None

            raise e from None

    def get_compute_config_id(
        self, compute_config_name: Optional[str] = None
    ) -> Optional[str]:
        if compute_config_name is not None:
            cluster_computes = self._internal_api_client.search_compute_templates_api_v2_compute_templates_search_post(
                ComputeTemplateQuery(
                    orgwide=True,
                    name={"equals": compute_config_name},
                    include_anonymous=True,
                    archive_status=ArchiveStatus.ALL,
                    # TODO(edoakes): implement version strings.
                    version=None,
                )
            ).results

            if len(cluster_computes) == 0:
                return None

            compute_template: DecoratedComputeTemplate = cluster_computes[0]
            return compute_template.id

        # If the compute config name is not provided, we pick an appropriate default.
        #
        #   - If running in a workspace, we use the workspace's compute config, with
        #     a minor transformation if auto_select_worker_config is applied.
        #
        #   - Otherwise, we use the default compute config provided by the API.

        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            workspace_compute_config: DecoratedComputeTemplate = self.get_compute_config(
                workspace_cluster.cluster_compute_id
            )
            workspace_config: ClusterComputeConfig = workspace_compute_config.config
            if workspace_config.auto_select_worker_config:
                workspace_config = self._apply_standardized_head_node_type(
                    workspace_config
                )
                return self.create_anonymous_compute_config(workspace_config)
            else:
                return workspace_cluster.cluster_compute_id

        # NOTE(edoakes): for some reason the API endpoint is called "cluster compute" but this
        # is the non-deprecated API to use for compute configs.
        return self._external_api_client.get_default_cluster_compute().result.id

    def _apply_standardized_head_node_type(
        self, compute_config: ClusterComputeConfig
    ) -> ClusterComputeConfig:
        """
        Apply the following transformations to the provided compute config:

        1. Standardize the head node instance type.
        2. Disable scheduling on the head node.
        """
        # Retrieve the default cluster compute config.
        default_compute_config: DecoratedComputeTemplate = self._external_api_client.get_default_cluster_compute().result.config

        # Standardize the head node instance type.
        compute_config.head_node_type.instance_type = (
            default_compute_config.head_node_type.instance_type
        )

        # Disable scheduling on the head node.
        if compute_config.head_node_type.resources is None:
            compute_config.head_node_type.resources = {}
        compute_config.head_node_type.resources["CPU"] = 0

        return compute_config

    def get_cluster_env_name(self, cluster_env_build_id: str) -> Optional[str]:
        try:
            build: ClusterEnvironmentBuild = self._external_api_client.get_cluster_environment_build(
                cluster_env_build_id
            ).result
            cluster_env: ClusterEnvironment = self._external_api_client.get_cluster_environment(
                build.cluster_environment_id
            ).result
            return f"{cluster_env.name}:{build.revision}"
        except ApiException as e:
            if e.status == 404:
                return None

            raise e from None

    def get_default_build_id(self) -> str:
        """Get default build id.

        If running in a workspace, it will return the workspace's cluster environment build ID.
        Else it will return the default cluster environment build ID.
        """
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.cluster_environment_build_id
        result: ClusterEnvironmentBuild = self._external_api_client.get_default_cluster_environment_build(
            DEFAULT_PYTHON_VERSION, DEFAULT_RAY_VERSION,
        ).result
        return result.id

    @staticmethod
    def _get_cluster_env_name_from_image_uri(image_uri: str) -> str:
        if len(image_uri) == 0:
            raise ValueError("image_uri cannot be empty.")

        pattern = re.compile("^[A-Za-z0-9_-]+$")
        # Keep only characters that match the pattern
        escaped = []
        for c in image_uri:
            if not pattern.match(c):
                escaped.append("-")
            else:
                escaped.append(c)
        return "".join(escaped)

    def _get_cluster_env_by_name(self, name: str) -> Optional[ClusterEnvironment]:
        cluster_envs = self._external_api_client.search_cluster_environments(
            {
                "name": {"equals": name},
                "paging": {"count": 1},
                "include_anonymous": True,
            }
        ).results
        return cluster_envs[0] if cluster_envs else None

    def get_cluster_env_build_id(self, image_uri: str) -> str:
        """Get the cluster environment build ID for the cluster environment with provided image_uri.

        It maps a image_uri to a cluster env name and then use the name to get the cluster env.
        If there exists a cluster environment for the image_uri, it will reuse the cluster env.
        Else it will create a new cluster environment.
        It will create a new cluster environment build with the provided image_uri or try to reuse one with the same image_uri if exists.

        The same URI should map to the same cluster env name and therefore the build but it is not guaranteed since
        the name format can change.

        """
        cluster_env_name = self._get_cluster_env_name_from_image_uri(image_uri)

        existing_cluster_env = self._get_cluster_env_by_name(cluster_env_name)

        if existing_cluster_env is None:
            # this creates a cluster env only and it does not trigger a build to avoid the race condition
            # when creating a cluster environment and a build at the same time and then list builds for the cluster environment later.
            # ```
            #     cluster_env == self._external_api_client.create_cluster_environment(..., image_uri=image_uri)
            #     build == self._external_api_client.create_cluster_environment_build(..., cluster_env_id=cluster_env.id)
            # ```
            # The race condition can happen if another build for the same cluster envrionment is created between the two calls.

            cluster_environment = self._external_api_client.create_cluster_environment(
                CreateClusterEnvironment(name=cluster_env_name, anonymous=True)
            ).result
            cluster_env_id = cluster_environment.id
        else:
            cluster_env_id = existing_cluster_env.id
            # since we encode the image_uri into the cluster env name, there should exist one and only one build that matches the image_uri.
            cluster_env_builds = self._external_api_client.list_cluster_environment_builds(
                cluster_environment_id=cluster_env_id, count=1
            ).results
            build = cluster_env_builds[0] if cluster_env_builds else None
            if (
                build is not None
                and build.docker_image_name == image_uri
                and build.status == ClusterEnvironmentBuildStatus.SUCCEEDED
            ):
                return build.id

        # Still create a new build if the cluster env already exists but the build does not match the image_uri.
        result = self._external_api_client.create_cluster_environment_build(
            CreateClusterEnvironmentBuild(
                # For historical reasons, we have to use docker_image_name instead of image_uri; but it is just a URI to the image.
                cluster_environment_id=cluster_env_id,
                docker_image_name=image_uri,
            )
        ).result

        assert result.completed
        return result.cluster_environment_build_id

    def send_workspace_notification(
        self, notification: WorkspaceNotification,
    ):
        if not self.inside_workspace():
            return

        try:
            r = requests.post(WORKSPACE_NOTIFICATION_ADDRESS, json=notification.dict())
            r.raise_for_status()
        except Exception:
            logger.exception(
                "Failed to send workspace notification. "
                "This should not happen, so please contact Anyscale support."
            )

    def get_service(self, name: str) -> Optional[ServiceModel]:
        # TODO(edoakes): this endpoint is very slow and there's no reason we should need
        # to use this complex list endpoint just to fetch a service by name.
        paging_token = None
        project_id = self.get_project_id()
        service: Optional[ServiceModel] = None
        while True:
            resp = self._external_api_client.list_services(
                project_id=project_id,
                name=name,
                count=self.LIST_ENDPOINT_COUNT,
                paging_token=paging_token,
            )
            for result in resp.results:
                if result.name == name:
                    service = result
                    break

            paging_token = resp.metadata.next_paging_token
            if service is not None or paging_token is None:
                break

        return service

    def rollout_service(self, model: ApplyServiceModel) -> ServiceModel:
        result: ServiceModel = self._external_api_client.rollout_service(model).result
        return result

    def rollback_service(
        self, service_id: str, *, max_surge_percent: Optional[int] = None
    ) -> ServiceModel:
        result: ServiceModel = self._external_api_client.rollback_service(
            service_id,
            rollback_service_model=RollbackServiceModel(
                max_surge_percent=max_surge_percent
            ),
        )
        return result

    def terminate_service(self, service_id: str) -> ServiceModel:
        result: ServiceModel = self._external_api_client.terminate_service(service_id)
        return result

    def upload_local_dir_to_cloud_storage(
        self, local_dir: str, *, cloud_id: str, excludes: Optional[List[str]] = None
    ) -> str:
        if not pathlib.Path(local_dir).is_dir():
            raise RuntimeError(f"Path '{local_dir}' is not a valid directory.")

        with zip_local_dir(local_dir, excludes=excludes) as (
            _,
            zip_file_bytes,
            content_hash,
        ):
            request = CloudDataBucketPresignedUploadRequest(
                file_type=CloudDataBucketFileType.RUNTIME_ENV_PACKAGES,
                file_name=RUNTIME_ENV_PACKAGE_FORMAT.format(content_hash=content_hash),
            )
            info: CloudDataBucketPresignedUploadInfo = self._internal_api_client.generate_cloud_data_bucket_presigned_upload_url_api_v2_clouds_cloud_id_generate_cloud_data_bucket_presigned_upload_url_post(
                cloud_id, request
            ).result
            requests.put(info.upload_url, data=zip_file_bytes).raise_for_status()

        return info.file_uri
