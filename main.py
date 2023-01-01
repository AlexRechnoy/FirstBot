from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from botTimer import send_locko_message, send_locko_moex_message, noon_send_message, send_cb_message
from botAsyncCommands import cmd_help, cmd_start, cmd_photo, cmd_bear, callback_find_best, callback_start_notify, \
                             callback_stop_notify, callback_show_all, cmd_currencies, cmd_add_photo, cmd_any_words,\
                             cmd_request_location, cmd_process_location
from botDispatcher import dp
import argparse
from botCMDs import botCMD


def create_parser():
    myparser = argparse.ArgumentParser()
    myparser.add_argument('endproc', nargs='?')
    return myparser


####################
dp.register_callback_query_handler(callback_find_best, text="find_best")
dp.register_callback_query_handler(callback_start_notify, text="start_notify")
dp.register_callback_query_handler(callback_stop_notify, text="stop_notify")
dp.register_callback_query_handler(callback_show_all, text="show_all")
dp.register_message_handler(cmd_help, commands="help")
dp.register_message_handler(cmd_start, commands="start")
dp.register_message_handler(cmd_photo, commands="photo")
dp.register_message_handler(cmd_bear, commands="bear")
dp.register_message_handler(cmd_request_location, commands="location")
dp.register_message_handler(cmd_process_location, content_types=['location'])
dp.register_message_handler(cmd_currencies, commands="currencies")
dp.register_message_handler(cmd_add_photo, content_types=["photo"])
dp.register_message_handler(cmd_any_words)

scheduler = AsyncIOScheduler()
scheduler.add_job(send_locko_message, "interval", minutes=5, args=(dp, botCMD))
scheduler.add_job(send_locko_moex_message, "interval", minutes=150, args=(dp, botCMD))
scheduler.add_job(noon_send_message, "cron", hour='12', minute='00', second='00', args=(dp, botCMD))
scheduler.add_job(send_cb_message, "cron", hour='15', minute='00', second='00', args=(dp, botCMD))
####################

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if not namespace.endproc:
        scheduler.start()
        executor.start_polling(dp, skip_updates=True)
