import copy
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Union

import yaml


IMAGE_URI_PATTERN = re.compile(
    r"^"
    # Optional registry host: hostname with optional port
    r"((?P<host>[a-zA-Z0-9.-]+)(?::(?P<port>[0-9]+))?/)?"
    # Repository name: user_name/repository
    r"(?P<repository>[a-zA-Z0-9-_]+/([a-zA-Z0-9-/_])+)"
    # Optional Tag: version or string after ':'
    r"(:(?P<tag>[a-zA-Z0-9_.-]+))?"
    # Optional Digest: string after '@'
    # Note that when both tag and digest are provided, the tag is ignored.
    r"(@(?P<digest>[a-zA-Z0-9]+))?"
    r"$"
)


class ServiceConfig:
    def __init__(
        self,
        *,
        applications: List[Dict[str, Any]],
        name: Optional[str] = None,
        image_uri: Optional[str] = None,
        compute_config: Optional[Union[Dict, str]] = None,
        working_dir: Optional[str] = None,
        excludes: Optional[List[str]] = None,
        requirements: Optional[Union[str, List[str]]] = None,
        query_auth_token_enabled: Optional[bool] = None,
        grpc_options: Optional[Dict[str, Any]] = None,
        http_options: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        if len(kwargs) > 0:
            raise ValueError(f"Unrecognized options: {list(kwargs.keys())}.")

        if name is not None and not isinstance(name, str):
            raise TypeError("'name' must be a string.")

        if image_uri is not None and not isinstance(image_uri, str):
            raise TypeError("'image_uri' must be a string.")

        if compute_config is not None and not isinstance(compute_config, (str, dict)):
            raise TypeError("'compute_config' must be a string or dictionary.")

        if working_dir is not None and not isinstance(working_dir, str):
            raise TypeError("'working_dir' must be a string.")

        if excludes is not None and (
            not isinstance(excludes, list)
            or not all(isinstance(e, str) for e in excludes)
        ):
            raise TypeError("'excludes' must be a list of strings.")

        if not isinstance(applications, list):
            raise TypeError("'applications' must be a list.")
        elif len(applications) == 0:
            raise ValueError("'applications' cannot be empty.")

        if query_auth_token_enabled is not None and not isinstance(
            query_auth_token_enabled, bool
        ):
            raise TypeError("'query_auth_token_enabled' must be a boolean.")

        self._validate_grpc_options(grpc_options)
        self._validate_http_options(http_options)

        self._name = name
        self._image_uri = image_uri
        self._compute_config = compute_config
        self._query_auth_token_enabled = (
            query_auth_token_enabled if query_auth_token_enabled is not None else True
        )
        self._http_options = http_options
        self._grpc_options = grpc_options
        self._applications = self._override_application_runtime_envs(
            applications=applications,
            working_dir=working_dir,
            excludes=excludes,
            requirements=requirements,
        )

        self._validate_import_paths(self._applications)
        if self._image_uri:
            self._validate_image_uri(self._image_uri)

    def _validate_import_paths(self, applications: List[Dict[str, Any]]):
        for app in applications:
            import_path = app.get("import_path", None)
            if not import_path:
                raise ValueError("Every application must specify an import path.")

            if not isinstance(import_path, str):
                raise TypeError(f"'import_path' must be a string, got: {import_path}")

            if (
                import_path.count(":") != 1
                or import_path.rfind(":") in {0, len(import_path) - 1}
                or import_path.rfind(".") in {0, len(import_path) - 1}
            ):
                raise ValueError(
                    f"'import_path' must be of the form: 'module.optional_submodule:app', but got: '{import_path}'."
                )

    def _validate_image_uri(self, image_uri: str):
        matches = IMAGE_URI_PATTERN.match(image_uri)
        if not matches:
            raise ValueError(
                f"Invalid image URI: '{image_uri}'. Must be in the format: [registry_host/]user_name/repository[:tag][@digest]."
            )

    def _validate_grpc_options(self, grpc_options: Optional[Dict[str, Any]]):
        """Validate the `grpc_options` field.

        This will be passed through as part of the Ray Serve config, but some fields are
        disallowed (not valid when deploying Anyscale services).
        """
        if grpc_options is None:
            return
        elif not isinstance(grpc_options, dict):
            raise TypeError("'grpc_options' must be a dict.")

        banned_options = {
            "port",
        }
        banned_options_passed = {o for o in banned_options if o in grpc_options}
        if len(banned_options_passed) > 0:
            raise ValueError(
                "The following provided 'grpc_options' are not permitted "
                f"in Anyscale: {banned_options_passed}."
            )

    def _validate_http_options(self, http_options: Optional[Dict[str, Any]]):
        """Validate the `http_options` field.

        This will be passed through as part of the Ray Serve config, but some fields are
        disallowed (not valid when deploying Anyscale services).
        """
        if http_options is None:
            return
        elif not isinstance(http_options, dict):
            raise TypeError("'http_options' must be a dict.")

        banned_options = {"host", "port", "root_path"}
        banned_options_passed = {o for o in banned_options if o in http_options}
        if len(banned_options_passed) > 0:
            raise ValueError(
                "The following provided 'http_options' are not permitted "
                f"in Anyscale: {banned_options_passed}."
            )

    def _override_application_runtime_envs(
        self,
        applications: List[Dict[str, Any]],
        *,
        working_dir: Optional[str],
        excludes: Optional[List[str]],
        requirements: Union[None, str, List[str]],
    ) -> List[Dict[str, Any]]:
        """Override the runtime_env field of the provided applications.

        Fields that are modified:
            - 'working_dir' is overwritten with the passed working_dir.
            - 'pip' is overwritten with the passed requirements.
            - 'excludes' is extended with the passed excludes list.
        """
        applications = copy.deepcopy(applications)
        for application in applications:
            runtime_env = application.get("runtime_env", {})
            if working_dir is not None:
                runtime_env["working_dir"] = working_dir

            if excludes is not None:
                # Extend the list of excludes rather than overwriting it.
                runtime_env["excludes"] = runtime_env.get("excludes", []) + excludes

            if requirements is not None:
                runtime_env["pip"] = requirements

            if runtime_env:
                application["runtime_env"] = runtime_env

        return applications

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "name": self._name,
            "image_uri": self._image_uri,
            "compute_config": self._compute_config,
            "applications": self._applications,
            "query_auth_token_enabled": self._query_auth_token_enabled,
        }
        if self._grpc_options is not None:
            d["grpc_options"] = self._grpc_options
        if self._http_options is not None:
            d["http_options"] = self._http_options

        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(**d)

    @classmethod
    def from_yaml(cls, path: str):
        with open(path) as f:
            return cls.from_dict(yaml.safe_load(f))

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def image_uri(self) -> Optional[str]:
        return self._image_uri

    @property
    def compute_config(self) -> Optional[Union[str, Dict]]:
        return self._compute_config

    @property
    def applications(self) -> List[Dict[str, Any]]:
        return self._applications

    @property
    def query_auth_token_enabled(self) -> bool:
        return self._query_auth_token_enabled

    @property
    def grpc_options(self) -> Optional[Dict[str, Any]]:
        return self._grpc_options

    @property
    def http_options(self) -> Optional[Dict[str, Any]]:
        return self._http_options

    def options(  # noqa: PLR0913
        self,
        applications: Optional[List[Dict[str, Any]]] = None,
        name: Optional[str] = None,
        image_uri: Optional[str] = None,
        compute_config: Optional[str] = None,
        working_dir: Optional[str] = None,
        excludes: Optional[List[str]] = None,
        requirements: Optional[Union[str, List[str]]] = None,
        query_auth_token_enabled: Optional[bool] = None,
        grpc_options: Optional[Dict[str, Any]] = None,
        http_options: Optional[Dict[str, Any]] = None,
    ) -> "ServiceConfig":
        return ServiceConfig(
            applications=applications or self.applications,
            name=name or self.name,
            image_uri=image_uri or self.image_uri,
            compute_config=compute_config or self.compute_config,
            working_dir=working_dir,
            excludes=excludes,
            requirements=requirements,
            query_auth_token_enabled=query_auth_token_enabled
            if query_auth_token_enabled is not None
            else self.query_auth_token_enabled,
            grpc_options=grpc_options or self.grpc_options,
            http_options=http_options or self.http_options,
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceConfig):
            return all(
                [
                    self.name == other.name,
                    self.image_uri == other.image_uri,
                    self.compute_config == other.compute_config,
                    self.applications == other.applications,
                    self.query_auth_token_enabled == other.query_auth_token_enabled,
                    self.grpc_options == other.grpc_options,
                    self.http_options == other.http_options,
                ]
            )

        return False

    def __str__(self) -> str:
        return str(self.to_dict())


