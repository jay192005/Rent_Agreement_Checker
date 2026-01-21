import google.generativeai as genai
import os
import json
import traceback # Import traceback for detailed error logging

# --- Part 1: Rule-Based Pre-analysis ---

DANGER_KEYWORDS = {
    # High-Risk Phrases (potentially illegal or highly unfair)
    "waive your rights": 95,
    "landlord is not responsible for any injury": 90,
    "access the property without notice": 85,
    "tenant is responsible for all repairs": 80,
    "confess judgment": 98,
    "security deposit is non-refundable": 88,

    # Medium-Risk Phrases (warrants caution and clarification)
    "automatic renewal": 70,
    "rent increases may occur": 65,
    "at the landlord's sole discretion": 60,
    "as-is condition": 55,
    "late fees of more than 5%": 68,

    # Low-Risk Phrases (common but good to be aware of)
    "no pets": 20,
    "no alterations or improvements": 25,
    "subletting requires prior consent": 15,
}

def analyze_text_with_rules(text):
    """
    Performs a simple keyword-based scan of the text.
    Returns a list of found issues and a preliminary score.
    """
    print("--- 1. EXECUTING: Rule-based analysis in ai.py ---")
    found_issues = []
    total_score = 0
    issue_count = 0
    text_lower = text.lower()

    for phrase, score in DANGER_KEYWORDS.items():
        if phrase in text_lower:
            issue_count += 1
            total_score += score
            found_issues.append({"phrase": phrase, "score": score})
    
    preliminary_score = (total_score / issue_count) if issue_count > 0 else 0
    
    return {
        "found_issues": found_issues,
        "preliminary_score": int(preliminary_score)
    }


# --- Part 2: Gemini AI Analysis (with improved error handling) ---

def analyze_with_gemini(text, preliminary_findings, state=""):
    """
    Analyzes the text using the Gemini API, providing it with context from the rule-based scan.
    """
    print("--- 2. EXECUTING: Gemini analysis in ai.py ---")
    # --- NEW: Add a guard clause to prevent empty API calls ---
    if not text or not text.strip():
        print("--- ERROR: Text for Gemini analysis is empty. Skipping API call. ---")
        # This error is more specific than the generic "Failed to get analysis"
        return {"error": "The document appears to be empty or could not be read. Please check the file and try again."}

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or len(api_key) < 30: # Basic check for a valid key format
            print("--- FATAL ERROR: Gemini API key is missing or invalid in .env file. ---")
            return {
                "error": "Server configuration error: Ensure a valid GEMINI_API_KEY is in your .env file."
            }
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Updated to use the latest 1.5 flash model

        location_context = f"The user has specified that this agreement is for {state}, India. Please consider this location in your legal analysis." if state else "The user has not specified a location. Provide a general analysis."

        system_prompt = f"""
        You are an expert AI legal assistant specializing in Indian contract law for tenant and consumer rights.
        Your task is to analyze the provided document text and identify potentially unfair, risky, or problematic clauses.
        {location_context}

        I have already performed a basic keyword scan and found these potential issues: {preliminary_findings}. Use this as a starting point, but perform your own comprehensive analysis.

        Your response MUST be a single, valid JSON object with the following structure:
        {{
            "ratingScore": <an integer from 0 (Critical) to 100 (Perfect)>,
            "ratingText": "<a string: "CRITICAL", "DANGER", "CAUTION", "SAFE", or "PERFECT">,
            "shortSummary": "<a one-sentence summary of the overall risk>",
            "aiSummary": "<a detailed paragraph summarizing the key findings>",
            "redFlags": [
                {{
                    "priority": "<'high', 'medium', or 'low'>",
                    "title": "Problematic Clause",
                    "issue": "<A direct quote or summary of the problematic clause>",
                    "recommendation": "<A suggestion on how to address this issue>"
                }}
            ],
            "fairClauses": [
                {{
                    "title": "<A summary of a fair or standard clause>",
                    "recommendation": "<A brief explanation of why this clause is fair>"
                }}
            ],
            "recommendations": [
                "<A string with an actionable next step for the user>",
                "<Another actionable next step>"
            ]
        }}

        Analyze the following document:
        """

        full_prompt = f"{system_prompt}\n\n--- DOCUMENT TEXT ---\n{text}"
        
        # --- NEW: Add generation config and safety settings ---
        # This helps prevent the API from throwing an error on safety blocks
        # and instead lets us inspect the reason.
        generation_config = {
            "response_mime_type": "application/json", # Request JSON output directly
        }

        response = model.generate_content(full_prompt, generation_config=generation_config)
        
        # --- NEW: Check for safety blocks before trying to parse ---
        if not response.parts:
            # This happens if the content is blocked by safety settings
            print("---!!! GEMINI API ERROR: Response was blocked. !!!---")
            print(f"--- Finish Reason: {response.prompt_feedback} ---")
            return {"error": "The analysis was blocked by the AI's safety filter. This can sometimes happen with legal documents. Please try again or modify the document."}

        cleaned_response_text = response.text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:]
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3]
        
        # The response might still have a 'role' or other non-JSON parts.
        # Find the first '{' and the last '}' to extract the JSON object.
        # cleaned_response_text = cleaned_response_text[cleaned_response_text.find('{'):cleaned_response_text.rfind('}')+1]

        print("--- 3. RECEIVED response from Gemini. ---")
        return json.loads(cleaned_response_text)

    except Exception as e:
        # --- IMPROVED ERROR LOGGING ---
        print("\n" + "="*50)
        print("---!!! GEMINI API ERROR !!! ---")
        print(f"--- An exception occurred: {e} ---")
        # Print the full traceback to the console for detailed debugging
        traceback.print_exc() 
        print("="*50 + "\n")
        return {
            "error": "Failed to get analysis from AI. Please try again later."
        }

