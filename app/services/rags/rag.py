# from app.core.config import settings
# from app.db.chroma.client import chroma_client

# from openai import OpenAI

# class RAG():
#     def __init__(self, rag_id: str, llm_model: str):
#         self.rag_id = rag_id
#         self.llm_model = llm_model
#         self.openai_client = OpenAI(api_key=settings.openai_api_key)
    
#     def generate_response(self, messages) -> str:
#         """
#         messages를 받아서 chormaDB에서 유사한 문서를 검색하고, LLM을 통해 응답을 생성합니다.
#         """

#         query = messages[-1]['content']
#         query_embedding = chroma_client._get_embedding(query)

#         # ChromaDB에서 유사한 문서 검색
#         collection_name = chroma_client.get_chroma_collection_name(self.rag_id)
#         results = chroma_client.search_documents(
#             collection_name=collection_name,
#             query=query_embedding,
#             n_results=5,  # 상위 5개 문서 검색
#             include=['documents', 'metadatas']
#         )

#         print(f"Search results: {results}")
        
#         # 검색된 문서들을 컨텍스트로 구성
#         context_docs = []
#         if results['documents'] and results['documents'][0]:
#             for doc in results['documents'][0]:
#                 context_docs.append(doc)
        
#         context = "\n\n".join(context_docs)
        
#         # LLM에게 전달할 시스템 메시지 구성
#         system_message = f"""당신은 주어진 문서들을 바탕으로 질문에 답하는 AI 어시스턴트입니다.
# 다음 문서들을 참고하여 답변해주세요:

# {context}

# 문서에 없는 내용에 대해서는 "제공된 문서에서 해당 정보를 찾을 수 없습니다"라고 답변해주세요."""

#         # OpenAI API 호출
#         response = self.openai_client.chat.completions.create(
#             model=self.llm_model,
#             messages=[
#                 {"role": "system", "content": system_message},
#                 *messages
#             ],

#         )
        
#         return response.choices[0].message.content