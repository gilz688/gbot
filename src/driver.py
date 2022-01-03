from bot import Bot
from beepy import beep
import schedule
import signal
import time
import sys
from selenium.common.exceptions import NoSuchElementException

bot = Bot()
PIN = '1234'
running = True

@schedule.repeat(schedule.every(3).seconds)
def job():
    try:
        print("Opening app...")
        bot.start()

        print("Logging into GCash...")
        bot.login(PIN)

        print("Opening GForest...")
        bot.open_gforest()

        print("Looking for energy...")
        bubbles = bot.find_energy()

        if(len(bubbles) > 0):
            beep(sound="ping")
            for bubble in bubbles:
                _, _, energy = bubble
                print("Collecting " + energy + " energy...")
                bot.collect_energy(bubble)
        else:
            print("No energy found.")
    except NoSuchElementException as e:
        print(e)

    finally:
        print("Closing app...")
        bot.stop()

def handler(signum, frame):
    print("Stopping bot...")
    running = False
    schedule.clear()
    sys.exit()

def main():
    running = True
    signal.signal(signal.SIGINT, handler)

    while(running):
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()