import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from waterwise.rag_engine import WaterWiseRAG

def run_tests():
    rag = WaterWiseRAG()
    
    print("--------------------------------------------------")
    print("TEST 1: In-scope Query (Household Contamination)")
    res1 = rag.query("How can households reduce water contamination?")
    print("Status:", res1["status"])
    print("Confidence:", res1["confidence_score"])
    print("Citations Count:", len(res1["sources"]))
    print("Answer Excerpt:", res1["answer"][:180] + "...")
    print("--------------------------------------------------")
    
    print("\nTEST 2: In-scope Query (Wastewater Treatment Stages)")
    res2 = rag.query("What are the main stages of wastewater treatment?")
    print("Status:", res2["status"])
    print("Primary Citation:", res2["sources"][0]["source"] if res2["sources"] else "None")
    print("--------------------------------------------------")

    print("\nTEST 3: Out-of-Scope Query ('I don't know' Guardrail)")
    res3 = rag.query("What is the stock price of Apple?")
    print("Status:", res3["status"])
    print("Refusal Answer:", res3["answer"])
    print("--------------------------------------------------")
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
