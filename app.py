from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv("config.env")

endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

app = Flask(__name__)

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

@app.route("/", methods=["GET", "POST"])
def feedback():
    sentiment = None
    message = ""
    color = "neutral"

    if request.method == "POST":
        user_feedback = request.form["feedback"]
        response = client.analyze_sentiment([user_feedback])[0]

        sentiment = response.sentiment
        scores = response.confidence_scores

        if sentiment == "positive":
            message = f"Thank you! We're glad you're happy. (Confidence: {scores.positive:.2f})"
            color = "positive"
        elif sentiment == "negative":
            message = f"We're sorry to hear that. We'll look into it. (Confidence: {scores.negative:.2f})"
            color = "negative"
        else:
            message = f"Thanks for your input. Let us know more. (Neutral confidence: {scores.neutral:.2f})"
            color = "neutral"

        # ✅ Place the debug prints inside the POST block
        print("User input:", user_feedback)
        print("Sentiment:", sentiment)
        print("Message:", message)

    return render_template("feedback.html", message=message, color=color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)