# RAG (Retrieval-Augmented Generation)

RAG is a technique that combines an **LLM with a retrieval system**.

The retrieval system searches external sources such as:

* Documents
* Databases
* Knowledge bases
* PDFs
* Websites
* Internal company data

When the LLM needs additional information, the relevant information is retrieved and provided to the LLM so it can generate a **more accurate and context-aware answer**.

---

# Tokens

A **token** is a unit of text that an LLM processes.

A token can represent:

* A character
* Part of a word
* A complete word
* Sometimes multiple characters/words depending on the tokenizer

Example:

```text
"Hello" → may be 1 token
"I am" → may be 2 tokens
```

> Tokenization depends on the tokenizer and model, so we should not assume that every word equals exactly one token.

### Why tokens matter?

Tokens affect:

* Context window
* API cost
* Processing speed
* Input/output limits

---

# Context Window

The **context window** is the maximum amount of tokens an LLM can process at one time.

It includes things such as:

```text
User Query
+
System Instructions
+
Conversation History
+
Retrieved Documents
+
LLM Response
```

For example, if a model has a context window of **128K tokens**, the total input context and generated output must fit within the model's supported limits.

### Why is context window important in RAG?

We usually cannot send an entire large document to the LLM.

Instead:

```text
Large Document
      ↓
Chunking
      ↓
Retrieve relevant chunks
      ↓
Send only relevant chunks to LLM
      ↓
Generate Answer
```

This reduces unnecessary context and can improve efficiency and relevance.

---

# RAG Pipeline

A typical RAG system has two major pipelines:

```text
1. Ingestion Pipeline
2. Retrieval Pipeline
```

---

# 1. Ingestion Pipeline

The ingestion pipeline converts raw documents into searchable vector representations.

### Flow

```text
Source Documents
      ↓
Document Loading
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Model
      ↓
Vector Embeddings
      ↓
Vector Database
```

### Example

Suppose we have a **10 MB document**.

```text
10 MB Document
      ↓
Chunking
      ↓
10,000 Chunks
      ↓
Embedding Model
      ↓
10,000 Vector Embeddings
      ↓
Vector Database
```

Each chunk is converted into a numerical vector.

Example:

```text
"Cat is a small furry domestic animal"
                    ↓
        Embedding Model
                    ↓
             [34, 21, 75]
```

The actual vector will normally have many more dimensions than this example.

---

# 2. Retrieval Pipeline

When a user asks a question, the system searches the vector database for relevant information.

### Flow

```text
User Query
    ↓
Embedding Model
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Chunks
    ↓
Re-ranking (Optional)
    ↓
Relevant Context
    ↓
LLM
    ↓
Final Answer
```

### Example

User asks:

```text
"What is the company's leave policy?"
```

The query is converted into an embedding.

The vector database searches for chunks that are **semantically similar** to the query.

The most relevant chunks are then given to the LLM.

```text
User Query
     ↓
Embedding
     ↓
Vector DB
     ↓
Top-K Relevant Chunks
     ↓
LLM
     ↓
Answer
```

---

# Embeddings

An **embedding** is a numerical/vector representation of data such as:

* Text
* Sentences
* Documents
* Images
* Other types of data

The goal is to represent the **semantic meaning** of the input in vector space.

Example:

```text
cat     → [34, 21, 75]
kitten  → [33, 20, 60]
elephant → [2, 55, 34]
```

In a real embedding system, vectors typically contain hundreds or thousands of dimensions.

Semantically similar text tends to have vectors that are closer together according to a chosen similarity/distance measure.

---

# Embedding Model

An **embedding model** converts text into vectors.

Example:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Popular embedding providers/models include:

### OpenAI

```text
text-embedding-3-small
text-embedding-3-large
```

`text-embedding-3-large` supports up to **3072 dimensions**, and its dimensionality can be reduced using the model's supported dimensions parameter.

### Other Providers

```text
Mistral
Voyage AI
Cohere
Hugging Face
```

---

# Important RAG Rule

### Use the same embedding model for documents and user queries.

During ingestion:

```text
Document Chunk
      ↓
Embedding Model
      ↓
Document Vector
      ↓
Vector DB
```

During retrieval:

```text
User Query
      ↓
Same Embedding Model
      ↓
Query Vector
      ↓
Vector DB
```

This keeps the document vectors and query vectors in the **same embedding space**, allowing meaningful similarity comparisons.

---

# Vector Database

A **vector database** stores and searches vector embeddings efficiently.

It typically stores:

```text
Vector
+
Original Text / Chunk
+
Metadata
```

Example:

```text
Vector:
[0.21, -0.43, 0.87, ...]

Text:
"Employees can take 20 days of annual leave."

Metadata:
{
    "source": "company_policy.pdf",
    "page": 12
}
```

### Popular Vector Databases / Vector Stores

```text
FAISS
Pinecone
ChromaDB
Weaviate
Qdrant
Milvus
```

You can also use **PostgreSQL with pgvector** for vector search.

---

# Similarity Search

Similarity search finds vectors that are closest to the query vector.

Common similarity/distance methods include:

```text
Cosine Similarity
Euclidean Distance
Dot Product
```

Example:

```text
User Query
    ↓
Query Embedding
    ↓
[0.21, 0.43, 0.67]
    ↓
Vector DB
    ↓
Find Similar Vectors
    ↓
Top-K Chunks
```

---

# Re-ranking

Sometimes the initial vector search returns several potentially relevant chunks.

A **re-ranker** can then reorder these results based on their relevance to the query.

```text
Query
 ↓
Vector Search
 ↓
Top 10 Chunks
 ↓
Re-ranker
 ↓
Top 3 Most Relevant Chunks
 ↓
LLM
```

This can improve retrieval quality.

---

# Complete RAG Architecture

```text
                 INGESTION
                     │
             ┌───────▼────────┐
             │ Source Documents│
             └───────┬────────┘
                     ↓
                Chunking
                     ↓
              Embedding Model
                     ↓
               Embeddings
                     ↓
              Vector Database
                     │
                     │
              ───────┼────────
                     │
                     │
                 RETRIEVAL
                     │
                 User Query
                     ↓
              Embedding Model
                     ↓
               Query Embedding
                     ↓
              Similarity Search
                     ↓
              Relevant Chunks
                     ↓
                 Re-ranking
                     ↓
               Context + Query
                     ↓
                    LLM
                     ↓
              Generated Answer
```

# RAG in One Line

> **RAG = Retrieve relevant information → provide it as context to the LLM → generate an answer.**

### Core RAG Stack

```text
Python
   ↓
Document Loaders
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
Re-ranker
   ↓
LLM
   ↓
Answer
```

This is the **core RAG knowledge** you should be comfortable explaining in an AI Engineer interview.


#Gen AI :
one input --> one output . interaction end here 

prompt --->LLM ---> Response 
a simple chain 

no tools 
no memory between calls 
no decision 
no loops 

#Ai agent  --> LLM with tools 
LLM + Tools + State, running in a loop until the goal is done 

Goal --> LLM -->tools--->web search / API / Database ---> LLM ---> result 


#Agentic AI  --> combination of multiple AI Agents 
start --> Plan Trip --> Approve(yes or no ) --> find flight --> approve (yes or no )  --> book hotel --> End 

Loops and retries   / Shared data / Long waits 

Langchain help you call a LLM 
Langgraph help you orchestrate and intelligent system 


state : THe shared backpack of data that travels through the whole flow 
Node : A worker that does excatly one job . in code just a python function 
Edge : connection between those node 
Graph : combine of state node and edge is Graph 



