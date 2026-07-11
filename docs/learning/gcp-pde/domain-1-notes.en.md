<!-- i18n: language-switcher -->
[English](domain-1-notes.en.md) | [日本語](domain-1-notes.md)

# PDE Domain 1: Design Data Processing Systems — 50 Questions Compact Notes

Target: Udemy Practice Exam Domain 1 (Architecture & Planning) 50 questions
Policy: Reduce all questions to "Requirement Keywords → Correct Pattern." In the real exam, 70% is decided instantly by the key requirement words.
Reference Date: July 2026

---

## 0. Thought Process of the Question Setter (This alone makes elimination easy)

1. **Managed > self-managed**. Choosing to build Jenkins/Atlas/Hadoop/Vault on GKE/GCE by oneself is almost always incorrect.
2. **Native features > custom-built**. Self-made orchestration/re-queuing/deletion jobs with Cloud Functions + Firestore are incorrect.
3. **Requirement numbers fix the answer**. RPO=0 → active-active. Bandwidth 1Gbps + deadline → offline transfer. 50k writes/sec → Bigtable/Spanner.
4. Signaling: "business users" + "less experienced team" = choose low operational load managed solutions.
5. Multiple-choice questions often combine "implementation pillars" + "visualization/audit pillars" (e.g., verification pipeline + dashboard).

---

## 1. Requirement Keywords → Immediate Response Table

| Requirement Keyword | Answer |
|---|---|
| Global + ACID + 99.999% + Instant visibility | Spanner multi-region (external consistency) |
| Large write KV/time-series + single-digit ms + no strong consistency needed + low cost | Bigtable (row key design) |
| Reinforced PostgreSQL suitable for single region | AlloyDB (*Exclude immediately if global requirement appears*) |
| OLTP + real-time analytics in one DB | Spanner + change streams → BigQuery |
| Bandwidth shortage (1Gbps) + hundreds of TB + deadline | Transfer Appliance (supports NFS/SMB) |
| DB migration + minimal downtime (minutes) | Database Migration Service (continuous CDC) |
| Teradata → BigQuery | BigQuery Data Transfer Service |
| Isolate bad records + replay | Dataflow side outputs + error bucket/DLQ |
| Exactly-once / idempotent | BigQuery MERGE (with unique key) + Dataflow exactly-once sink |
| Complex dependencies + wait for data + retries + re-queuing | Cloud Composer (sensors + Dataplex Lineage) |
| Simple workflow + declarative + low ops | Cloud Workflows (YAML) |
| CI/CD | Cloud Build + testing + approval gates + Terraform |
| Cannot be decrypted by Google | Cloud EKM (external key: Thales/Fortanix) |
| Immediate revocation / environment encryption separation | CMEK + environment-specific key ring + audit logs |
| Prevent data exfiltration | VPC Service Controls perimeter (+ access levels for exceptions) |
| Public internet prohibited | Private Google Access + no external IP + VPC-SC |
| Auto-detection & pseudonymization of PII | Cloud DLP (infoTypes / FPE de-identification) |
| Column-level access control | policy tags (column security) + Fine-Grained Reader |
| Mathematical proof of non-re-identifiability | Differential Privacy (ε, δ + privacy budget) |
| Unified governance + domain ownership + automatic classification | Dataplex (lakes/zones + DLP integration + zone IAM) |
| Cross-search + tags + re-queuing | Data Catalog (+ Lineage API) |
| Controlled data sharing across org/project | Analytics Hub / authorized views |
| Cost: Time-series table | partitioning + clustering + partition expiration |
| Cost: High-frequency dashboard queries | BI Engine + materialized views |
| Workload separation + performance guarantee | BigQuery Editions + separate reservation + priority |
| Access management at scale (hundreds of people) | Google Groups + dataset-level role + HR automation |
| Automatic deletion after retention period | GCS Lifecycle + BQ table/partition expiration |
| PITR + non-impactful backup | Cloud SQL automated backups + binary logging |
| Avoid lock-in / multi-cloud | open format (Parquet/Iceberg/Delta) + OSS engines (Spark/Trino) |
| Data lake + schema evolution + in-place analysis | GCS (Parquet/Avro) + zones + Dataproc + BQ external tables |
| Schema evolution in streaming | Schema Registry + Avro + BQ schema relaxation |
| Residency (region retention) | dataset/bucket location + Org Policy (location constraints) + VPC-SC |
| RPO=0 / RTO<60s | active-active (Pub/Sub replication + parallel pipelines + Spanner + deduplication) |
| RTO 15 min / RPO 5 min + low cost | Warm standby (template + IaC automated deployment + snapshots) |
| DR regulatory audit trail | Production-like staging + monthly drills + monitoring metrics |

