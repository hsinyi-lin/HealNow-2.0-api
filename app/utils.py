import random
import string

import openai
from flask import current_app
from flask_mail import Message

from app.models import Verification, db


def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def send_verification_code(email, code):
    mail = current_app.extensions['mail']

    msg = Message('Verification Code', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your verification code is: {code}'

    mail.send(msg)

    verification = Verification(email=email, code=code)

    db.session.add(verification)
    db.session.commit()


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
