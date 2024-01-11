import random
import string

import openai
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from flask import current_app


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def call_chatgpt(content):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一位會用一句話給予鼓勵的心理諮商師"},
            {"role": "user", "content": content}
        ]
    )

    response_message = completion['choices'][0]['message']['content'].strip()

    return response_message


def azure_text_analysis(content):
    endpoint = current_app.config['AZURE_LANGUAGE_ENDPOINT']
    key = current_app.config['AZURE_LANGUAGE_KEY']

    credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    response = text_analytics_client.analyze_sentiment([content], language='zh')

    result = response[0]

    sentiment = result.sentiment
    scores = result.confidence_scores

    if sentiment == 'positive':
        flag = 1
    elif sentiment == 'neutral':
        flag = 2
    else:
        flag = 3

    return {
        'sentiment': flag,
        'positive': float(scores.positive),
        'neutral': float(scores.neutral),
        'negative': float(scores.negative)
    }

