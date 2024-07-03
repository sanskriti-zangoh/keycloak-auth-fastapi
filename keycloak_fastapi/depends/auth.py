from core.settings import load_settings, AuthSettings

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID, KeycloakAdmin
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


auth: AuthSettings = load_settings("AuthSettings")

# Configure Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=auth.server_url,
    client_id=auth.keycloak_client_id,
    realm_name=auth.realm_name,
    client_secret_key=auth.keycloak_client_secret,
    verify=True
)

keycloak_admin = KeycloakAdmin(
    server_url=auth.server_url,
    username="admin",
    password="admin",
    realm_name=auth.realm_name,
    client_id=auth.keycloak_client_id,
    client_secret_key=auth.keycloak_client_secret,
    verify=True
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_idp_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/auth",
    tokenUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/token",
    refreshUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/token"
)

oauth2_scheme_google = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/auth",
    tokenUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/token",
    refreshUrl=f"{auth.server_url}/realms/{auth.realm_name}/protocol/openid-connect/token"
)