class ServiceState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    # TODO(edoakes): UPDATING comes up while rolling out and rolling back.
    # This is very unexpected from a customer's point of view, we should fix it.
    UPDATING = "UPDATING"
    ROLLING_OUT = "ROLLING_OUT"
    ROLLING_BACK = "ROLLING_BACK"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    UNHEALTHY = "UNHEALTHY"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"

    def __str__(self):
        return self.name


# TODO(edoakes): we should have a corresponding ServiceVersionState.
class ServiceVersionStatus:
    def __init__(
        self, *, name: str, weight: int, config: Union[ServiceConfig, Dict],
    ):
        self._name: str = name
        self._weight: int = weight

        if isinstance(config, Dict):
            config = ServiceConfig(**config)

        self._config: ServiceConfig = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def config(self) -> ServiceConfig:
        return self._config

    def to_dict(self, *, exclude_details: bool = False) -> Dict[str, Any]:
        d = {
            "name": self._name,
            "weight": self._weight,
        }
        if not exclude_details:
            d["config"] = self._config.to_dict()

        return d

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceVersionStatus):
            return all(
                [
                    self.name == other.name,
                    self.weight == other.weight,
                    self.config == other.config,
                ]
            )

        return False

    def __repr__(self) -> str:
        return f"ServiceVersionStatus(name='{self._name}', weight='{self._weight}')"

    def __str__(self) -> str:
        return str(self.to_dict())


