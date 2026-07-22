<!-- i18n: language-switcher -->
[English](cloud-philosophies.md) | [日本語](cloud-philosophies.ja.md)

# Comparing four cloud philosophies

This is not a ranking. It extracts recurring design tendencies from each provider's landing-zone, resource-hierarchy, and Well-Architected guidance. Individual services have exceptions, so verify the exact resource scope and SLA before deciding.

## At a glance

| Perspective | AWS | Azure | Google Cloud | OCI |
|---|---|---|---|---|
| Starting point | Compose small building blocks | Place workloads under an enterprise control plane | Use a global infrastructure and managed platform | Run database and enterprise workloads in explicit administrative partitions |
| Primary isolation unit | Account | Subscription | Project | Compartment |
| Hierarchy | Organization → OU → account | Entra tenant → management group → subscription → resource group | Organization → folder → project | Tenancy → nested compartment |
| Governance | SCP, Control Tower, Config | Azure Policy, management groups, Landing Zones | Organization Policy, hierarchical firewall policies, IAM deny | IAM policies, Security Zones, quotas |
| Identity characteristic | Identity and resource policies both matter | Entra ID and Azure RBAC are separate layers | Principals receive role bindings inherited through the resource hierarchy | Policy statements define what a subject may do and where |
| Network characteristic | VPCs are regional; subnets are zonal | VNets are regional and integrate with ARM, Entra, and Policy | Global and regional resources coexist; global load balancing and project design are prominent | VCNs are regional; DRGs and compartments shape enterprise networks |
| Reliability characteristic | Explicitly compose isolation across accounts, AZs, and Regions | Align zone and region design with the central platform operating model | Emphasize SLOs, error budgets, global traffic, and managed data | Make Availability Domains, Fault Domains, and database characteristics explicit |
| Core question | Which account, Region, and service responsibility boundary owns this? | Which tenant, management-group, and subscription policies govern this? | What user SLO and global or regional scope does this require? | Which compartment, AD/FD, and database design owns this? |

## AWS: composable primitives and account isolation

AWS exposes clear service-level responsibility boundaries and encourages architectures that compose identity, networking, events, and storage. That flexibility makes early account vending, centralized logging, and guardrails important.

- Separate production, non-production, security, log archive, and network concerns with accounts.
- Build OUs around common controls and operating needs, not the organization chart.
- Verify both the data path and authorization for VPC endpoints, resource policies, and KMS key policies.
- Check each managed service's exact multi-AZ and multi-Region responsibility split.

Official guidance: [AWS multi-account design principles](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html)

## Azure: enterprise hierarchy and policy-driven governance

Azure organizes enterprise identity, policy, and hybrid environments around the Microsoft Entra tenant, management groups, subscriptions, and Azure Resource Manager. A subscription is a policy, quota, and management boundary as well as a billing boundary.

- Separate platform landing zones from application landing zones.
- Group management hierarchy nodes by common policy needs rather than the organization chart.
- Distribute guardrails with Azure Policy and give workload teams autonomy through subscription vending.
- Do not confuse Entra directory roles with Azure RBAC roles.

Official guidance: [Azure landing-zone design principles](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-principles)

## Google Cloud: project boundaries, a global platform, and SRE

Google Cloud treats projects as practical API, quota, billing, and IAM units, with policy inherited from organizations and folders. Global and regional resources coexist, while data, Kubernetes, global load balancing, and SRE practices strongly influence architecture.

- Treat projects as lifecycle, quota, IAM, and billing boundaries—not folders.
- Identify whether every resource is zonal, regional, global, or multi-regional.
- Define user-facing SLIs/SLOs and data correctness, not only service uptime.
- Design the hierarchy around policy, environments, and team autonomy.

Official guidance: [Resource hierarchy](https://docs.cloud.google.com/architecture/landing-zones/decide-resource-hierarchy) / [Reliability pillar](https://docs.cloud.google.com/architecture/framework/reliability)

## OCI: compartment governance and database-centered enterprise design

OCI partitions a tenancy with nested compartments, creating boundaries for IAM, operations, quotas, networking, security, and cost. Its Oracle Database and enterprise-system focus makes performance, licensing, and data residency especially explicit.

- Treat compartments as IAM, operating, and quota boundaries—not folders.
- Read the policy verb (`inspect`, `read`, `use`, or `manage`), resource type, and location together.
- Verify the Region, Availability Domain, and Fault Domain combination.
- Separate database-specific HA, backup, and DR responsibilities from the application layer.

Official guidance: [OCI Cloud Adoption Framework](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/home.htm) / [OCI Core Landing Zone](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/oci-core-landing-zone.htm)

## Five checks for an “equivalent” service

1. Resource scope: global, regional, or zonal.
2. Isolation boundary: account, subscription, project, or compartment.
3. Control inheritance: how higher-level policies inherit and deny.
4. Data-plane failure behavior: whether existing traffic continues during a control-plane outage.
5. Operator responsibility: who patches, backs up, scales, and fails over.

Similar names do not imply a portable architecture when these five properties differ.
