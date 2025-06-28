# from flask import Flask, render_template, request
# from openai import OpenAI
# import os
#
# app = Flask(__name__)
#
# # --- AI Configuration (keep your API key secure!) ---
# # It's highly recommended to load your API key from an environment variable.
# # Example for setting it (in your terminal before running Flask app):
# # export GOOGLE_AI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
# # For Windows (Command Prompt): set GOOGLE_AI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
# # For Windows (PowerShell): $env:GOOGLE_AI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
#
# # client = OpenAI(
# #     api_key=os.environ.get("GOOGLE_AI_API_KEY"),
# #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # )
#
# # --- For demonstration, if you absolutely must hardcode (NOT recommended for production) ---
# client = OpenAI(
#     api_key="AIzaSyC0p5gSNh4y2iJ_pHgh8gFOoH_HpINkyMk", # REPLACE THIS WITH YOUR REAL KEY
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )
# # --- End AI Configuration ---
#
#
# @app.route('/')
# def index():
#     """Renders the main form page."""
#     return render_template('calculator.html')
#
# @app.route('/ask_ai', methods=['POST'])
# def ask_ai():
#     """Handles the form submission and gets AI response."""
#     user_input = request.form.get('user_question') # Changed from 'username' for clarity
#
#     if not user_input:
#         return render_template('response.html', ai_response="Please enter a question.")
#
#     java_variable = "Java" # Or whatever context you need
#
#     try:
#         response = client.chat.completions.create(
#             model="gemini-2.5-flash",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant. Explain concepts clearly."},
#                 {
#                     "role": "user",
#                     "content": f"Explain How to learn {java_variable}. User question: {user_input}"
#                     # Combine your fixed context with user input
#                 }
#             ]
#         )
#
#         ai_response_content = "Sorry, I couldn't get a response."
#         if response.choices and response.choices[0].message and response.choices[0].message.content:
#             ai_response_content = response.choices[0].message.content
#         else:
#             print("API did not return expected content in response.choices[0].message.content")
#
#
#         # Render a new template, passing the AI's response
#         return render_template('response.html', ai_response=ai_response_content)
#
#     except Exception as e:
#         # Handle API errors gracefully
#         print(f"Error calling OpenAI API: {e}")
#         return render_template('response.html', ai_response=f"An error occurred: {e}")
#
# if __name__ == '__main__':
#     app.run(debug=True) # debug=True is good for local development, turn off for production



import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# --- AI Configuration ---
# IMPORTANT: For server-side applications (like this Flask app),
# you should use a Google Cloud API Key with the Generative Language API enabled,
# NOT a Google AI Studio (browser/Android) API Key.
# Ensure this key is loaded securely from an environment variable.

# How to set environment variable:
# Linux/macOS:
#   export GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_CLOUD_API_KEY"
# Windows Command Prompt:
#   set GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_CLOUD_API_KEY"
# Windows PowerShell:
#   $env:GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_CLOUD_API_KEY"
# Replace "YOUR_ACTUAL_GOOGLE_CLOUD_API_KEY" with your real key.

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    # This is a fallback for testing, but NOT recommended for production.
    # In production, ensure GOOGLE_API_KEY is ALWAYS set as an environment variable.
    logger.warning("GOOGLE_API_KEY environment variable not set. Using a placeholder/hardcoded key.")
    logger.warning("This is INSECURE for production. Please set the environment variable.")
    # REPLACE THIS WITH YOUR ACTUAL GOOGLE CLOUD API KEY FOR TESTING,
    # BUT REMOVE THIS LINE ENTIRELY FOR PRODUCTION DEPLOYMENTS.
api_key = "AIzaSyA4V2UauwqK1qiN9LfuP5PARGiLSvwM5pA" # <--- REPLACE THIS LINE WITH YOUR REAL KEY OR RELY ON ENV VAR

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    # Handle this more gracefully in a real app, perhaps by not starting the Flask app.
# --- End AI Configuration ---





@app.route('/')
def interface():
    """Renders the main calculator page."""
    return render_template('firstView.html')


@app.route('/calculator')
def calculator():
    """Renders the main calculator page."""
    return render_template('calculator.html')



@app.route('/OFDM')
def OFDM():
    """Renders the main calculator page."""
    return render_template('OFDM.html')



@app.route('/link budget')
def link():
    """Renders the main calculator page."""
    return render_template('link budget.html')



@app.route('/Cellular System Design')
def cellular():
    """Renders the main calculator page."""
    return render_template('Cellular System Design.html')




@app.route('/get_ai_insights', methods=['POST'])
def get_ai_insights():
    """Handles the AJAX request for AI insights."""
    try:
        data = request.get_json()
        user_ai_question = data.get('user_ai_question', '').strip()
        input_data = data.get('input_data', {})
        calculated_results = data.get('calculated_results', {})

        if not user_ai_question:
            logger.warning("Received AI insights request with no user question.")
            return jsonify({"error": "Please ask a question for AI insights."}), 400

        # Construct the detailed prompt for the AI
        prompt_parts = [
            "You are an expert in wireless communication systems. A user has provided parameters for a bit rate calculator and their calculated outputs. They want your insights.",
            "\n\n--- Input Parameters ---"
        ]

        for key, value in input_data.items():
            prompt_parts.append(f"- {key}: { {value} }") # Added brackets for clarity in prompt

        prompt_parts.append("\n\n--- Calculated Results ---")
        for key, value in calculated_results.items():
            prompt_parts.append(f"- {key}: { {value} }") # Added brackets for clarity in prompt

        prompt_parts.append(f"\n\n--- User's Question ---")
        prompt_parts.append(user_ai_question)
        prompt_parts.append("\n\nPlease provide a detailed, clear, and human-readable explanation based on these values and the user's question.")

        full_prompt = "\n".join(prompt_parts)
        logger.info(f"Generated prompt for AI: \n{full_prompt}")

        # Call the Gemini API
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a helpful and knowledgeable AI assistant specializing in wireless communication systems. Provide clear, structured, and easy-to-understand explanations using the provided data."},
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.7, # Adjust for creativity vs. directness
            max_tokens=4000 # Increased to 4000 to allow for more detailed responses
        )

        ai_response_content = "Sorry, I couldn't get a clear response from the AI."
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            ai_response_content = response.choices[0].message.content
            logger.info("AI response received successfully.")
        else:
            logger.warning("AI API did not return expected content in response.choices[0].message.content.")
            if response.choices:
                logger.warning(f"Full choices received: {response.choices[0]}")
            ai_response_content = "The AI did not provide a clear text response. Please try again."

        # Return the AI response as JSON
        return jsonify({"ai_response": ai_response_content})

    except Exception as e:
        logger.error(f"An error occurred in /get_ai_insights: {e}", exc_info=True)
        # Ensure we always return JSON, even for unexpected errors
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # For local development, set debug=True. Turn off for production.
    # When debug=True, Flask provides more detailed error pages (often HTML).
    # In production, debug=False ensures it doesn't leak sensitive info.
    app.run(debug=True)
