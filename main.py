import time
import os

import cherrypy
import telebot
from telebot import apihelper

from source.bot import initial_bot
from source.config import *
from source.log import log

BOT = initial_bot(use_logging=True, level_name='INFO')
server_logger = log('server', 'server.log', 'INFO')


class WebHookServer(object):
    @cherrypy.expose()
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            BOT.process_new_updates([update])
            server_logger.info(f"New updates. Info: {[update]}")
            return ''
        else:
            server_logger.info(f"Server error! Error status 403")
            raise cherrypy.HTTPError(403)


def main():
    if USE_PROXY:
        apihelper.proxy = PROXY
    if USE_WEB_HOOK:
        server_logger.info("Start main function")
        BOT.remove_webhook()
        time.sleep(1)
        BOT.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
        server_logger.info("Web hook has been set success")
        access_log = cherrypy.log.access_log
        for handler in tuple(access_log.handlers):
            access_log.removeHandler(handler)
        cherrypy.config.update({
            'server.socket_host': WEBHOOK_LISTEN,
            'server.socket_port': WEBHOOK_PORT,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': WEBHOOK_SSL_CERT,
            'server.ssl_private_key': WEBHOOK_SSL_PRIV
        })
        server_logger.info("Server is started success")
        cherrypy.quickstart(WebHookServer(), WEBHOOK_URL_PATH, {'/': {}})
    else:
        BOT.polling(none_stop=True, interval=0, timeout=60)


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    main()
