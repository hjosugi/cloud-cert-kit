<!-- i18n: language-switcher -->
[English](flashcards.md) | [日本語](flashcards.ja.md)

# AIP-C01 comparisons and flashcards

Hide each answer and allow ten seconds. Add only cards you cannot explain to the [wrong-answer log](wrong-answers.en.md).

## RAG and data

### 1

**Q.** Vector search misses CVE IDs and error codes. What should change first?<br>
**A.** Use hybrid keyword and vector search. Extract IDs into a keyword clause or metadata filter.

### 2

**Q.** The correct chunk is in the top-k set but ranks too low. What should you add?<br>
**A.** A reranker. It cannot recover an answer that initial retrieval never returned.

### 3

**Q.** A small clause must match precisely, but the answer needs surrounding context. Which chunking strategy fits?<br>
**A.** Hierarchical chunking: index and search child chunks, then return the corresponding parent.

### 4

**Q.** How do you select the latest approved policy for a specific region or business unit?<br>
**A.** Store fields such as timestamp, approval state, region, and business unit as metadata and filter on them.

### 5

**Q.** What is wrong with copying all metadata into every chunk body?<br>
**A.** It adds tokens and noise, can fragment during chunking, and loses reliable structured filtering.

### 6

**Q.** One product index must accept both image and text queries. Which model class is required?<br>
**A.** A multimodal embedding model; a text-only embedding cannot represent images.

### 7

**Q.** What is a low-operations RAG pattern for documents in S3?<br>
**A.** Bedrock Knowledge Bases with an embedding model, a managed vector store, and RetrieveAndGenerate.

### 8

**Q.** How can S3 updates reach a Knowledge Base near real time?<br>
**A.** S3 event → EventBridge → Lambda → `StartIngestionJob`.

### 9

**Q.** How does conversation memory differ from a Knowledge Base?<br>
**A.** Memory stores per-session or per-actor state and preferences; a Knowledge Base retrieves from a shared document corpus.

### 10

**Q.** Which managed service extracts structured JSON from PDFs, images, and audio?<br>
**A.** Bedrock Data Automation; combine it with Glue for tabular formats such as CSV when needed.

## Implementation and agents

### 11

**Q.** How can you implement a ReAct loop, branches, retries, timeouts, and audit history with little custom orchestration code?<br>
**A.** AWS Step Functions.

### 12

**Q.** A webhook needs an immediate acknowledgement and future fan-out to more consumers. What pattern fits?<br>
**A.** Validate with API Gateway/Lambda, publish to EventBridge, and fan out with rules.

### 13

**Q.** How do you buffer a burst for asynchronous processing by one worker pool?<br>
**A.** Amazon SQS.

### 14

**Q.** Non-developers need to edit prompt chains and conditional branches. What should they use?<br>
**A.** Bedrock Flows.

### 15

**Q.** Two foundation models should produce separate artifacts concurrently and merge them deterministically. What design fits?<br>
**A.** A Step Functions Parallel state followed by a Lambda merge.

### 16

**Q.** An agent calls a tool with an empty `orderId`. What should be fixed before changing models?<br>
**A.** Use a typed tool schema, server-side validation, and structured errors so the agent asks for missing information.

### 17

**Q.** Why is an in-memory circuit breaker inside Lambda unreliable?<br>
**A.** State is not shared across concurrent execution environments and reuse is not guaranteed. Use a shared store such as DynamoDB with TTL.

### 18

**Q.** Can a Cognito JWT be sent directly to the Bedrock Runtime API?<br>
**A.** No. The API uses AWS credentials, SigV4 signing, and IAM authorization.

### 19

**Q.** How can an Okta workforce use Bedrock securely from local scripts?<br>
**A.** Federate Okta with IAM Identity Center, assign a permission set, and use short-lived credentials.

### 20

**Q.** What is the basic conversation-history schema for `ConverseStream`?<br>
**A.** A `messages` array whose turns contain `role` and `content`.

## Safety and governance

### 21

**Q.** Which managed control filters harmful topics and profanity in real time?<br>
**A.** Bedrock Guardrails content, denied-topic, and word filters.

### 22

**Q.** How can you hide PII before the model while preserving conversation relationships?<br>
**A.** Detect it with Comprehend and replace entities with stable placeholders; add Guardrails masking as defense in depth.

### 23

**Q.** Which service continuously discovers PII left in an S3 audit bucket?<br>
**A.** Amazon Macie.

### 24

