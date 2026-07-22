<!-- i18n: language-switcher -->
[English](scenario-drills.md) | [日本語](scenario-drills.ja.md)

# AIP-C01 scenario drills

These are original exercises, not copied exam questions. For each one, say the requirement words, candidate design, and elimination reason aloud before opening the answer.

## 1. Version-aware RAG

Several departments store different versions of one policy in S3. Answers must use only the latest approved version for the requested department. What is the lowest-operations improvement?

<details><summary>Answer</summary>

Ingest `business_unit`, `approved`, and `effective_at` as metadata and filter at retrieval time. More embedding dimensions cannot guarantee version or approval state.
</details>

## 2. Exact IDs and symptoms

An operations assistant must reach the same runbook for `DB-781` and “connections drop intermittently.”

<details><summary>Answer</summary>

Combine keyword search over error-code fields with vector search over the narrative text. Rerank top candidates when needed.
</details>

## 3. Chunk size

In a 100-page contract, an exception is two sentences long, but the answer needs the conditions from its full section.

<details><summary>Answer</summary>

Use hierarchical chunking: search a small child containing the exception and return its larger parent as context.
</details>

## 4. Frequently changing facts

A product price list changes daily. A team proposes fine-tuning a custom model every week to keep answers current.

<details><summary>Answer</summary>

Use RAG or a deterministic data tool, not fine-tuning. Update the index or database and answer prices only from retrieved results.
</details>

## 5. Webhook acknowledgement

A partner webhook needs a response within two seconds. Generated explanations go to CRM, notification, and audit systems, and more consumers will be added later.

<details><summary>Answer</summary>

Validate the signature in API Gateway/Lambda, publish to EventBridge, and acknowledge. Invoke Bedrock downstream and fan out the generated event with rules.
</details>

## 6. Bursty ingestion

On-premises devices can use only HTTPS. Thousands of events arrive at shift change, and events must survive a Bedrock outage.

<details><summary>Answer</summary>

Use API Gateway → SQS service integration → Lambda consumer → Bedrock. The queue absorbs the burst and temporary outage.
</details>

## 7. Agent loops

During an external API outage, an agent repeatedly requests the same tool and increases token cost.

<details><summary>Answer</summary>

Track tool failures in Step Functions and stop with a Choice condition. Put a shared circuit breaker in DynamoDB with TTL and fail fast during cooldown.
</details>

## 8. Tool parameters

The model sometimes sends an empty array instead of a string for `customerId`.

<details><summary>Answer</summary>

Use a typed schema, strict server-side validation, and a structured error such as `INVALID_CUSTOMER_ID`. Retries alone do not repair the contract.
</details>

## 9. Human approval

A qualified reviewer must edit and approve a generated denial notice before sending it. Review can take hours.

<details><summary>Answer</summary>

Use a Step Functions callback/wait pattern, accept edits and approval through an API, and store draft, final text, and reviewer feedback in DynamoDB.
</details>

## 10. PII

Names and phone numbers from customer chat must not reach the model, but references to the same person must remain consistent.

<details><summary>Answer</summary>

Detect PII with Comprehend and replace it with stable placeholders such as `<NAME_1>`. Add Guardrails input/output masking as defense in depth.
</details>

## 11. Policy validation

The system must detect logical conflict with a lending-communication policy and always prevent sending when a conflict exists.

<details><summary>Answer</summary>

Use Automated Reasoning checks for policy findings, then have application code inspect those findings and block, rewrite, or fall back. The checks operate in detection mode.
</details>

## 12. Audit evidence

An auditor asks both who invoked an API and which sources produced a particular answer.

<details><summary>Answer</summary>

Use CloudTrail for API identity/activity. Use an application decision log for the model ID, prompt version, retrieved source IDs, and response metadata.
</details>

## 13. Private connectivity

A Lambda function in a private subnet must reach Bedrock, Athena, and S3 without using the public internet.

<details><summary>Answer</summary>

Use interface VPC endpoints for Bedrock and Athena and a gateway endpoint for S3. A NAT Gateway to public endpoints does not satisfy a private service-path requirement.
</details>

## 14. Deterministic SQL

A proposal lets a model generate arbitrary Athena SQL, but non-`SELECT` operations must be impossible.

<details><summary>Answer</summary>

Map intent to allowlisted, parameterized `SELECT` templates. Do not rely only on string inspection of freely generated SQL.
</details>

## 15. Perceived latency

Traffic is bursty, the team does not want dedicated capacity, and chat abandonment must decrease.

<details><summary>Answer</summary>

Stream tokens with `ConverseStream` to reduce time to first token. Provisioned Throughput is not required by this requirement.
</details>

## 16. Nightly workload

Five hundred thousand transcripts must be summarized to S3 overnight, and synchronous invocations are throttled.

<details><summary>Answer</summary>

Use Bedrock batch inference with S3 input and output as an offline job.
</details>

## 17. Predictable peak

Synchronous requests grow 10× for 30 minutes at 09:00 on weekdays, and the workload must stay on one model in one Region.

<details><summary>Answer</summary>

Size Provisioned Throughput from forecast requests/tokens per minute and invoke the provisioned model ARN.
</details>

## 18. Context overflow

Sending every conversation turn and every RAG chunk exceeds the context limit.

<details><summary>Answer</summary>

Use `CountTokens` before invocation, compress old turns into a running summary, retain recent turns, and cap retrieved chunks.
</details>

## 19. Release gate

Answers vary slightly after a prompt change, but quality must remain at least as good as the previous version under an automated gate.

<details><summary>Answer</summary>

Compare baseline and candidate on a fixed prompt dataset with Model Evaluations or a judge model and gate on a quality threshold. Do not use exact matching.
</details>

## 20. Agent evaluation

The endpoint always returns HTTP 200, but the agent calls three unnecessary tools before answering.

<details><summary>Answer</summary>

Measure goal attainment and tool/parameter accuracy, then inspect traces for tool count and loops. Availability alone does not measure task success.
</details>
