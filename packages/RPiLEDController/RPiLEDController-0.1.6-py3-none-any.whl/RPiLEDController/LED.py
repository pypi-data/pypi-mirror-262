class LEDTrigger:
    NONE = "none"
    RC_FEEDBACK = "rc-feedback"
    KBD_SCROLLLOCK = "kbd-scrolllock"
    KBD_NUMLOCK = "kbd-numlock"
    KBD_CAPSLOCK = "kbd-capslock"
    KBD_KANALOCK = "kbd-kanalock"
    KBD_SHIFTLOCK = "kbd-shiftlock"
    KBD_ALTGRLOCK = "kbd-altgrlock"
    KBD_CTRLLOCK = "kbd-ctrllock"
    KBD_ALTLOCK = "kbd-altlock"
    KBD_SHIFTLLOCK = "kbd-shiftllock"
    KBD_SHIFTRLOCK = "kbd-shiftrlock"
    KBD_CTRLLLOCK = "kbd-ctrlllock"
    KBD_CTRLRLOCK = "kbd-ctrlrlock"
    TIMER = "timer"
    ONESHOT = "oneshot"
    HEARTBEAT = "heartbeat"
    BACKLIGHT = "backlight"
    CPU = "cpu"
    CPU0 = "cpu0"
    CPU1 = "cpu1"
    CPU2 = "cpu2"
    CPU3 = "cpu3"
    DEFAULT_ON = "default-on"
    INPUT = "input"
    PANIC = "panic"
    ACTPWR = "actpwr"
    MMC1 = "mmc1"
    MMC0 = "mmc0"
    RFKILL_ANY = "rfkill-any"
    RFKILL_NONE = "rfkill-none"
    RFKILL0 = "rfkill0"
    RFKILL1 = "rfkill1"


class LEDState:
    ON = 1
    OFF = 0

class LED:

    def __init__(self, name: str = "ACT", default_state: int = LEDState.OFF, default_trigger: str = LEDTrigger.MMC0):
        """

        :param str name: The name of the LED
        :param int default_state: The default state of the LED.
        :param bool reversed: Whether the LED is reversed (on is off and off is on)
        """

        self.name = name
        self.default_state = default_state
        self.reversed = reversed
        self.state = self.get_state(True)

        if self.state != self.default_state:
            self.state = self.default_state
            self.off() if self.default_state == LEDState.OFF else self.on()

        self.trigger = default_trigger

    def __str__(self):
        return f"LED: {self.name} | Current State: {self.state} | Default State: {self.default_state}"

    def get_state(self, osState: bool = False):
        """
        Returns the state of the LED

        :param bool osState: Whether to get the state from the OS or the object
        """
        if osState:
            import os
            with open(f"/sys/class/leds/{self.name}/brightness", "r") as file:
                return int(file.read())
        return self.state

    def toggle_led(self):
        """
        Toggles the LED on or off
        """
        if self.state == LEDState.ON:
            self.off()
            return
        self.on()

    def on(self):
        """
        Turns the LED on
        """
        import os
        self.state = LEDState.ON
        os.system(f"echo {self.state} > /sys/class/leds/{self.name}/brightness")

    def off(self):
        """
        Turns the LED off
        """
        import os
        self.state = LEDState.OFF
        os.system(f"echo {self.state} > /sys/class/leds/{self.name}/brightness")

    def reserve(self):
        """
        Reserves the LED for use.
        """
        import os
        os.system(f"echo none > /sys/class/leds/{self.name}/trigger")

    def release(self):
        """
        Releases the LED for use.
        """
        import os
        os.system(f"echo {self.trigger} > /sys/class/leds/{self.name}/trigger")