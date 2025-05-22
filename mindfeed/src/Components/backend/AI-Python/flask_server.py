from flask import Flask, request, jsonify
import subprocess
import os
import sys
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Set the maximum number of requests to be processed concurrently
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    print("Request received at /text-to-speech")
    data = request.get_json()
    print("Request data:", data)
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Get the absolute path of the text_to_speech_gui.py script
        script_path = os.path.join(os.path.dirname(__file__), "text_to_speech_gui.py")
        print("Script path:", script_path)
        print("Current working directory:", os.getcwd())

        # Pass the text to the Python GUI application
        # Launch the Python GUI application in the background
        process = subprocess.Popen(
            [sys.executable, script_path, text],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Wait for the process to complete
        stdout, stderr = process.communicate()

        # Get the output and error messages
        output, error = process.communicate()
        print("Output:", output)
        print("Error:", error)

        # Check if the process completed successfully
        if process.returncode == 0:
            print("Python application executed successfully.")
            print("Captured stdout:", stdout)

            # Extract the "Translated text:" information from stdout
            translated_text = None
            for line in stdout.splitlines():
                if line.startswith("Translated text:"):
                    translated_text = line.replace("Translated text:", "").strip()
                    break

            return jsonify({
                "status": "completed",
                "message": "Text sent to Python program successfully.",
                "translated_text": translated_text,
                "stdout": stdout
                }), 200
        else:
            error_message = process.stderr.read()
            print("Error(Could not 'jsonify' translated text):", error_message)
            return jsonify({
                "status": "error",
                "message": "Python application failed.",
                "stderr": stderr
            }), 500
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "Flask server is running!"}), 200

if __name__ == "__main__":
    app.run(port=5000)