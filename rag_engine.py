import os
import json
import requests
try:
    from embeddings import KnowledgeVectorStore
except ImportError:
    from waterwise.embeddings import KnowledgeVectorStore

SYSTEM_PROMPT = """You are the official WHO Water & Sanitation AI Assistant, specialized in UN Sustainable Development Goal 6 (Clean Water and Sanitation).
Your purpose is to deliver accurate, authoritative, and actionable guidance regarding drinking-water safety, sanitation, hygiene, wastewater treatment, and water management.

CRITICAL INSTRUCTIONS:
1. Base your answer SOLELY on the provided Context excerpts from authoritative sources (WHO Guidelines for Drinking-water Quality, UN-Water, Jal Jeevan Mission, UNESCO).
2. For every key fact, cite the specific Source and Section in brackets, e.g. [WHO Guidelines for Drinking-water Quality, Ch. 7].
3. If the provided context DOES NOT contain sufficient information to answer the user's question, you MUST reply with:
   "I couldn't find sufficient information in the available authoritative WHO, UN-Water, and sanitation sources to answer this question."
4. Do NOT hallucinate, guess, or incorporate external unsubstantiated claims.
5. Format your response clearly with a direct answer summary, key points, and actionable guidance.
"""

class WaterWiseRAG:
    def __init__(self, data_path: Optional[str] = None):
        self.vector_store = KnowledgeVectorStore(data_path=data_path)
        self.ibm_api_key = os.getenv("IBM_API_KEY") or os.getenv("WATSONX_API_KEY") or os.getenv("IBM_BOB_KEY")
        self.ibm_project_id = os.getenv("IBM_PROJECT_ID", "default-who-water-project")
        self.ibm_url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        self.ibm_model_id = os.getenv("IBM_MODEL_ID", "ibm/granite-3-8b-instruct")

    def query(self, question: str, top_k: int = 3, threshold: float = 0.05) -> Dict[str, Any]:
        """
        Executes the full RAG pipeline:
        1. Semantic Retrieval from WHO & Partner Knowledge Base
        2. Relevance Evaluation & Fallback Check
        3. Grounded Generation with IBM Bob / Granite LLM
        4. Citation Mapping
        """
        retrieved_docs = self.vector_store.retrieve(question, top_k=top_k, min_similarity=threshold)

        if not retrieved_docs:
            return {
                "question": question,
                "answer": "I couldn't find sufficient information in the available authoritative WHO and sanitation sources to answer this question.",
                "sources": [],
                "confidence_score": 0.0,
                "status": "NO_RELEVANT_CONTEXT",
                "retrieved_count": 0,
                "model_engine": "IBM Bob / Granite (WHO Safety Guardrail)"
            }

        # Build Context String
        context_blocks = []
        sources = []
        max_score = 0.0

        for doc, score in retrieved_docs:
            max_score = max(max_score, score)
            context_blocks.append(
                f"Source: {doc.get('source')}\n"
                f"Topic: {doc.get('topic')}\n"
                f"Section: {doc.get('section')}\n"
                f"Content: {doc.get('content')}\n"
            )
            sources.append({
                "source": doc.get("source"),
                "topic": doc.get("topic"),
                "section": doc.get("section"),
                "excerpt": doc.get("content"),
                "similarity_score": round(score, 3)
            })

        combined_context = "\n---\n".join(context_blocks)
        
        # Generate Answer via IBM Bob / WatsonX / Fallback
        answer, engine_used = self._generate_answer(question, combined_context, sources)

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "confidence_score": round(min(max_score * 3.5, 0.98), 2),
            "status": "SUCCESS",
            "retrieved_count": len(retrieved_docs),
            "model_engine": engine_used
        }

    def _generate_answer(self, question: str, context: str, sources: List[Dict[str, Any]]) -> tuple:
        """Calls IBM Bob / WatsonX API if API key exists, otherwise uses Grounded Synthesizer."""
        # 1. Direct IBM Bob / WatsonX (Granite LLM) API call
        if self.ibm_api_key:
            try:
                token_resp = requests.post(
                    "https://iam.cloud.ibm.com/identity/token",
                    data={
                        "apikey": self.ibm_api_key,
                        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=5
                )
                if token_resp.status_code == 200:
                    access_token = token_resp.json().get("access_token")
                    
                    gen_url = f"{self.ibm_url}/ml/v1/text/generation?version=2023-05-29"
                    payload = {
                        "input": f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:",
                        "parameters": {
                            "decoding_method": "greedy",
                            "max_new_tokens": 512,
                            "min_new_tokens": 10,
                            "temperature": 0.2
                        },
                        "model_id": self.ibm_model_id,
                        "project_id": self.ibm_project_id
                    }
                    gen_resp = requests.post(
                        gen_url,
                        json=payload,
                        headers={
                            "Authorization": f"Bearer {access_token}",
                            "Content-Type": "application/json"
                        },
                        timeout=10
                    )
                    if gen_resp.status_code == 200:
                        results = gen_resp.json().get("results", [])
                        if results and "generated_text" in results[0]:
                            return results[0]["generated_text"].strip(), f"IBM Bob / watsonx.ai ({self.ibm_model_id})"
            except Exception:
                pass

        # 2. Try Google Gemini if configured
        if os.getenv("GOOGLE_API_KEY"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nUser Question: {question}\n\nAnswer:"
                resp = model.generate_content(prompt)
                if resp and resp.text:
                    return resp.text.strip(), "Google Gemini Grounded LLM"
            except Exception:
                pass

        # 3. High-Fidelity Grounded Synthesizer (IBM Bob Simulation / Zero-Latency Mode)
        return self._synthesize_grounded_response(question, sources), "IBM Bob RAG Synthesizer (Local Mode)"

    def _synthesize_grounded_response(self, question: str, sources: List[Dict[str, Any]]) -> str:
        """Synthesizes structured, source-cited grounded answers from retrieved chunks."""
        primary = sources[0]
        
        formatted_answer = f"**WHO-Grounded Guidance & Standards:**\n\n"
        
        for s in sources:
            source_label = f"**[{s['source']} — {s['section']}]**"
            content = s['excerpt']
            formatted_answer += f"• **{s['topic']}**: {content}\n  {source_label}\n\n"
            
        formatted_answer += "🎯 **SDG 6 Compliance & Public Health Impact:**\n"
        formatted_answer += f"Adhering to these documented protocols from *{primary['source']}* directly mitigates microbiological and chemical risks, ensuring full alignment with WHO Drinking-water Quality Standards and UN SDG Targets 6.1 & 6.3."
        
        return formatted_answer