class ServiceStatus:
    def __init__(
        self,
        *,
        service_id: str,
        name: str,
        state: ServiceState,
        query_url: str,
        query_auth_token: Optional[str] = None,
        primary_version: Optional[Union[ServiceVersionStatus, Dict]] = None,
        canary_version: Optional[Union[ServiceVersionStatus, Dict]] = None,
    ):
        self._service_id: str = service_id
        self._name: str = name
        self._state: ServiceState = ServiceState(state)
        self._query_url: str = query_url
        self._query_auth_token: Optional[str] = query_auth_token

        if isinstance(primary_version, dict):
            primary_version = ServiceVersionStatus(**primary_version)
        self._primary_version: Optional[ServiceVersionStatus] = primary_version

        if isinstance(canary_version, dict):
            canary_version = ServiceVersionStatus(**canary_version)
        self._canary_version: Optional[ServiceVersionStatus] = canary_version

    @property
    def service_id(self) -> str:
        return self._service_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> ServiceState:
        return self._state

    @property
    def query_url(self) -> str:
        return self._query_url

    @property
    def query_auth_token(self) -> Optional[str]:
        return self._query_auth_token

    @property
    def primary_version(self) -> Optional[ServiceVersionStatus]:
        return self._primary_version

    @property
    def canary_version(self) -> Optional[ServiceVersionStatus]:
        return self._canary_version

    def to_dict(self, *, exclude_details: bool = False) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "service_id": self._service_id,
            "name": self._name,
            "state": str(self._state),
            "query_url": self._query_url,
        }
        if self._query_auth_token is not None:
            d["query_auth_token"] = self._query_auth_token

        if self._primary_version is not None:
            d["primary_version"] = self._primary_version.to_dict(
                exclude_details=exclude_details
            )

        if self._canary_version is not None:
            d["canary_version"] = self._canary_version.to_dict(
                exclude_details=exclude_details
            )

        return d

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceStatus):
            return all(
                [
                    self.service_id == other.service_id,
                    self.name == other.name,
                    self.state == other.state,
                    self.query_url == other.query_url,
                    self.query_auth_token == other.query_auth_token,
                    self.primary_version == other.primary_version,
                    self.canary_version == other.canary_version,
                ]
            )

        return False

    def __repr__(self) -> str:
        return f"ServiceStatus(name='{self._name}')"

    def __str__(self) -> str:
        return str(self.to_dict())
