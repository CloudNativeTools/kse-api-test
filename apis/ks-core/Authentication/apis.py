from typing import Optional
from attrs import define, field
from .models import (
    OauthProviderMetadata,
    ErrorsError,
    V1beta1User,
    OauthSpec,
    OauthStatus,
    OauthTokenReview,
    OauthToken,
    JoseJSONWebKeySet,
    TokenClaims,
)
from aomaker.core.api_object import BaseAPIObject as BaseAPI
from aomaker.core.router import router

__ALL__ = [
    "OpenidConfigurationAPI",
    "UnbindTOTPAuthKeyAPI",
    "GenerateTOTPAuthKeyAPI",
    "BindTOTPAuthKeyAPI",
    "TokenReviewAPI",
    "OpenidAuthorizeGetAPI",
    "OpenidAuthorizePostAPI",
    "OauthCallbackAPI",
    "OpenidKeysAPI",
    "LogoutAPI",
    "OpenidTokenAPI",
    "OpenidUserinfoAPI",
]


@define(kw_only=True)
@router.get("/.well-known/openid-configuration")
class OpenidConfigurationAPI(BaseAPI[OauthProviderMetadata]):
    """The OpenID Provider's configuration information can be retrieved."""

    response: Optional[OauthProviderMetadata] = field(default=OauthProviderMetadata)
    endpoint_id: Optional[str] = field(default="openid-configuration")


@define(kw_only=True)
@router.delete("/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey")
class UnbindTOTPAuthKeyAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "Username"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="UnbindTOTPAuthKey")


@define(kw_only=True)
@router.get("/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey")
class GenerateTOTPAuthKeyAPI(BaseAPI[V1beta1User]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "Username"})

    path_params: PathParams
    response: Optional[V1beta1User] = field(default=V1beta1User)
    endpoint_id: Optional[str] = field(default="GenerateTOTPAuthKey")


@define(kw_only=True)
@router.post("/kapis/iam.kubesphere.io/v1beta1/users/{user}/authkey")
class BindTOTPAuthKeyAPI(BaseAPI[ErrorsError]):
    """None"""

    @define
    class PathParams:
        user: str = field(metadata={"description": "Username"})

    path_params: PathParams
    response: Optional[ErrorsError] = field(default=ErrorsError)
    endpoint_id: Optional[str] = field(default="BindTOTPAuthKey")


@define(kw_only=True)
@router.post("/oauth/authenticate")
class TokenReviewAPI(BaseAPI[OauthTokenReview]):
    """Token Review attempts to authenticate a token to a known user. Note: TokenReview requests may be cached by the webhook token authenticator plugin in the kube-apiserver."""

    @define
    class RequestBodyModel:
        apiVersion: str = field(metadata={"description": "Kubernetes API version"})
        kind: str = field(metadata={"description": "kind of the API object"})
        spec: Optional[OauthSpec] = field(default=None)
        status: Optional[OauthStatus] = field(
            default=None, metadata={"description": "token review status"}
        )

    request_body: RequestBodyModel

    response: Optional[OauthTokenReview] = field(default=OauthTokenReview)
    endpoint_id: Optional[str] = field(default="token-review")