---

## 2. 50 Questions One-line Summaries

| # | Scenario Key Point | Correct Answer | Decisive Point |
|---|---|---|---|
| 1 | Dataflow 50 CI/CD pipelines (2-choice) | Terraform IaC + lint + template validation / Cloud Build + unit/integration tests + sequential deployment + approval gate | IaC enables configuration review; tests & gates prevent production accidents |
| 2 | RTO15min / RPO5min / low cost | Template + Terraform auto deployment + Pub/Sub replication + 5-min BQ snapshots | Active-active is too costly; manual is too slow → warm standby |
| 3 | Dispatch: balance=strong consistency, history=result consistency | Spanner multi-region + critical=strong consistency + non-critical=bounded staleness read + read replica | Use data type-specific consistency requirements |
| 4 | 50k TPS / global / ACID / 99.999% | Spanner multi-region | All four conditions simultaneously = Spanner only |
| 5 | Cloud SQL deadlock + analysis delay 24h | Spanner + interleaved + change streams → BigQuery | Single DB for OLTP + real-time analysis = change streams |
| 6 | 10 million/day quality verification + isolation + partner reports | Dataflow verification → valid: BigQuery / invalid: GCS + reason + logging + dashboard | CF times out; BigQuery constraints cause entire load failure |
| 7 | Complex dependencies + wait for arrival + retries + re-queuing | Cloud Composer + sensors + Dataplex Lineage | Sensors and DAG directly meet requirements |
| 8 | Departmental sharing + fine-grained + audit (2-choice) | Analytics Hub / authorized views + audit logs | Hide base tables and share only necessary parts; export duplication is incorrect |
| 9 | HIPAA (key management + residency + audit) | CMEK + single region + audit logs + VPC-SC + **BAA** | Choose options with BAA agreement |
| 10 | Google cannot decrypt + 90-day rotation + immediate revocation (2-choice) | EKM / Cloud Audit Logs | "Google cannot technically access" = EKM only. CMEK is insufficient. |
| 11 | Use real test data without PHI in development | DLP de-identification + separate project + VPC-SC | Anonymize while maintaining referential integrity. Masking is problematic for production access. |
| 12 | PB scale + catalog + auto classification + domain ownership | Dataplex (lakes/zones + DLP + zone IAM) | Keep data in place, unify without moving |
| 13 | 500TB / 1Gbps / 3 weeks / NAS | Transfer Appliance | Physical transfer needed; network too slow |
| 14 | 3 temperature tiers (daily/monthly/yearly) + 10-year retention | Standard/Nearline/Archive + Lifecycle auto-migration | Access frequency → class-based storage (textbook pattern) |
| 15 | 5-year data, recent 90 days focus queries | date partitioning + clustering + partition expiration | Monthly table sharding (not recommended: anti-pattern) |
| 16 | EU/US residency + cross-border analysis permitted | location control + VPC-SC + IAM | Encryption alone does not guarantee residency |
| 17 | $50k/month, mixed workloads | partition + cluster + BI Engine + MV + reservations | Full combo is correct pattern |
| 18 | Dataflow detection within 5 min + PagerDuty (2-choice) | Monitoring alert policies (lag/freshness/worker) / log-based metrics → PagerDuty | Manual review & custom monitoring are incorrect |
| 19 | Oracle 200 nodes / 50TB / 30 min downtime / inexperienced | DMS continuous CDC → Cloud SQL / AlloyDB | dump/import too slow; Datastream for analytics |
| 20 | 3-region regulation + central visibility + regional autonomy | Dataplex federation + Policy Tags + Org Policy for region lock | "No centralized management, unified visibility" = Dataplex |
| 21 | Prevent PHI exfiltration (2-choice) | VPC-SC perimeter / access levels | DLP detects but does not block data exfiltration |
| 22 | Teradata 500TB / 3 months / 1Gbps / incremental (2-choice) | Transfer Appliance + incremental / BQ DTS for Teradata | Initial physical; incremental native integration |
| 23 | Prevent duplicate payment processing | MERGE on transaction_id + exactly-once sink | In-memory deduplication is not durable; Pub/Sub deduplication is not idempotent processing |
| 24 | Slow dashboards + $10k/month (2-choice) | materialized views / BI Engine | Pre-aggregation + in-memory combo |
| 25 | Stock data RPO=0 / RTO<60s | Pub/Sub replication + dual-region pipelines + Spanner multi-region + dedup | Snapshot method fails to meet RPO/RTO |
| 26 | 500 people / 20 departments / assign within 1 hour | Google Groups + dataset-level Viewer + HR automation + audit logs | Groups are the only scalable option |
| 27 | Real-time 5 sec + daily attribution (2-choice) | 5s tumbling window streaming / daily batch | Lambda-style selection. 24h session window is a trap. |
| 28 | AWS coexistence + avoid lock-in | Delta Lake + Databricks + Fivetran | Open format + unified platform |
| 29 | Public internet prohibited | Private Google Access + no external IP + VPC-SC | Interconnect/VPN are for on-prem; unrelated here |
| 30 | Simple + complex workflows mixed | Composer (complex) + Workflows (simple) combined | All Composer is too costly & operationally heavy |
| 31 | Immediate quarantine + replay of IoT anomalies | Dataflow side outputs + DLQ + alerting | Same pattern as Q49 |
| 32 | Control ad-hoc expensive queries + department cost visibility | reservations + custom quotas + partition/cluster + BI Engine + labels | Time-shifting irrelevant to BQ pricing |
| 33 | Data lake (IoT + ERP + RDB) + schema evolution | GCS (Parquet/Avro) + raw/curated zones + Data Catalog + Dataproc + BQ external tables | Native BQ storage is costly; Bigtable is for different use case |
| 34 | Cloud SQL 30-day PITR / RTO2h / no impact on production | automated backups + binary logging | pg_dump causes load & granularity issues |
| 35 | Correct overly broad SA permissions | per-pipeline SA + minimal predefined roles | "Shared SA" approaches are all incorrect |
| 36 | Variation of Q6 (2-choice) | Dataflow verification + error bucket / Looker Studio visualization | Implementation pillar + visualization pillar |
| 37 | Schema evolution breaks ingestion | Schema Registry + Avro validation + Dataflow transformation + BQ relaxation | Pre-issuance validation is key; auto-detect is post-facto |
| 38 | DR compliance audit trail | Production-like staging + monthly drills + synthetic data + monitoring | Chaos testing in finance is forbidden; quarterly is insufficient |
| 39 | Immediate read disable + dev/prod encryption separation | CMEK + environment-specific key ring + auto-rotation + audit logs | Key destroy = immediate disable; EKM not needed here (if "Google cannot" is a requirement) |
| 40 | Aggregate data allowed / PII not allowed (2-choice) | DLP de-identify (FPE) / column policy tags | Mass production of views is unmaintainable |
| 41 | Multi-cloud portability (2-choice) | Dataproc Spark + Parquet + Iceberg + WIF / Delta/Hudi + Ranger + Trino | BQ Omni / Storage Write API are GCP-dependent traps |
| 42 | Cross-platform detection + PII + lineage | Dataplex + DLP + Data Catalog + Lineage | Building OSS solutions is a classic incorrect choice |
| 43 | 50k writes/sec KV time-series + no strong consistency + low budget | Bigtable | Firestore/Cloud SQL lack throughput; Spanner overkill |
| 44 | Automatic deletion after 7 years | GCS Lifecycle + BQ table expiration | Custom delete jobs are all incorrect |
| 45 | End-to-end lineage: Datastream → Dataflow → BigQuery → dbt → Looker | Data Catalog lineage + Dataflow lineage + Lineage API + dbt integration | Custom SQL parsers / commercial tools are incorrect |
| 46 | Re-identification impossible even with external data | Differential Privacy (ε=1.0, δ=1e-5) + limited aggregation + budget management | Masking / k-anonymity / synthetic data are weak guarantees |
| 47 | Separate dashboards and data science | Enterprise edition + reservation split (70/30) + priority | On-demand quotas do not guarantee performance |
| 48 | EU/US separation + aggregation-only collaboration | Separate projects + single region + Org Policy + VPC-SC | Multi-region setups violate physical separation |
| 49 | Malformed JSON halts entire pipeline | ParDo try-catch + side output → GCS error bucket | Pub/Sub DLQ cannot handle processing failures inside |
| 50 | Automatic tagging for thousands of tables | Data Catalog + DLP inspection templates + tag templates | Manual forms / regex solutions are incorrect |

