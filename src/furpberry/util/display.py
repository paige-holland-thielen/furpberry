from furpberry.util.pins import Pin
from furpberry.util.logger import get_logger
import ST7789 as st7789
from PIL import Image

logger = get_logger(__name__)


class Display:
    # Pin mapping for eyes.
    # The st7789 python drivers use BCM numbers and everything else in my repo uses board numbering
    # Because BCM numbering is bonkers and board numbering actually makes sense
    def __init__(
        self,
        spi_id: int,
        x_offset: int = 0,
        y_offset: int = 0,
        height: int = 240,
        width: int = 240,
        rotation: int = 0,
        invert: bool = False,
    ) -> None:
        self.spi_id = spi_id
        self.eye_name = "LEFT" if spi_id == 1 else "RIGHT"
        self.CLK = Pin.PI23.value  # BCM 11
        self.SDA = Pin.PI19.value  # BCM 10
        self.DC = Pin.PI22.value   # BCM 25
        self.BACKLIGHT = Pin.PI29.value
        self._height = height
        self._width = width
        self._rotation = rotation
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._invert = invert

        if spi_id == 0:
            self.RST = Pin.PI31.value
            self.CS = 0
            # Only right eye (spi_id=0) controls the shared backlight
            backlight_pin = self.BACKLIGHT
        elif spi_id == 1:
            self.RST = Pin.PI18.value
            self.CS = 1
            # Left eye doesn't control backlight to avoid GPIO conflict
            backlight_pin = None
        else:
            raise ValueError("Invalid SPI ID")

        self.display = st7789.ST7789(
            height=self._height,
            width=self._width,
            rotation=self._rotation,
            port=0,
            cs=self.CS,
            dc=self.DC,
            rst=self.RST,
            backlight=backlight_pin,
            spi_speed_hz=20 * 1000 * 1000,
            offset_left=self._x_offset,
            offset_top=self._y_offset,
            invert=self._invert,
        )

        logger.info(f"{self.eye_name} eye display initialized")
        # begin() is deprecated in 0.0.4 but harmless - initialization happens in __init__
        self.display.begin()
        self.close_eye()

    def open_eye(self, image: Image) -> None:
        logger.debug(f"{self.eye_name} eye: opening")
        self.display.display(image)
        self.backlight(True)

    def close_eye(self):
        logger.debug(f"{self.eye_name} eye: closing")
        self.backlight(False)

    def backlight(self, on: bool) -> None:
        # Only right eye (spi_id=0) has backlight control
        # Left eye backlight calls are no-ops since the backlight is shared
        if self.spi_id == 0:
            self.display.set_backlight(on)
        else:
            logger.debug(f"{self.eye_name} eye: backlight control skipped (controlled by RIGHT eye)")
