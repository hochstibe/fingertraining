# fingertraining
# Stefan Hochuli, 14.09.2021,
# Folder: speck_weg/app File: message.py
#


class Message:
    def __init__(self, title: str, text: str, level: str, informative_text: str = None,
                 button_accept_name: str = None, button_reject_name: str = None):
        # required
        self.title = title
        self.text = text
        self._level = level  # protected
        # optional
        self.informative_text = informative_text
        self.button_accept_name = button_accept_name
        self.button_reject_name = button_reject_name

        # self.level = self._level

        # if the message is accepted (only possible with an accept button)
        self.accept: bool = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):

        if value not in ['information', 'question', 'warning', 'critical']:
            raise NotImplementedError(
                "Level must be one of 'information', 'question', 'warning' or 'critical'.")
        self._level = value

    def __repr__(self):
        return f'Message(title={self.title}, text={self.text}, level={self.level})'
