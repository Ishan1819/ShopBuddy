
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
    url = "https://www.amazon.in/Nike-Revolution-8-Green-Black-Green-STRIKE-WHITE-HJ9198-301-7UK/dp/B0DPHYZMR5/ref=sr_1_3?dib=eyJ2IjoiMSJ9.1IiQRYowTIewJTnt1YQd-J57RT-cejVbr3P3VIeDlOanJ8DQWibL9R-U4BoXLYBqjb5hfYqX5Gl5_7Gpm7Gt0QrJJbGh3JWA3uTJTQU-LRLvujA9kDvcIMR6t7P5RWoC33uajvf1TSHFDc9lrP0Xbl1vyDPYWescD4SPXXiFxR-JuUlMhVXLQa7ShZD-PZEYNGf8Yv_DDRZmavmhvsE6WQnSIe2UnY2nRiq_HyVrmxpwRTtUKCLodTV7lUSOr_He3c3Kuoo5QPi6LVInVghOr-zPKjHCjz2TyF2XauN7J3o.OzvqS1z6nhq8KZUd64qCGEElnclyLcBpsvO9vAYveQk&dib_tag=se&keywords=Nike&nsdOptOutPara"
    target_price = 5000
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

