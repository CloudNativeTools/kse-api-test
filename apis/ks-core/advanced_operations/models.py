from __future__ import annotations

from datetime import datetime
from typing import Optional, Any, Dict, List
from attrs import define, field

__ALL__ = [
    "ErrorsError",
    "V1SecretReference",
    "RegistriesLabels",
    "RegistriesConfig",
    "RegistriesContainerConfig",
    "RegistriesHistory",
    "RegistriesRootfs",
    "RegistriesImageBlob",
    "RegistriesManifestConfig",
    "RegistriesLayers",
    "RegistriesImageManifest",
    "RegistriesImageDetails",
]


@define(kw_only=True)
class ErrorsError:
    message: str = field(metadata={"description": "error message"})


@define(kw_only=True)
class V1SecretReference:
    name: Optional[str] = field(
        default=None,
        metadata={
            "description": "name is unique within a namespace to reference a secret resource."
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "description": "namespace defines the space within which the secret name must be unique."
        },
    )


@define(kw_only=True)
class RegistriesLabels:
    maintainer: str = field()


@define(kw_only=True)
class RegistriesConfig:
    ArgsEscaped: Optional[bool] = field(
        default=None,
        metadata={"description": "Command is already escaped (Windows only)"},
    )
    AttachStderr: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stderr."}
    )
    AttachStdin: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stdin."}
    )
    AttachStdout: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stdout."}
    )
    Cmd: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "Command to run specified as a string or an array of strings."
        },
    )
    Domainname: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value containing the domain name to use for the container."
        },
    )
    Entrypoint: Optional[Any] = field(
        default=None,
        metadata={
            "description": "The entry point set for the container as a string or an array of strings."
        },
    )
    Env: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'A list of environment variables in the form of ["VAR=value", ...]'
        },
    )
    ExposedPorts: Optional[Dict] = field(
        default=None,
        metadata={
            "description": 'An object mapping ports to an empty object in the form of: "ExposedPorts": { "<port>/<tcp|udp>: {}" }'
        },
    )
    Hostname: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value containing the hostname to use for the container."
        },
    )
    Image: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string specifying the image name to use for the container."
        },
    )
    Labels: Optional[RegistriesLabels] = field(
        default=None, metadata={"description": "The map of labels to a container."}
    )
    OnBuild: Optional[Any] = field(
        default=None,
        metadata={
            "description": "ONBUILD metadata that were defined in the image's Dockerfile."
        },
    )
    OpenStdin: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, opens stdin"}
    )
    StdinOnce: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Boolean value, close stdin after the 1 attached client disconnects."
        },
    )
    StopSignal: Optional[str] = field(
        default=None,
        metadata={
            "description": "Signal to stop a container as a string or unsigned integer."
        },
    )
    Tty: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Boolean value, Attach standard streams to a tty, including stdin if it is not closed."
        },
    )
    User: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value specifying the user inside the container."
        },
    )
    Volumes: Optional[Any] = field(
        default=None,
        metadata={
            "description": "An object mapping mount point paths (strings) inside the container to empty objects."
        },
    )
    WorkingDir: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string specifying the working directory for commands to run in."
        },
    )


@define(kw_only=True)
class RegistriesContainerConfig:
    ArgsEscaped: Optional[bool] = field(
        default=None,
        metadata={"description": "Command is already escaped (Windows only)"},
    )
    AttachStderr: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stderr."}
    )
    AttachStdin: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stdin."}
    )
    AttachStdout: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, attaches to stdout."}
    )
    Cmd: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "Command to run specified as a string or an array of strings."
        },
    )
    Domainname: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value containing the domain name to use for the container."
        },
    )
    Entrypoint: Optional[Any] = field(
        default=None,
        metadata={
            "description": "The entry point set for the container as a string or an array of strings."
        },
    )
    Env: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'A list of environment variables in the form of ["VAR=value", ...]'
        },
    )
    ExposedPorts: Optional[Dict] = field(
        default=None,
        metadata={
            "description": 'An object mapping ports to an empty object in the form of: "ExposedPorts": { "<port>/<tcp|udp>: {}" }'
        },
    )
    Hostname: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value containing the hostname to use for the container."
        },
    )
    Image: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string specifying the image name to use for the container."
        },
    )
    Labels: Optional[RegistriesLabels] = field(
        default=None, metadata={"description": "The map of labels to a container."}
    )
    OnBuild: Optional[Any] = field(
        default=None,
        metadata={
            "description": "ONBUILD metadata that were defined in the image's Dockerfile."
        },
    )
    OpenStdin: Optional[bool] = field(
        default=None, metadata={"description": "Boolean value, opens stdin"}
    )
    StdinOnce: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Boolean value, close stdin after the 1 attached client disconnects."
        },
    )
    StopSignal: Optional[str] = field(
        default=None,
        metadata={
            "description": "Signal to stop a container as a string or unsigned integer."
        },
    )
    Tty: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Boolean value, Attach standard streams to a tty, including stdin if it is not closed."
        },
    )
    User: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string value specifying the user inside the container."
        },
    )
    Volumes: Optional[Any] = field(
        default=None,
        metadata={
            "description": "An object mapping mount point paths (strings) inside the container to empty objects."
        },
    )
    WorkingDir: Optional[str] = field(
        default=None,
        metadata={
            "description": "A string specifying the working directory for commands to run in."
        },
    )


