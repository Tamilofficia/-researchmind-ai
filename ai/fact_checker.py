import google.generativeai as genai

model = genai.GenerativeModel("models/gemini-2.5-flash")

def verify_claims(claims, arxiv_context):
    """
    Use Gemini to verify claims against the context downloaded from ArXiv.
    """
    
    context_str = "\n\n".join([f"Title: {paper['title']}\nAbstract: {paper['abstract']}" for paper in arxiv_context])
    
    prompt = f"""
    You are an expert fact-checker mapping the claims of a research paper against the existing ArXiv database.
    
    Your goal is two-fold:
    1. Summarize the overall literature consensus based on the retrieved ArXiv abstracts. Do other papers generally agree or disagree with this direction?
    2. Determine if the specific extracted claims are Supported, Contradicted, or Unverified based solely on the provided ArXiv abstracts.

    ArXiv Context:
    {context_str}
    
    Extracted Claims to Verify:
    {claims}
    
    Please provide your analysis in a structured, easy to read format:
    
    ### literature Review & Scientific Consensus
    [Write a 3-4 sentence paragraph summarizing the related papers found on ArXiv and what the general consensus is regarding the topic.]
    
    ### Fact-Checking Report
    For each major claim, state:
    - Claim: [The claim text]
    - Status: [Supported / Contradicted / Unverified]
    - Justification: [Brief reason why, citing the ArXiv context if applicable]
    """

    response = model.generate_content(prompt)
    
    return response.text
