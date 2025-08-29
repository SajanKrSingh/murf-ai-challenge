import google.generativeai as genai
from serpapi import GoogleSearch
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

system_instructions = """You are Zarex... (your full prompt here)"""

def get_llm_response(user_query: str, history: List[Dict[str, Any]], gemini_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instructions)
        chat = model.start_chat(history=history)
        response = chat.send_message(user_query)
        return response.text, chat.history
    except Exception as e:
        logger.error(f"Error getting LLM response: {e}")
        return "I'm sorry, I encountered an error with the language model.", history

def get_web_response(user_query: str, history: List[Dict[str, Any]], gemini_api_key: str, serpapi_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    try:
        params = {"q": user_query, "api_key": serpapi_api_key, "engine": "google"}
        search = GoogleSearch(params)
        results = search.get_dict()
        if "organic_results" in results:
            search_context = "\n".join([result.get("snippet", "") for result in results["organic_results"][:5]])
            prompt_with_context = f"Based on these search results: '{search_context}', answer the user's query: '{user_query}'"
            return get_llm_response(prompt_with_context, history, gemini_api_key)
        else:
            return "I couldn't find any relevant information on the web.", history
    except Exception as e:
        logger.error(f"Error getting web response: {e}")
        return "I'm sorry, I failed to search the web.", history