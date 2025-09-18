from __future__ import annotations

from typing import Optional, List, Any, Dict
from attrs import define, field

__ALL__ = [
    "ApiWorkloads",
    "V1ManagedFieldsEntry",
    "V1OwnerReference",
    "V1ObjectMeta",
    "V1LabelSelectorRequirement",
    "V1LabelSelector",
    "V1PreferredSchedulingTerm",
    "V1NodeSelector",
    "V1NodeAffinity",
    "V1WeightedPodAffinityTerm",
    "V1PodAffinityTerm",
    "V1PodAffinity",
    "V1PodAntiAffinity",
    "V1Affinity",
    "V1EnvVar",
    "V1EnvFromSource",
    "V1LifecycleHandler",
    "V1Lifecycle",
    "V1ExecAction",
    "V1GRPCAction",
    "V1HTTPGetAction",
    "V1TCPSocketAction",
    "V1Probe",
    "V1ContainerPort",
    "V1ContainerResizePolicy",
    "V1ResourceRequirements",
    "V1Capabilities",
    "V1SELinuxOptions",
    "V1SeccompProfile",
    "V1WindowsSecurityContextOptions",
    "V1SecurityContext",
    "V1VolumeDevice",
    "V1VolumeMount",
    "V1Container",
    "V1PodDNSConfigOption",
    "V1PodDNSConfig",
    "V1EphemeralContainer",
    "V1HostAlias",
    "V1LocalObjectReference",
    "V1PodOS",
    "V1PodReadinessGate",
    "V1ClaimSource",
    "V1PodResourceClaim",
    "V1PodSchedulingGate",
    "V1Sysctl",
    "V1PodSecurityContext",
    "V1Toleration",
    "V1TopologySpreadConstraint",
    "V1AWSElasticBlockStoreVolumeSource",
    "V1AzureDiskVolumeSource",
    "V1AzureFileVolumeSource",
    "V1CephFSVolumeSource",
    "V1CinderVolumeSource",
    "V1ConfigMapVolumeSource",
    "V1CSIVolumeSource",
    "V1DownwardAPIVolumeSource",
    "V1EmptyDirVolumeSource",
    "V1PersistentVolumeClaimTemplate",
    "V1EphemeralVolumeSource",
    "V1FCVolumeSource",
    "V1FlexVolumeSource",
    "V1FlockerVolumeSource",
    "V1GCEPersistentDiskVolumeSource",
    "V1GitRepoVolumeSource",
    "V1GlusterfsVolumeSource",
    "V1HostPathVolumeSource",
    "V1ISCSIVolumeSource",
    "V1NFSVolumeSource",
    "V1PersistentVolumeClaimVolumeSource",
    "V1PhotonPersistentDiskVolumeSource",
    "V1PortworxVolumeSource",
    "V1ProjectedVolumeSource",
    "V1QuobyteVolumeSource",
    "V1RBDVolumeSource",
    "V1ScaleIOVolumeSource",
    "V1SecretVolumeSource",
    "V1StorageOSVolumeSource",
    "V1VsphereVirtualDiskVolumeSource",
    "V1Volume",
    "V1PodSpec",
    "V1PodTemplateSpec",
    "V1RollingUpdateDaemonSet",
    "V1DaemonSetUpdateStrategy",
    "V1DaemonSetSpec",
    "V1DaemonSetCondition",
    "V1DaemonSetStatus",
    "V1DaemonSet",
    "V1ReplicaSetSpec",
    "V1ReplicaSetCondition",
    "V1ReplicaSetStatus",
    "V1ReplicaSet",
    "V1ResourceQuotaStatus",
    "ApiResourceQuota",
    "V1StatefulSetOrdinals",
    "V1StatefulSetPersistentVolumeClaimRetentionPolicy",
    "V1RollingUpdateStatefulSetStrategy",
    "V1StatefulSetUpdateStrategy",
    "V1TypedLocalObjectReference",
    "V1TypedObjectReference",
    "V1VolumeResourceRequirements",
    "V1PersistentVolumeClaimSpec",
    "V1PersistentVolumeClaimCondition",
    "V1ModifyVolumeStatus",
    "V1PersistentVolumeClaimStatus",
    "V1PersistentVolumeClaim",
    "V1StatefulSetSpec",
    "V1StatefulSetCondition",
    "V1StatefulSetStatus",
    "V1StatefulSet",
    "ApiListResult",
    "V1HealthConfig",
    "V1Config",
    "V1History",
    "V1Hash",
    "V1RootFS",
    "V1ConfigFile",
    "V2ImageConfig",
    "OverviewMetricValue",
    "OverviewMetricData",
    "OverviewMetric",
    "OverviewMetricResults",
    "V1Secret",
    "V2RepositoryTags",
]


@define(kw_only=True)
class ApiWorkloads:
    data: Dict = field(metadata={"description": "the number of unhealthy workloads"})
    namespace: str = field(metadata={"description": "the name of the namespace"})
    items: Optional[Dict] = field(
        default=None, metadata={"description": "unhealthy workloads"}
    )


@define(kw_only=True)
class V1ManagedFieldsEntry:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": 'APIVersion defines the version of this resource that this field set applies to. The format is "group/version" just like the top-level APIVersion field. It is necessary to track the version of a field set because it cannot be automatically converted.'
        },
    )
    fieldsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'FieldsType is the discriminator for the different fields format and version. There is currently only one possible value: "FieldsV1"'
        },
    )
    fieldsV1: Optional[str] = field(
        default=None,
        metadata={
            "description": 'FieldsV1 holds the first JSON version format as described in the "FieldsV1" type.'
        },
    )
    manager: Optional[str] = field(
        default=None,
        metadata={
            "description": "Manager is an identifier of the workflow managing these fields."
        },
    )
    operation: Optional[str] = field(
        default=None,
        metadata={
            "description": "Operation is the type of operation which lead to this ManagedFieldsEntry being created. The only valid values for this field are 'Apply' and 'Update'."
        },
    )
    subresource: Optional[str] = field(
        default=None,
        metadata={
            "description": "Subresource is the name of the subresource used to update that object, or empty string if the object was updated through the main resource. The value of this field is used to distinguish between managers, even if they share the same name. For example, a status update will be distinct from a regular update using the same manager name. Note that the APIVersion field is not related to the Subresource field and it always corresponds to the version of the main resource."
        },
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "description": "Time is the timestamp of when the ManagedFields entry was added. The timestamp will also be updated if a field is added, the manager changes any of the owned fields value or removes a field. The timestamp does not update when a field is removed from the entry because another manager took it over."
        },
    )


@define(kw_only=True)
class V1OwnerReference:
    apiVersion: str = field(metadata={"description": "API version of the referent."})
    kind: str = field(
        metadata={
            "description": "Kind of the referent. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        }
    )
    name: str = field(
        metadata={
            "description": "Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names#names"
        }
    )
    uid: str = field(
        metadata={
            "description": "UID of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names#uids"
        }
    )
    blockOwnerDeletion: Optional[bool] = field(
        default=None,
        metadata={
            "description": 'If true, AND if the owner has the "foregroundDeletion" finalizer, then the owner cannot be deleted from the key-value store until this reference is removed. See https://kubernetes.io/docs/concepts/architecture/garbage-collection/#foreground-deletion for how the garbage collector interacts with this field and enforces the foreground deletion. Defaults to false. To set this field, a user needs "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be returned.'
        },
    )
    controller: Optional[bool] = field(
        default=None,
        metadata={
            "description": "If true, this reference points to the managing controller."
        },
    )


@define(kw_only=True)
class V1ObjectMeta:
    annotations: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations"
        },
    )
    creationTimestamp: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
CreationTimestamp is a timestamp representing the server time when this object was created. It is not guaranteed to be set in happens-before order across separate operations. Clients may not set this value. It is represented in RFC3339 form and is in UTC.

Populated by the system. Read-only. Null for lists. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
"""
        },
    )
    deletionGracePeriodSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Number of seconds allowed for this object to gracefully terminate before it will be removed from the system. Only set when deletionTimestamp is also set. May only be shortened. Read-only."
        },
    )
    deletionTimestamp: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
DeletionTimestamp is RFC 3339 date and time at which this resource will be deleted. This field is set by the server when a graceful deletion is requested by the user, and is not directly settable by a client. The resource is expected to be deleted (no longer visible from resource lists, and not reachable by name) after the time in this field, once the finalizers list is empty. As long as the finalizers list contains items, deletion is blocked. Once the deletionTimestamp is set, this value may not be unset or be set further into the future, although it may be shortened or the resource may be deleted prior to this time. For example, a user may request that a pod is deleted in 30 seconds. The Kubelet will react by sending a graceful termination signal to the containers in the pod. After that 30 seconds, the Kubelet will send a hard termination signal (SIGKILL) to the container and after cleanup, remove the pod from the API. In the presence of network partitions, this object may still exist after this timestamp, until an administrator or automated process can determine the resource is fully terminated. If not set, graceful deletion of the object has not been requested.

Populated by the system when a graceful deletion is requested. Read-only. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
"""
        },
    )
    finalizers: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "Must be empty before the object is deleted from the registry. Each entry is an identifier for the responsible component that will remove the entry from the list. If the deletionTimestamp of the object is non-nil, entries in this list can only be removed. Finalizers may be processed and removed in any order.  Order is NOT enforced because it introduces significant risk of stuck finalizers. finalizers is a shared field, any actor with permission can reorder it. If the finalizer list is processed in order, then this can lead to a situation in which the component responsible for the first finalizer in the list is waiting for a signal (field value, external system, or other) produced by a component responsible for a finalizer later in the list, resulting in a deadlock. Without enforced ordering finalizers are free to order amongst themselves and are not vulnerable to ordering changes in the list."
        },
    )
    generateName: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
GenerateName is an optional prefix, used by the server, to generate a unique name ONLY IF the Name field has not been provided. If this field is used, the name returned to the client will be different than the name passed. This value will also be combined with a unique suffix. The provided value has the same validation rules as the Name field, and may be truncated by the length of the suffix required to make the value unique on the server.

If this field is specified and the generated name exists, the server will return a 409.

Applied only if Name is not specified. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#idempotency
"""
        },
    )
    generation: Optional[int] = field(
        default=None,
        metadata={
            "description": "A sequence number representing a specific generation of the desired state. Populated by the system. Read-only."
        },
    )
    labels: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels"
        },
    )
    managedFields: Optional[List[V1ManagedFieldsEntry]] = field(
        default=None,
        metadata={
            "description": "ManagedFields maps workflow-id and version to the set of fields that are managed by that workflow. This is mostly for internal housekeeping, and users typically shouldn't need to set or understand this field. A workflow can be the user's name, a controller's name, or the name of a specific apply path like \"ci-cd\". The set of fields is always in the version that the workflow used when modifying the object."
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name must be unique within a namespace. Is required when creating resources, although some resources may allow a client to request the generation of an appropriate name automatically. Name is primarily intended for creation idempotence and configuration definition. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names#names"
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
Namespace defines the space within which each name must be unique. An empty namespace is equivalent to the \"default\" namespace, but \"default\" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty.

Must be a DNS_LABEL. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces
"""
        },
    )
    ownerReferences: Optional[List[V1OwnerReference]] = field(
        default=None,
        metadata={
            "description": "List of objects depended by this object. If ALL objects in the list have been deleted, this object will be garbage collected. If this object is managed by a controller, then an entry in this list will point to this controller, with the controller field set to true. There cannot be more than one managing controller."
        },
    )
    resourceVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
An opaque value that represents the internal version of this object that can be used by clients to determine when objects have changed. May be used for optimistic concurrency, change detection, and the watch operation on a resource or set of resources. Clients must treat these values as opaque and passed unmodified back to the server. They may only be valid for a particular resource or set of resources.

Populated by the system. Read-only. Value must be treated as opaque by clients and . More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency
"""
        },
    )
    selfLink: Optional[str] = field(
        default=None,
        metadata={
            "description": "Deprecated: selfLink is a legacy read-only field that is no longer populated by the system."
        },
    )
    uid: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
UID is the unique in time and space value for this object. It is typically generated by the server on successful creation of a resource and is not allowed to change on PUT operations.

Populated by the system. Read-only. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names#uids
"""
        },
    )


@define(kw_only=True)
class V1LabelSelectorRequirement:
    key: str = field(
        metadata={"description": "key is the label key that the selector applies to."}
    )
    operator: str = field(
        metadata={
            "description": "operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist."
        }
    )
    values: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch."
        },
    )


@define(kw_only=True)
class V1LabelSelector:
    matchExpressions: Optional[List[V1LabelSelectorRequirement]] = field(
        default=None,
        metadata={
            "description": "matchExpressions is a list of label selector requirements. The requirements are ANDed."
        },
    )
    matchLabels: Optional[Dict] = field(
        default=None,
        metadata={
            "description": 'matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.'
        },
    )


@define(kw_only=True)
class V1PreferredSchedulingTerm:
    preference: Any = field(
        metadata={
            "description": "A node selector term, associated with the corresponding weight."
        }
    )
    weight: Any = field(
        metadata={
            "description": "Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100."
        }
    )


@define(kw_only=True)
class V1NodeSelector:
    nodeSelectorTerms: List[Any] = field(
        metadata={
            "description": "Required. A list of node selector terms. The terms are ORed."
        }
    )


