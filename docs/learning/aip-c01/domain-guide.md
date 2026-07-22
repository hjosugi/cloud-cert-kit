<!-- i18n: language-switcher -->
[English](domain-guide.md) | [日本語](domain-guide.ja.md)

# AIP-C01 domain decision guide

The official blueprint weights the domains at D1 31%, D2 26%, D3 20%, D4 12%, and D5 11%. Success depends less on memorizing every service than on mapping requirement words to defensible design patterns.

Official source: [AWS Certified Generative AI Developer - Professional Exam Guide](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01.html)

## Domain 1: Foundation Model Integration, Data Management, and Compliance — 31%

This domain covers model and embedding selection, RAG ingestion and retrieval, structured and unstructured data, and lifecycle management for models, prompts, and configurations.

### RAG decision order

1. If knowledge changes frequently, prefer RAG over fine-tuning.
2. If exact identifiers matter, prefer hybrid search over vector-only search.
3. If a precise clause and its larger context are both needed, use hierarchical chunking.
4. If version, department, Region, or access limits matter, use metadata filtering.
5. If the right result is already in top-k but ranked poorly, add a reranker.

| Method | Strength | Limitation | Signal |
|---|---|---|---|
| Keyword | IDs, names, exact matches | Weak on paraphrases | CVE, error code, model number |
| Vector | Meaning and paraphrases | Can miss exact IDs | Natural language, similar symptoms |
| Hybrid | Exact and semantic retrieval | Requires a deliberate index design | IDs mixed with prose |
| Reranking | Improves top-k order | Adds latency and cost | Correct candidate already retrieved |
| Metadata filter | Limits version, department, or access | Depends on metadata quality | Latest, approved, business unit |

### Chunking

| Strategy | Choose when | Caution |
|---|---|---|
| Fixed | Documents are uniform and ingestion must stay simple | Meaning can split at arbitrary boundaries |
| Semantic | Meaningful boundaries matter | Adds model cost during ingestion |
| Hierarchical | Search a precise child and return a broader parent | Preserve and understand the parent-child link |
| No chunking | Whole-document retrieval is truly required | Accuracy degrades on long, multi-topic documents |

### Data-service choices

| Input or requirement | Low-operations choice |
|---|---|
| RAG over S3 documents | Bedrock Knowledge Bases |
| SharePoint or Confluence | Supported Knowledge Base connector |
| Salesforce data also retained in S3 | AppFlow → S3 → Knowledge Base |
| Structured extraction from PDF, image, or audio | Bedrock Data Automation |
| CSV normalization | AWS Glue |
| Real-time PII detection | Comprehend and/or Guardrails |
| PII discovery in stored S3 data | Macie |

Remember that DynamoDB is not the general answer for k-NN search, text-only embeddings do not embed images, Prompt Management versions prompts rather than models, and Knowledge Bases are retrieval—not conversation memory.

## Domain 2: Implementation and Integration — 26%

| Requirement | Pattern |
|---|---|
| Immediate response | API Gateway → Lambda → Bedrock Runtime |
| Token streaming | WebSocket/SSE → `ConverseStream` |
| Long-running asynchronous work | API → SQS → worker → result store and job ID |
| Large nightly workload | Bedrock batch inference with S3 input/output |
| Immediate webhook acknowledgement | API Gateway → validation → EventBridge or SQS |
| Fan-out to several consumers | EventBridge rules |

### Choose the orchestrator

| Service | Use it for | Avoid it for |
|---|---|---|
| Step Functions | Branches, retries, approval waits, parallel work, audit history, bounded agent loops | Stateless fan-out only |
| EventBridge | Decoupled fan-out, content routing, adding consumers | Stateful ordering |
| SQS | Bursts, backpressure, and replay | Broadcasting one message to every consumer |
| Bedrock Flows | Prompt chains editable by non-developers | Strict, long-running business workflows |

### Agent-tool boundary

- Define types, required fields, and descriptions in the tool schema.
- Validate again in the tool; never trust model-generated parameters.
- Return structured errors that let the agent request missing information.
- Restrict the execution role to the exact table, bucket, and secret resources.
- Bound tool failures and loop count in the workflow.
- Store a cross-invocation circuit breaker in shared state such as DynamoDB with TTL, not Lambda memory.

Bedrock Runtime uses IAM and SigV4. Do not send a browser JWT directly. For workforce SSO, federate an external IdP through IAM Identity Center and issue short-lived credentials with model-scoped inference permissions.

