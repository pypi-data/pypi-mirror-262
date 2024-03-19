from pathlib import Path
import ssl
from typing import Any
import pydantic
from authlib.common.security import generate_token
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from authlib.jose import JWTClaims, JsonWebToken, JsonWebKey
from authlib.oauth2.rfc7523 import PrivateKeyJWT

from starlette import status
from starlette.datastructures import URL
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse


class User(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr | None
    roles: list[str]
    """Complete access token. Required for token propagation."""
    token: str


class KeycloakOAuth2:
    def __init__(
        self,
        client_id: str,
        client_secret: str | bytes | None,
        server_metadata_url: str,
        client_kwargs: dict[str, Any],
        base_url: str = "/",
        logout_target: str = "/",
    ) -> None:
        self.code_verifier = generate_token(48)
        self._base_url = base_url
        self._logout_page = logout_target

        oauth = OAuth()

        # HACK: load custom certificate including default certifi cacert chain
        if verify := client_kwargs.get("verify"):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23, verify=verify)
            client_kwargs["verify"] = ssl_context

        oauth.register(
            name="keycloak",
            # client_id and client_secret are created in keycloak
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=server_metadata_url,
            client_kwargs=client_kwargs,
            code_challenge_method="S256",
        )

        assert isinstance(oauth.keycloak, StarletteOAuth2App)
        self.keycloak = oauth.keycloak

    async def setup_signed_jwt(self, keypair: Path, public_key: Path) -> None:
        """Setup client authentication for signed JWT.

        :param keypair: Path to keypair.pem, generated via `openssl genrsa - out keypair.pem 2048`
        :param public_key: Path to publickey.crt, generated via `openssl rsa -in keypair.pem -pubout -out publickey.crt`
        """
        self.keycloak.client_secret = keypair.read_bytes()
        self.pub = JsonWebKey.import_key(
            public_key.read_text(), {"kty": "RSA", "use": "sig"}
        ).as_dict()

        metadata = await self.keycloak.load_server_metadata()
        auth_method = PrivateKeyJWT(metadata["token_endpoint"])
        self.keycloak.client_auth_methods = [auth_method]
        self.keycloak.client_kwargs.update(
            {
                "token_endpoint_auth_method": auth_method.name,
            }
        )

    def setup_fastapi_routes(self) -> None:
        """Create FastAPI router and register API endpoints."""
        import fastapi

        self.router = fastapi.APIRouter()
        self.router.add_api_route("/login", self.login_page)
        self.router.add_api_route("/callback", self.auth)
        self.router.add_api_route("/logout", self.logout)
        self.router.add_api_route("/certs", self.public_keys)

    async def public_keys(self, request: Request) -> dict[str, Any]:
        return {"keys": [self.pub]}

    async def login_page(
        self, request: Request, redirect_target: str | None = None
    ) -> RedirectResponse:
        """Redirect to Keycloak login page."""
        redirect_uri = (
            URL(redirect_target)
            if redirect_target
            else request.url_for("auth")  # /auth/callback
        )
        if next := request.query_params.get("next"):
            redirect_uri = redirect_uri.include_query_params(next=next)
        return await self.keycloak.authorize_redirect(
            request, redirect_uri, code_verifier=self.code_verifier
        )

    async def auth(self, request: Request) -> RedirectResponse:
        """Authorize user with Keycloak access token."""
        token = await self.keycloak.authorize_access_token(request)
        claims = await self.parse_claims(token)
        user = User(
            name=claims["preferred_username"],
            email=claims.get("email"),
            roles=claims["realm_access"]["roles"],
            token=token["access_token"],
        )
        request.session["user"] = user.model_dump(mode="json")
        redirect_uri = request.query_params.get("next") or self._base_url
        return RedirectResponse(redirect_uri)

    async def parse_claims(self, token: dict[str, Any]) -> JWTClaims:
        metadata = await self.keycloak.load_server_metadata()
        alg_values: list[str] = metadata.get(
            "id_token_signing_alg_values_supported"
        ) or ["RS256"]
        jwt = JsonWebToken(alg_values)
        jwk_set = await self.keycloak.fetch_jwk_set()
        claims = jwt.decode(
            token["access_token"],
            key=JsonWebKey.import_key_set(jwk_set),
        )
        return claims

    async def logout(self, request: Request) -> RedirectResponse:
        """Deauthorize user and redirect to logout page."""
        request.session.pop("user", None)
        return RedirectResponse(self._logout_page)

    @staticmethod
    async def get_user(request: Request) -> User:
        if (user := request.session.get("user")) is not None:
            return User.model_validate(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
