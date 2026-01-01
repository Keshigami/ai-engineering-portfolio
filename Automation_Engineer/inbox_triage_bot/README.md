# Project Title: Ops Inbox Triage Bot

## 1. Problem Statement & Business Impact

- **The Problem**: Operations teams are overwhelmed by generic inboxes, resulting in slow response times to high-value leads.
- **Goal**: Automatically classify, summarize, and route emails to reduce manual triaging by 70%.
- **Metric of Success**: Correct routing > 95%, Triage time < 5s per email.

## 2. Technical Solution

- **Approach**: Built a pipeline that uses an LLM to extract intent and structured metadata from unstructured emails.
- **Stack**: Python, OpenAI, Pydantic, Streamlit.
- **Diagram**: [Incoming Email] -> [Prompt Engineering] -> [LLM Classifier] -> [Routing Engine (Slack/CRM)]

## 3. Evaluation & Results

- **Performance**: High reliability in distinguishing "Sales" from "Spam".
- **Efficiency**: Significantly faster than human triage (5s vs ~2min per email).
- **Tradeoffs**: Used GPT-3.5-Turbo's JSON mode for deterministic output over custom regex-based parsing.

## 4. Case Study Narrative

- **Context**: Highlights AI's role in workflow automation and decision-making.
- **Implementation**: Created a script that validates LLM output against a strict schema before triggering downstream actions.
- **Limitations**: Sarcastic or extremely short emails can lead to misclassification.
- **Next Steps**: Connect to a live Gmail/Outlook API via webhooks for real-time automation.
