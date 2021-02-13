from xvfbwrapper import Xvfb
from upc_meet_manager import UPCMeetManager
import threading
import subprocess
from queue import Queue


def start_bot(q):
    with Xvfb(width=1920, height=1080, colordepth=24) as xvfb:
        q.put(xvfb.new_display)
        meet_url = "https://meet.google.com/pmj-gjaz-ksn"
        user = "alexandre.perez.josende"
        mail_domain = "estudiantat.upc.edu"
        passwd = "Alex224683"
        m = UPCMeetManager(user + "@" + mail_domain, user,
                           passwd, resolution=(1920, 1080))
        m.meet_while(meet_url, 40, 40, 0.3)


q = Queue()
bot_thread = threading.Thread(target=start_bot, args=(q,))
bot_thread.start()
display = q.get(block=True, timeout=10)
ffmpeg_p = subprocess.Popen(["ffmpeg", "-y", "-f", "x11grab", "-r", "15", "-video_size",
                             "1920x1080", "-draw_mouse", "0", "-i", f":{display}",
                             "-f", "pulse", "-ac", "2", "-i", "default", "/output/video.webm"])
bot_thread.join()
ffmpeg_p.kill()
