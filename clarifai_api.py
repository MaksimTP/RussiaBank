from clarifai.rag import RAG

rag_agent = RAG.setup(user_id="charlsib")
rag_agent.upload(file_path="data/Navalniy.pdf")
rag_agent.upload(file_path="data/U.pdf")

# rag_agent.chat(messages=[{"role":"human", "content": "Summarize this pdf"}])
