# config


class Configuration(object):
    DATABASE = {
        'name': 'promopuffincore.db',
        'engine': 'SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'putsomethingheresomeday'
    PROMOPUFFIN_API_KEY = 'somekey'