import google.generativeai as genai
import os
import json
import traceback # Import traceback for detailed error logging

# --- Part 1: Rule-Based Pre-analysis ---

DANGER_KEYWORDS = {
    # High-Risk Phrases (potentially illegal or highly unfair)
    "waive your rights": 95,
    "landlord is not responsible for any injury": 90,
    "access the property without notice": 85,
    "tenant is responsible for all repairs": 80,
    "confess judgment": 98,
    "security deposit is non-refundable": 88,

    # Medium-Risk Phrases (warrants caution and clarification)
    "automatic renewal": 70,
    "rent increases may occur": 65,
    "at the landlord's sole discretion": 60,
    "as-is condition": 55,
    "late fees of more than 5%": 68,

    # Low-Risk Phrases (common but good to be aware of)
    "no pets": 20,
    "no alterations or improvements": 25,
    "subletting requires prior consent": 15,
}

def analyze_text_with_rules(text):
    """
    Performs a simple keyword-based scan of the text.
    Returns a list of found issues and a preliminary score.
    """
    print("--- 1. EXECUTING: Rule-based analysis in ai.py ---")
    found_issues = []
    total_score = 0
    issue_count = 0
    text_lower = text.lower()

    for phrase, score in DANGER_KEYWORDS.items():
        if phrase in text_lower:
            issue_count += 1
            total_score += score
            found_issues.append({"phrase": phrase, "score": score})
    
    preliminary_score = (total_score / issue_count) if issue_count > 0 else 0
    
    return {
        "found_issues": found_issues,
        "preliminary_score": int(preliminary_score)
    }


# --- Part 2: Gemini AI Analysis (with improved error handling) ---

def analyze_with_gemini(text, preliminary_findings, state=""):
    """
    Analyzes the text using the Gemini API, providing it with context from the rule-based scan.
    """
    print("--- 2. EXECUTING: Gemini analysis in ai.py ---")
    try:
        # Force reload environment variables
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        api_key = os.getenv("GEMINI_API_KEY")
        print(f"--- DEBUG: API Key loaded: {api_key[:20] if api_key else 'None'}... ---")
        
        if not api_key or len(api_key) < 30: # Basic check for a valid key format
            print("--- FATAL ERROR: Gemini API key is missing or invalid in .env file. ---")
            return {
                "error": "Server configuration error: Ensure a valid GEMINI_API_KEY is in your .env file."
            }
            
        # Remove quotes if present
        api_key = api_key.strip('"\'')
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')  # Updated to working model

        location_context = f"The user has specified that this agreement is for {state}, India. Please consider this location in your legal analysis." if state else "The user has not specified a location. Provide a general analysis."

        system_prompt = f"""
        You are an expert AI legal assistant specializing in Indian contract law for tenant and consumer rights.
        Your task is to analyze the provided document text and identify potentially unfair, risky, or problematic clauses.
        {location_context}

        I have already performed a basic keyword scan and found these potential issues: {preliminary_findings}. Use this as a starting point, but perform your own comprehensive analysis.

        Your response MUST be a single, valid JSON object with the following structure:
        {{
            "ratingScore": <an integer from 0 (Critical) to 100 (Perfect)>,
            "ratingText": "<a string: "CRITICAL", "DANGER", "CAUTION", "SAFE", or "PERFECT">,
            "shortSummary": "<a one-sentence summary of the overall risk>",
            "aiSummary": "<a detailed paragraph summarizing the key findings>",
            "redFlags": [
                {{
                    "priority": "<'high', 'medium', or 'low'>",
                    "title": "Problematic Clause",
                    "issue": "<A direct quote or summary of the problematic clause>",
                    "recommendation": "<A suggestion on how to address this issue>"
                }}
            ],
            "fairClauses": [
                {{
                    "title": "<A summary of a fair or standard clause>",
                    "recommendation": "<A brief explanation of why this clause is fair>"
                }}
            ],
            "recommendations": [
                "<A string with an actionable next step for the user>",
                "<Another actionable next step>"
            ]
        }}

        Analyze the following document:
        """

        full_prompt = f"{system_prompt}\n\n--- DOCUMENT TEXT ---\n{text}"
        
        response = model.generate_content(full_prompt)
        
        # Clean the response to ensure it's a valid JSON string
        cleaned_response_text = response.text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:]
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3]
        
        print("--- 3. RECEIVED response from Gemini. ---")
        return json.loads(cleaned_response_text)

    except Exception as e:
        # --- IMPROVED ERROR LOGGING ---
        print("\n" + "="*50)
        print("---!!! GEMINI API ERROR !!! ---")
        print(f"--- An exception occurred: {e} ---")
        
        # Check for specific error types
        error_message = str(e).lower()
        if "api key" in error_message and ("invalid" in error_message or "expired" in error_message):
            print("--- ERROR TYPE: API Key Issue ---")
            return {
                "error": "Your Gemini API key has expired or is invalid. Please get a new API key from https://aistudio.google.com/app/apikey and update your .env file."
            }
        elif "quota" in error_message or "limit" in error_message:
            print("--- ERROR TYPE: Quota/Rate Limit ---")
            return {
                "error": "API quota exceeded. Please try again later or check your Gemini API usage limits."
            }
        elif "network" in error_message or "connection" in error_message:
            print("--- ERROR TYPE: Network Issue ---")
            return {
                "error": "Network connection issue. Please check your internet connection and try again."
            }
        else:
            print("--- ERROR TYPE: Unknown ---")
        
        # Print the full traceback to the console for detailed debugging
        traceback.print_exc() 
        print("="*50 + "\n")
        return {
            "error": "Failed to get analysis from AI. Please try again later."
        }
