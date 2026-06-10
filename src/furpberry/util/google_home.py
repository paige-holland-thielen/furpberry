import pychromecast
from pychromecast.controllers import BaseController
from furpberry.util.logger import get_logger

logger = get_logger(__name__)


class YouTubeMusicController(BaseController):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.player_state = "UNKNOWN"

    def receive_message(self, message, data):
        # Callback method that pychromecast invokes when messages arrive on the namespace
        # Since youtube music doesn't follow the standard chromecast protocol (because why would it?),
        # these messages help interpret the special states the namespace uses to communicate status
        if isinstance(data, dict):
            if data.get('type') == 'MEDIA_STATUS' and 'status' in data:
                if len(data['status']) > 0 and 'playerState' in data['status'][0]:
                    self.player_state = data['status'][0]['playerState']
        return True


class GoogleHome:
    def __init__(self, name: str = "furby"):
        self.chromecasts, self.browser = pychromecast.get_listed_chromecasts(friendly_names=[name])
        self.cast = self.chromecasts[0]
        self.mc = self.cast.media_controller
        self.cast.wait()
        self.yt_music_controller = None
        for ns in self.cast.status.namespaces:
            controller = YouTubeMusicController(ns)
            self.cast.register_handler(controller)
            # Save one to check later (or save all)
            if self.yt_music_controller is None:
                self.yt_music_controller = controller

    def read_status(self):
        self.mc.update_status()
        # standard chromecast protocol app status (this will work for spotify)
        if self.mc.status and self.mc.status.player_state == "PLAYING":
            logger.debug("Chromecast: PLAYING (standard protocol)")
            return True
        # special hacked youtube music app status
        if self.yt_music_controller and self.yt_music_controller.player_state == "PLAYING":
            logger.debug("Chromecast: PLAYING (YouTube Music)")
            return True
        logger.debug("Chromecast: not playing")
        return False

    def stop(self):
        pychromecast.discovery.stop_discovery(self.browser)
