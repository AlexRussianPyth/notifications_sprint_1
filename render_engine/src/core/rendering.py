import logging

from core.extraction import UserDataExtractor
from core.schemas import Notification
from core.url_shortener import Bitly
from jinja2 import BaseLoader, Environment
from jinja2.exceptions import TemplateSyntaxError
from pydantic import ValidationError

logger = logging.getLogger()


class JanjaTemplateRender():

    def template_render(self, template: str, data: dict) -> str:
        template = Environment(loader=BaseLoader).from_string(template)
        try:
            letter = template.render(**data)
        except TemplateSyntaxError:
            logger.exception('Template syntax error %s.', template)
        print(letter, type(letter))
        return letter


class MessageHandler():
    def __init__(self,
                 user_info: UserDataExtractor,
                 template_render: JanjaTemplateRender,
                 url_shortener: Bitly) -> None:
        self.user_info = user_info
        self.render = template_render
        self.url_shortener = url_shortener

    def make_letter(self, message):

        try:
            users = message.get('users')
            template = message.pop('template')
        except KeyError:
            logger.exception("Validation error: check user_id and template.")
            return None

        redirect_url = message.get('redirect_url', None)
        if redirect_url:
            message['redirect_url'] = self.url_shortener.short(redirect_url)

        for user in users:
            user_info = self.user_info.get_info(user)
            if not user_info:
                logger.error("User not found id %s", user)
                continue

            render_data = {**message, **user_info}
            print(render_data)
            letter = self.render.template_render(template, render_data)
            try:
                notification = Notification(letter=letter, **render_data)
            except ValidationError:
                logger.exception('Error to create notification')
                return
            yield notification.dict()
