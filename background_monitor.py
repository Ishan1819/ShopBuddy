
import time
import sys
import os
import signal
import json
from datetime import datetime

# Ignore interrupt signals to prevent background process from stopping
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all the monitoring functions
from backend.bots.price_notifier_bot import check_price_and_notify, send_email, update_monitor_status

def background_monitor():
    url = "https://www.amazon.in/Puma-Unisex-Adult-Sneakers-8-30642203/dp/B07QJPLWGZ/ref=sr_1_5?dib=eyJ2IjoiMSJ9.vCbls3Xo7E9BZLrZIHD_FSONLJQcWlYTQHMCBi2h9XRpG-2rCfvcLZX_H9Y6k8IY_se2ljEp_Xfjh4ISxMF5yvYxkW8ZSBwPney5i9n3zN8N6ELCMVccE-wesnXwmWyUlR55Xw_zrALS2TF7IMf_l5G1wgg6vOuddBse3KS97K9I2GGZfErtJb2EAS8JG_wWkegW6H85jdSF1FR47mHPMvxN13eyLnjhmM_-KLM4lUPOvAs6aYIE9yaaa6uXD77xK0rNQgcgStZ2aFrwPM9i7o-VnheMDpeQxf3savCIApc.jQdAMqHbuVy_wRJ-p_X2d4U8eHZxs1vEsqeXXnEGWyw&dib_tag=se&keywords=Puma+shoes&nsdOptOutParam=true&qid=1752129911&sr=8-5"
    target_price = 2000
    interval_seconds = 120
    
    print(f"[BACKGROUND] Background monitoring started for: {url}")
    print(f"[BACKGROUND] Target Price: Rs.{target_price}")
    print(f"[BACKGROUND] Check Interval: {interval_seconds} seconds")
    
    # Update status to show it's running in background
    update_monitor_status("background_active")
    
    while True:
        try:
            check_price_and_notify(url, target_price)
            time.sleep(interval_seconds)
        except Exception as e:
            print(f"[ERROR] Error in background monitoring: {e}")
            # Continue monitoring even if there's an error
            time.sleep(interval_seconds)