@define(kw_only=True)
class V1NodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[V1PreferredSchedulingTerm]
    ] = field(
        default=None,
        metadata={
            "description": 'The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding matchExpressions; the node(s) with the highest sum are the most preferred.'
        },
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[V1NodeSelector] = field(
        default=None,
        metadata={
            "description": "If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to an update), the system may or may not try to eventually evict the pod from its node."
        },
    )


@define(kw_only=True)
class V1WeightedPodAffinityTerm:
    podAffinityTerm: Any = field(
        metadata={
            "description": "Required. A pod affinity term, associated with the corresponding weight."
        }
    )
    weight: Any = field(
        metadata={
            "description": "weight associated with matching the corresponding podAffinityTerm, in the range 1-100."
        }
    )


@define(kw_only=True)
class V1PodAffinityTerm:
    topologyKey: Any = field(
        metadata={
            "description": "This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching the labelSelector in the specified namespaces, where co-located is defined as running on a node whose value of the label with key topologyKey matches that of any node on which any of the selected pods is running. Empty topologyKey is not allowed."
        }
    )
    labelSelector: Optional[Any] = field(
        default=None,
        metadata={
            "description": "A label query over a set of resources, in this case pods. If it's null, this PodAffinityTerm matches with no Pods."
        },
    )
    matchLabelKeys: Optional[Any] = field(
        default=None,
        metadata={
            "description": "MatchLabelKeys is a set of pod label keys to select which pods will be taken into consideration. The keys are used to lookup values from the incoming pod labels, those key-value labels are merged with `LabelSelector` as `key in (value)` to select the group of existing pods which pods will be taken into consideration for the incoming pod's pod (anti) affinity. Keys that don't exist in the incoming pod labels will be ignored. The default value is empty. The same key is forbidden to exist in both MatchLabelKeys and LabelSelector. Also, MatchLabelKeys cannot be set when LabelSelector isn't set. This is an alpha field and requires enabling MatchLabelKeysInPodAffinity feature gate."
        },
    )
    mismatchLabelKeys: Optional[Any] = field(
        default=None,
        metadata={
            "description": "MismatchLabelKeys is a set of pod label keys to select which pods will be taken into consideration. The keys are used to lookup values from the incoming pod labels, those key-value labels are merged with `LabelSelector` as `key notin (value)` to select the group of existing pods which pods will be taken into consideration for the incoming pod's pod (anti) affinity. Keys that don't exist in the incoming pod labels will be ignored. The default value is empty. The same key is forbidden to exist in both MismatchLabelKeys and LabelSelector. Also, MismatchLabelKeys cannot be set when LabelSelector isn't set. This is an alpha field and requires enabling MatchLabelKeysInPodAffinity feature gate."
        },
    )
    namespaceSelector: Optional[Any] = field(
        default=None,
        metadata={
            "description": 'A label query over the set of namespaces that the term applies to. The term is applied to the union of the namespaces selected by this field and the ones listed in the namespaces field. null selector and null or empty namespaces list means "this pod\'s namespace". An empty selector ({}) matches all namespaces.'
        },
    )
    namespaces: Optional[Any] = field(
        default=None,
        metadata={
            "description": 'namespaces specifies a static list of namespace names that the term applies to. The term is applied to the union of the namespaces listed in this field and the ones selected by namespaceSelector. null or empty namespaces list and null namespaceSelector means "this pod\'s namespace".'
        },
    )


@define(kw_only=True)
class V1PodAffinity:
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[V1WeightedPodAffinityTerm]
    ] = field(
        default=None,
        metadata={
            "description": 'The scheduler will prefer to schedule pods to nodes that satisfy the affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred.'
        },
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[
        List[V1PodAffinityTerm]
    ] = field(
        default=None,
        metadata={
            "description": "If the affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied."
        },
    )


@define(kw_only=True)
class V1PodAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution: Optional[
        List[V1WeightedPodAffinityTerm]
    ] = field(
        default=None,
        metadata={
            "description": 'The scheduler will prefer to schedule pods to nodes that satisfy the anti-affinity expressions specified by this field, but it may choose a node that violates one or more of the expressions. The node that is most preferred is the one with the greatest sum of weights, i.e. for each node that meets all of the scheduling requirements (resource request, requiredDuringScheduling anti-affinity expressions, etc.), compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the node(s) with the highest sum are the most preferred.'
        },
    )
    requiredDuringSchedulingIgnoredDuringExecution: Optional[
        List[V1PodAffinityTerm]
    ] = field(
        default=None,
        metadata={
            "description": "If the anti-affinity requirements specified by this field are not met at scheduling time, the pod will not be scheduled onto the node. If the anti-affinity requirements specified by this field cease to be met at some point during pod execution (e.g. due to a pod label update), the system may or may not try to eventually evict the pod from its node. When there are multiple elements, the lists of nodes corresponding to each podAffinityTerm are intersected, i.e. all terms must be satisfied."
        },
    )


@define(kw_only=True)
class V1Affinity:
    nodeAffinity: Optional[V1NodeAffinity] = field(
        default=None,
        metadata={
            "description": "Describes node affinity scheduling rules for the pod."
        },
    )
    podAffinity: Optional[V1PodAffinity] = field(
        default=None,
        metadata={
            "description": "Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s))."
        },
    )
    podAntiAffinity: Optional[V1PodAntiAffinity] = field(
        default=None,
        metadata={
            "description": "Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s))."
        },
    )


@define(kw_only=True)
class V1EnvVar:
    name: str = field(
        metadata={
            "description": "Name of the environment variable. Must be a C_IDENTIFIER."
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "description": 'Variable references $(VAR_NAME) are expanded using the previously defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "".'
        },
    )
    valueFrom: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Source for the environment variable's value. Cannot be used if value is not empty."
        },
    )


@define(kw_only=True)
class V1EnvFromSource:
    configMapRef: Optional[Any] = field(
        default=None, metadata={"description": "The ConfigMap to select from"}
    )
    prefix: Optional[str] = field(
        default=None,
        metadata={
            "description": "An optional identifier to prepend to each key in the ConfigMap. Must be a C_IDENTIFIER."
        },
    )
    secretRef: Optional[Any] = field(
        default=None, metadata={"description": "The Secret to select from"}
    )


@define(kw_only=True)
class V1LifecycleHandler:
    exec: Optional[Any] = field(
        default=None, metadata={"description": "Exec specifies the action to take."}
    )
    httpGet: Optional[Any] = field(
        default=None,
        metadata={"description": "HTTPGet specifies the http request to perform."},
    )
    sleep: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Sleep represents the duration that the container should sleep before being terminated."
        },
    )
    tcpSocket: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Deprecated. TCPSocket is NOT supported as a LifecycleHandler and kept for the backward compatibility. There are no validation of this field and lifecycle hooks will fail in runtime when tcp handler is specified."
        },
    )


@define(kw_only=True)
class V1Lifecycle:
    postStart: Optional[V1LifecycleHandler] = field(
        default=None,
        metadata={
            "description": "PostStart is called immediately after a container is created. If the handler fails, the container is terminated and restarted according to its restart policy. Other management of the container blocks until the hook completes. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks"
        },
    )
    preStop: Optional[V1LifecycleHandler] = field(
        default=None,
        metadata={
            "description": "PreStop is called immediately before a container is terminated due to an API request or management event such as liveness/startup probe failure, preemption, resource contention, etc. The handler is not called if the container crashes or exits. The Pod's termination grace period countdown begins before the PreStop hook is executed. Regardless of the outcome of the handler, the container will eventually terminate within the Pod's termination grace period (unless delayed by finalizers). Other management of the container blocks until the hook completes or until the termination grace period is reached. More info: https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks"
        },
    )


@define(kw_only=True)
class V1ExecAction:
    command: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Command is the command line to execute inside the container, the working directory for the command  is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy."
        },
    )


@define(kw_only=True)
class V1GRPCAction:
    port: Any = field(
        metadata={
            "description": "Port number of the gRPC service. Number must be in the range 1 to 65535."
        }
    )
    service: Any = field(
        metadata={
            "description": """\
Service is the name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md).

If this is not specified, the default behavior is defined by gRPC.
"""
        }
    )


@define(kw_only=True)
class V1HTTPGetAction:
    port: Any = field(
        metadata={
            "description": "Name or number of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME."
        }
    )
    host: Optional[Any] = field(
        default=None,
        metadata={
            "description": 'Host name to connect to, defaults to the pod IP. You probably want to set "Host" in httpHeaders instead.'
        },
    )
    httpHeaders: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Custom headers to set in the request. HTTP allows repeated headers."
        },
    )
    path: Optional[Any] = field(
        default=None, metadata={"description": "Path to access on the HTTP server."}
    )
    scheme: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Scheme to use for connecting to the host. Defaults to HTTP."
        },
    )


@define(kw_only=True)
class V1TCPSocketAction:
    port: Any = field(
        metadata={
            "description": "Number or name of the port to access on the container. Number must be in the range 1 to 65535. Name must be an IANA_SVC_NAME."
        }
    )
    host: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Optional: Host name to connect to, defaults to the pod IP."
        },
    )


@define(kw_only=True)
class V1Probe:
    exec: Optional[V1ExecAction] = field(
        default=None, metadata={"description": "Exec specifies the action to take."}
    )
    failureThreshold: Optional[int] = field(
        default=None,
        metadata={
            "description": "Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1."
        },
    )
    grpc: Optional[V1GRPCAction] = field(
        default=None,
        metadata={"description": "GRPC specifies an action involving a GRPC port."},
    )
    httpGet: Optional[V1HTTPGetAction] = field(
        default=None,
        metadata={"description": "HTTPGet specifies the http request to perform."},
    )
    initialDelaySeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Number of seconds after the container has started before liveness probes are initiated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        },
    )
    periodSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1."
        },
    )
    successThreshold: Optional[int] = field(
        default=None,
        metadata={
            "description": "Minimum consecutive successes for the probe to be considered successful after having failed. Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1."
        },
    )
    tcpSocket: Optional[V1TCPSocketAction] = field(
        default=None,
        metadata={"description": "TCPSocket specifies an action involving a TCP port."},
    )
    terminationGracePeriodSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Optional duration in seconds the pod needs to terminate gracefully upon probe failure. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. If this value is nil, the pod's terminationGracePeriodSeconds will be used. Otherwise, this value overrides the value provided by the pod spec. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). This is a beta field and requires enabling ProbeTerminationGracePeriod feature gate. Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset."
        },
    )
    timeoutSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        },
    )


@define(kw_only=True)
class V1ContainerPort:
    containerPort: int = field(
        metadata={
            "description": "Number of port to expose on the pod's IP address. This must be a valid port number, 0 < x < 65536."
        }
    )
    hostIP: Optional[str] = field(
        default=None,
        metadata={"description": "What host IP to bind the external port to."},
    )
    hostPort: Optional[int] = field(
        default=None,
        metadata={
            "description": "Number of port to expose on the host. If specified, this must be a valid port number, 0 < x < 65536. If HostNetwork is specified, this must match ContainerPort. Most containers do not need this."
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "description": "If specified, this must be an IANA_SVC_NAME and unique within the pod. Each named port in a pod must have a unique name. Name for the port that can be referred to by services."
        },
    )
    protocol: Optional[str] = field(
        default=None,
        metadata={
            "description": 'Protocol for port. Must be UDP, TCP, or SCTP. Defaults to "TCP".'
        },
    )


@define(kw_only=True)
class V1ContainerResizePolicy:
    resourceName: str = field(
        metadata={
            "description": "Name of the resource to which this resource resize policy applies. Supported values: cpu, memory."
        }
    )
    restartPolicy: str = field(
        metadata={
            "description": "Restart policy to apply when specified resource is resized. If not specified, it defaults to NotRequired."
        }
    )


@define(kw_only=True)
class V1ResourceRequirements:
    claims: Optional[List[Any]] = field(
        default=None,
        metadata={
            "description": """\
Claims lists the names of resources, defined in spec.resourceClaims, that are used by this container.

This is an alpha field and requires enabling the DynamicResourceAllocation feature gate.

This field is immutable. It can only be set for containers.
"""
        },
    )
    limits: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        },
    )
    requests: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. Requests cannot exceed Limits. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        },
    )


@define(kw_only=True)
class V1Capabilities:
    add: Optional[Any] = field(
        default=None, metadata={"description": "Added capabilities"}
    )
    drop: Optional[Any] = field(
        default=None, metadata={"description": "Removed capabilities"}
    )


@define(kw_only=True)
class V1SELinuxOptions:
    level: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Level is SELinux level label that applies to the container."
        },
    )
    role: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Role is a SELinux role label that applies to the container."
        },
    )
    type: Optional[Any] = field(
        default=None,
        metadata={
            "description": "Type is a SELinux type label that applies to the container."
        },
    )
    user: Optional[Any] = field(
        default=None,
        metadata={
            "description": "User is a SELinux user label that applies to the container."
        },
    )


@define(kw_only=True)
class V1SeccompProfile:
    type: Any = field(
        metadata={
            "description": """\
type indicates which kind of seccomp profile will be applied. Valid options are:

Localhost - a profile defined in a file on the node should be used. RuntimeDefault - the container runtime default profile should be used. Unconfined - no profile should be applied.
"""
        }
    )
    localhostProfile: Optional[Any] = field(
        default=None,
        metadata={
            "description": 'localhostProfile indicates a profile defined in a file on the node should be used. The profile must be preconfigured on the node to work. Must be a descending path, relative to the kubelet\'s configured seccomp profile location. Must be set if type is "Localhost". Must NOT be set for any other type.'
        },
    )


@define(kw_only=True)
class V1WindowsSecurityContextOptions:
    gmsaCredentialSpec: Optional[Any] = field(
        default=None,
        metadata={
            "description": "GMSACredentialSpec is where the GMSA admission webhook (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of the GMSA credential spec named by the GMSACredentialSpecName field."
        },
    )
    gmsaCredentialSpecName: Optional[Any] = field(
        default=None,
        metadata={
            "description": "GMSACredentialSpecName is the name of the GMSA credential spec to use."
        },
    )
    hostProcess: Optional[Any] = field(
        default=None,
        metadata={
            "description": "HostProcess determines if a container should be run as a 'Host Process' container. All of a Pod's containers must have the same effective HostProcess value (it is not allowed to have a mix of HostProcess containers and non-HostProcess containers). In addition, if HostProcess is true then HostNetwork must also be set to true."
        },
    )
    runAsUserName: Optional[Any] = field(
        default=None,
        metadata={
            "description": "The UserName in Windows to run the entrypoint of the container process. Defaults to the user specified in image metadata if unspecified. May also be set in PodSecurityContext. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence."
        },
    )


