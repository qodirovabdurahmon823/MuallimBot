from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.sqlite import Database, Channel, Subjects, Books, Lessons, TestsDB
from pprint import pprint as print

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="data/sqlite/main.db")
channel = Channel(db_name='data/sqlite/channels.db')
subjectsdb = Subjects(db_name='data/sqlite/subjects.db')
booksdb = Books(db_name='data/sqlite/books.db')
lessonsdb = Lessons(db_name='data/sqlite/lessons.db')
testsdb = TestsDB(db_name='data/sqlite/tests.db')
# for i in range(11, 100):
#     print(testsdb.create_test(subject="Matematika", test_name=f"Test {i}", shuffling_type="shuffle_all"))
