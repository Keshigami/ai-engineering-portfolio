# Project Title: Support Ticket Classifier

## 1. Problem Statement & Business Impact

- **The Problem**: High-volume support teams spend 20% of their time manually triaging and tagging tickets.
- **Goal**: Auto-tag and prioritize incoming tickets to reduce manual effort by 50%.
- **Metric of Success**: Accuracy > 90%, Latency < 2s per ticket.

## 2. Technical Solution

- **Approach**: Built a FastAPI endpoint that leverages LLM function calling/JSON mode to classify text into structured metadata.
- **Stack**: FastAPI, OpenAI GPT-3.5-Turbo, Pydantic.
- **Diagram**: [Webhook/Input] -> [FastAPI] -> [LLM] -> [Structured Metadata] -> [Inbox Routing]

## 3. Evaluation & Results

- **Performance**: High semantic accuracy for standard categories (billing, tech).
- **Efficiency**: Cost ~$0.002 per ticket using GPT-3.5-Turbo.
- **Tradeoffs**: Chose GPT-3.5-Turbo over GPT-4 for 10x lower cost and sufficient classification accuracy.

## 4. Case Study Narrative

- **Context**: Demonstrates applied NLP and LLM integration into standard software architectures.
- **Implementation**: Developed a robust API that handles unstructured text and returns JSON-compatible objects for downstream automation.
- **Limitations**: Requires clear system prompts to maintain tag consistency.
- **Next Steps**: Implement few-shot examples to handle niche technical queries.
