"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)

from reconcile.gql_definitions.fragments.aws_infra_management_account import AWSInfrastructureManagementAccount
from reconcile.gql_definitions.fragments.aws_vpc import AWSVPC
from reconcile.gql_definitions.fragments.ocm_environment import OCMEnvironment
from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment AWSInfrastructureManagementAccount on AWSInfrastructureManagementAccount_v1 {
  account {
    name
    uid
    terraformUsername
    resourcesDefaultRegion
    automationToken {
      ... VaultSecret
    }
  }
  accessLevel
  default
}

fragment AWSVPC on AWSVPC_v1 {
  name
  description
  account {
    name
    uid
    terraformUsername
    automationToken {
      ... VaultSecret
    }
  }
  region
  vpc_id
  cidr_block
  subnets {
    id
  }
}

fragment OCMEnvironment on OpenShiftClusterManagerEnvironment_v1 {
    name
    labels
    url
    accessTokenClientId
    accessTokenUrl
    accessTokenClientSecret {
        ... VaultSecret
    }
}

fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query ClustersWithPeering {
  clusters: clusters_v1
  {
    path
    name
    ocm {
      name
      environment {
        ... OCMEnvironment
      }
      orgId
      accessTokenClientId
      accessTokenUrl
      accessTokenClientSecret {
        ... VaultSecret
      }
      blockedVersions
    }
    awsInfrastructureManagementAccounts {
      ... AWSInfrastructureManagementAccount
    }

    spec {
      region
      hypershift
      private
      ... on ClusterSpecROSA_v1 {
        account {
          name
          uid
        }
      }
    }
    network {
      vpc
    }
    peering {
      connections {
        name
        provider
        manageRoutes
        delete
        ... on ClusterPeeringConnectionAccount_v1 {
          vpc {
            ... AWSVPC
          }
          assumeRole
          manageAccountRoutes
        }
        ... on ClusterPeeringConnectionAccountVPCMesh_v1 {
          account {
            name
            uid
            terraformUsername
            automationToken {
              ... VaultSecret
            }
          }
          tags
        }
        ... on ClusterPeeringConnectionAccountTGW_v1 {
          account {
            name
            uid
            terraformUsername
            automationToken {
              ... VaultSecret
            }
          }
          tags
          cidrBlock
          manageSecurityGroups
          manageRoute53Associations
          allowPrivateHcpApiAccess
          assumeRole
        }
        ... on ClusterPeeringConnectionClusterRequester_v1 {
          cluster {
            name
            network {
              vpc
            }
            spec {
              region
            }
            awsInfrastructureManagementAccounts {
              ... AWSInfrastructureManagementAccount
            }
            peering {
              connections {
                name
                provider
                manageRoutes
                ... on ClusterPeeringConnectionClusterAccepter_v1 {
                  name
                  cluster {
                    name
                  }
                  awsInfrastructureManagementAccount {
                    name
                    uid
                    terraformUsername
                    automationToken {
                      ... VaultSecret
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    disable {
      integrations
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class OpenShiftClusterManagerV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    environment: OCMEnvironment = Field(..., alias="environment")
    org_id: str = Field(..., alias="orgId")
    access_token_client_id: Optional[str] = Field(..., alias="accessTokenClientId")
    access_token_url: Optional[str] = Field(..., alias="accessTokenUrl")
    access_token_client_secret: Optional[VaultSecret] = Field(..., alias="accessTokenClientSecret")
    blocked_versions: Optional[list[str]] = Field(..., alias="blockedVersions")


class ClusterSpecV1(ConfiguredBaseModel):
    region: str = Field(..., alias="region")
    hypershift: Optional[bool] = Field(..., alias="hypershift")
    private: bool = Field(..., alias="private")


class AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    uid: str = Field(..., alias="uid")


class ClusterSpecROSAV1(ClusterSpecV1):
    account: Optional[AWSAccountV1] = Field(..., alias="account")


class ClusterNetworkV1(ConfiguredBaseModel):
    vpc: str = Field(..., alias="vpc")


class ClusterPeeringConnectionV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    provider: str = Field(..., alias="provider")
    manage_routes: Optional[bool] = Field(..., alias="manageRoutes")
    delete: Optional[bool] = Field(..., alias="delete")


class ClusterPeeringConnectionAccountV1(ClusterPeeringConnectionV1):
    vpc: AWSVPC = Field(..., alias="vpc")
    assume_role: Optional[str] = Field(..., alias="assumeRole")
    manage_account_routes: Optional[bool] = Field(..., alias="manageAccountRoutes")


class ClusterPeeringConnectionAccountVPCMeshV1_AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    uid: str = Field(..., alias="uid")
    terraform_username: Optional[str] = Field(..., alias="terraformUsername")
    automation_token: VaultSecret = Field(..., alias="automationToken")


class ClusterPeeringConnectionAccountVPCMeshV1(ClusterPeeringConnectionV1):
    account: ClusterPeeringConnectionAccountVPCMeshV1_AWSAccountV1 = Field(..., alias="account")
    tags: Optional[Json] = Field(..., alias="tags")


class ClusterPeeringConnectionAccountTGWV1_AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    uid: str = Field(..., alias="uid")
    terraform_username: Optional[str] = Field(..., alias="terraformUsername")
    automation_token: VaultSecret = Field(..., alias="automationToken")


class ClusterPeeringConnectionAccountTGWV1(ClusterPeeringConnectionV1):
    account: ClusterPeeringConnectionAccountTGWV1_AWSAccountV1 = Field(..., alias="account")
    tags: Optional[Json] = Field(..., alias="tags")
    cidr_block: Optional[str] = Field(..., alias="cidrBlock")
    manage_security_groups: Optional[bool] = Field(..., alias="manageSecurityGroups")
    manage_route53_associations: Optional[bool] = Field(..., alias="manageRoute53Associations")
    allow_private_hcp_api_access: Optional[bool] = Field(..., alias="allowPrivateHcpApiAccess")
    assume_role: Optional[str] = Field(..., alias="assumeRole")


class ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterNetworkV1(ConfiguredBaseModel):
    vpc: str = Field(..., alias="vpc")


class ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterSpecV1(ConfiguredBaseModel):
    region: str = Field(..., alias="region")


class ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterPeeringV1_ClusterPeeringConnectionV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    provider: str = Field(..., alias="provider")
    manage_routes: Optional[bool] = Field(..., alias="manageRoutes")


class ClusterPeeringConnectionClusterAccepterV1_ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class ClusterPeeringConnectionClusterAccepterV1_AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    uid: str = Field(..., alias="uid")
    terraform_username: Optional[str] = Field(..., alias="terraformUsername")
    automation_token: VaultSecret = Field(..., alias="automationToken")


class ClusterPeeringConnectionClusterAccepterV1(ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterPeeringV1_ClusterPeeringConnectionV1):
    name: str = Field(..., alias="name")
    cluster: ClusterPeeringConnectionClusterAccepterV1_ClusterV1 = Field(..., alias="cluster")
    aws_infrastructure_management_account: Optional[ClusterPeeringConnectionClusterAccepterV1_AWSAccountV1] = Field(..., alias="awsInfrastructureManagementAccount")


class ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterPeeringV1(ConfiguredBaseModel):
    connections: list[Union[ClusterPeeringConnectionClusterAccepterV1, ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterPeeringV1_ClusterPeeringConnectionV1]] = Field(..., alias="connections")


class ClusterPeeringConnectionClusterRequesterV1_ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    network: Optional[ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterNetworkV1] = Field(..., alias="network")
    spec: Optional[ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterSpecV1] = Field(..., alias="spec")
    aws_infrastructure_management_accounts: Optional[list[AWSInfrastructureManagementAccount]] = Field(..., alias="awsInfrastructureManagementAccounts")
    peering: Optional[ClusterPeeringConnectionClusterRequesterV1_ClusterV1_ClusterPeeringV1] = Field(..., alias="peering")


class ClusterPeeringConnectionClusterRequesterV1(ClusterPeeringConnectionV1):
    cluster: ClusterPeeringConnectionClusterRequesterV1_ClusterV1 = Field(..., alias="cluster")


class ClusterPeeringV1(ConfiguredBaseModel):
    connections: list[Union[ClusterPeeringConnectionAccountTGWV1, ClusterPeeringConnectionAccountV1, ClusterPeeringConnectionAccountVPCMeshV1, ClusterPeeringConnectionClusterRequesterV1, ClusterPeeringConnectionV1]] = Field(..., alias="connections")


class DisableClusterAutomationsV1(ConfiguredBaseModel):
    integrations: Optional[list[str]] = Field(..., alias="integrations")


class ClusterV1(ConfiguredBaseModel):
    path: str = Field(..., alias="path")
    name: str = Field(..., alias="name")
    ocm: Optional[OpenShiftClusterManagerV1] = Field(..., alias="ocm")
    aws_infrastructure_management_accounts: Optional[list[AWSInfrastructureManagementAccount]] = Field(..., alias="awsInfrastructureManagementAccounts")
    spec: Optional[Union[ClusterSpecROSAV1, ClusterSpecV1]] = Field(..., alias="spec")
    network: Optional[ClusterNetworkV1] = Field(..., alias="network")
    peering: Optional[ClusterPeeringV1] = Field(..., alias="peering")
    disable: Optional[DisableClusterAutomationsV1] = Field(..., alias="disable")


class ClustersWithPeeringQueryData(ConfiguredBaseModel):
    clusters: Optional[list[ClusterV1]] = Field(..., alias="clusters")


def query(query_func: Callable, **kwargs: Any) -> ClustersWithPeeringQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        ClustersWithPeeringQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return ClustersWithPeeringQueryData(**raw_data)