@define(kw_only=True)
class V1SecurityContext:
    allowPrivilegeEscalation: Optional[bool] = field(
        default=None,
        metadata={
            "description": "AllowPrivilegeEscalation controls whether a process can gain more privileges than its parent process. This bool directly controls if the no_new_privs flag will be set on the container process. AllowPrivilegeEscalation is true always when the container is: 1) run as Privileged 2) has CAP_SYS_ADMIN Note that this field cannot be set when spec.os.name is windows."
        },
    )
    capabilities: Optional[V1Capabilities] = field(
        default=None,
        metadata={
            "description": "The capabilities to add/drop when running containers. Defaults to the default set of capabilities granted by the container runtime. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    privileged: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Run container in privileged mode. Processes in privileged containers are essentially equivalent to root on the host. Defaults to false. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    procMount: Optional[str] = field(
        default=None,
        metadata={
            "description": "procMount denotes the type of proc mount to use for the containers. The default is DefaultProcMount which uses the container runtime defaults for readonly paths and masked paths. This requires the ProcMountType feature flag to be enabled. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    readOnlyRootFilesystem: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether this container has a read-only root filesystem. Default is false. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    runAsGroup: Optional[int] = field(
        default=None,
        metadata={
            "description": "The GID to run the entrypoint of the container process. Uses runtime default if unset. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    runAsNonRoot: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence."
        },
    )
    runAsUser: Optional[int] = field(
        default=None,
        metadata={
            "description": "The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    seLinuxOptions: Optional[V1SELinuxOptions] = field(
        default=None,
        metadata={
            "description": "The SELinux context to be applied to the container. If unspecified, the container runtime will allocate a random SELinux context for each container.  May also be set in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    seccompProfile: Optional[V1SeccompProfile] = field(
        default=None,
        metadata={
            "description": "The seccomp options to use by this container. If seccomp options are provided at both the pod & container level, the container options override the pod options. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    windowsOptions: Optional[V1WindowsSecurityContextOptions] = field(
        default=None,
        metadata={
            "description": "The Windows specific settings applied to all containers. If unspecified, the options from the PodSecurityContext will be used. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is linux."
        },
    )


@define(kw_only=True)
class V1VolumeDevice:
    devicePath: str = field(
        metadata={
            "description": "devicePath is the path inside of the container that the device will be mapped to."
        }
    )
    name: str = field(
        metadata={
            "description": "name must match the name of a persistentVolumeClaim in the pod"
        }
    )


@define(kw_only=True)
class V1VolumeMount:
    mountPath: str = field(
        metadata={
            "description": "Path within the container at which the volume should be mounted.  Must not contain ':'."
        }
    )
    name: str = field(metadata={"description": "This must match the Name of a Volume."})
    mountPropagation: Optional[str] = field(
        default=None,
        metadata={
            "description": "mountPropagation determines how mounts are propagated from the host to container and the other way around. When not set, MountPropagationNone is used. This field is beta in 1.10."
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Mounted read-only if true, read-write otherwise (false or unspecified). Defaults to false."
        },
    )
    subPath: Optional[str] = field(
        default=None,
        metadata={
            "description": "Path within the volume from which the container's volume should be mounted. Defaults to \"\" (volume's root)."
        },
    )
    subPathExpr: Optional[str] = field(
        default=None,
        metadata={
            "description": "Expanded path within the volume from which the container's volume should be mounted. Behaves similarly to SubPath but environment variable references $(VAR_NAME) are expanded using the container's environment. Defaults to \"\" (volume's root). SubPathExpr and SubPath are mutually exclusive."
        },
    )


@define(kw_only=True)
class V1Container:
    name: str = field(
        metadata={
            "description": "Name of the container specified as a DNS_LABEL. Each container in a pod must have a unique name (DNS_LABEL). Cannot be updated."
        }
    )
    args: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'Arguments to the entrypoint. The container image\'s CMD is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container\'s environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell'
        },
    )
    command: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'Entrypoint array. Not executed within a shell. The container image\'s ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container\'s environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell'
        },
    )
    env: Optional[List[V1EnvVar]] = field(
        default=None,
        metadata={
            "description": "List of environment variables to set in the container. Cannot be updated."
        },
    )
    envFrom: Optional[List[V1EnvFromSource]] = field(
        default=None,
        metadata={
            "description": "List of sources to populate environment variables in the container. The keys defined within a source must be a C_IDENTIFIER. All invalid keys will be reported as an event when the container is starting. When a key exists in multiple sources, the value associated with the last source will take precedence. Values defined by an Env with a duplicate key will take precedence. Cannot be updated."
        },
    )
    image: Optional[str] = field(
        default=None,
        metadata={
            "description": "Container image name. More info: https://kubernetes.io/docs/concepts/containers/images This field is optional to allow higher level config management to default or override container images in workload controllers like Deployments and StatefulSets."
        },
    )
    imagePullPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More info: https://kubernetes.io/docs/concepts/containers/images#updating-images"
        },
    )
    lifecycle: Optional[V1Lifecycle] = field(
        default=None,
        metadata={
            "description": "Actions that the management system should take in response to container lifecycle events. Cannot be updated."
        },
    )
    livenessProbe: Optional[V1Probe] = field(
        default=None,
        metadata={
            "description": "Periodic probe of container liveness. Container will be restarted if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        },
    )
    ports: Optional[List[V1ContainerPort]] = field(
        default=None,
        metadata={
            "description": 'List of ports to expose from the container. Not specifying a port here DOES NOT prevent that port from being exposed. Any port which is listening on the default "0.0.0.0" address inside a container will be accessible from the network. Modifying this array with strategic merge patch may corrupt the data. For more information See https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated.'
        },
    )
    readinessProbe: Optional[V1Probe] = field(
        default=None,
        metadata={
            "description": "Periodic probe of container service readiness. Container will be removed from service endpoints if the probe fails. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        },
    )
    resizePolicy: Optional[List[V1ContainerResizePolicy]] = field(
        default=None,
        metadata={"description": "Resources resize policy for the container."},
    )
    resources: Optional[V1ResourceRequirements] = field(
        default=None,
        metadata={
            "description": "Compute Resources required by this container. Cannot be updated. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        },
    )
    restartPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": 'RestartPolicy defines the restart behavior of individual containers in a pod. This field may only be set for init containers, and the only allowed value is "Always". For non-init containers or when this field is not specified, the restart behavior is defined by the Pod\'s restart policy and the container type. Setting the RestartPolicy as "Always" for the init container will have the following effect: this init container will be continually restarted on exit until all regular containers have terminated. Once all regular containers have completed, all init containers with restartPolicy "Always" will be shut down. This lifecycle differs from normal init containers and is often referred to as a "sidecar" container. Although this init container still starts in the init container sequence, it does not wait for the container to complete before proceeding to the next init container. Instead, the next init container starts immediately after this init container is started, or after any startupProbe has successfully completed.'
        },
    )
    securityContext: Optional[V1SecurityContext] = field(
        default=None,
        metadata={
            "description": "SecurityContext defines the security options the container should be run with. If set, the fields of SecurityContext override the equivalent fields of PodSecurityContext. More info: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/"
        },
    )
    startupProbe: Optional[V1Probe] = field(
        default=None,
        metadata={
            "description": "StartupProbe indicates that the Pod has successfully initialized. If specified, no other probes are executed until this completes successfully. If this probe fails, the Pod will be restarted, just as if the livenessProbe failed. This can be used to provide different probe parameters at the beginning of a Pod's lifecycle, when it might take a long time to load data or warm a cache, than during steady-state operation. This cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes"
        },
    )
    stdin: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether this container should allocate a buffer for stdin in the container runtime. If this is not set, reads from stdin in the container will always result in EOF. Default is false."
        },
    )
    stdinOnce: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether the container runtime should close the stdin channel after it has been opened by a single attach. When stdin is true the stdin stream will remain open across multiple attach sessions. If stdinOnce is set to true, stdin is opened on container start, is empty until the first client attaches to stdin, and then remains open and accepts data until the client disconnects, at which time stdin is closed and remains closed until the container is restarted. If this flag is false, a container processes that reads from stdin will never receive an EOF. Default is false"
        },
    )
    terminationMessagePath: Optional[str] = field(
        default=None,
        metadata={
            "description": "Optional: Path at which the file to which the container's termination message will be written is mounted into the container's filesystem. Message written is intended to be brief final status, such as an assertion failure message. Will be truncated by the node if greater than 4096 bytes. The total message length across all containers will be limited to 12kb. Defaults to /dev/termination-log. Cannot be updated."
        },
    )
    terminationMessagePolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Indicate how the termination message should be populated. File will use the contents of terminationMessagePath to populate the container status message on both success and failure. FallbackToLogsOnError will use the last chunk of container log output if the termination message file is empty and the container exited with an error. The log output is limited to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot be updated."
        },
    )
    tty: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether this container should allocate a TTY for itself, also requires 'stdin' to be true. Default is false."
        },
    )
    volumeDevices: Optional[List[V1VolumeDevice]] = field(
        default=None,
        metadata={
            "description": "volumeDevices is the list of block devices to be used by the container."
        },
    )
    volumeMounts: Optional[List[V1VolumeMount]] = field(
        default=None,
        metadata={
            "description": "Pod volumes to mount into the container's filesystem. Cannot be updated."
        },
    )
    workingDir: Optional[str] = field(
        default=None,
        metadata={
            "description": "Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Cannot be updated."
        },
    )


@define(kw_only=True)
class V1PodDNSConfigOption:
    name: Optional[str] = field(default=None, metadata={"description": "Required."})
    value: Optional[str] = field(default=None)


@define(kw_only=True)
class V1PodDNSConfig:
    nameservers: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "A list of DNS name server IP addresses. This will be appended to the base nameservers generated from DNSPolicy. Duplicated nameservers will be removed."
        },
    )
    options: Optional[List[V1PodDNSConfigOption]] = field(
        default=None,
        metadata={
            "description": "A list of DNS resolver options. This will be merged with the base options generated from DNSPolicy. Duplicated entries will be removed. Resolution options given in Options will override those that appear in the base DNSPolicy."
        },
    )
    searches: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "A list of DNS search domains for host-name lookup. This will be appended to the base search paths generated from DNSPolicy. Duplicated search paths will be removed."
        },
    )


@define(kw_only=True)
class V1EphemeralContainer:
    name: str = field(
        metadata={
            "description": "Name of the ephemeral container specified as a DNS_LABEL. This name must be unique among all containers, init containers and ephemeral containers."
        }
    )
    args: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'Arguments to the entrypoint. The image\'s CMD is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container\'s environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell'
        },
    )
    command: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": 'Entrypoint array. Not executed within a shell. The image\'s ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container\'s environment. If a variable cannot be resolved, the reference in the input string will be unchanged. Double $$ are reduced to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped references will never be expanded, regardless of whether the variable exists or not. Cannot be updated. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell'
        },
    )
    env: Optional[List[V1EnvVar]] = field(
        default=None,
        metadata={
            "description": "List of environment variables to set in the container. Cannot be updated."
        },
    )
    envFrom: Optional[List[V1EnvFromSource]] = field(
        default=None,
        metadata={
            "description": "List of sources to populate environment variables in the container. The keys defined within a source must be a C_IDENTIFIER. All invalid keys will be reported as an event when the container is starting. When a key exists in multiple sources, the value associated with the last source will take precedence. Values defined by an Env with a duplicate key will take precedence. Cannot be updated."
        },
    )
    image: Optional[str] = field(
        default=None,
        metadata={
            "description": "Container image name. More info: https://kubernetes.io/docs/concepts/containers/images"
        },
    )
    imagePullPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More info: https://kubernetes.io/docs/concepts/containers/images#updating-images"
        },
    )
    lifecycle: Optional[V1Lifecycle] = field(
        default=None,
        metadata={"description": "Lifecycle is not allowed for ephemeral containers."},
    )
    livenessProbe: Optional[V1Probe] = field(
        default=None,
        metadata={"description": "Probes are not allowed for ephemeral containers."},
    )
    ports: Optional[List[V1ContainerPort]] = field(
        default=None,
        metadata={"description": "Ports are not allowed for ephemeral containers."},
    )
    readinessProbe: Optional[V1Probe] = field(
        default=None,
        metadata={"description": "Probes are not allowed for ephemeral containers."},
    )
    resizePolicy: Optional[List[V1ContainerResizePolicy]] = field(
        default=None,
        metadata={"description": "Resources resize policy for the container."},
    )
    resources: Optional[V1ResourceRequirements] = field(
        default=None,
        metadata={
            "description": "Resources are not allowed for ephemeral containers. Ephemeral containers use spare resources already allocated to the pod."
        },
    )
    restartPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Restart policy for the container to manage the restart behavior of each container within a pod. This may only be set for init containers. You cannot set this field on ephemeral containers."
        },
    )
    securityContext: Optional[V1SecurityContext] = field(
        default=None,
        metadata={
            "description": "Optional: SecurityContext defines the security options the ephemeral container should be run with. If set, the fields of SecurityContext override the equivalent fields of PodSecurityContext."
        },
    )
    startupProbe: Optional[V1Probe] = field(
        default=None,
        metadata={"description": "Probes are not allowed for ephemeral containers."},
    )
    stdin: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether this container should allocate a buffer for stdin in the container runtime. If this is not set, reads from stdin in the container will always result in EOF. Default is false."
        },
    )
    stdinOnce: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether the container runtime should close the stdin channel after it has been opened by a single attach. When stdin is true the stdin stream will remain open across multiple attach sessions. If stdinOnce is set to true, stdin is opened on container start, is empty until the first client attaches to stdin, and then remains open and accepts data until the client disconnects, at which time stdin is closed and remains closed until the container is restarted. If this flag is false, a container processes that reads from stdin will never receive an EOF. Default is false"
        },
    )
    targetContainerName: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
If set, the name of the container from PodSpec that this ephemeral container targets. The ephemeral container will be run in the namespaces (IPC, PID, etc) of this container. If not set then the ephemeral container uses the namespaces configured in the Pod spec.

The container runtime must implement support for this feature. If the runtime does not support namespace targeting then the result of setting this field is undefined.
"""
        },
    )
    terminationMessagePath: Optional[str] = field(
        default=None,
        metadata={
            "description": "Optional: Path at which the file to which the container's termination message will be written is mounted into the container's filesystem. Message written is intended to be brief final status, such as an assertion failure message. Will be truncated by the node if greater than 4096 bytes. The total message length across all containers will be limited to 12kb. Defaults to /dev/termination-log. Cannot be updated."
        },
    )
    terminationMessagePolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Indicate how the termination message should be populated. File will use the contents of terminationMessagePath to populate the container status message on both success and failure. FallbackToLogsOnError will use the last chunk of container log output if the termination message file is empty and the container exited with an error. The log output is limited to 2048 bytes or 80 lines, whichever is smaller. Defaults to File. Cannot be updated."
        },
    )
    tty: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether this container should allocate a TTY for itself, also requires 'stdin' to be true. Default is false."
        },
    )
    volumeDevices: Optional[List[V1VolumeDevice]] = field(
        default=None,
        metadata={
            "description": "volumeDevices is the list of block devices to be used by the container."
        },
    )
    volumeMounts: Optional[List[V1VolumeMount]] = field(
        default=None,
        metadata={
            "description": "Pod volumes to mount into the container's filesystem. Subpath mounts are not allowed for ephemeral containers. Cannot be updated."
        },
    )
    workingDir: Optional[str] = field(
        default=None,
        metadata={
            "description": "Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Cannot be updated."
        },
    )


@define(kw_only=True)
class V1HostAlias:
    hostnames: Optional[List[str]] = field(
        default=None, metadata={"description": "Hostnames for the above IP address."}
    )
    ip: Optional[str] = field(
        default=None, metadata={"description": "IP address of the host file entry."}
    )


@define(kw_only=True)
class V1LocalObjectReference:
    name: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        },
    )


@define(kw_only=True)
class V1PodOS:
    name: str = field(
        metadata={
            "description": "Name is the name of the operating system. The currently supported values are linux and windows. Additional value may be defined in future and can be one of: https://github.com/opencontainers/runtime-spec/blob/master/config.md#platform-specific-configuration Clients should expect to handle additional values and treat unrecognized values in this field as os: null"
        }
    )


@define(kw_only=True)
class V1PodReadinessGate:
    conditionType: str = field(
        metadata={
            "description": "ConditionType refers to a condition in the pod's condition list with matching type."
        }
    )


@define(kw_only=True)
class V1ClaimSource:
    resourceClaimName: Optional[str] = field(
        default=None,
        metadata={
            "description": "ResourceClaimName is the name of a ResourceClaim object in the same namespace as this pod."
        },
    )
    resourceClaimTemplateName: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
ResourceClaimTemplateName is the name of a ResourceClaimTemplate object in the same namespace as this pod.

The template will be used to create a new ResourceClaim, which will be bound to this pod. When this pod is deleted, the ResourceClaim will also be deleted. The pod name and resource name, along with a generated component, will be used to form a unique name for the ResourceClaim, which will be recorded in pod.status.resourceClaimStatuses.

This field is immutable and no changes will be made to the corresponding ResourceClaim by the control plane after creating the ResourceClaim.
"""
        },
    )


@define(kw_only=True)
class V1PodResourceClaim:
    name: str = field(
        metadata={
            "description": "Name uniquely identifies this resource claim inside the pod. This must be a DNS_LABEL."
        }
    )
    source: Optional[V1ClaimSource] = field(
        default=None,
        metadata={"description": "Source describes where to find the ResourceClaim."},
    )


@define(kw_only=True)
class V1PodSchedulingGate:
    name: str = field(
        metadata={
            "description": "Name of the scheduling gate. Each scheduling gate must have a unique name field."
        }
    )


@define(kw_only=True)
class V1Sysctl:
    name: str = field(metadata={"description": "Name of a property to set"})
    value: str = field(metadata={"description": "Value of a property to set"})


