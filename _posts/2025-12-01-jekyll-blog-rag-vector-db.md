---
layout: post
title: "Building a RAG System for Your Jekyll Blog with AWS Bedrock Claude"
excerpt: "Building a RAG System for Your Jekyll Blog with AWS Bedrock Claude"
disqus_id: /2025/12/01/jekyll-blog-rag-vector-db/
tags:
    - Bedrock
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

Head over to the [Complete source code on GitHub](https://github.com/madhur/jekyll-blog-rag)

Ever wanted to create a smart assistant that can answer questions specifically about your blog content? In this post, I'll walk you through building a Retrieval Augmented Generation (RAG) system that indexes all your Jekyll blog posts in a vector database and uses AWS Bedrock Claude to provide intelligent answers based solely on your content.

## What We're Building

Our RAG system will:
- ✅ Automatically discover and parse Jekyll blog posts
- ✅ Create semantic embeddings of blog content
- ✅ Store embeddings in a FAISS vector database
- ✅ Use AWS Bedrock Claude to answer questions
- ✅ Ensure responses are based only on blog content
- ✅ Provide source citations for transparency

## Architecture Overview

```
Jekyll Blog Posts → Content Processing → Embeddings → Vector DB (FAISS)
                                                           ↓
User Question → Query Embeddings → Similarity Search → Context Retrieval
                                                           ↓
Context + Question → AWS Bedrock Claude → Contextualized Answer
```

## Why This Approach Works

**Traditional Search Limitations**: Standard blog search relies on keyword matching, missing semantic relationships and context.

**RAG Advantages**:
- **Semantic Understanding**: Vector embeddings capture meaning, not just keywords
- **Context-Aware Responses**: Claude understands nuanced technical concepts
- **Source Attribution**: Always cites which blog posts informed the answer
- **Content Accuracy**: Responses are grounded in your actual writing

## Prerequisites

Before we dive in, ensure you have:

- A Jekyll blog with markdown posts
- Python 3.8+ environment
- AWS account with Bedrock access
- Basic familiarity with vector databases

## Core Components Explained

### 1. Content Discovery and Parsing

The system automatically finds Jekyll posts in common locations:

```python
post_patterns = [
    self.blog_path / "_posts" / "*.md",
    self.blog_path / "_posts" / "*.markdown",
    self.blog_path / "blog" / "*.md",
    self.blog_path / "posts" / "*.md",
]
```

It then parses the frontmatter and content, extracting metadata like titles, dates, tags, and categories while cleaning the markdown for better indexing.

### 2. Content Chunking Strategy

Long blog posts are split into overlapping chunks to improve retrieval accuracy:

```python
def chunk_content(self, content: str, max_tokens: int = 500, overlap: int = 50):
    """Split content into overlapping chunks for better retrieval."""
    tokens = self.tokenizer.encode(content)
    chunks = []
    
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = self.tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        
        if end == len(tokens):
            break
        start = end - overlap
    
    return chunks
```

**Why Chunking Matters**:
- **Improved Precision**: Smaller chunks mean more precise matches
- **Context Preservation**: Overlap ensures important context isn't lost
- **Efficient Processing**: Manageable sizes for embedding models

### 3. Embedding Generation

We use Sentence Transformers for creating semantic embeddings:

```python
self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Combine title and content for richer context
text_to_embed = f"Title: {post.title}\n\nContent: {chunk}"
embeddings = self.embedding_model.encode(all_chunks)
```

The `all-MiniLM-L6-v2` model provides excellent semantic understanding while being computationally efficient.

### 4. FAISS Vector Database

FAISS (Facebook AI Similarity Search) provides lightning-fast similarity search:

```python
# Create index optimized for cosine similarity
dimension = embeddings.shape[1]
self.faiss_index = faiss.IndexFlatIP(dimension)

# Normalize for cosine similarity
faiss.normalize_L2(embeddings)
self.faiss_index.add(embeddings.astype('float32'))
```

### 5. AWS Bedrock Integration

The system uses Claude 3.5 Sonnet via Bedrock for intelligent responses:

```python
def query_bedrock_claude(self, prompt: str, context: str) -> str:
    system_prompt = f"""You are an AI assistant that answers questions based ONLY on the provided blog post content. 

Rules:
1. ONLY use information from the provided blog post excerpts
2. If the blog posts don't contain enough information, say so explicitly
3. Always cite which blog post(s) you're referencing by title
4. Do not use any external knowledge beyond what's in the blog posts
5. Be concise but thorough in your responses

Blog post content:
{context}"""

    response = self.bedrock_client.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": f"Question: {prompt}"}]
        })
    )
    
    return json.loads(response['body'].read())['content'][0]['text']
```

## Installation and Setup

### 1. Install Dependencies

```bash
pip install boto3 sentence-transformers faiss-cpu python-frontmatter tiktoken numpy
```

### 2. Configure AWS Credentials

Choose your preferred method:

```bash
# Option A: AWS CLI
aws configure

# Option B: Environment Variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# Option C: Use IAM roles (if running on EC2)
```

### 3. Enable Bedrock Model Access

1. Navigate to AWS Bedrock console in your region (ap-south-1)
2. Go to "Model access" in the left sidebar
3. Request access to Claude models if not already enabled
4. Wait for approval (usually instant for Claude models)

### 4. Update Configuration

Modify the blog path in the script to match your Jekyll site:

```python
rag = JekyllBlogRAG(
    blog_path="/your/jekyll/blog/path",
    aws_region="ap-south-1"
)
```

## Usage Examples

Once set up, you can ask sophisticated questions:

**Technical Implementation Questions**:
```
Q: "How do I implement authentication in React applications?"
A: Based on your blog post "React Authentication Best Practices", you can implement authentication using JWT tokens with...
```

**Architecture and Design**:
```
Q: "What are the pros and cons of microservices architecture?"
A: In your post "Microservices vs Monoliths: A Practical Guide", you outlined several key advantages of microservices...
```

**Performance Optimization**:
```
Q: "How can I optimize database queries for better performance?"
A: Your blog post "Database Optimization Techniques" covers several strategies including indexing, query optimization...
```

## Performance Considerations

### Indexing Performance
- **Initial Setup**: ~2-5 minutes for 100 blog posts
- **Query Time**: ~100-200ms per question
- **Memory Usage**: ~50MB for 1000 post chunks

### Optimization Tips

1. **Chunk Size Tuning**: Experiment with chunk sizes (300-800 tokens)
2. **Embedding Model Selection**: Balance accuracy vs speed
3. **Index Persistence**: Save/load indices to avoid re-indexing
4. **Batch Processing**: Process multiple queries together

## Advanced Features You Can Add

### 1. Incremental Updates
Track file modification times to only re-index changed posts:

```python
def needs_reindexing(self, file_path: Path) -> bool:
    """Check if file needs re-indexing based on modification time."""
    last_indexed = self.get_last_indexed_time(file_path)
    file_mtime = file_path.stat().st_mtime
    return file_mtime > last_indexed
```

### 2. Semantic Filtering
Add filters for categories, tags, or date ranges:

```python
def search_with_filters(self, query: str, categories: List[str] = None, 
                       date_range: tuple = None) -> List[Dict]:
    """Search with additional filtering criteria."""
    results = self.search_similar_chunks(query, top_k=20)
    
    if categories:
        results = [r for r in results if any(cat in r['categories'] for cat in categories)]
    
    if date_range:
        results = [r for r in results if date_range[0] <= r['date'] <= date_range[1]]
    
    return results[:5]  # Return top 5 after filtering
```

### 3. Multi-Modal Support
Extend to handle images and code snippets:

```python
def extract_code_blocks(self, content: str) -> List[Dict]:
    """Extract and index code blocks separately."""
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(code_pattern, content, re.DOTALL)
    
    return [{'language': lang, 'code': code} for lang, code in matches]
```

## Troubleshooting Common Issues

### 1. No Blog Posts Found
```python
# Debug post discovery
post_files = self.find_posts()
print(f"Checking paths: {[str(p) for p in post_patterns]}")
print(f"Found files: {[str(f) for f in post_files]}")
```

### 2. AWS Bedrock Access Errors
- Verify region configuration matches your model access
- Check IAM permissions for Bedrock actions
- Confirm model access is granted in Bedrock console

### 3. Memory Issues with Large Blogs
- Reduce chunk size or increase overlap
- Process posts in batches
- Use FAISS indices with compression

## Security Considerations

### 1. Content Filtering
Ensure sensitive information isn't indexed:

```python
def should_index_post(self, post: BlogPost) -> bool:
    """Check if post should be indexed (skip drafts, private posts)."""
    if 'draft' in post.categories or 'private' in post.tags:
        return False
    return True
```

### 2. Query Sanitization
Validate and sanitize user inputs:

```python
def sanitize_query(self, query: str) -> str:
    """Sanitize user query to prevent injection attacks."""
    # Remove potentially harmful characters
    return re.sub(r'[<>\"\'%;()&+]', '', query).strip()
```

### 3. Rate Limiting
Implement rate limiting for production use:

```python
from time import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    def allow_request(self, client_id: str) -> bool:
        now = time()
        client_requests = self.requests[client_id]
        
        # Remove old requests
        client_requests[:] = [req_time for req_time in client_requests 
                             if now - req_time < self.time_window]
        
        if len(client_requests) < self.max_requests:
            client_requests.append(now)
            return True
        
        return False
```

## Cost Optimization

### AWS Bedrock Costs
- **Claude 3.5 Sonnet**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **Typical Query**: ~$0.01-0.05 per question
- **Monthly Budget**: ~$10-50 for moderate usage

### Cost Reduction Strategies
1. **Caching**: Store responses for common queries
2. **Batch Processing**: Group similar questions
3. **Model Selection**: Use smaller models for simpler queries
4. **Context Optimization**: Send only relevant chunks

## Future Enhancements

### 1. Web Interface
Build a React/Vue frontend:

```javascript
// Example API integration
const askQuestion = async (question) => {
  const response = await fetch('/api/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question})
  });
  return response.json();
};
```

### 2. Analytics Dashboard
Track popular queries and content performance:

```python
def log_query_analytics(self, query: str, results: List[Dict], 
                       response_time: float):
    """Log query analytics for insights."""
    analytics_data = {
        'timestamp': datetime.now(),
        'query': query,
        'num_results': len(results),
        'response_time': response_time,
        'top_posts': [r['title'] for r in results[:3]]
    }
    
    # Store in database or analytics service
    self.store_analytics(analytics_data)
```

### 3. Multi-Language Support
Extend to support multiple languages:

```python
def detect_language(self, content: str) -> str:
    """Detect content language for appropriate processing."""
    from langdetect import detect
    return detect(content)

def get_embedding_model(self, language: str) -> SentenceTransformer:
    """Select appropriate embedding model for language."""
    models = {
        'en': 'all-MiniLM-L6-v2',
        'hi': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        # Add more language models as needed
    }
    return SentenceTransformer(models.get(language, models['en']))
```

## Conclusion

Building a RAG system for your Jekyll blog creates a powerful way to make your content more accessible and useful. The combination of semantic search with Claude's reasoning capabilities provides responses that are both accurate and contextually rich.

The system we've built offers:
- **Intelligent Search**: Goes beyond keyword matching
- **Authoritative Responses**: Always grounded in your actual content
- **Scalable Architecture**: Handles growing blog content efficiently
- **Cost-Effective Operation**: Reasonable costs for individual blogs

Whether you're building this for personal use or considering it for a larger content site, the principles and code provided give you a solid foundation to build upon.

## Resources and Next Steps

- [Complete source code on GitHub](https://github.com/madhur/jekyll-blog-rag)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers Guide](https://www.sbert.net/)


