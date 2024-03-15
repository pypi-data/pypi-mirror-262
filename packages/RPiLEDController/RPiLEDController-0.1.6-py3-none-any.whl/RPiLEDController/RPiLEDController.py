from RPiLEDController.LED import LED, LEDTrigger
from RPiLEDController.RPiSupportedVersions import RPiSupportedVersions


class RPiLEDController:

    def __init__(self, RPiVersion:int=RPiSupportedVersions.RPi4):
        """

        :param int RPiVersion: The version of the Raspberry Pi that the LED controller is running on.
        :raises ValueError: If the version of the Raspberry Pi is not supported.
        """
        if not RPiSupportedVersions.is_supported_version(RPiVersion):
            raise ValueError("The version of the Raspberry Pi is not supported. Supported versions are: " + str(RPiSupportedVersions.get_supported_versions()) + ".")

        self.RPiVersion = RPiVersion

        act_name = "ACT"
        pwr_name = "PWR"

        if self.RPiVersion < RPiSupportedVersions.RPi4:
            act_name = "led0"
            pwr_name = "led1"

        self.act_led = LED(act_name, default_trigger=LEDTrigger.MMC0)
        self.pwr_led = LED(pwr_name, default_trigger=LEDTrigger.DEFAULT_ON)

        self.reserve()

        print(self.act_led)
        print(self.pwr_led)

    def act_reserve(self):
        """
        Reserves the activity LED for use.
        """
        self.act_led.reserve()

    def act_release(self):
        """
        Releases the activity LED for use.
        """
        self.act_led.release()

    def pwr_reserve(self):
        """
        Reserves the power LED for use.
        """
        self.pwr_led.reserve()

    def pwr_release(self):
        """
        Releases the power LED for use.
        """
        self.pwr_led.release()

    def reserve(self):
        """
        Reserves the LED for use.
        """
        self.act_led.reserve()
        self.pwr_led.reserve()

    def release(self):
        """
        Releases the LED for use.
        """
        self.act_led.release()
        self.pwr_led.release()

    def act_on(self):
        """
        Turns on the activity LED.
        """
        self.act_led.on()

    def act_off(self):
        """
        Turns off the activity LED.
        """
        self.act_led.off()

    def act_toggle(self):
        """
        Toggles the activity LED.
        """
        self.act_led.toggle_led()

    def pwr_on(self):
        """
        Turns on the power LED.
        """
        self.pwr_led.on()

    def pwr_off(self):
        """
        Turns off the power LED.
        """
        self.pwr_led.off()

    def pwr_toggle(self):
        """
        Toggles the power LED.
        """
        self.pwr_led.toggle_led()