**Q.** What do contextual-grounding checks measure?<br>
**A.** Whether a response is grounded in its source and relevant to the query—not PII filtering or prompt-injection defense.

### 25

**Q.** Do Automated Reasoning checks automatically block a violating response?<br>
**A.** No. They return findings; the application must block, rewrite, clarify, or fall back.

### 26

**Q.** Why are Automated Reasoning checks not a prompt-injection defense?<br>
**A.** They validate supplied content against a policy; they do not identify and block malicious instructions themselves.

### 27

**Q.** Can CloudTrail reconstruct which sources supported an answer?<br>
**A.** No. It records API activity. Log source IDs, prompt versions, and response metadata in an application decision log.

### 28

**Q.** How can you see which Knowledge Base and action group an agent used?<br>
**A.** Inspect the agent trace.

### 29

**Q.** What pattern prevents a model from inventing transaction amounts?<br>
**A.** Execute an allowlisted, parameterized, read-only query or tool and answer only from its result set.

### 30

**Q.** How do WAF and Guardrails differ?<br>
**A.** WAF protects the HTTP surface from web exploits; Guardrails apply safety controls to natural-language inputs and outputs.

## Cost and performance

### 31

**Q.** How can repeated deterministic requests avoid a foundation-model invocation entirely?<br>
**A.** Cache by a fingerprint of the normalized prompt and model configuration, for example at CloudFront.

### 32

**Q.** Does prompt caching remove the model invocation?<br>
**A.** No. It reuses processing of a shared prompt prefix.

### 33

**Q.** What makes a semantic cache harder than an exact cache?<br>
**A.** It adds query-embedding cost and needs a similarity threshold that avoids incorrect hits.

### 34

**Q.** What most directly reduces user-perceived latency?<br>
**A.** Stream output to reduce time to first token; measure it separately from full-completion latency.

### 35

**Q.** How should hundreds of thousands of nightly summaries be processed?<br>
**A.** Bedrock batch inference with input and output in S3.

### 36

**Q.** Traffic grows predictably by 10× for 45 minutes each morning in one Region. What should you evaluate?<br>
**A.** Provisioned Throughput sized from the required requests and tokens per minute.

### 37

**Q.** How can a US workload absorb a regional impairment or quota spike?<br>
**A.** Use an appropriate US geographic cross-Region inference profile.

### 38

**Q.** Do retries and backoff increase throttling capacity?<br>
**A.** No. They smooth transient failures but do not create capacity.

### 39

**Q.** How can context-window overflow be prevented before invocation?<br>
**A.** Use `CountTokens`, remove old turns or retrieved chunks when over budget, and summarize history when needed.

### 40

**Q.** Lambda creates a new TLS connection on every invocation. What should change?<br>
**A.** Initialize the SDK or HTTP client outside the handler and use connection pooling/keep-alive.

## Evaluation and release

### 41

**Q.** What is an appropriate pre-deployment regression test for a prompt or model change?<br>
**A.** Run Bedrock Model Evaluations on a fixed prompt dataset and gate on quality relative to the baseline.

### 42

**Q.** Why is exact-string matching unsuitable for generated answers?<br>
**A.** Correct meaning can have different wording. Use semantic quality metrics or a judge model.

### 43

**Q.** Can ROUGE or BLEU alone measure factuality?<br>
**A.** No. String overlap does not adequately measure hallucination, consistency, or fluency.

### 44

**Q.** What does a RAG evaluation dataset need besides prompts?<br>
**A.** Ground truth such as expected retrieved text or reference responses.

### 45

**Q.** Which RAG metrics should be separated?<br>
**A.** Retrieval context relevance/coverage versus generation faithfulness, answer relevance, and citation quality.

### 46

**Q.** Is HTTP 200 enough to prove agent task success?<br>
**A.** No. Measure goal attainment, tool selection, parameter accuracy, and loop count.

### 47

**Q.** How can a rollout automatically revert when error rate or latency degrades?<br>
**A.** Use canary or linear deployment with CloudWatch alarms and automatic rollback.

### 48

**Q.** How can production regressions be detected continuously?<br>
**A.** Run representative workflows on a schedule with CloudWatch Synthetics and alarms.

### 49

**Q.** Give an example of separating model quality from operational performance.<br>
**A.** Correctness/helpfulness are quality; latency, errors, and token count are operational. Measure both without treating one as a substitute.

### 50

**Q.** What should be checked before choosing fine-tuning?<br>
**A.** Confirm that RAG, prompting, Guardrails, and deterministic validation cannot solve a stable behavior/style requirement; include update cadence and lifecycle cost.
