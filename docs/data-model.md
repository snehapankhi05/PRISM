# PRISM Data Model

## Core Persistence Flow

Source
  ↓
FactGraph
  ↓
OutputDraft
  ↓
ProvenanceLink
  ↓
RenderedAsset

Controls and Job metadata coordinate the generation process.

## Core Entities

- Source
- FactGraph
- Controls / Job
- OutputDraft
- ProvenanceLink
- StyleMemory
- RenderedAsset

## Source

Represents the original content submitted to PRISM.

Initial fields:

- `id`
- `source_type`
- `title`
- `content`
- `metadata`
- `created_at`
- `updated_at`

## FactGraph

Represents the structured, versioned factual representation extracted from a Source.

Initial fields:

- `id`
- `source_id`
- `version`
- `graph_data`
- `extraction_metadata`
- `created_at`
- `updated_at`

## Controls

Represents operator-selected generation controls.

Initial fields:

- `target_audience`
- `tone`
- `language`
- `level_of_detail`
- `communication_objective`
- `content_style`

## Job

Represents one generation workflow execution.

Initial fields:

- `id`
- `source_id`
- `fact_graph_id`
- `status`
- `controls`
- `created_at`
- `updated_at`

## Output Types

PRISM supports these output types:

1. LinkedIn Post
2. Twitter/X Post
3. Advisory
4. Infographic
5. Executive Summary
6. Presentation
7. Video

## OutputDraft

Represents a generated content draft for one requested output type.

Initial fields:

- `id`
- `job_id`
- `output_type`
- `version`
- `content`
- `status`
- `quality_metadata`
- `created_at`
- `updated_at`

## ProvenanceLink

Connects a generated claim or content element back to the source evidence.

Initial fields:

- `id`
- `output_draft_id`
- `source_id`
- `source_reference`
- `claim_reference`
- `confidence`
- `created_at`

## RenderedAsset

Represents a final rendered file generated from an OutputDraft.

Initial fields:

- `id`
- `output_draft_id`
- `asset_type`
- `file_path`
- `mime_type`
- `metadata`
- `created_at`

## StyleMemory

Represents reusable style preferences or learned style information associated with content generation.

Initial fields:

- `id`
- `name`
- `description`
- `style_data`
- `created_at`
- `updated_at`

## Relationships

- One Source can have multiple FactGraph versions.
- One Source can be associated with multiple Jobs.
- One Job uses one selected FactGraph version.
- One Job can produce multiple OutputDrafts.
- One OutputDraft belongs to one Job.
- One OutputDraft can have multiple ProvenanceLinks.
- One OutputDraft can have multiple RenderedAssets.
- One Source can be referenced by multiple ProvenanceLinks.
- StyleMemory can be associated with generation workflows when implemented.

