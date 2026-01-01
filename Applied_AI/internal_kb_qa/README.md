# Project Title: Internal Knowledge-Base Q&A (RAG)

## 1. Problem Statement & Business Impact

- **The Problem**: Employees spend hours searching through disparate PDFs and Notion docs for company processes.
- **Goal**: Provide an instant Q&A interface that answers questions with 100% grounded citations.
- **Metric of Success**: Retrieval precision > 85%, Hallucination rate < 1%.

## 2. Technical Solution

- **Approach**: Implemented a Retrieval-Augmented Generation (RAG) pipeline using LangChain.
- **Stack**: LangChain, ChromaDB, OpenAI, Streamlit.
- **Diagram**: [PDF Docs] -> [Recursive Partitioning] -> [Vector DB] -> [Similarity Search] -> [LLM with Context]

## 3. Evaluation & Results

- **Performance**: High grounding accuracy; citations ensure users can verify answers.
- **Efficiency**: RAG reduces LLM context window costs compared to passing all docs.
- **Tradeoffs**: Chose ChromaDB for this v1 (local/fast) over Pinecone to allow for zero-cost developer setup.

## 4. Case Study Narrative

- **Context**: Demonstrates the "Gold Standard" of business AI: RAG.
- **Implementation**: Built a chunking and embedding pipeline that converts unstructured PDFs into a searchable vector space.
- **Limitations**: Currently relies on text; does not handle tables/images in PDFs well.
- **Next Steps**: Integrate an agentic layer to choose between multiple vector stores or external web search.