## Domain 3: AI Safety, Security, and Governance — 20%

| Guardrail component | Purpose |
|---|---|
| Content filter | Harmful content and prompt attacks |
| Denied topics | Business-prohibited subjects |
| Word filter | Prohibited exact phrases |
| Sensitive-information filter | Block or mask PII |
| Contextual-grounding check | Source grounding and query relevance |
| Automated Reasoning checks | Return findings about logical consistency with policy rules |

Automated Reasoning checks are a detection layer. The application must decide whether to serve, rewrite, clarify, or fall back. They do not replace prompt-injection defenses or denied-topic controls.

### Defense in depth

```text
WAF and API validation
        ↓
input normalization and stable PII placeholders
        ↓
Bedrock Guardrails
        ↓
model, Knowledge Base, and agent tools
        ↓
deterministic output-schema and PII validation
        ↓
safe response contract
```

WAF owns web exploits, Guardrails own generative-AI content controls, IAM owns AWS resource authorization, and application validation owns deterministic business rules.

### Deterministic data access

For exact values such as transaction amount, inventory, or approval state:

1. Map user intent to an allowlisted operation.
2. Execute a parameterized read-only query or typed tool.
3. Give the model only that result set.
4. Log the source ID, query-template version, and model ID.

CloudTrail answers who called an AWS API. Application logs record prompt/model/source/result decisions. Agent trace records Knowledge Base and tool orchestration. Do not substitute one for another.

## Domain 4: Operational Efficiency and Optimization — 12%

| Symptom | Primary response |
|---|---|
| Users wait for the first output | Streaming to reduce time to first token |
| Many identical deterministic requests | Fingerprinted edge cache |
| Long shared system prompt | Prompt caching |
| Expensive model receives simple requests | Intelligent prompt routing or model cascade |
| Large nightly workload | Batch inference |
| Predictable synchronous peak | Provisioned Throughput |
| Regional impairment or quota spike | Cross-Region inference profile |
| Context-window overflow | `CountTokens`, pruning, summarization, and fewer retrieved chunks |
| Lambda connection setup is slow | Reuse SDK clients and keep-alive connections |

An edge cache avoids the model call. Prompt caching still calls the model and reuses shared-prefix processing. Semantic caching adds embedding cost and false-hit threshold management. Retry/backoff smooths transient failures but does not add capacity.

## Domain 5: Testing, Validation, and Troubleshooting — 11%

| Target | Representative metrics |
|---|---|
| Model response | Correctness, helpfulness, fluency, robustness |
| Retrieval | Context relevance, coverage, precision |
| RAG generation | Faithfulness, answer relevance, citation quality |
| Agent | Goal attainment, tool selection, parameter accuracy, loop count |
| Production API | Latency, error, availability, token usage |

Use a ground-truth dataset that includes expected retrieved text or reference responses, not prompts alone. Compare baseline and candidate with Model Evaluations, gate deployment on quality, roll out with canary or linear traffic, automatically roll back on operational alarms, and continuously exercise representative workflows with synthetics.

Reject exact-string matching as the sole generation metric, latency or token count as a quality proxy, and HTTP 200 as proof of agent success.

## Fifteen final rules

1. Use RAG for current knowledge, prompts for behavior and format, Guardrails for policy, and customization only for a demonstrated stable need.
2. Combine exact IDs and natural language with hybrid search.
3. Search children and return parent context with hierarchical chunking.
4. Keep metadata structured and filterable instead of copying it into prose.
5. Step Functions holds state, EventBridge fans out, SQS buffers, and Flows models prompt workflows.
6. Revalidate every model-generated tool argument at the tool boundary.
7. Use Comprehend/Guardrails for live PII and Macie for discovery in S3.
8. Automated Reasoning returns findings; application code enforces the outcome.
9. CloudTrail records API activity; agent trace records orchestration.
10. Return exact values only from an allowlisted query or tool result.
11. Streaming improves perceived latency, provisioned capacity handles predictable load, and batch handles offline work.
12. Edge caching avoids a model call; prompt caching does not.
13. `CountTokens` budgets input before a call; `maxTokens` caps output.
14. Use fixed-dataset quality gates before release and synthetics plus alarms after release.
15. Choose fine-tuning, GPU hosting, or custom pipelines only when the requirement explicitly justifies them.
