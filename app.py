import streamlit as st
import requests
import os

from dotenv import load_dotenv

load_dotenv()

API_SEARCH_URL = os.getenv("API_SEARCH_URL", "http://localhost:8000/search")
API_UPLOAD_URL = os.getenv("API_UPLOAD_URL", "http://localhost:8000/upload-pdf")

st.set_page_config(page_title="PDF Knowledge Assistant", layout="centered")

st.title("📄 PDF Knowledge Assistant")
st.write("Upload PDFs and ask questions from them.")

st.subheader("📤 Upload a PDF")

uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

if uploaded_file:
    st.info(f"Selected file: **{uploaded_file.name}**")

    if st.button("Upload PDF"):
        with st.spinner("Uploading and processing PDF..."):
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(API_UPLOAD_URL, files=files, timeout=300)

                if response.status_code == 200:
                    resp = response.json()
                    st.success(f"PDF uploaded & processed! Saved at: {resp['saved_path']}")
                else:
                    st.error(f"Upload failed: {response.text}")

            except Exception as e:
                st.error(f"Upload error: {e}")


st.markdown("---")


st.subheader("🔍 Ask something from your documents")

query = st.text_area("Enter your query:", height=150)

response_type = st.selectbox(
    "Select response type:",
    ["agent_response", "llm_response"],
    index=0
)

mapped_type = "agent" if response_type == "agent_response" else "llm_response"

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "query": query,
                    "response_type": response_type.replace("_response", "")
                }

                response = requests.post(API_SEARCH_URL, json=payload, timeout=120)

                if response.status_code != 200:
                    st.error(f"Server error: {response.text}")
                else:
                    st.subheader(" Response")
                    # Handle both JSON and text responses
                    try:
                        result = response.json()
                        st.write(result)
                    except:
                        st.write(response.text)

            except Exception as e:
                st.error(f"Failed to get response: {e}")