@define(kw_only=True)
class RegistriesHistory:
    created: Optional[datetime] = field(
        default=None, metadata={"description": "Created time."}
    )
    created_by: Optional[str] = field(
        default=None, metadata={"description": "Created command."}
    )
    empty_layer: Optional[bool] = field(
        default=None, metadata={"description": "Layer empty or not."}
    )


@define(kw_only=True)
class RegistriesRootfs:
    diff_ids: Optional[List[str]] = field(
        default=None, metadata={"description": "Contain ids of layer list"}
    )
    type: Optional[str] = field(
        default=None, metadata={"description": 'Root filesystem type, always "layers"'}
    )


@define(kw_only=True)
class RegistriesImageBlob:
    rootfs_omitempty: RegistriesRootfs = field(
        metadata={
            "description": "Root filesystem.",
            "original_name": "rootfs omitempty",
        }
    )
    architecture: Optional[str] = field(
        default=None,
        metadata={
            "description": "The architecture field specifies the CPU architecture, for example amd64 or ppc64le."
        },
    )
    config: Optional[RegistriesConfig] = field(
        default=None,
        metadata={
            "description": "The config field references a configuration object for a container."
        },
    )
    container: Optional[str] = field(
        default=None, metadata={"description": "Container id."}
    )
    container_config: Optional[RegistriesContainerConfig] = field(
        default=None, metadata={"description": "The config data of container."}
    )
    created: Optional[datetime] = field(
        default=None, metadata={"description": "Create time."}
    )
    docker_version: Optional[str] = field(
        default=None, metadata={"description": "docker version."}
    )
    history: Optional[List[RegistriesHistory]] = field(
        default=None, metadata={"description": "The data of history update."}
    )
    os: Optional[str] = field(
        default=None, metadata={"description": "Operating system."}
    )


@define(kw_only=True)
class RegistriesManifestConfig:
    digest: Optional[str] = field(
        default=None,
        metadata={
            "description": "The digest of the content, as defined by the Registry V2 HTTP API Specificiation. Reference https://docs.docker.com/registry/spec/api/#digest-parameter"
        },
    )
    mediaType: Optional[str] = field(
        default=None, metadata={"description": "The MIME type of the image."}
    )
    size: Optional[int] = field(
        default=None, metadata={"description": "The size in bytes of the image."}
    )


@define(kw_only=True)
class RegistriesLayers:
    digest: Optional[str] = field(
        default=None,
        metadata={
            "description": "The digest of the content, as defined by the Registry V2 HTTP API Specificiation. Reference https://docs.docker.com/registry/spec/api/#digest-parameter"
        },
    )
    mediaType: Optional[str] = field(
        default=None, metadata={"description": "The MIME type of the layer."}
    )
    size: Optional[int] = field(
        default=None, metadata={"description": "The size in bytes of the layer."}
    )


@define(kw_only=True)
class RegistriesImageManifest:
    config: Optional[RegistriesManifestConfig] = field(
        default=None,
        metadata={
            "description": "The config field references a configuration object for a container."
        },
    )
    layers: Optional[List[RegistriesLayers]] = field(
        default=None, metadata={"description": "Fields of an item in the layers list."}
    )
    mediaType: Optional[str] = field(
        default=None, metadata={"description": "The MIME type of the manifest."}
    )
    schemaVersion: Optional[int] = field(
        default=None,
        metadata={
            "description": "This field specifies the image manifest schema version as an integer."
        },
    )


@define(kw_only=True)
class RegistriesImageDetails:
    imageBlob: Optional[RegistriesImageBlob] = field(
        default=None,
        metadata={
            "description": "Retrieve the blob from the registry identified. Reference: https://docs.docker.com/registry/spec/api/#blob"
        },
    )
    imageManifest: Optional[RegistriesImageManifest] = field(
        default=None,
        metadata={
            "description": "Retrieve the manifest from the registry identified. Reference: https://docs.docker.com/registry/spec/api/#manifest"
        },
    )
    imageTag: Optional[str] = field(
        default=None, metadata={"description": "image tag."}
    )
    message: Optional[str] = field(
        default=None, metadata={"description": "Status message."}
    )
    registry: Optional[str] = field(
        default=None, metadata={"description": "registry domain."}
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "description": 'Status is the status of the image search, such as "succeeded".'
        },
    )
