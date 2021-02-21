from fastapi_mail import FastMail, MessageSchema

from fastapi import Request

from core.configs import email_conf

from db.models import UserDB

async def on_after_register(user: UserDB, request: Request, ):
    html = """
    <p>Thank you for registering!</p> 
    """
    message = MessageSchema(
        subject="Terima kasih kerana mendaftar!",
        recipients=[user.email],
        body=html,
        subtype='html'
    )
    fm = FastMail(email_conf)
    await fm.send_message(message)

async def on_after_forgot_password(user: UserDB, token: str, request: Request):
    
    message = MessageSchema(
        subject="Reset password request",
        recipients=[user.email],
        body=f'Here is your reset token\n\n {token}'
    )
    fm = FastMail(email_conf)
    await fm.send_message(message)