---

## 3. Common Traps (Cut immediately upon seeing)

- **Self-managed operations**: Jenkins/Atlas/Ranger/Hadoop/Vault/Great Expectations on GKE/GCE/Cloud Run → operational burden, incorrect.
- **Heavy processing with Cloud Functions**: Timeout (minutes) and execution model unsuitable for large data.
- **Non-existent features**: Dataflow "multi-region mode," BigQuery "synchronous cross-region replication," "row-level constraints on INSERT" do not exist.
- **Misuse of DLP**: DLP detects/de-identifies; does not block transfer or access control (that’s VPC-SC/IAM).
- **Pub/Sub deduplication ≠ idempotency**: Deduplication prevents duplicate delivery, not reprocessing after ack.
- **External tables**: Slow; performance/SLA-sensitive contexts are incorrect.
- **Manual processes**: Spreadsheets, weekly reviews, manual approvals, re-queuing → conflicts with scale / sub-hour requirements.
- **Table sharding (`table_202401`)**: Anti-pattern; always prefer partitioning.
- **Time-shift cost reduction in BigQuery**: No such billing model exists.
- **k-anonymity / synthetic data "proof"**: Risks of background knowledge attacks; only differential privacy offers mathematical guarantees.
- **Encryption for residency**: Encryption alone does not prevent physical data movement.
- **Multi-region "region separation"**: Multi-region is for replication, not separation; counterproductive for strict residency.

