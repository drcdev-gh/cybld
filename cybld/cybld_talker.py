#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import datetime
import logging
import random

from cybld import cybld_helpers

# --------------------------------------------------------------------------


class CyBldTalker:

    def __init__(self, enabled):
        self.enabled = enabled

    def say_hello(self):
        if not self.enabled:
            return

        logging.info(self._get_hello())

    def say_goodbye(self):
        if not self.enabled:
            return

        logging.info(self._get_goodbye())

    def say_success(self):
        if not self.enabled:
            return

        cybld_helpers.print_centered_text(self._get_success(), True)

    def say_fail(self):
        if not self.enabled:
            return

        cybld_helpers.print_centered_text(self._get_fail(), False)

    def _get_hello(self) -> str:
        morning_start   = datetime.time(5, 0, 0)
        afternoon_start = datetime.time(12, 30, 0)
        evening_start   = datetime.time(16, 00, 0)
        night_start     = datetime.time(21, 00, 0)

        current = datetime.datetime.now().time()

        if current > morning_start and current < afternoon_start:
            return self._get_hello_morning()
        elif current > afternoon_start and current < evening_start:
            return self._get_hello_afternoon()
        elif current > evening_start and current < night_start:
            return self._get_hello_evening()
        elif current > night_start:
            return self._get_hello_night()
        else:
            return "Hello there!"

    def _get_hello_morning(self) -> str:
        choices = ["Good morning!", "How about breakfast at Tiffanys?",
                   "Hope you enjoyed your coffee!",
                   "But what about second breakfast?"]
        return "".join(random.sample(choices, 1))

    def _get_hello_afternoon(self) -> str:
        choices = ["Good day sir!", "Good afternoon!"]
        return "".join(random.sample(choices, 1))

    def _get_hello_evening(self) -> str:
        choices = ["Good evening!"]
        return "".join(random.sample(choices, 1))

    def _get_hello_night(self) -> str:
        choices = ["Hello night owl. Drank too much coffee?",
                   "You should probably go to sleep...",
                   "Just one more bug, right?"]
        return "".join(random.sample(choices, 1))

    def _get_goodbye(self) -> str:
        choices = ["Bye-bye!", "See you around", "Goodbye!",
                   "Cya!"]
        return "".join(random.sample(choices, 1))

    def _get_success(self) -> str:
        choices = ["You did it!", "I love it", "Are you a wizard?",
                   "Let's just say it's a winning streak",
                   "That's one for the history books",
                   "Well done, whoever did that", "Noice"]
        return "".join(random.sample(choices, 1))

    def _get_fail(self) -> str:
        choices = ["Last resort: Push and claim that it works on your machine",
                   "Oh, embarrassing", "Uh, What a mess",
                   "Huuugh that's not good", "Oh boy",
                   "Relax. It's just a bunch of 0s and 1s",
                   "Might want to get on that",
                   "Better luck next time", "Take a deep breath...",
                   "Why, Why?, Why?, Why?, Why?",
                   "What the hell is going on?", "It could be worse..."]
        return "".join(random.sample(choices, 1))