@define(kw_only=True)
class V1PodSecurityContext:
    fsGroup: Optional[int] = field(
        default=None,
        metadata={
            "description": """\
A special supplemental group that applies to all containers in a pod. Some volume types allow the Kubelet to change the ownership of that volume to be owned by the pod:

1. The owning GID will be the FSGroup 2. The setgid bit is set (new files created in the volume will be owned by FSGroup) 3. The permission bits are OR'd with rw-rw
"""
        },
    )
    fsGroupChangePolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsGroupChangePolicy defines behavior of changing ownership and permission of the volume before being exposed inside Pod. This field will only apply to volume types which support fsGroup based ownership(and permissions). It will have no effect on ephemeral volume types such as: secret, configmaps and emptydir. Valid values are "OnRootMismatch" and "Always". If not specified, "Always" is used. Note that this field cannot be set when spec.os.name is windows.'
        },
    )
    runAsGroup: Optional[int] = field(
        default=None,
        metadata={
            "description": "The GID to run the entrypoint of the container process. Uses runtime default if unset. May also be set in SecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence for that container. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    runAsNonRoot: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Indicates that the container must run as a non-root user. If true, the Kubelet will validate the image at runtime to ensure that it does not run as UID 0 (root) and fail to start the container if it does. If unset or false, no such validation will be performed. May also be set in SecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence."
        },
    )
    runAsUser: Optional[int] = field(
        default=None,
        metadata={
            "description": "The UID to run the entrypoint of the container process. Defaults to user specified in image metadata if unspecified. May also be set in SecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence for that container. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    seLinuxOptions: Optional[V1SELinuxOptions] = field(
        default=None,
        metadata={
            "description": "The SELinux context to be applied to all containers. If unspecified, the container runtime will allocate a random SELinux context for each container.  May also be set in SecurityContext.  If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence for that container. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    seccompProfile: Optional[V1SeccompProfile] = field(
        default=None,
        metadata={
            "description": "The seccomp options to use by the containers in this pod. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    supplementalGroups: Optional[List[int]] = field(
        default=None,
        metadata={
            "description": "A list of groups applied to the first process run in each container, in addition to the container's primary GID, the fsGroup (if specified), and group memberships defined in the container image for the uid of the container process. If unspecified, no additional groups are added to any container. Note that group memberships defined in the container image for the uid of the container process are still effective, even if they are not included in this list. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    sysctls: Optional[List[V1Sysctl]] = field(
        default=None,
        metadata={
            "description": "Sysctls hold a list of namespaced sysctls used for the pod. Pods with unsupported sysctls (by the container runtime) might fail to launch. Note that this field cannot be set when spec.os.name is windows."
        },
    )
    windowsOptions: Optional[V1WindowsSecurityContextOptions] = field(
        default=None,
        metadata={
            "description": "The Windows specific settings applied to all containers. If unspecified, the options within a container's SecurityContext will be used. If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence. Note that this field cannot be set when spec.os.name is linux."
        },
    )


@define(kw_only=True)
class V1Toleration:
    effect: Optional[str] = field(
        default=None,
        metadata={
            "description": "Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute."
        },
    )
    key: Optional[str] = field(
        default=None,
        metadata={
            "description": "Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys."
        },
    )
    operator: Optional[str] = field(
        default=None,
        metadata={
            "description": "Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category."
        },
    )
    tolerationSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system."
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "description": "Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string."
        },
    )


@define(kw_only=True)
class V1TopologySpreadConstraint:
    maxSkew: int = field(
        metadata={
            "description": "MaxSkew describes the degree to which pods may be unevenly distributed. When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference between the number of matching pods in the target topology and the global minimum. The global minimum is the minimum number of matching pods in an eligible domain or zero if the number of eligible domains is less than MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 2/2/1: In this case, the global minimum is 1."
        }
    )
    topologyKey: str = field(
        metadata={
            "description": 'TopologyKey is the key of node labels. Nodes that have a label with this key and identical values are considered to be in the same topology. We consider each <key, value> as a "bucket", and try to put balanced number of pods into each bucket. We define a domain as a particular instance of a topology. Also, we define an eligible domain as a domain whose nodes meet the requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey is "kubernetes.io/hostname", each Node is a domain of that topology. And, if TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that topology. It\'s a required field.'
        }
    )
    whenUnsatisfiable: str = field(
        metadata={
            "description": """\
WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the scheduler not to schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any location,
  but giving higher precedence to topologies that would help reduce the
  skew.
A constraint is considered \"Unsatisfiable\" for an incoming pod if and only if every possible node assignment for that pod would violate \"MaxSkew\" on some topology. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1:
"""
        }
    )
    labelSelector: Optional[V1LabelSelector] = field(
        default=None,
        metadata={
            "description": "LabelSelector is used to find matching pods. Pods that match this label selector are counted to determine the number of pods in their corresponding topology domain."
        },
    )
    matchLabelKeys: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": """\
MatchLabelKeys is a set of pod label keys to select the pods over which spreading will be calculated. The keys are used to lookup values from the incoming pod labels, those key-value labels are ANDed with labelSelector to select the group of existing pods over which spreading will be calculated for the incoming pod. The same key is forbidden to exist in both MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when LabelSelector isn't set. Keys that don't exist in the incoming pod labels will be ignored. A null or empty list means only match against labelSelector.

This is a beta field and requires the MatchLabelKeysInPodTopologySpread feature gate to be enabled (enabled by default).
"""
        },
    )
    minDomains: Optional[int] = field(
        default=None,
        metadata={
            "description": """\
MinDomains indicates a minimum number of eligible domains. When the number of eligible domains with matching topology keys is less than minDomains, Pod Topology Spread treats \"global minimum\" as 0, and then the calculation of Skew is performed. And when the number of eligible domains with matching topology keys equals or greater than minDomains, this value has no effect on scheduling. As a result, when the number of eligible domains is less than minDomains, scheduler won't schedule more than maxSkew Pods to those domains. If value is nil, the constraint behaves as if MinDomains is equal to 1. Valid values are integers greater than 0. When value is not nil, WhenUnsatisfiable must be DoNotSchedule.

For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to 5 and pods with the same labelSelector spread as 2/2/2:
"""
        },
    )
    nodeAffinityPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
NodeAffinityPolicy indicates how we will treat Pod's nodeAffinity/nodeSelector when calculating pod topology spread skew. Options are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in the calculations.

If this value is nil, the behavior is equivalent to the Honor policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag.
"""
        },
    )
    nodeTaintsPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": """\
NodeTaintsPolicy indicates how we will treat node taints when calculating pod topology spread skew. Options are: - Honor: nodes without taints, along with tainted nodes for which the incoming pod has a toleration, are included. - Ignore: node taints are ignored. All nodes are included.

If this value is nil, the behavior is equivalent to the Ignore policy. This is a beta-level feature default enabled by the NodeInclusionPolicyInPodTopologySpread feature flag.
"""
        },
    )


@define(kw_only=True)
class V1AWSElasticBlockStoreVolumeSource:
    volumeID: str = field(
        metadata={
            "description": "volumeID is unique ID of the persistent disk resource in AWS (Amazon EBS volume). More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore'
        },
    )
    partition: Optional[int] = field(
        default=None,
        metadata={
            "description": 'partition is the partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty).'
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly value true will force the readOnly setting in VolumeMounts. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        },
    )


@define(kw_only=True)
class V1AzureDiskVolumeSource:
    diskName: str = field(
        metadata={
            "description": "diskName is the Name of the data disk in the blob storage"
        }
    )
    diskURI: str = field(
        metadata={"description": "diskURI is the URI of data disk in the blob storage"}
    )
    cachingMode: Optional[str] = field(
        default=None,
        metadata={
            "description": "cachingMode is the Host Caching mode: None, Read Only, Read Write."
        },
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is Filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "kind expected values are Shared: multiple blob disks per storage account  Dedicated: single blob disk per storage account  Managed: azure managed data disk (only in managed availability set). defaults to shared"
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )


@define(kw_only=True)
class V1AzureFileVolumeSource:
    secretName: str = field(
        metadata={
            "description": "secretName is the  name of secret that contains Azure Storage Account Name and Key"
        }
    )
    shareName: str = field(
        metadata={"description": "shareName is the azure share Name"}
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )


@define(kw_only=True)
class V1CephFSVolumeSource:
    monitors: List[str] = field(
        metadata={
            "description": "monitors is Required: Monitors is a collection of Ceph monitors More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        }
    )
    path: Optional[str] = field(
        default=None,
        metadata={
            "description": "path is Optional: Used as the mounted root, rather than the full Ceph tree, default is /"
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly is Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        },
    )
    secretFile: Optional[str] = field(
        default=None,
        metadata={
            "description": "secretFile is Optional: SecretFile is the path to key ring for User, default is /etc/ceph/user.secret More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef is Optional: SecretRef is reference to the authentication secret for User, default is empty. More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        },
    )
    user: Optional[str] = field(
        default=None,
        metadata={
            "description": "user is optional: User is the rados user name, default is admin More info: https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it"
        },
    )


@define(kw_only=True)
class V1CinderVolumeSource:
    volumeID: str = field(
        metadata={
            "description": "volumeID used to identify the volume in cinder. More info: https://examples.k8s.io/mysql-cinder-pd/README.md"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://examples.k8s.io/mysql-cinder-pd/README.md'
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts. More info: https://examples.k8s.io/mysql-cinder-pd/README.md"
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef is optional: points to a secret object containing parameters used to connect to OpenStack."
        },
    )


@define(kw_only=True)
class V1ConfigMapVolumeSource:
    defaultMode: Optional[int] = field(
        default=None,
        metadata={
            "description": "defaultMode is optional: mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set."
        },
    )
    items: Optional[List[Any]] = field(
        default=None,
        metadata={
            "description": "items if unspecified, each key-value pair in the Data field of the referenced ConfigMap will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the ConfigMap, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'."
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        },
    )
    optional: Optional[bool] = field(
        default=None,
        metadata={
            "description": "optional specify whether the ConfigMap or its keys must be defined"
        },
    )


@define(kw_only=True)
class V1CSIVolumeSource:
    driver: str = field(
        metadata={
            "description": "driver is the name of the CSI driver that handles this volume. Consult with your admin for the correct name as registered in the cluster."
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType to mount. Ex. "ext4", "xfs", "ntfs". If not provided, the empty value is passed to the associated CSI driver which will determine the default filesystem to apply.'
        },
    )
    nodePublishSecretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "nodePublishSecretRef is a reference to the secret object containing sensitive information to pass to the CSI driver to complete the CSI NodePublishVolume and NodeUnpublishVolume calls. This field is optional, and  may be empty if no secret is required. If the secret object contains more than one secret, all secret references are passed."
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly specifies a read-only configuration for the volume. Defaults to false (read/write)."
        },
    )
    volumeAttributes: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "volumeAttributes stores driver-specific properties that are passed to the CSI driver. Consult your driver's documentation for supported values."
        },
    )


@define(kw_only=True)
class V1DownwardAPIVolumeSource:
    defaultMode: Optional[int] = field(
        default=None,
        metadata={
            "description": "Optional: mode bits to use on created files by default. Must be a Optional: mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set."
        },
    )
    items: Optional[List[Any]] = field(
        default=None,
        metadata={"description": "Items is a list of downward API volume file"},
    )


@define(kw_only=True)
class V1EmptyDirVolumeSource:
    medium: Optional[str] = field(
        default=None,
        metadata={
            "description": 'medium represents what type of storage medium should back this directory. The default is "" which means to use the node\'s default medium. Must be an empty string (default) or Memory. More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir'
        },
    )
    sizeLimit: Optional[str] = field(
        default=None,
        metadata={
            "description": "sizeLimit is the total amount of local storage required for this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir"
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaimTemplate:
    spec: Any = field(
        metadata={
            "description": "The specification for the PersistentVolumeClaim. The entire content is copied unchanged into the PVC that gets created from this template. The same fields as in a PersistentVolumeClaim are also valid here."
        }
    )
    metadata: Optional[Any] = field(
        default=None,
        metadata={
            "description": "May contain labels and annotations that will be copied into the PVC when creating it. No other fields are allowed and will be rejected during validation."
        },
    )


@define(kw_only=True)
class V1EphemeralVolumeSource:
    volumeClaimTemplate: Optional[V1PersistentVolumeClaimTemplate] = field(
        default=None,
        metadata={
            "description": """\
Will be used to create a stand-alone PVC to provision the volume. The pod in which this EphemeralVolumeSource is embedded will be the owner of the PVC, i.e. the PVC will be deleted together with the pod.  The name of the PVC will be `<pod name>-<volume name>` where `<volume name>` is the name from the `PodSpec.Volumes` array entry. Pod validation will reject the pod if the concatenated name is not valid for a PVC (for example, too long).

An existing PVC with that name that is not owned by the pod will *not* be used for the pod to avoid using an unrelated volume by mistake. Starting the pod is then blocked until the unrelated PVC is removed. If such a pre-created PVC is meant to be used by the pod, the PVC has to updated with an owner reference to the pod once the pod exists. Normally this should not be necessary, but it may be useful when manually reconstructing a broken cluster.

This field is read-only and no changes will be made by Kubernetes to the PVC after it has been created.