@define(kw_only=True)
@router.get("/oauth/authorize")
class OpenidAuthorizeGetAPI(BaseAPI):
    """The authorization endpoint is used to interact with the resource owner and obtain an authorization grant."""

    @define
    class QueryParams:
        response_type: str = field(
            metadata={
                "description": 'The value MUST be one of "code" for requesting an authorization code as described by [RFC6749] Section 4.1.1, "token" for requesting an access token (implicit grant) as described by [RFC6749] Section 4.2.2.'
            }
        )
        client_id: str = field(
            metadata={
                "description": "OAuth 2.0 Client Identifier valid at the Authorization Server."
            }
        )
        redirect_uri: str = field(
            metadata={
                "description": "Redirection URI to which the response will be sent. This URI MUST exactly match one of the Redirection URI values for the Client pre-registered at the OpenID Provider."
            }
        )
        scope: Optional[str] = field(
            default=None,
            metadata={
                "description": "OpenID Connect requests MUST contain the openid scope value. If the openid scope value is not present, the behavior is entirely unspecified."
            },
        )
        state: Optional[str] = field(
            default=None,
            metadata={
                "description": "Opaque value used to maintain state between the request and the callback."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="openid-authorize-get")


@define(kw_only=True)
@router.post("/oauth/authorize")
class OpenidAuthorizePostAPI(BaseAPI):
    """The authorization endpoint is used to interact with the resource owner and obtain an authorization grant."""

    @define
    class RequestBodyModel:
        client_id: str = field()
        redirect_uri: str = field()
        response_type: Optional[str] = field(default=None)
        scope: Optional[str] = field(default=None)
        state: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    endpoint_id: Optional[str] = field(default="openid-authorize-post")


@define(kw_only=True)
@router.get("/oauth/callback/{callback}")
class OauthCallbackAPI(BaseAPI[OauthToken]):
    """None"""

    @define
    class PathParams:
        callback: str = field(metadata={"description": "The identity provider name."})

    @define
    class QueryParams:
        access_token: str = field(
            metadata={
                "description": "The access token issued by the authorization server."
            }
        )
        token_type: str = field(
            metadata={
                "description": "The type of the token issued as described in [RFC6479] Section 7.1. Value is case insensitive."
            }
        )
        state: str = field(
            metadata={
                "description": 'if the "state" parameter was present in the client authorization request.The exact value received from the client.'
            }
        )
        expires_in: Optional[str] = field(
            default=None,
            metadata={
                "description": 'The lifetime in seconds of the access token.  For example, the value "3600" denotes that the access token will expire in one hour from the time the response was generated.If omitted, the authorization server SHOULD provide the expiration time via other means or document the default value.'
            },
        )
        scope: Optional[str] = field(
            default=None,
            metadata={
                "description": "if identical to the scope requested by the client;otherwise, REQUIRED.  The scope of the access token as described by [RFC6479] Section 3.3."
            },
        )

    path_params: PathParams
    query_params: QueryParams = field(factory=QueryParams)
    response: Optional[OauthToken] = field(default=OauthToken)
    endpoint_id: Optional[str] = field(default="oauth-callback")


@define(kw_only=True)
@router.get("/oauth/keys")
class OpenidKeysAPI(BaseAPI[JoseJSONWebKeySet]):
    """This contains the signing key(s) the RP uses to validate signatures from the OP."""

    response: Optional[JoseJSONWebKeySet] = field(default=JoseJSONWebKeySet)
    endpoint_id: Optional[str] = field(default="openid-keys")


@define(kw_only=True)
@router.get("/oauth/logout")
class LogoutAPI(BaseAPI):
    """This endpoint takes an ID token and logs the user out of KubeSphere if the subject matches the current session."""

    @define
    class QueryParams:
        id_token_hint: Optional[str] = field(
            default=None,
            metadata={
                "description": "ID Token previously issued by the OP to the RP passed to the Logout Endpoint as a hint about the End-User's current authenticated session with the Client. This is used as an indication of the identity of the End-User that the RP is requesting be logged out by the OP."
            },
        )
        post_logout_redirect_uri: Optional[str] = field(
            default=None,
            metadata={
                "description": "URL to which the RP is requesting that the End-User's User Agent be redirected after a logout has been performed."
            },
        )
        state: Optional[str] = field(
            default=None,
            metadata={
                "description": "Opaque value used by the RP to maintain state between the logout request and the callback to the endpoint specified by the post_logout_redirect_uri parameter."
            },
        )

    query_params: QueryParams = field(factory=QueryParams)
    endpoint_id: Optional[str] = field(default="logout")


@define(kw_only=True)
@router.post("/oauth/token")
class OpenidTokenAPI(BaseAPI[OauthToken]):
    """The resource owner password credentials grant type is suitable in
    cases where the resource owner has a trust relationship with the
    client, such as the device operating system or a highly privileged application."""

    @define
    class RequestBodyModel:
        grant_type: str = field()
        client_id: str = field()
        client_secret: str = field()
        username: Optional[str] = field(default=None)
        password: Optional[str] = field(default=None)
        code: Optional[str] = field(default=None)

    request_body: RequestBodyModel

    response: Optional[OauthToken] = field(default=OauthToken)
    endpoint_id: Optional[str] = field(default="openid-token")


@define(kw_only=True)
@router.get("/oauth/userinfo")
class OpenidUserinfoAPI(BaseAPI[TokenClaims]):
    """UserInfo Endpoint is an OAuth 2.0 Protected Resource that returns Claims about the authenticated End-User."""

    response: Optional[TokenClaims] = field(default=TokenClaims)
    endpoint_id: Optional[str] = field(default="openid-userinfo")
