import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from alert import DiscordAlertBot
import time

DiscordAlertBot.send_message("sening test")