import config
import logging
from pyowm import OWM
from pyowm.utils.config import get_default_config

from aiogram import Bot, Dispatcher, executor, types

config_dict = get_default_config()
config_dict['language'] = 'ru' 

owm = OWM( '8d66ad755c2c2bc774526a02a911364b', config_dict  )

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# echo
@dp.message_handler()
async def echo(message: types.Message):
  mgr = owm.weather_manager()
  observation = mgr.weather_at_place(message.text)
  w = observation.weather
  temp = w.temperature('celsius')["temp"]
  answer = "Сейчас в " + message.text + " " + w.detailed_status + "\n"
  answer += "Температура сейчас в районе " + str(temp) + "\n\n"

  if temp < 10:
    answer += "Сейчас ппц как холодно, одевайся как танк!"
  elif temp < 20:
    answer += "Сейчас холодно, оденься потеплее."
  else:
    answer += "Температура норм, одевай что угодно."

  await message.answer(answer)

#run long-polling
if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)