Required, must not be nil.
"""
        },
    )


@define(kw_only=True)
class V1FCVolumeSource:
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )
    lun: Optional[int] = field(
        default=None, metadata={"description": "lun is Optional: FC target lun number"}
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly is Optional: Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )
    targetWWNs: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "targetWWNs is Optional: FC target worldwide names (WWNs)"
        },
    )
    wwids: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "wwids Optional: FC volume world wide identifiers (wwids) Either wwids or combination of targetWWNs and lun must be set, but not both simultaneously."
        },
    )


@define(kw_only=True)
class V1FlexVolumeSource:
    driver: str = field(
        metadata={
            "description": "driver is the name of the driver to use for this volume."
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem depends on FlexVolume script.'
        },
    )
    options: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "options is Optional: this field holds extra command options if any."
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly is Optional: defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef is Optional: secretRef is reference to the secret object containing sensitive information to pass to the plugin scripts. This may be empty if no secret object is specified. If the secret object contains more than one secret, all secrets are passed to the plugin scripts."
        },
    )


@define(kw_only=True)
class V1FlockerVolumeSource:
    datasetName: Optional[str] = field(
        default=None,
        metadata={
            "description": "datasetName is Name of the dataset stored as metadata -> name on the dataset for Flocker should be considered as deprecated"
        },
    )
    datasetUUID: Optional[str] = field(
        default=None,
        metadata={
            "description": "datasetUUID is the UUID of the dataset. This is unique identifier of a Flocker dataset"
        },
    )


@define(kw_only=True)
class V1GCEPersistentDiskVolumeSource:
    pdName: str = field(
        metadata={
            "description": "pdName is unique name of the PD resource in GCE. Used to identify the disk in GCE. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk'
        },
    )
    partition: Optional[int] = field(
        default=None,
        metadata={
            "description": 'partition is the partition in the volume that you want to mount. If omitted, the default is to mount by volume name. Examples: For volume /dev/sda1, you specify the partition as "1". Similarly, the volume partition for /dev/sda is "0" (or you can leave the property empty). More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk'
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        },
    )


@define(kw_only=True)
class V1GitRepoVolumeSource:
    repository: str = field(metadata={"description": "repository is the URL"})
    directory: Optional[str] = field(
        default=None,
        metadata={
            "description": "directory is the target directory name. Must not contain or start with '..'.  If '.' is supplied, the volume directory will be the git repository.  Otherwise, if specified, the volume will contain the git repository in the subdirectory with the given name."
        },
    )
    revision: Optional[str] = field(
        default=None,
        metadata={
            "description": "revision is the commit hash for the specified revision."
        },
    )


@define(kw_only=True)
class V1GlusterfsVolumeSource:
    endpoints: str = field(
        metadata={
            "description": "endpoints is the endpoint name that details Glusterfs topology. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        }
    )
    path: str = field(
        metadata={
            "description": "path is the Glusterfs volume path. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        }
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the Glusterfs volume to be mounted with read-only permissions. Defaults to false. More info: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod"
        },
    )


@define(kw_only=True)
class V1HostPathVolumeSource:
    path: str = field(
        metadata={
            "description": "path of the directory on the host. If the path is a symlink, it will follow the link to the real path. More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath"
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": 'type for HostPath Volume Defaults to "" More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath'
        },
    )


@define(kw_only=True)
class V1ISCSIVolumeSource:
    iqn: str = field(
        metadata={"description": "iqn is the target iSCSI Qualified Name."}
    )
    lun: int = field(
        metadata={"description": "lun represents iSCSI Target Lun number."}
    )
    targetPortal: str = field(
        metadata={
            "description": "targetPortal is iSCSI Target Portal. The Portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260)."
        }
    )
    chapAuthDiscovery: Optional[bool] = field(
        default=None,
        metadata={
            "description": "chapAuthDiscovery defines whether support iSCSI Discovery CHAP authentication"
        },
    )
    chapAuthSession: Optional[bool] = field(
        default=None,
        metadata={
            "description": "chapAuthSession defines whether support iSCSI Session CHAP authentication"
        },
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi'
        },
    )
    initiatorName: Optional[str] = field(
        default=None,
        metadata={
            "description": "initiatorName is the custom iSCSI Initiator Name. If initiatorName is specified with iscsiInterface simultaneously, new iSCSI interface <target portal>:<volume name> will be created for the connection."
        },
    )
    iscsiInterface: Optional[str] = field(
        default=None,
        metadata={
            "description": "iscsiInterface is the interface Name that uses an iSCSI transport. Defaults to 'default' (tcp)."
        },
    )
    portals: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "portals is the iSCSI Target Portal List. The portal is either an IP or ip_addr:port if the port is other than default (typically TCP ports 860 and 3260)."
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false."
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef is the CHAP Secret for iSCSI target and initiator authentication"
        },
    )


@define(kw_only=True)
class V1NFSVolumeSource:
    path: str = field(
        metadata={
            "description": "path that is exported by the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        }
    )
    server: str = field(
        metadata={
            "description": "server is the hostname or IP address of the NFS server. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        }
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the NFS export to be mounted with read-only permissions. Defaults to false. More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaimVolumeSource:
    claimName: str = field(
        metadata={
            "description": "claimName is the name of a PersistentVolumeClaim in the same namespace as the pod using this volume. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        }
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly Will force the ReadOnly setting in VolumeMounts. Default false."
        },
    )


@define(kw_only=True)
class V1PhotonPersistentDiskVolumeSource:
    pdID: str = field(
        metadata={
            "description": "pdID is the ID that identifies Photon Controller persistent disk"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )


@define(kw_only=True)
class V1PortworxVolumeSource:
    volumeID: str = field(
        metadata={"description": "volumeID uniquely identifies a Portworx volume"}
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fSType represents the filesystem type to mount Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )


@define(kw_only=True)
class V1ProjectedVolumeSource:
    sources: List[Any] = field(
        metadata={"description": "sources is the list of volume projections"}
    )
    defaultMode: Optional[int] = field(
        default=None,
        metadata={
            "description": "defaultMode are the mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set."
        },
    )


@define(kw_only=True)
class V1QuobyteVolumeSource:
    registry: str = field(
        metadata={
            "description": "registry represents a single or multiple Quobyte Registry services specified as a string as host:port pair (multiple entries are separated with commas) which acts as the central registry for volumes"
        }
    )
    volume: str = field(
        metadata={
            "description": "volume is a string that references an already created Quobyte volume by name."
        }
    )
    group: Optional[str] = field(
        default=None,
        metadata={"description": "group to map volume access to Default is no group"},
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the Quobyte volume to be mounted with read-only permissions. Defaults to false."
        },
    )
    tenant: Optional[str] = field(
        default=None,
        metadata={
            "description": "tenant owning the given Quobyte volume in the Backend Used with dynamically provisioned Quobyte volumes, value is set by the plugin"
        },
    )
    user: Optional[str] = field(
        default=None,
        metadata={
            "description": "user to map volume access to Defaults to serivceaccount user"
        },
    )


@define(kw_only=True)
class V1RBDVolumeSource:
    image: str = field(
        metadata={
            "description": "image is the rados image name. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        }
    )
    monitors: List[str] = field(
        metadata={
            "description": "monitors is a collection of Ceph monitors. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type of the volume that you want to mount. Tip: Ensure that the filesystem type is supported by the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More info: https://kubernetes.io/docs/concepts/storage/volumes#rbd'
        },
    )
    keyring: Optional[str] = field(
        default=None,
        metadata={
            "description": "keyring is the path to key ring for RBDUser. Default is /etc/ceph/keyring. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        },
    )
    pool: Optional[str] = field(
        default=None,
        metadata={
            "description": "pool is the rados pool name. Default is rbd. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly here will force the ReadOnly setting in VolumeMounts. Defaults to false. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef is name of the authentication secret for RBDUser. If provided overrides keyring. Default is nil. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        },
    )
    user: Optional[str] = field(
        default=None,
        metadata={
            "description": "user is the rados user name. Default is admin. More info: https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it"
        },
    )


@define(kw_only=True)
class V1ScaleIOVolumeSource:
    gateway: str = field(
        metadata={
            "description": "gateway is the host address of the ScaleIO API Gateway."
        }
    )
    secretRef: V1LocalObjectReference = field(
        metadata={
            "description": "secretRef references to the secret for ScaleIO user and other sensitive information. If this is not provided, Login operation will fail."
        }
    )
    system: str = field(
        metadata={
            "description": "system is the name of the storage system as configured in ScaleIO."
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Default is "xfs".'
        },
    )
    protectionDomain: Optional[str] = field(
        default=None,
        metadata={
            "description": "protectionDomain is the name of the ScaleIO Protection Domain for the configured storage."
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )
    sslEnabled: Optional[bool] = field(
        default=None,
        metadata={
            "description": "sslEnabled Flag enable/disable SSL communication with Gateway, default false"
        },
    )
    storageMode: Optional[str] = field(
        default=None,
        metadata={
            "description": "storageMode indicates whether the storage for a volume should be ThickProvisioned or ThinProvisioned. Default is ThinProvisioned."
        },
    )
    storagePool: Optional[str] = field(
        default=None,
        metadata={
            "description": "storagePool is the ScaleIO Storage Pool associated with the protection domain."
        },
    )
    volumeName: Optional[str] = field(
        default=None,
        metadata={
            "description": "volumeName is the name of a volume already created in the ScaleIO system that is associated with this volume source."
        },
    )


@define(kw_only=True)
class V1SecretVolumeSource:
    defaultMode: Optional[int] = field(
        default=None,
        metadata={
            "description": "defaultMode is Optional: mode bits used to set permissions on created files by default. Must be an octal value between 0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON requires decimal values for mode bits. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set."
        },
    )
    items: Optional[List[Any]] = field(
        default=None,
        metadata={
            "description": "items If unspecified, each key-value pair in the Data field of the referenced Secret will be projected into the volume as a file whose name is the key and content is the value. If specified, the listed keys will be projected into the specified paths, and unlisted keys will not be present. If a key is specified which is not present in the Secret, the volume setup will error unless it is marked optional. Paths must be relative and may not contain the '..' path or start with '..'."
        },
    )
    optional: Optional[bool] = field(
        default=None,
        metadata={
            "description": "optional field specify whether the Secret or its keys must be defined"
        },
    )
    secretName: Optional[str] = field(
        default=None,
        metadata={
            "description": "secretName is the name of the secret in the pod's namespace to use. More info: https://kubernetes.io/docs/concepts/storage/volumes#secret"
        },
    )


@define(kw_only=True)
class V1StorageOSVolumeSource:
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is the filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )
    readOnly: Optional[bool] = field(
        default=None,
        metadata={
            "description": "readOnly defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts."
        },
    )
    secretRef: Optional[V1LocalObjectReference] = field(
        default=None,
        metadata={
            "description": "secretRef specifies the secret to use for obtaining the StorageOS API credentials.  If not specified, default values will be attempted."
        },
    )
    volumeName: Optional[str] = field(
        default=None,
        metadata={
            "description": "volumeName is the human-readable name of the StorageOS volume.  Volume names are only unique within a namespace."
        },
    )
    volumeNamespace: Optional[str] = field(
        default=None,
        metadata={
            "description": 'volumeNamespace specifies the scope of the volume within StorageOS.  If no namespace is specified then the Pod\'s namespace will be used.  This allows the Kubernetes name scoping to be mirrored within StorageOS for tighter integration. Set VolumeName to any name to override the default behaviour. Set to "default" if you are not using namespaces within StorageOS. Namespaces that do not pre-exist within StorageOS will be created.'
        },
    )


@define(kw_only=True)
class V1VsphereVirtualDiskVolumeSource:
    volumePath: str = field(
        metadata={
            "description": "volumePath is the path that identifies vSphere volume vmdk"
        }
    )
    fsType: Optional[str] = field(
        default=None,
        metadata={
            "description": 'fsType is filesystem type to mount. Must be a filesystem type supported by the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified.'
        },
    )
    storagePolicyID: Optional[str] = field(
        default=None,
        metadata={
            "description": "storagePolicyID is the storage Policy Based Management (SPBM) profile ID associated with the StoragePolicyName."
        },
    )
    storagePolicyName: Optional[str] = field(
        default=None,
        metadata={
            "description": "storagePolicyName is the storage Policy Based Management (SPBM) profile name."
        },
    )


@define(kw_only=True)
class V1Volume:
    name: str = field(
        metadata={
            "description": "name of the volume. Must be a DNS_LABEL and unique within the pod. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        }
    )
    awsElasticBlockStore: Optional[V1AWSElasticBlockStoreVolumeSource] = field(
        default=None,
        metadata={
            "description": "awsElasticBlockStore represents an AWS Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore"
        },
    )
    azureDisk: Optional[V1AzureDiskVolumeSource] = field(
        default=None,
        metadata={
            "description": "azureDisk represents an Azure Data Disk mount on the host and bind mount to the pod."
        },
    )
    azureFile: Optional[V1AzureFileVolumeSource] = field(
        default=None,
        metadata={
            "description": "azureFile represents an Azure File Service mount on the host and bind mount to the pod."
        },
    )
    cephfs: Optional[V1CephFSVolumeSource] = field(
        default=None,
        metadata={
            "description": "cephFS represents a Ceph FS mount on the host that shares a pod's lifetime"
        },
    )
    cinder: Optional[V1CinderVolumeSource] = field(
        default=None,
        metadata={
            "description": "cinder represents a cinder volume attached and mounted on kubelets host machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md"
        },
    )
    configMap: Optional[V1ConfigMapVolumeSource] = field(
        default=None,
        metadata={
            "description": "configMap represents a configMap that should populate this volume"
        },
    )
    csi: Optional[V1CSIVolumeSource] = field(
        default=None,
        metadata={
            "description": "csi (Container Storage Interface) represents ephemeral storage that is handled by certain external CSI drivers (Beta feature)."
        },
    )
    downwardAPI: Optional[V1DownwardAPIVolumeSource] = field(
        default=None,
        metadata={
            "description": "downwardAPI represents downward API about the pod that should populate this volume"
        },
    )
    emptyDir: Optional[V1EmptyDirVolumeSource] = field(
        default=None,
        metadata={
            "description": "emptyDir represents a temporary directory that shares a pod's lifetime. More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir"
        },
    )
    ephemeral: Optional[V1EphemeralVolumeSource] = field(
        default=None,
        metadata={
            "description": """\
ephemeral represents a volume that is handled by a cluster storage driver. The volume's lifecycle is tied to the pod that defines it - it will be created before the pod starts, and deleted when the pod is removed.

Use this if: a) the volume is only needed while the pod runs, b) features of normal volumes like restoring from snapshot or capacity
   tracking are needed,
c) the storage driver is specified through a storage class, and d) the storage driver supports dynamic volume provisioning through
   a PersistentVolumeClaim (see EphemeralVolumeSource for more
   information on the connection between this volume type
   and PersistentVolumeClaim).

Use PersistentVolumeClaim or one of the vendor-specific APIs for volumes that persist for longer than the lifecycle of an individual pod.

Use CSI for light-weight local ephemeral volumes if the CSI driver is meant to be used that way - see the documentation of the driver for more information.

