<!-- i18n: language-switcher -->
[English](cloud-philosophies.md) | [日本語](cloud-philosophies.ja.md)

# 4クラウドの思想を比較する

これは優劣表ではない。各社の公式landing zone、resource hierarchy、Well-Architected guidanceから、設計時に現れやすい傾向を抽出したもの。個々のserviceは例外を持つため、最終判断はresource scopeとSLAを確認する。

## 一枚比較

| 観点 | AWS | Azure | Google Cloud | OCI |
|---|---|---|---|---|
| 出発点 | 小さいbuilding blockを組み合わせる | enterprise control planeへworkloadを載せる | global infrastructureとmanaged platformを活用する | database・enterprise workloadを明確な区画で動かす |
| 主要な隔離単位 | account | subscription | project | compartment |
| 上位階層 | Organization→OU→Account | Entra tenant→Management Group→Subscription→Resource Group | Organization→Folder→Project | Tenancy→nested Compartment |
| 統制 | SCP、Control Tower、Config | Azure Policy、Management Group、Landing Zone | Organization Policy、hierarchical firewall、IAM deny | IAM Policy、Security Zone、Quota |
| identityの癖 | resource policyとidentity policyの両面 | Entra IDとAzure RBACの二層 | principal+role binding、resource hierarchy継承 | subjectが何をどこでできるかをpolicy文で表す |
| networkの癖 | VPCはregional、subnetはAZ。serviceごとのendpoint設計 | VNetはregional、ARM/Entra/Policyとのenterprise統合 | global/regional resourceが混在。global LBとproject設計が強い | VCNはregional、DRG/compartmentとenterprise networkを構成 |
| reliabilityの癖 | failure isolationをaccount/AZ/Regionへ明示的に組む | zone/regionに加えcentral platform運用との整合 | SLO、error budget、global traffic、managed dataを重視 | Availability Domain/Fault DomainとDB service特性を明示 |
| 運用の中心 | CloudWatch、CloudTrail、Config、Systems Manager | Azure Monitor、Activity Log、Policy、Defender | Cloud Monitoring/Logging/Trace、SRE practice | Monitoring、Logging、Audit、Cloud Guard |
| 設計者への問い | どのaccount・Region・service責任境界に置くか | どのtenant/MG/subscription policyで統制するか | user experience SLOとglobal/regional scopeは何か | どのcompartment・AD/FD・DB構成に置くか |

## AWS: composable primitivesとaccount isolation

AWSはserviceごとの責任境界が明確で、IAM、network、event、storageを組み合わせてarchitectureを作る傾向が強い。自由度が高いぶん、account vending、central logging、guardrailを先に作らないと構成差が拡大する。

設計時の観点:

- production/non-production、security、log archive、networkをaccountで分離する。
- OUは組織図ではなく、共通controlとsecurity/operational needで作る。
- VPC endpoint、resource policy、KMS key policyのようにdata pathとauthorizationをserviceごとに確認する。
- managed serviceでもmulti-AZ/multi-Regionの責任範囲はserviceごとに違う。

公式: [AWS multi-account design principles](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html)

## Azure: enterprise hierarchyとpolicy-driven governance

AzureはMicrosoft Entra tenant、Management Group、Subscription、Azure Resource Managerを軸に、enterprise全体のidentity・policy・hybrid environmentを統制する思想が強い。subscriptionはbillingだけでなくpolicy、quota、management boundaryでもある。

設計時の観点:

- platform landing zoneとapplication landing zoneを分ける。
- Management Group hierarchyは組織図のコピーではなく、同じpolicyを必要とするworkload typeでまとめる。
- Azure Policyでguardrailを配りつつ、subscription vendingでworkload teamへ自治を渡す。
- Entra directory roleとAzure RBAC roleを混同しない。

公式: [Azure landing zone design principles](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-principles)

## Google Cloud: project boundary、global platform、SRE

Google CloudはprojectをAPI、quota、billing、IAMの実務単位として扱い、Organization/Folderからpolicyを継承する。global resourceとregional resourceが混在し、data/analytics、Kubernetes、global load balancing、SREの考え方がarchitectureへ入りやすい。

設計時の観点:

- projectを単なるresource groupとして扱わず、lifecycle・quota・IAM・billing boundaryとして設計する。
- resourceがzonal/regional/global/multi-regionalのどれかを最初に確認する。
- availabilityではservice稼働だけでなく、user-facing SLI/SLOとdata correctnessを定義する。
- hierarchyは組織図よりpolicy、environment、team autonomyから決める。

公式: [Google Cloud resource hierarchy](https://docs.cloud.google.com/architecture/landing-zones/decide-resource-hierarchy) / [Reliability pillar](https://docs.cloud.google.com/architecture/framework/reliability)

## OCI: compartment governanceとdatabase-centered enterprise

OCIはtenancy内をnested compartmentで区画化し、IAM policy、quota、network、security、costの運用境界を作る。Oracle Databaseや既存enterprise systemとの接続で、性能・license・data residencyを明示的に扱いやすい。

設計時の観点:

- compartmentをfolderではなくIAM/operation/quota boundaryとして扱う。
- policyのverb (`inspect/read/use/manage`) とresource type、locationを読む。
- Region、Availability Domain、Fault Domainの組合せを確認する。
- DB service固有のHA/backup/DR責任とapplication tierを分けて考える。

公式: [OCI Cloud Adoption Framework](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/home.htm) / [OCI Core Landing Zone](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/oci-core-landing-zone.htm)

## 同等サービス比較で必ず見る5点

1. resource scope: global / regional / zonal
2. isolation boundary: account / subscription / project / compartment
3. control inheritance: 上位policyがどう継承・denyされるか
4. data plane failure: control plane停止時も既存trafficが流れるか
5. operator responsibility: patch、backup、scaling、failoverのどこまでmanagedか

名前が似ていても、この5点が違えば移植時のarchitectureは同じにならない。
