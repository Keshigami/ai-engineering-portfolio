# Project Title: Content Ops Assistant

## 1. Problem Statement & Business Impact

- **The Problem**: Marketing teams spend days tailoring a single campaign brief for different social channels and personas.
- **Goal**: Accelerate content production by 10x while maintaining brand consistency.
- **Metric of Success**: Content generation time < 10s, Tone consistency score > 90%.

## 2. Technical Solution

- **Approach**: Built a multi-prompt orchestration tool that maps a single source of truth (brief) to diverse output formats using dynamic prompt templates.
- **Stack**: Streamlit, OpenAI GPT-3.5-Turbo, Python.
- **Diagram**: [Brief] -> [Tone/Brand Injection] -> [Parallel LLM Calls] -> [Multi-Channel Copy]

## 3. Evaluation & Results

- **Performance**: Capable of generating a full campaign set (Email, Social, Ads) in under 15 seconds.
- **Efficiency**: Cost-effective content scaling compared to traditional agency work.
- **Tradeoffs**: Chose Streamlit for the UI to prioritize rapid iteration and proof-of-concept over a complex React frontend.

## 4. Case Study Narrative

- **Context**: Showcases the power of generative AI in creative workflows and the importance of "brand guardrails."
- **Implementation**: Developed a dashboard with adjustable "brand sliders" that modify the LLM's system prompt in real-time.
- **Limitations**: High-stakes copy still requires a human-in-the-loop for final approval.
- **Next Steps**: Integrate DALL-E 3 for automatic social media image generation matching the copy's tone.
