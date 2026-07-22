<!-- i18n: language-switcher -->
[English](release-intelligence.md) | [日本語](release-intelligence.ja.md)

# Reading cloud releases for design and operations

Track releases that change an existing architecture assumption, not the number of new features.

## Eight checks

1. Stage: preview, GA, deprecation, retirement, or security fix.
2. Scope: global, regional, zonal, account-level, or another boundary.
3. Existing resources: automatic, opt-in, new resources only, or all resources.
4. Data plane: traffic, data formats, or consistency changes.
5. Control plane: API, IAM, policy, or default changes.
6. Operations: metric, log, quota, runbook, or backup changes.
7. Economics: pricing, commitments, egress, or licensing changes.
8. Cross-cloud: how the responsibility boundary differs from an equivalent capability elsewhere.

## Actions by stage

| Stage | Architect | Operator |
|---|---|---|
| Preview | Record as an option; avoid production dependency | Validate in a sandbox; check SLA, support, and Regions |
| GA | Revisit constraints in existing ADRs | Validate metrics, quotas, cost, and runbooks |
| Default change | Diff security and availability assumptions | Inventory whether existing or new resources are affected |
| Deprecation | Select the replacement and migration architecture | Create a dated issue with owner, inventory, and rollback |
| Security | Evaluate exposure and compensating controls | Apply the patch or mitigation and retain completion evidence |

## Provider-specific reading

### AWS

Releases are often service-specific. Check Region availability, IAM actions, service quotas, existing-resource behavior, and CloudFormation/API support.

### Azure

Follow preview-to-GA transitions as well as Azure Policy, API versions, SKU retirements, and Entra/Defender integration. Check the effect of rollout across subscriptions and management groups.

### Google Cloud

Product release notes often group several services by day. Check launch stage, global or regional scope, quota, data/model versions, and deprecated APIs.

### OCI

Check database versions, Region and Availability Domain coverage, shapes, network behavior, IAM policy examples, and differences between console, API, CLI, and SDK support.

## Review record

```markdown
## <date> <release title>
- Provider / service:
- Stage / deadline:
- Affected inventory:
- Design impact:
- Operations impact:
- Cross-cloud equivalent and difference:
- Action / owner / due date:
- Official source:
```
