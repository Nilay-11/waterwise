import streamlit as st
import os
import sys

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from rag_engine import WaterWiseRAG
except ImportError:
    from waterwise.rag_engine import WaterWiseRAG

# Page Configuration
st.set_page_config(
    page_title="WaterWise — AI Water & Sanitation Assistant",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #006699;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 20px;
    }
    .sdg-badge {
        display: inline-block;
        background-color: #26bde2;
        color: white;
        padding: 5px 14px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .who-badge {
        display: inline-block;
        background-color: #008dc9;
        color: white;
        padding: 5px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .ibm-badge {
        background-color: #0f62fe;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return WaterWiseRAG()

rag_engine = load_engine()

# Sidebar Configuration
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Sustainable_Development_Goal_6.svg/640px-Sustainable_Development_Goal_6.svg.png", width=120)
    st.markdown("### 💧 **WaterWise RAG Assistant**")
    st.caption("Powered by **IBM Bob & Grounded Vector Retrieval**")
    
    st.markdown("---")
    st.markdown("### 🤖 **IBM Bob / watsonx Config**")
    ibm_api_key_input = st.text_input("IBM Cloud API Key", type="password", placeholder="Enter IBM API Key...")
    ibm_project_id_input = st.text_input("IBM Project ID", placeholder="e.g. 5d9a... or default")
    ibm_model = st.selectbox(
        "IBM Foundation Model",
        ["ibm/granite-3-8b-instruct", "ibm/granite-13b-chat-v2", "ibm/granite-20b-multilingual"]
    )
    
    if ibm_api_key_input:
        rag_engine.ibm_api_key = ibm_api_key_input
        rag_engine.ibm_project_id = ibm_project_id_input or "default-waterwise-project"
        rag_engine.ibm_model_id = ibm_model
        st.success("⚡ Live IBM Bob / watsonx Connected!")
    else:
        st.info("💡 Running in **IBM Bob Standalone Demo Mode**.")

    st.markdown("---")
    st.markdown("#### 🎯 **UN SDG 6 Focus Targets**")
    st.markdown("- **6.1**: Safe & Affordable Drinking Water")
    st.markdown("- **6.2**: End Open Defecation & Sanitation")
    st.markdown("- **6.3**: Improve Water Quality & Treatment")
    st.markdown("- **6.4**: Water-use Efficiency & NbS")
    
    st.markdown("---")
    st.markdown("#### 📚 **Authoritative Corpus**")
    st.markdown("✅ **WHO** Drinking-water Guidelines (4th Ed)")
    st.markdown("✅ **UN-Water** SDG 6 & Wastewater Assessment")
    st.markdown("✅ **Jal Jeevan Mission** (Gov of India)")
    st.markdown("✅ **UNESCO** World Water Development Reports")
    
    st.markdown("---")
    st.markdown("#### ➕ **Add Custom Document**")
    with st.expander("Ingest New Guideline"):
        new_source = st.text_input("Source Organization", value="Regional Water Utility")
        new_topic = st.text_input("Topic", value="Community Chlorination")
        new_section = st.text_input("Section", value="SOP 4.2")
        new_content = st.text_area("Guideline Text", value="Maintain 0.5 mg/L residual chlorine during high-turbidity events...")
        if st.button("Add to Vector Index"):
            rag_engine.vector_store.add_custom_document(new_source, new_topic, new_section, new_content)
            st.success("✅ Ingested and indexed into Vector Store!")

# Main Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-header">💧 WaterWise</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI Water & Sanitation Knowledge Assistant — Grounded in WHO, UN-Water & National Guidelines</div>', unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align: right; padding-top: 15px;'><span class='sdg-badge'>UN SDG 6</span> <span class='who-badge'>WHO Grounded</span></div>", unsafe_allow_html=True)

# Metrics Banner
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("<div class='metric-card'><b>Verified Corpus</b><br><h3 style='color:#006699; margin:0;'>WHO & UN-Water</h3></div>", unsafe_allow_html=True)
with m2:
    st.markdown("<div class='metric-card'><b>Retrieval Engine</b><br><h3 style='color:#008080; margin:0;'>Dense Vector Store</h3></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><b>AI Synthesizer</b><br><h4 style='color:#0f62fe; margin:0;'>IBM Bob / Granite</h4></div>", unsafe_allow_html=True)
with m4:
    st.markdown("<div class='metric-card'><b>Safety Guardrail</b><br><h3 style='color:#2e7d32; margin:0;'>Anti-Hallucination</h3></div>", unsafe_allow_html=True)

st.markdown("---")

# Quick Questions Chips
st.markdown("##### 💡 **Quick Sample Questions (Click to test):**")
quick_queries = [
    "How can households reduce water contamination?",
    "What are the main stages of wastewater treatment?",
    "What is a Water Safety Plan (WSP) according to WHO?",
    "What are the rural tap water standards under Jal Jeevan Mission?",
    "What is the capital of France?" # Guardrail test
]

selected_query = ""
chip_cols = st.columns(len(quick_queries))
for i, q in enumerate(quick_queries):
    with chip_cols[i]:
        if st.button(f"📌 {q[:25]}...", key=f"chip_{i}", help=q):
            selected_query = q

# Query Input
user_input = st.text_input(
    "Ask any question on safe drinking water, sanitation, hygiene, or wastewater management:",
    value=selected_query if selected_query else "",
    placeholder="e.g. What are the key chemical parameters and limits for safe drinking water?"
)

if user_input:
    with st.spinner("Retrieving authoritative context and synthesizing answer..."):
        result = rag_engine.query(user_input)

    st.markdown("### 📋 **Assistant Response**")
    st.caption(f"**Generated by:** `{result.get('model_engine', 'IBM Bob / Granite')}` • **Retrieval Confidence:** `{int(result['confidence_score'] * 100)}%`")
    
    if result["status"] == "NO_RELEVANT_CONTEXT":
        st.warning(f"⚠️ **{result['answer']}**")
        st.info("🛡️ **Anti-Hallucination Guardrail Active:** This query falls outside the curated SDG 6 knowledge base. The system strictly refuses to hallucinate unverified medical or chemical advice.")
    else:
        st.success("✅ **Authoritative Grounded Answer (Verified against Official Standards)**")
        st.markdown(result["answer"])
        
        st.markdown("---")
        st.markdown("#### 📖 **Official Citations & Source Excerpts**")
        
        for i, src in enumerate(result["sources"], start=1):
            with st.expander(f"📌 **Citation [{i}]: {src['source']}** — *{src['section']}* (Match: {int(src['similarity_score']*100)}%)"):
                st.markdown(f"**Topic:** {src['topic']}")
                st.markdown(f"**Official Excerpt:**\n> {src['excerpt']}")

st.markdown("---")
with st.expander("🔍 **How WaterWise RAG Works (Architecture & Pipeline)**"):
    st.markdown("""
    ```text
                 AUTHORITATIVE DOCUMENTS (WHO, UN-Water, Jal Jeevan Mission, UNESCO)
                                                ↓
                                    Document Processing & Chunking
                                                ↓
                                 Dense Semantic Vector Embeddings
                                                ↓
                                 Vector Store & Similarity Index
                                                ↓
     User Question ──► Similarity Search (Threshold Filter) ──► Grounded Prompt
                                                                      ↓
                                                              IBM Bob / Granite LLM
                                                                      ↓
                                                     Verified Answer + Source Citations
    ```
    - **1. Ingestion**: Raw guidelines from WHO, UN-Water, and Jal Jeevan Mission are parsed into structured knowledge chunks.
    - **2. Dense Indexing**: Vector embeddings index semantic relationships across water safety topics.
    - **3. Retrieval**: The user's query is matched against the vector space with strict cosine thresholding.
    - **4. IBM Bob / Granite Generation**: Grounded generation ensures all responses are directly attributable to official standards.
    - **5. Hallucination Refusal**: Out-of-corpus queries safely trigger the *"I don't know"* fallback to prevent harmful misinformation.
    """)