A pod can use both types of ephemeral volumes and persistent volumes at the same time.
"""
        },
    )
    fc: Optional[V1FCVolumeSource] = field(
        default=None,
        metadata={
            "description": "fc represents a Fibre Channel resource that is attached to a kubelet's host machine and then exposed to the pod."
        },
    )
    flexVolume: Optional[V1FlexVolumeSource] = field(
        default=None,
        metadata={
            "description": "flexVolume represents a generic volume resource that is provisioned/attached using an exec based plugin."
        },
    )
    flocker: Optional[V1FlockerVolumeSource] = field(
        default=None,
        metadata={
            "description": "flocker represents a Flocker volume attached to a kubelet's host machine. This depends on the Flocker control service being running"
        },
    )
    gcePersistentDisk: Optional[V1GCEPersistentDiskVolumeSource] = field(
        default=None,
        metadata={
            "description": "gcePersistentDisk represents a GCE Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk"
        },
    )
    gitRepo: Optional[V1GitRepoVolumeSource] = field(
        default=None,
        metadata={
            "description": "gitRepo represents a git repository at a particular revision. DEPRECATED: GitRepo is deprecated. To provision a container with a git repo, mount an EmptyDir into an InitContainer that clones the repo using git, then mount the EmptyDir into the Pod's container."
        },
    )
    glusterfs: Optional[V1GlusterfsVolumeSource] = field(
        default=None,
        metadata={
            "description": "glusterfs represents a Glusterfs mount on the host that shares a pod's lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md"
        },
    )
    hostPath: Optional[V1HostPathVolumeSource] = field(
        default=None,
        metadata={
            "description": "hostPath represents a pre-existing file or directory on the host machine that is directly exposed to the container. This is generally used for system agents or other privileged things that are allowed to see the host machine. Most containers will NOT need this. More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath"
        },
    )
    iscsi: Optional[V1ISCSIVolumeSource] = field(
        default=None,
        metadata={
            "description": "iscsi represents an ISCSI Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: https://examples.k8s.io/volumes/iscsi/README.md"
        },
    )
    nfs: Optional[V1NFSVolumeSource] = field(
        default=None,
        metadata={
            "description": "nfs represents an NFS mount on the host that shares a pod's lifetime More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs"
        },
    )
    persistentVolumeClaim: Optional[V1PersistentVolumeClaimVolumeSource] = field(
        default=None,
        metadata={
            "description": "persistentVolumeClaimVolumeSource represents a reference to a PersistentVolumeClaim in the same namespace. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        },
    )
    photonPersistentDisk: Optional[V1PhotonPersistentDiskVolumeSource] = field(
        default=None,
        metadata={
            "description": "photonPersistentDisk represents a PhotonController persistent disk attached and mounted on kubelets host machine"
        },
    )
    portworxVolume: Optional[V1PortworxVolumeSource] = field(
        default=None,
        metadata={
            "description": "portworxVolume represents a portworx volume attached and mounted on kubelets host machine"
        },
    )
    projected: Optional[V1ProjectedVolumeSource] = field(
        default=None,
        metadata={
            "description": "projected items for all in one resources secrets, configmaps, and downward API"
        },
    )
    quobyte: Optional[V1QuobyteVolumeSource] = field(
        default=None,
        metadata={
            "description": "quobyte represents a Quobyte mount on the host that shares a pod's lifetime"
        },
    )
    rbd: Optional[V1RBDVolumeSource] = field(
        default=None,
        metadata={
            "description": "rbd represents a Rados Block Device mount on the host that shares a pod's lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md"
        },
    )
    scaleIO: Optional[V1ScaleIOVolumeSource] = field(
        default=None,
        metadata={
            "description": "scaleIO represents a ScaleIO persistent volume attached and mounted on Kubernetes nodes."
        },
    )
    secret: Optional[V1SecretVolumeSource] = field(
        default=None,
        metadata={
            "description": "secret represents a secret that should populate this volume. More info: https://kubernetes.io/docs/concepts/storage/volumes#secret"
        },
    )
    storageos: Optional[V1StorageOSVolumeSource] = field(
        default=None,
        metadata={
            "description": "storageOS represents a StorageOS volume attached and mounted on Kubernetes nodes."
        },
    )
    vsphereVolume: Optional[V1VsphereVirtualDiskVolumeSource] = field(
        default=None,
        metadata={
            "description": "vsphereVolume represents a vSphere volume attached and mounted on kubelets host machine"
        },
    )


@define(kw_only=True)
class V1PodSpec:
    containers: List[V1Container] = field(
        metadata={
            "description": "List of containers belonging to the pod. Containers cannot currently be added or removed. There must be at least one container in a Pod. Cannot be updated."
        }
    )
    activeDeadlineSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Optional duration in seconds the pod may be active on the node relative to StartTime before the system will actively try to mark it failed and kill associated containers. Value must be a positive integer."
        },
    )
    affinity: Optional[V1Affinity] = field(
        default=None,
        metadata={"description": "If specified, the pod's scheduling constraints"},
    )
    automountServiceAccountToken: Optional[bool] = field(
        default=None,
        metadata={
            "description": "AutomountServiceAccountToken indicates whether a service account token should be automatically mounted."
        },
    )
    dnsConfig: Optional[V1PodDNSConfig] = field(
        default=None,
        metadata={
            "description": "Specifies the DNS parameters of a pod. Parameters specified here will be merged to the generated DNS configuration based on DNSPolicy."
        },
    )
    dnsPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Set DNS policy for the pod. Defaults to \"ClusterFirst\". Valid values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy. To have DNS options set along with hostNetwork, you have to specify DNS policy explicitly to 'ClusterFirstWithHostNet'."
        },
    )
    enableServiceLinks: Optional[bool] = field(
        default=None,
        metadata={
            "description": "EnableServiceLinks indicates whether information about services should be injected into pod's environment variables, matching the syntax of Docker links. Optional: Defaults to true."
        },
    )
    ephemeralContainers: Optional[List[V1EphemeralContainer]] = field(
        default=None,
        metadata={
            "description": "List of ephemeral containers run in this pod. Ephemeral containers may be run in an existing pod to perform user-initiated actions such as debugging. This list cannot be specified when creating a pod, and it cannot be modified by updating the pod spec. In order to add an ephemeral container to an existing pod, use the pod's ephemeralcontainers subresource."
        },
    )
    hostAliases: Optional[List[V1HostAlias]] = field(
        default=None,
        metadata={
            "description": "HostAliases is an optional list of hosts and IPs that will be injected into the pod's hosts file if specified. This is only valid for non-hostNetwork pods."
        },
    )
    hostIPC: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Use the host's ipc namespace. Optional: Default to false."
        },
    )
    hostNetwork: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Host networking requested for this pod. Use the host's network namespace. If this option is set, the ports that will be used must be specified. Default to false."
        },
    )
    hostPID: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Use the host's pid namespace. Optional: Default to false."
        },
    )
    hostUsers: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Use the host's user namespace. Optional: Default to true. If set to true or not present, the pod will be run in the host user namespace, useful for when the pod needs a feature only available to the host user namespace, such as loading a kernel module with CAP_SYS_MODULE. When set to false, a new userns is created for the pod. Setting false is useful for mitigating container breakout vulnerabilities even allowing users to run their containers as root without actually having root privileges on the host. This field is alpha-level and is only honored by servers that enable the UserNamespacesSupport feature."
        },
    )
    hostname: Optional[str] = field(
        default=None,
        metadata={
            "description": "Specifies the hostname of the Pod If not specified, the pod's hostname will be set to a system-defined value."
        },
    )
    imagePullSecrets: Optional[List[V1LocalObjectReference]] = field(
        default=None,
        metadata={
            "description": "ImagePullSecrets is an optional list of references to secrets in the same namespace to use for pulling any of the images used by this PodSpec. If specified, these secrets will be passed to individual puller implementations for them to use. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod"
        },
    )
    initContainers: Optional[List[V1Container]] = field(
        default=None,
        metadata={
            "description": "List of initialization containers belonging to the pod. Init containers are executed in order prior to containers being started. If any init container fails, the pod is considered to have failed and is handled according to its restartPolicy. The name for an init container or normal container must be unique among all containers. Init containers may not have Lifecycle actions, Readiness probes, Liveness probes, or Startup probes. The resourceRequirements of an init container are taken into account during scheduling by finding the highest request/limit for each resource type, and then using the max of of that value or the sum of the normal containers. Limits are applied to init containers in a similar fashion. Init containers cannot currently be added or removed. Cannot be updated. More info: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/"
        },
    )
    nodeName: Optional[str] = field(
        default=None,
        metadata={
            "description": "NodeName is a request to schedule this pod onto a specific node. If it is non-empty, the scheduler simply schedules this pod onto that node, assuming that it fits resource requirements."
        },
    )
    nodeSelector: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "NodeSelector is a selector which must be true for the pod to fit on a node. Selector which must match a node's labels for the pod to be scheduled on that node. More info: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/"
        },
    )
    os: Optional[V1PodOS] = field(
        default=None,
        metadata={
            "description": """\
Specifies the OS of the containers in the pod. Some pod and container fields are restricted if this is set.

If the OS field is set to linux, the following fields must be unset: -securityContext.windowsOptions

If the OS field is set to windows, following fields must be unset: - spec.hostPID - spec.hostIPC - spec.hostUsers - spec.securityContext.seLinuxOptions - spec.securityContext.seccompProfile - spec.securityContext.fsGroup - spec.securityContext.fsGroupChangePolicy - spec.securityContext.sysctls - spec.shareProcessNamespace - spec.securityContext.runAsUser - spec.securityContext.runAsGroup - spec.securityContext.supplementalGroups - spec.containers[*].securityContext.seLinuxOptions - spec.containers[*].securityContext.seccompProfile - spec.containers[*].securityContext.capabilities - spec.containers[*].securityContext.readOnlyRootFilesystem - spec.containers[*].securityContext.privileged - spec.containers[*].securityContext.allowPrivilegeEscalation - spec.containers[*].securityContext.procMount - spec.containers[*].securityContext.runAsUser - spec.containers[*].securityContext.runAsGroup
"""
        },
    )
    overhead: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Overhead represents the resource overhead associated with running a pod for a given RuntimeClass. This field will be autopopulated at admission time by the RuntimeClass admission controller. If the RuntimeClass admission controller is enabled, overhead must not be set in Pod create requests. The RuntimeClass admission controller will reject Pod create requests which have the overhead already set. If RuntimeClass is configured and selected in the PodSpec, Overhead will be set to the value defined in the corresponding RuntimeClass, otherwise it will remain unset and treated as zero. More info: https://git.k8s.io/enhancements/keps/sig-node/688-pod-overhead/README.md"
        },
    )
    preemptionPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "PreemptionPolicy is the Policy for preempting pods with lower priority. One of Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if unset."
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "description": "The priority value. Various system components use this field to find the priority of the pod. When Priority Admission Controller is enabled, it prevents users from setting this field. The admission controller populates this field from PriorityClassName. The higher the value, the higher the priority."
        },
    )
    priorityClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": 'If specified, indicates the pod\'s priority. "system-node-critical" and "system-cluster-critical" are two special keywords which indicate the highest priorities with the former being the highest priority. Any other name must be defined by creating a PriorityClass object with that name. If not specified, the pod priority will be default or zero if there is no default.'
        },
    )
    readinessGates: Optional[List[V1PodReadinessGate]] = field(
        default=None,
        metadata={
            "description": 'If specified, all readiness gates will be evaluated for pod readiness. A pod is ready when all its containers are ready AND all conditions specified in the readiness gates have status equal to "True" More info: https://git.k8s.io/enhancements/keps/sig-network/580-pod-readiness-gates'
        },
    )
    resourceClaims: Optional[List[V1PodResourceClaim]] = field(
        default=None,
        metadata={
            "description": """\
ResourceClaims defines which ResourceClaims must be allocated and reserved before the Pod is allowed to start. The resources will be made available to those containers which consume them by name.

This is an alpha field and requires enabling the DynamicResourceAllocation feature gate.

This field is immutable.
"""
        },
    )
    restartPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "Restart policy for all containers within the pod. One of Always, OnFailure, Never. In some contexts, only a subset of those values may be permitted. Default to Always. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy"
        },
    )
    runtimeClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": 'RuntimeClassName refers to a RuntimeClass object in the node.k8s.io group, which should be used to run this pod.  If no RuntimeClass resource matches the named class, the pod will not be run. If unset or empty, the "legacy" RuntimeClass will be used, which is an implicit class with an empty definition that uses the default runtime handler. More info: https://git.k8s.io/enhancements/keps/sig-node/585-runtime-class'
        },
    )
    schedulerName: Optional[str] = field(
        default=None,
        metadata={
            "description": "If specified, the pod will be dispatched by specified scheduler. If not specified, the pod will be dispatched by default scheduler."
        },
    )
    schedulingGates: Optional[List[V1PodSchedulingGate]] = field(
        default=None,
        metadata={
            "description": """\
SchedulingGates is an opaque list of values that if specified will block scheduling the pod. If schedulingGates is not empty, the pod will stay in the SchedulingGated state and the scheduler will not attempt to schedule the pod.

SchedulingGates can only be set at pod creation time, and be removed only afterwards.

This is a beta feature enabled by the PodSchedulingReadiness feature gate.
"""
        },
    )
    securityContext: Optional[V1PodSecurityContext] = field(
        default=None,
        metadata={
            "description": "SecurityContext holds pod-level security attributes and common container settings. Optional: Defaults to empty.  See type description for default values of each field."
        },
    )
    serviceAccount: Optional[str] = field(
        default=None,
        metadata={
            "description": "DeprecatedServiceAccount is a depreciated alias for ServiceAccountName. Deprecated: Use serviceAccountName instead."
        },
    )
    serviceAccountName: Optional[str] = field(
        default=None,
        metadata={
            "description": "ServiceAccountName is the name of the ServiceAccount to use to run this pod. More info: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/"
        },
    )
    setHostnameAsFQDN: Optional[bool] = field(
        default=None,
        metadata={
            "description": "If true the pod's hostname will be configured as the pod's FQDN, rather than the leaf name (the default). In Linux containers, this means setting the FQDN in the hostname field of the kernel (the nodename field of struct utsname). In Windows containers, this means setting the registry value of hostname for the registry key HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters to FQDN. If a pod does not have FQDN, this has no effect. Default to false."
        },
    )
    shareProcessNamespace: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Share a single process namespace between all of the containers in a pod. When this is set containers will be able to view and signal processes from other containers in the same pod, and the first process in each container will not be assigned PID 1. HostPID and ShareProcessNamespace cannot both be set. Optional: Default to false."
        },
    )
    subdomain: Optional[str] = field(
        default=None,
        metadata={
            "description": 'If specified, the fully qualified Pod hostname will be "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not specified, the pod will not have a domainname at all.'
        },
    )
    terminationGracePeriodSeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Optional duration in seconds the pod needs to terminate gracefully. May be decreased in delete request. Value must be non-negative integer. The value zero indicates stop immediately via the kill signal (no opportunity to shut down). If this value is nil, the default grace period will be used instead. The grace period is the duration in seconds after the processes running in the pod are sent a termination signal and the time when the processes are forcibly halted with a kill signal. Set this value longer than the expected cleanup time for your process. Defaults to 30 seconds."
        },
    )
    tolerations: Optional[List[V1Toleration]] = field(
        default=None, metadata={"description": "If specified, the pod's tolerations."}
    )
    topologySpreadConstraints: Optional[List[V1TopologySpreadConstraint]] = field(
        default=None,
        metadata={
            "description": "TopologySpreadConstraints describes how a group of pods ought to spread across topology domains. Scheduler will schedule pods in a way which abides by the constraints. All topologySpreadConstraints are ANDed."
        },
    )
    volumes: Optional[List[V1Volume]] = field(
        default=None,
        metadata={
            "description": "List of volumes that can be mounted by containers belonging to the pod. More info: https://kubernetes.io/docs/concepts/storage/volumes"
        },
    )


@define(kw_only=True)
class V1PodTemplateSpec:
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    spec: Optional[V1PodSpec] = field(
        default=None,
        metadata={
            "description": "Specification of the desired behavior of the pod. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        },
    )


@define(kw_only=True)
class V1RollingUpdateDaemonSet:
    maxSurge: Optional[str] = field(
        default=None,
        metadata={
            "description": "The maximum number of nodes with an existing available DaemonSet pod that can have an updated DaemonSet pod during during an update. Value can be an absolute number (ex: 5) or a percentage of desired pods (ex: 10%). This can not be 0 if MaxUnavailable is 0. Absolute number is calculated from percentage by rounding up to a minimum of 1. Default value is 0. Example: when this is set to 30%, at most 30% of the total number of nodes that should be running the daemon pod (i.e. status.desiredNumberScheduled) can have their a new pod created before the old pod is marked as deleted. The update starts by launching new pods on 30% of nodes. Once an updated pod is available (Ready for at least minReadySeconds) the old DaemonSet pod on that node is marked deleted. If the old pod becomes unavailable for any reason (Ready transitions to false, is evicted, or is drained) an updated pod is immediatedly created on that node without considering surge limits. Allowing surge implies the possibility that the resources consumed by the daemonset on any given node can double if the readiness check fails, and so resource intensive daemonsets should take into account that they may cause evictions during disruption."
        },
    )
    maxUnavailable: Optional[str] = field(
        default=None,
        metadata={
            "description": "The maximum number of DaemonSet pods that can be unavailable during the update. Value can be an absolute number (ex: 5) or a percentage of total number of DaemonSet pods at the start of the update (ex: 10%). Absolute number is calculated from percentage by rounding up. This cannot be 0 if MaxSurge is 0 Default value is 1. Example: when this is set to 30%, at most 30% of the total number of nodes that should be running the daemon pod (i.e. status.desiredNumberScheduled) can have their pods stopped for an update at any given time. The update starts by stopping at most 30% of those DaemonSet pods and then brings up new DaemonSet pods in their place. Once the new pods are available, it then proceeds onto other DaemonSet pods, thus ensuring that at least 70% of original number of DaemonSet pods are available at all times during the update."
        },
    )


@define(kw_only=True)
class V1DaemonSetUpdateStrategy:
    rollingUpdate: Optional[V1RollingUpdateDaemonSet] = field(
        default=None,
        metadata={
            "description": 'Rolling update config params. Present only if type = "RollingUpdate".'
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": 'Type of daemon set update. Can be "RollingUpdate" or "OnDelete". Default is RollingUpdate.'
        },
    )


@define(kw_only=True)
class V1DaemonSetSpec:
    selector: V1LabelSelector = field(
        metadata={
            "description": "A label query over pods that are managed by the daemon set. Must match in order to be controlled. It must match the pod template's labels. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        }
    )
    template: V1PodTemplateSpec = field(
        metadata={
            "description": 'An object that describes the pod that will be created. The DaemonSet will create exactly one copy of this pod on every node that matches the template\'s node selector (or on every node if no node selector is specified). The only allowed template.spec.restartPolicy value is "Always". More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template'
        }
    )
    minReadySeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "The minimum number of seconds for which a newly created DaemonSet pod should be ready without any of its container crashing, for it to be considered available. Defaults to 0 (pod will be considered available as soon as it is ready)."
        },
    )
    revisionHistoryLimit: Optional[int] = field(
        default=None,
        metadata={
            "description": "The number of old history to retain to allow rollback. This is a pointer to distinguish between explicit zero and not specified. Defaults to 10."
        },
    )
    updateStrategy: Optional[V1DaemonSetUpdateStrategy] = field(
        default=None,
        metadata={
            "description": "An update strategy to replace existing DaemonSet pods with new pods."
        },
    )


@define(kw_only=True)
class V1DaemonSetCondition:
    status: str = field(
        metadata={
            "description": "Status of the condition, one of True, False, Unknown."
        }
    )
    type: str = field(metadata={"description": "Type of DaemonSet condition."})
    lastTransitionTime: Optional[str] = field(
        default=None,
        metadata={
            "description": "Last time the condition transitioned from one status to another."
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "description": "A human readable message indicating details about the transition."
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={"description": "The reason for the condition's last transition."},
    )


@define(kw_only=True)
class V1DaemonSetStatus:
    currentNumberScheduled: int = field(
        metadata={
            "description": "The number of nodes that are running at least 1 daemon pod and are supposed to run the daemon pod. More info: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        }
    )
    desiredNumberScheduled: int = field(
        metadata={
            "description": "The total number of nodes that should be running the daemon pod (including nodes correctly running the daemon pod). More info: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        }
    )
    numberMisscheduled: int = field(
        metadata={
            "description": "The number of nodes that are running the daemon pod, but are not supposed to run the daemon pod. More info: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/"
        }
    )
    numberReady: int = field(
        metadata={
            "description": "numberReady is the number of nodes that should be running the daemon pod and have one or more of the daemon pod running with a Ready Condition."
        }
    )
    collisionCount: Optional[int] = field(
        default=None,
        metadata={
            "description": "Count of hash collisions for the DaemonSet. The DaemonSet controller uses this field as a collision avoidance mechanism when it needs to create the name for the newest ControllerRevision."
        },
    )
    conditions: Optional[List[V1DaemonSetCondition]] = field(
        default=None,
        metadata={
            "description": "Represents the latest available observations of a DaemonSet's current state."
        },
    )
    numberAvailable: Optional[int] = field(
        default=None,
        metadata={
            "description": "The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and available (ready for at least spec.minReadySeconds)"
        },
    )
    numberUnavailable: Optional[int] = field(
        default=None,
        metadata={
            "description": "The number of nodes that should be running the daemon pod and have none of the daemon pod running and available (ready for at least spec.minReadySeconds)"
        },
    )
    observedGeneration: Optional[int] = field(
        default=None,
        metadata={
            "description": "The most recent generation observed by the daemon set controller."
        },
    )
    updatedNumberScheduled: Optional[int] = field(
        default=None,
        metadata={
            "description": "The total number of nodes that are running updated daemon pod"
        },
    )


@define(kw_only=True)
class V1DaemonSet:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        },
    )
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    spec: Optional[V1DaemonSetSpec] = field(
        default=None,
        metadata={
            "description": "The desired behavior of this daemon set. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        },
    )
    status: Optional[V1DaemonSetStatus] = field(
        default=None,
        metadata={
            "description": "The current status of this daemon set. This data may be out of date by some window of time. Populated by the system. Read-only. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        },
    )


@define(kw_only=True)
class V1ReplicaSetSpec:
    selector: V1LabelSelector = field(
        metadata={
            "description": "Selector is a label query over pods that should match the replica count. Label keys and values that must match in order to be controlled by this replica set. It must match the pod template's labels. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        }
    )
    minReadySeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Minimum number of seconds for which a newly created pod should be ready without any of its container crashing, for it to be considered available. Defaults to 0 (pod will be considered available as soon as it is ready)"
        },
    )
    replicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "Replicas is the number of desired replicas. This is a pointer to distinguish between explicit zero and unspecified. Defaults to 1. More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller"
        },
    )
    template: Optional[V1PodTemplateSpec] = field(
        default=None,
        metadata={
            "description": "Template is the object that describes the pod that will be created if insufficient replicas are detected. More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template"
        },
    )


@define(kw_only=True)
class V1ReplicaSetCondition:
    status: str = field(
        metadata={
            "description": "Status of the condition, one of True, False, Unknown."
        }
    )
    type: str = field(metadata={"description": "Type of replica set condition."})
    lastTransitionTime: Optional[str] = field(
        default=None,
        metadata={
            "description": "The last time the condition transitioned from one status to another."
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "description": "A human readable message indicating details about the transition."
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={"description": "The reason for the condition's last transition."},
    )


@define(kw_only=True)
class V1ReplicaSetStatus:
    replicas: int = field(
        metadata={
            "description": "Replicas is the most recently observed number of replicas. More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller"
        }
    )
    availableReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "The number of available replicas (ready for at least minReadySeconds) for this replica set."
        },
    )
    conditions: Optional[List[V1ReplicaSetCondition]] = field(
        default=None,
        metadata={
            "description": "Represents the latest available observations of a replica set's current state."
        },
    )
    fullyLabeledReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "The number of pods that have labels matching the labels of the pod template of the replicaset."
        },
    )
    observedGeneration: Optional[int] = field(
        default=None,
        metadata={
            "description": "ObservedGeneration reflects the generation of the most recently observed ReplicaSet."
        },
    )
    readyReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "readyReplicas is the number of pods targeted by this ReplicaSet with a Ready Condition."
        },
    )


@define(kw_only=True)
class V1ReplicaSet:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        },
    )
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "If the Labels of a ReplicaSet are empty, they are defaulted to be the same as the Pod(s) that the ReplicaSet manages. Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    spec: Optional[V1ReplicaSetSpec] = field(
        default=None,
        metadata={
            "description": "Spec defines the specification of the desired behavior of the ReplicaSet. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        },
    )
    status: Optional[V1ReplicaSetStatus] = field(
        default=None,
        metadata={
            "description": "Status is the most recently observed status of the ReplicaSet. This data may be out of date by some window of time. Populated by the system. Read-only. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        },
    )


@define(kw_only=True)
class V1ResourceQuotaStatus:
    hard: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Hard is the set of enforced hard limits for each named resource. More info: https://kubernetes.io/docs/concepts/policy/resource-quotas/"
        },
    )
    used: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Used is the current observed total usage of the resource in the namespace."
        },
    )


@define(kw_only=True)
class ApiResourceQuota:
    data: V1ResourceQuotaStatus = field(
        metadata={"description": "resource quota status"}
    )
    namespace: str = field(metadata={"description": "namespace"})


@define(kw_only=True)
class V1StatefulSetOrdinals:
    start: int = field(
        metadata={
            "description": """\
