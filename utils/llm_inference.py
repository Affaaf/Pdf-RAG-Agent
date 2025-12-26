
import os
from groq import Groq
from configs.constants import Const

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def llm_agent(user_query: str, extracted_chunks: list) -> str:
    """
    Sends the user query + extracted vector DB results to Groq LLM
    and returns the model's synthesized answer.
    """
    context_text = "\n\n---\n\n".join(
        f"From file: {c.file_name} (page {c.page_number})\nContent:\n{c.content}"
        for c in extracted_chunks
    )

    system_prompt = (
        "You are an analytical assistant. "
        "Use the extracted document chunks to answer the user's query. "
        "Only use information present in the extracted data. "
        "If the answer is not in the data, say that it was not found."
    )

    user_prompt = f"""
    User query:
    {user_query}

    Extracted data:
    {context_text}

    Please analyze the above and provide the best possible answer.
    """

    response = client.chat.completions.create(
        model=Const.MODEL_NAME,

        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content


def llm_response(user_query: str) -> str:
    system_prompt = (
        "You are an analytical assistant. "
        "Answer the user's question using only your own general knowledge. "
        "Do not rely on any external documents or context. "
        "If you genuinely do not know the answer, respond that you are unable to answer."
    )

    user_prompt = f"User Query:\n{user_query}\n\nProvide the best possible answer."

    response = client.chat.completions.create(
        model=Const.MODEL_NAME,

        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