---

## 4. Common Decision Axes for Judgement

### DB Selection (Q3,4,5,43)
- **Spanner**: Global / ACID / 99.999% / horizontal scale / external consistency. Change streams for analysis integration.
- **Bigtable**: High throughput KV / wide-column / single-digit ms / time-series / no SQL / no complex transactions.
- **AlloyDB**: High-performance PostgreSQL. *Exclude if global requirement appears.*
- **Cloud SQL**: Medium OLTP. Exclude for global / tens of thousands TPS.
- **Firestore**: Mobile/web document DB. Exclude for high throughput scenarios.

### Key Management (Q9,10,39)
1. **Google-managed**: No customer control → exclude if control is required.
2. **CMEK (Cloud KMS)**: Customer can disable/destroy → immediate revocation, environment separation via key rings, auto-rotation, audit logs.
3. **EKM**: Keys outside Google. Only if "Google cannot decrypt" explicitly appears.

### DR Response (Q2,25,38)
- **RPO=0 & RTO seconds** → active-active (multi-region, deduplication). Check for language indicating cost acceptance.
- **RTO minutes / RPO minutes & cost focus** → warm standby (template + IaC + snapshots/replication).
- **Testing** → production-like staging + monthly drills + automation + metrics. Chaos testing or quarterly drills are incorrect.

### Governance Product Roles (Q12,20,42,45,50)
- **Dataplex**: Organization (lakes/zones), domain ownership, profiling, quality, integrated governance.
- **Data Catalog**: Search, tags, lineage (now integrated with Dataplex).
- **DLP**: PII detection (infoTypes), de-identify (FPE/tokenization), risk analysis.
- **Analytics Hub**: Cross-organization/project data sharing via subscriptions.
- **VPC-SC**: Boundary.
- **Org Policy**: Preventive guardrails (location constraints, etc.).

---

## 5. Discrepancies Between Practice Questions and 2026 Reality (Countermeasures for Actual Exams)

- **Data Studio → Looker Studio** (renamed in 2022). All mentions in the exam are now Looker Studio.
- **Cloud Source Repositories**: Deprecated (2024). Use GitHub/GitLab + Cloud Build for CI/CD.
- **Data Catalog**: Merging into Dataplex Universal Catalog. In real exams, "Dataplex (Catalog)" may appear. Lineage is now Dataplex Lineage.
- **Firestore "10k writes/sec limit"**: Removed (2021). But the approach of "high throughput = Bigtable" remains valid.
- **Q22: Datastream + Teradata**: Incorrect. Datastream supports Oracle, MySQL, PostgreSQL, SQL Server, **not Teradata**. Use BigQuery DTS for Teradata → BigQuery. Trust the correct options accordingly.
- **Q3: "Table-level write region / consistency setting"**: Does not exist in Spanner. Actual: instance configuration (leader region, dual-region setup) + client-specified strong / bounded staleness reads. Understand as: critical=strong read, non-critical=stale read.
- **Q46: "Cloud DLP differential privacy library"**: Actually refers to **BigQuery's differential privacy aggregation (`SELECT WITH DIFFERENTIAL_PRIVACY`)** or Google OSS DP library. DLP provides re-identification risk analysis, not DP.
- **BQ Pricing**: Flat-rate discontinued; current is **Editions (Standard/Enterprise/Plus) + autoscaling slots**. (Q47 reflects current specs).
- **Support for Dataform / Datastream / BigLake / Iceberg**: Increasing in 2024 exam guides, but less emphasized here. Check official Exam Guide for updates.

---

## 6. How to Review Effectively

1. Hide the "Decisive Point" column, and answer immediately from the requirement keywords (aim: 50 questions in 15 minutes).
2. Review only the questions you got wrong by returning to the question text.
3. Keep in mind the discrepancies in section 5, then verify answers with official sample questions (Cloud Skills Boost).