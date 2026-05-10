from openai import OpenAI
import math

"""
Semantic Search Engine for Resumes

WHY: Understand resumes by meaning, not keywords
HOW: Use embeddings to compare semantic similarity
RESULT: Find relevant resumes even with different wording
"""

# Step 1: Define our resume database
RESUMES = [
    {
        "id": "1",
        "candidate": "Alice Johnson",
        "content": "Senior developer with 5 years experience in Python, JavaScript, and web development. "
                   "Built REST APIs using FastAPI. Experienced with AWS, Docker, and Kubernetes. "
                   "Led team of developers. Good with databases like PostgreSQL and MongoDB."
    },
    {
        "id": "2",
        "candidate": "Bob Smith",
        "content": "Junior developer with 1 year bootcamp training. "
                   "Skills in React, Node.js, and basic JavaScript. "
                   "Familiar with HTML, CSS. Worked on 3 small projects. "
                   "Learning web development."
    },
    {
        "id": "3",
        "candidate": "Charlie Brown",
        "content": "Machine learning engineer with 3 years experience. "
                   "Expert in Python, TensorFlow, PyTorch. "
                   "Built deep learning models for computer vision. "
                   "Experience with data preprocessing and model training. "
                   "Familiar with cloud platforms like AWS."
    },
    {
        "id": "4",
        "candidate": "Diana Prince",
        "content": "DevOps engineer with 4 years experience. "
                   "Expert in cloud infrastructure, AWS, Azure, GCP. "
                   "Experienced with Docker, Kubernetes, CI/CD pipelines. "
                   "Linux, networking, and infrastructure as code. "
                   "Worked at scale with thousands of servers."
    },
    {
        "id": "5",
        "candidate": "Eve Wilson",
        "content": "Data scientist with 2 years experience. "
                   "Strong in Python, SQL, and data analysis. "
                   "Used pandas, numpy, scikit-learn. "
                   "Created data visualizations with matplotlib and seaborn. "
                   "Statistical analysis and machine learning basics."
    }
]

print("✓ Loaded 5 resumes")

class SemanticSearchEngine:
    """
    Search engine that understands meaning of resumes.
    WHY: Match job requirements with relevant resumes
    HOW: Compare embeddings using semantic similarity
    """

    def __init__(self):
        self.client = openAI()
        self.model = "text-embedding-3-small"
        self.resumes = RESUMES
        self.embeddings = {}

    def embed_resumes(self):
        """
            WHY: Create vector representations of all resumes
            HOW: Send to OpenAI, store embeddings
            RESULT: Can compare semantically
        """  

        print("Embedding all Resumes !!")

        for resume in self.resumes:
            response = self.client.embeddings.create(
                input=resume["content"],
                model = self.model
            )

            self.embeddings[resume["id"]] = response.data[0].embedding
            print(f"  ✓ Embedded: {resume['candidate']}")
        
        print(f"✓ Embedded {len(self.resumes)} resumes\n")
    
    def cosine_similarity(self, vec1, vec2):
        """
        WHY: Compare two resume embeddings
        HOW: Calculate angle between vectors
        RESULT: Score from 0-1 (higher = more similar)
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
        magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def search(self,query,top_k=3):
        """
        WHY: Find resumes matching a job requirement
        HOW: Embed query, compare with all resumes
        RESULT: Top matching resumes ranked by similarity
        """

        # embed the query
        response = self.client.embeddings.create(
            input=query,
            model=self.model
        )
        query_embedding = response.data[0].embedding

        # calculate the similarity with all resumes
        results = []
        for resume in self.resumes:
            resume_embedding = self.embeddings[resume["id"]]
            similarity = self.cosine_similarity(
                query_embedding,
                resume_embedding
            )
            results.append({
                "candidate": resume["candidate"],
                "similarity": similarity,
                "content": resume["content"][:100] + "..."
            })

            results.sort(key=lambda x: x["similarity"],reverse=True)
            
            return results[:top_k]

    def search_by_keywords(self,keywords,top_k=3):
        """
            WHY: Search using keywords instead of full query
            HOW: Join keywords into query, embed, search
            RESULT: Find matching resumes
        """  
        query = f"Experince with {','.join(keywords)}" 
        return self.search(query,top_k) 
    
    def search_by_role(self,role,top_k=3):
        """
        WHY: Find candidates for a specific role
        HOW: Create role-specific query, search
        RESULT: Best candidates for that role
        """
        query = f"Candidate suitable for {role} position"
        return self.search(query, top_k)
    
    def compare_resume_to_job(self,candidate_id,job_description):
        """
            WHY: How well does candidate match job?
            HOW: Calculate similarity between resume and job
            RESULT: Match percentage
        """
        response = self.client.embeddings.create(
            input = job_description,
            model=self.model
        )

        job_emedding = response.data[0].embedding

        # find candidate
        candidate = next((r for r in self.resume if r["id"] == candidate_id),None)
        if not candidate:
            return None
        
        # calculate match
        candidate_embedding = self.embeddings[candidate_id]
        match_score = self.cosine_similarity(
            job_emedding,
            candidate_embedding
        )
        return {
            "candidate": candidate["candidate"],
            "match_score": match_score,
            "match_percentage": f"{match_score * 100:.1f}%"
        }
    
if __name__ == "__main__":
    engine = SemanticSearchEngine()
    engine.embed_resumes()

    # Try a search
    query = "Looking for Python developer with cloud experience"
    results = engine.search(query, top_k=2)

    print("\nTop matches:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['candidate']}")
        print(f"   Match score: {result['similarity']:.1%}")
        print(f"   Summary: {result['content']}")