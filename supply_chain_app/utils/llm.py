import google.generativeai as genai

def supply_chain_insight(df, query, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    summary = df.describe(include="all").to_string()

    prompt = f"""
    You are a top-tier supply chain analyst.
    You must answer the user query ONLY based on the dataset below.

    DATA SUMMARY:
    {summary}

    USER QUESTION:
    {query}
    """

    return model.generate_content(prompt).text