start is the number representing the first replica's index. It may be used to number replicas from an alternate index (eg: 1-indexed) over the default 0-indexed names, or to orchestrate progressive movement of replicas from one StatefulSet to another. If set, replica indices will be in the range:
  [.spec.ordinals.start, .spec.ordinals.start + .spec.replicas).
If unset, defaults to 0. Replica indices will be in the range:
  [0, .spec.replicas).
"""
        }
    )


@define(kw_only=True)
class V1StatefulSetPersistentVolumeClaimRetentionPolicy:
    whenDeleted: Optional[str] = field(
        default=None,
        metadata={
            "description": "WhenDeleted specifies what happens to PVCs created from StatefulSet VolumeClaimTemplates when the StatefulSet is deleted. The default policy of `Retain` causes PVCs to not be affected by StatefulSet deletion. The `Delete` policy causes those PVCs to be deleted."
        },
    )
    whenScaled: Optional[str] = field(
        default=None,
        metadata={
            "description": "WhenScaled specifies what happens to PVCs created from StatefulSet VolumeClaimTemplates when the StatefulSet is scaled down. The default policy of `Retain` causes PVCs to not be affected by a scaledown. The `Delete` policy causes the associated PVCs for any excess pods above the replica count to be deleted."
        },
    )


@define(kw_only=True)
class V1RollingUpdateStatefulSetStrategy:
    maxUnavailable: Optional[str] = field(
        default=None,
        metadata={
            "description": "The maximum number of pods that can be unavailable during the update. Value can be an absolute number (ex: 5) or a percentage of desired pods (ex: 10%). Absolute number is calculated from percentage by rounding up. This can not be 0. Defaults to 1. This field is alpha-level and is only honored by servers that enable the MaxUnavailableStatefulSet feature. The field applies to all pods in the range 0 to Replicas-1. That means if there is any unavailable pod in the range 0 to Replicas-1, it will be counted towards MaxUnavailable."
        },
    )
    partition: Optional[int] = field(
        default=None,
        metadata={
            "description": "Partition indicates the ordinal at which the StatefulSet should be partitioned for updates. During a rolling update, all pods from ordinal Replicas-1 to Partition are updated. All pods from ordinal Partition-1 to 0 remain untouched. This is helpful in being able to do a canary based deployment. The default value is 0."
        },
    )


@define(kw_only=True)
class V1StatefulSetUpdateStrategy:
    rollingUpdate: Optional[V1RollingUpdateStatefulSetStrategy] = field(
        default=None,
        metadata={
            "description": "RollingUpdate is used to communicate parameters when Type is RollingUpdateStatefulSetStrategyType."
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": "Type indicates the type of the StatefulSetUpdateStrategy. Default is RollingUpdate."
        },
    )


@define(kw_only=True)
class V1TypedLocalObjectReference:
    apiGroup: str = field(
        metadata={
            "description": "APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required."
        }
    )
    kind: str = field(
        metadata={"description": "Kind is the type of resource being referenced"}
    )
    name: str = field(
        metadata={"description": "Name is the name of resource being referenced"}
    )


@define(kw_only=True)
class V1TypedObjectReference:
    apiGroup: str = field(
        metadata={
            "description": "APIGroup is the group for the resource being referenced. If APIGroup is not specified, the specified Kind must be in the core API group. For any other third-party types, APIGroup is required."
        }
    )
    kind: str = field(
        metadata={"description": "Kind is the type of resource being referenced"}
    )
    name: str = field(
        metadata={"description": "Name is the name of resource being referenced"}
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "description": "Namespace is the namespace of resource being referenced Note that when a namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object is required in the referent namespace to allow that namespace's owner to accept the reference. See the ReferenceGrant documentation for details. (Alpha) This field requires the CrossNamespaceVolumeDataSource feature gate to be enabled."
        },
    )


@define(kw_only=True)
class V1VolumeResourceRequirements:
    limits: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Limits describes the maximum amount of compute resources allowed. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        },
    )
    requests: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Requests describes the minimum amount of compute resources required. If Requests is omitted for a container, it defaults to Limits if that is explicitly specified, otherwise to an implementation-defined value. Requests cannot exceed Limits. More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaimSpec:
    accessModes: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1"
        },
    )
    dataSource: Optional[V1TypedLocalObjectReference] = field(
        default=None,
        metadata={
            "description": "dataSource field can be used to specify either: * An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot) * An existing PVC (PersistentVolumeClaim) If the provisioner or an external controller can support the specified data source, it will create a new volume based on the contents of the specified data source. When the AnyVolumeDataSource feature gate is enabled, dataSource contents will be copied to dataSourceRef, and dataSourceRef contents will be copied to dataSource when dataSourceRef.namespace is not specified. If the namespace is specified, then dataSourceRef will not be copied to dataSource."
        },
    )
    dataSourceRef: Optional[V1TypedObjectReference] = field(
        default=None,
        metadata={
            "description": """\
dataSourceRef specifies the object from which to populate the volume with data, if a non-empty volume is desired. This may be any object from a non-empty API group (non core object) or a PersistentVolumeClaim object. When this field is specified, volume binding will only succeed if the type of the specified object matches some installed volume populator or dynamic provisioner. This field will replace the functionality of the dataSource field and as such if both fields are non-empty, they must have the same value. For backwards compatibility, when namespace isn't specified in dataSourceRef, both fields (dataSource and dataSourceRef) will be set to the same value automatically if one of them is empty and the other is non-empty. When namespace is specified in dataSourceRef, dataSource isn't set to the same value and must be empty. There are three important differences between dataSource and dataSourceRef: * While dataSource only allows two specific types of objects, dataSourceRef
  allows any non-core object, as well as PersistentVolumeClaim objects.
* While dataSource ignores disallowed values (dropping them), dataSourceRef
  preserves all values, and generates an error if a disallowed value is
  specified.
* While dataSource only allows local objects, dataSourceRef allows objects
  in any namespaces.
(Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled. (Alpha) Using the namespace field of dataSourceRef requires the CrossNamespaceVolumeDataSource feature gate to be enabled.
"""
        },
    )
    resources: Optional[V1VolumeResourceRequirements] = field(
        default=None,
        metadata={
            "description": "resources represents the minimum resources the volume should have. If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements that are lower than previous value but must still be higher than capacity recorded in the status field of the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources"
        },
    )
    selector: Optional[V1LabelSelector] = field(
        default=None,
        metadata={
            "description": "selector is a label query over volumes to consider for binding."
        },
    )
    storageClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": "storageClassName is the name of the StorageClass required by the claim. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1"
        },
    )
    volumeAttributesClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": "volumeAttributesClassName may be used to set the VolumeAttributesClass used by this claim. If specified, the CSI driver will create or update the volume with the attributes defined in the corresponding VolumeAttributesClass. This has a different purpose than storageClassName, it can be changed after the claim is created. An empty string value means that no VolumeAttributesClass will be applied to the claim but it's not allowed to reset this field to empty string once it is set. If unspecified and the PersistentVolumeClaim is unbound, the default VolumeAttributesClass will be set by the persistentvolume controller if it exists. If the resource referred to by volumeAttributesClass does not exist, this PersistentVolumeClaim will be set to a Pending state, as reflected by the modifyVolumeStatus field, until such as a resource exists. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#volumeattributesclass (Alpha) Using this field requires the VolumeAttributesClass feature gate to be enabled."
        },
    )
    volumeMode: Optional[str] = field(
        default=None,
        metadata={
            "description": "volumeMode defines what type of volume is required by the claim. Value of Filesystem is implied when not included in claim spec."
        },
    )
    volumeName: Optional[str] = field(
        default=None,
        metadata={
            "description": "volumeName is the binding reference to the PersistentVolume backing this claim."
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaimCondition:
    status: str = field()
    type: str = field()
    lastProbeTime: Optional[str] = field(
        default=None,
        metadata={"description": "lastProbeTime is the time we probed the condition."},
    )
    lastTransitionTime: Optional[str] = field(
        default=None,
        metadata={
            "description": "lastTransitionTime is the time the condition transitioned from one status to another."
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "description": "message is the human-readable message indicating details about last transition."
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "description": 'reason is a unique, this should be a short, machine understandable string that gives the reason for condition\'s last transition. If it reports "ResizeStarted" that means the underlying persistent volume is being resized.'
        },
    )


@define(kw_only=True)
class V1ModifyVolumeStatus:
    status: str = field(
        metadata={
            "description": """\
status is the status of the ControllerModifyVolume operation. It can be in any of following states:
 - Pending
   Pending indicates that the PersistentVolumeClaim cannot be modified due to unmet requirements, such as
   the specified VolumeAttributesClass not existing.
 - InProgress
   InProgress indicates that the volume is being modified.
 - Infeasible
  Infeasible indicates that the request has been rejected as invalid by the CSI driver. To
	  resolve the error, a valid VolumeAttributesClass needs to be specified.
Note: New statuses can be added in the future. Consumers should check for unknown statuses and fail appropriately.
"""
        }
    )
    targetVolumeAttributesClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": "targetVolumeAttributesClassName is the name of the VolumeAttributesClass the PVC currently being reconciled"
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaimStatus:
    accessModes: Optional[List[str]] = field(
        default=None,
        metadata={
            "description": "accessModes contains the actual access modes the volume backing the PVC has. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1"
        },
    )
    allocatedResourceStatuses: Optional[Dict] = field(
        default=None,
        metadata={
            "description": """\
allocatedResourceStatuses stores status of resource being resized for the given PVC. Key names follow standard Kubernetes label syntax. Valid values are either:
	* Un-prefixed keys:
		- storage - the capacity of the volume.
	* Custom resources must use implementation-defined prefixed names such as \"example.com/my-custom-resource\"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered reserved and hence may not be used.

ClaimResourceStatus can be in any of following states:
	- ControllerResizeInProgress:
		State set when resize controller starts resizing the volume in control-plane.
	- ControllerResizeFailed:
		State set when resize has failed in resize controller with a terminal error.
	- NodeResizePending:
		State set when resize controller has finished resizing the volume but further resizing of
		volume is needed on the node.
	- NodeResizeInProgress:
		State set when kubelet starts resizing the volume.
	- NodeResizeFailed:
		State set when resizing has failed in kubelet with a terminal error. Transient errors don't set
		NodeResizeFailed.
For example: if expanding a PVC for more capacity - this field can be one of the following states:
	- pvc.status.allocatedResourceStatus['storage'] = \"ControllerResizeInProgress\"
     - pvc.status.allocatedResourceStatus['storage'] = \"ControllerResizeFailed\"
     - pvc.status.allocatedResourceStatus['storage'] = \"NodeResizePending\"
     - pvc.status.allocatedResourceStatus['storage'] = \"NodeResizeInProgress\"
     - pvc.status.allocatedResourceStatus['storage'] = \"NodeResizeFailed\"
When this field is not set, it means that no resize operation is in progress for the given PVC.

A controller that receives PVC update with previously unknown resourceName or ClaimResourceStatus should ignore the update for the purpose it was designed. For example - a controller that only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.
"""
        },
    )
    allocatedResources: Optional[Dict] = field(
        default=None,
        metadata={
            "description": """\
allocatedResources tracks the resources allocated to a PVC including its capacity. Key names follow standard Kubernetes label syntax. Valid values are either:
	* Un-prefixed keys:
		- storage - the capacity of the volume.
	* Custom resources must use implementation-defined prefixed names such as \"example.com/my-custom-resource\"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered reserved and hence may not be used.

Capacity reported here may be larger than the actual capacity when a volume expansion operation is requested. For storage quota, the larger value from allocatedResources and PVC.spec.resources is used. If allocatedResources is not set, PVC.spec.resources alone is used for quota calculation. If a volume expansion capacity request is lowered, allocatedResources is only lowered if there are no expansion operations in progress and if the actual volume capacity is equal or lower than the requested capacity.

A controller that receives PVC update with previously unknown resourceName should ignore the update for the purpose it was designed. For example - a controller that only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.
"""
        },
    )
    capacity: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "capacity represents the actual resources of the underlying volume."
        },
    )
    conditions: Optional[List[V1PersistentVolumeClaimCondition]] = field(
        default=None,
        metadata={
            "description": "conditions is the current Condition of persistent volume claim. If underlying persistent volume is being resized then the Condition will be set to 'ResizeStarted'."
        },
    )
    currentVolumeAttributesClassName: Optional[str] = field(
        default=None,
        metadata={
            "description": "currentVolumeAttributesClassName is the current name of the VolumeAttributesClass the PVC is using. When unset, there is no VolumeAttributeClass applied to this PersistentVolumeClaim This is an alpha field and requires enabling VolumeAttributesClass feature."
        },
    )
    modifyVolumeStatus: Optional[V1ModifyVolumeStatus] = field(
        default=None,
        metadata={
            "description": "ModifyVolumeStatus represents the status object of ControllerModifyVolume operation. When this is unset, there is no ModifyVolume operation being attempted. This is an alpha field and requires enabling VolumeAttributesClass feature."
        },
    )
    phase: Optional[str] = field(
        default=None,
        metadata={
            "description": "phase represents the current phase of PersistentVolumeClaim."
        },
    )


@define(kw_only=True)
class V1PersistentVolumeClaim:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        },
    )
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    spec: Optional[V1PersistentVolumeClaimSpec] = field(
        default=None,
        metadata={
            "description": "spec defines the desired characteristics of a volume requested by a pod author. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        },
    )
    status: Optional[V1PersistentVolumeClaimStatus] = field(
        default=None,
        metadata={
            "description": "status represents the current information/status of a persistent volume claim. Read-only. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims"
        },
    )


@define(kw_only=True)
class V1StatefulSetSpec:
    selector: V1LabelSelector = field(
        metadata={
            "description": "selector is a label query over pods that should match the replica count. It must match the pod template's labels. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors"
        }
    )
    serviceName: str = field(
        metadata={
            "description": 'serviceName is the name of the service that governs this StatefulSet. This service must exist before the StatefulSet, and is responsible for the network identity of the set. Pods get DNS/hostnames that follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local where "pod-specific-string" is managed by the StatefulSet controller.'
        }
    )
    template: V1PodTemplateSpec = field(
        metadata={
            "description": 'template is the object that describes the pod that will be created if insufficient replicas are detected. Each pod stamped out by the StatefulSet will fulfill this Template, but have a unique identity from the rest of the StatefulSet. Each pod will be named with the format <statefulsetname>-<podindex>. For example, a pod in a StatefulSet named "web" with index number "3" would be named "web-3". The only allowed template.spec.restartPolicy value is "Always".'
        }
    )
    minReadySeconds: Optional[int] = field(
        default=None,
        metadata={
            "description": "Minimum number of seconds for which a newly created pod should be ready without any of its container crashing for it to be considered available. Defaults to 0 (pod will be considered available as soon as it is ready)"
        },
    )
    ordinals: Optional[V1StatefulSetOrdinals] = field(
        default=None,
        metadata={
            "description": 'ordinals controls the numbering of replica indices in a StatefulSet. The default ordinals behavior assigns a "0" index to the first replica and increments the index by one for each additional replica requested. Using the ordinals field requires the StatefulSetStartOrdinal feature gate to be enabled, which is beta.'
        },
    )
    persistentVolumeClaimRetentionPolicy: Optional[
        V1StatefulSetPersistentVolumeClaimRetentionPolicy
    ] = field(
        default=None,
        metadata={
            "description": "persistentVolumeClaimRetentionPolicy describes the lifecycle of persistent volume claims created from volumeClaimTemplates. By default, all persistent volume claims are created as needed and retained until manually deleted. This policy allows the lifecycle to be altered, for example by deleting persistent volume claims when their stateful set is deleted, or when their pod is scaled down. This requires the StatefulSetAutoDeletePVC feature gate to be enabled, which is alpha.  +optional"
        },
    )
    podManagementPolicy: Optional[str] = field(
        default=None,
        metadata={
            "description": "podManagementPolicy controls how pods are created during initial scale up, when replacing pods on nodes, or when scaling down. The default policy is `OrderedReady`, where pods are created in increasing order (pod-0, then pod-1, etc) and the controller will wait until each pod is ready before continuing. When scaling down, the pods are removed in the opposite order. The alternative policy is `Parallel` which will create pods in parallel to match the desired scale without waiting, and on scale down will delete all pods at once."
        },
    )
    replicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "replicas is the desired number of replicas of the given Template. These are replicas in the sense that they are instantiations of the same Template, but individual replicas also have a consistent identity. If unspecified, defaults to 1."
        },
    )
    revisionHistoryLimit: Optional[int] = field(
        default=None,
        metadata={
            "description": "revisionHistoryLimit is the maximum number of revisions that will be maintained in the StatefulSet's revision history. The revision history consists of all revisions not represented by a currently applied StatefulSetSpec version. The default value is 10."
        },
    )
    updateStrategy: Optional[V1StatefulSetUpdateStrategy] = field(
        default=None,
        metadata={
            "description": "updateStrategy indicates the StatefulSetUpdateStrategy that will be employed to update Pods in the StatefulSet when a revision is made to Template."
        },
    )
    volumeClaimTemplates: Optional[List[V1PersistentVolumeClaim]] = field(
        default=None,
        metadata={
            "description": "volumeClaimTemplates is a list of claims that pods are allowed to reference. The StatefulSet controller is responsible for mapping network identities to claims in a way that maintains the identity of a pod. Every claim in this list must have at least one matching (by name) volumeMount in one container in the template. A claim in this list takes precedence over any volumes in the template, with the same name."
        },
    )


@define(kw_only=True)
class V1StatefulSetCondition:
    status: str = field(
        metadata={
            "description": "Status of the condition, one of True, False, Unknown."
        }
    )
    type: str = field(metadata={"description": "Type of statefulset condition."})
    lastTransitionTime: Optional[str] = field(
        default=None,
        metadata={
            "description": "Last time the condition transitioned from one status to another."
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "description": "A human readable message indicating details about the transition."
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={"description": "The reason for the condition's last transition."},
    )


@define(kw_only=True)
class V1StatefulSetStatus:
    availableReplicas: int = field(
        metadata={
            "description": "Total number of available pods (ready for at least minReadySeconds) targeted by this statefulset."
        }
    )
    replicas: int = field(
        metadata={
            "description": "replicas is the number of Pods created by the StatefulSet controller."
        }
    )
    collisionCount: Optional[int] = field(
        default=None,
        metadata={
            "description": "collisionCount is the count of hash collisions for the StatefulSet. The StatefulSet controller uses this field as a collision avoidance mechanism when it needs to create the name for the newest ControllerRevision."
        },
    )
    conditions: Optional[List[V1StatefulSetCondition]] = field(
        default=None,
        metadata={
            "description": "Represents the latest available observations of a statefulset's current state."
        },
    )
    currentReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "currentReplicas is the number of Pods created by the StatefulSet controller from the StatefulSet version indicated by currentRevision."
        },
    )
    currentRevision: Optional[str] = field(
        default=None,
        metadata={
            "description": "currentRevision, if not empty, indicates the version of the StatefulSet used to generate Pods in the sequence [0,currentReplicas)."
        },
    )
    observedGeneration: Optional[int] = field(
        default=None,
        metadata={
            "description": "observedGeneration is the most recent generation observed for this StatefulSet. It corresponds to the StatefulSet's generation, which is updated on mutation by the API Server."
        },
    )
    readyReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "readyReplicas is the number of pods created for this StatefulSet with a Ready Condition."
        },
    )
    updateRevision: Optional[str] = field(
        default=None,
        metadata={
            "description": "updateRevision, if not empty, indicates the version of the StatefulSet used to generate Pods in the sequence [replicas-updatedReplicas,replicas)"
        },
    )
    updatedReplicas: Optional[int] = field(
        default=None,
        metadata={
            "description": "updatedReplicas is the number of Pods created by the StatefulSet controller from the StatefulSet version indicated by updateRevision."
        },
    )


@define(kw_only=True)
class V1StatefulSet:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        },
    )
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    spec: Optional[V1StatefulSetSpec] = field(
        default=None,
        metadata={
            "description": "Spec defines the desired identities of pods in this set."
        },
    )
    status: Optional[V1StatefulSetStatus] = field(
        default=None,
        metadata={
            "description": "Status is the current status of Pods in this StatefulSet. This data may be out of date by some window of time."
        },
    )


@define(kw_only=True)
class ApiListResult:
    items: List[Any] = field()
    totalItems: int = field()


@define(kw_only=True)
class V1HealthConfig:
    Interval: Optional[int] = field(default=None)
    Retries: Optional[int] = field(default=None)
    StartPeriod: Optional[int] = field(default=None)
    Test: Optional[List[str]] = field(default=None)
    Timeout: Optional[int] = field(default=None)


@define(kw_only=True)
class V1Config:
    ArgsEscaped: Optional[bool] = field(default=None)
    AttachStderr: Optional[bool] = field(default=None)
    AttachStdin: Optional[bool] = field(default=None)
    AttachStdout: Optional[bool] = field(default=None)
    Cmd: Optional[List[str]] = field(default=None)
    Domainname: Optional[str] = field(default=None)
    Entrypoint: Optional[List[str]] = field(default=None)
    Env: Optional[List[str]] = field(default=None)
    ExposedPorts: Optional[Dict] = field(default=None)
    Healthcheck: Optional[V1HealthConfig] = field(default=None)
    Hostname: Optional[str] = field(default=None)
    Image: Optional[str] = field(default=None)
    Labels: Optional[Dict] = field(default=None)
    MacAddress: Optional[str] = field(default=None)
    NetworkDisabled: Optional[bool] = field(default=None)
    OnBuild: Optional[List[str]] = field(default=None)
    OpenStdin: Optional[bool] = field(default=None)
    Shell: Optional[List[str]] = field(default=None)
    StdinOnce: Optional[bool] = field(default=None)
    StopSignal: Optional[str] = field(default=None)
    Tty: Optional[bool] = field(default=None)
    User: Optional[str] = field(default=None)
    Volumes: Optional[Dict] = field(default=None)
    WorkingDir: Optional[str] = field(default=None)


@define(kw_only=True)
class V1History:
    author: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    created: Optional[str] = field(default=None)
    created_by: Optional[str] = field(default=None)
    empty_layer: Optional[bool] = field(default=None)


@define(kw_only=True)
class V1Hash:
    Algorithm: str = field()
    Hex: str = field()


@define(kw_only=True)
class V1RootFS:
    diff_ids: List[V1Hash] = field()
    type: str = field()


@define(kw_only=True)
class V1ConfigFile:
    architecture: str = field()
    config: V1Config = field()
    os: str = field()
    rootfs: V1RootFS = field()
    author: Optional[str] = field(default=None)
    container: Optional[str] = field(default=None)
    created: Optional[str] = field(default=None)
    docker_version: Optional[str] = field(default=None)
    history: Optional[List[V1History]] = field(default=None)
    os_features: Optional[List[str]] = field(
        default=None, metadata={"original_name": "os.features"}
    )
    os_version: Optional[str] = field(
        default=None, metadata={"original_name": "os.version"}
    )
    variant: Optional[str] = field(default=None)


@define(kw_only=True)
class V2ImageConfig:
    ConfigFile: V1ConfigFile = field()


@define(kw_only=True)
class OverviewMetricValue:
    value: List[Any] = field()


@define(kw_only=True)
class OverviewMetricData:
    result: List[OverviewMetricValue] = field()
    resultType: str = field()


@define(kw_only=True)
class OverviewMetric:
    data: OverviewMetricData = field()
    metric_name: str = field()


@define(kw_only=True)
class OverviewMetricResults:
    results: List[OverviewMetric] = field()


@define(kw_only=True)
class V1Secret:
    apiVersion: Optional[str] = field(
        default=None,
        metadata={
            "description": "APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        },
    )
    data: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "Data contains the secret data. Each key must consist of alphanumeric characters, '-', '_' or '.'. The serialized form of the secret data is a base64 encoded string, representing the arbitrary (possibly non-string) data value here. Described in https://tools.ietf.org/html/rfc4648#section-4"
        },
    )
    immutable: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Immutable, if set to true, ensures that data stored in the Secret cannot be updated (only object metadata can be modified). If not set to true, the field can be modified at any time. Defaulted to nil."
        },
    )
    kind: Optional[str] = field(
        default=None,
        metadata={
            "description": "Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        },
    )
    metadata: Optional[V1ObjectMeta] = field(
        default=None,
        metadata={
            "description": "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        },
    )
    stringData: Optional[Dict] = field(
        default=None,
        metadata={
            "description": "stringData allows specifying non-binary secret data in string form. It is provided as a write-only input field for convenience. All keys and values are merged into the data field on write, overwriting any existing values. The stringData field is never output when reading from the API."
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": "Used to facilitate programmatic handling of secret data. More info: https://kubernetes.io/docs/concepts/configuration/secret/#secret-types"
        },
    )


@define(kw_only=True)
class V2RepositoryTags:
    registry: str = field()
    repository: str = field()
    tags: List[str] = field()
