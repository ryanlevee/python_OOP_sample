# import inspect
import os
# import re
import traceback
from datetime import date, datetime

# from notify import notify_email


def traceback_logger(s, ex=""):
    now = datetime.now()
    root = os.path.dirname(os.path.abspath(__file__))

    print(f'\nTRACEBACK START:\n{now}\n{traceback.format_exc()}')

    with open(f'{root}/error_logs/{date.today()}_traceback_{s}.log', 'a+') as f:
        f.write(str(now) + '\n')
        f.write(traceback.format_exc() + '\n')

    # source = re.search(r'(?!\\)(\w+\.py)', inspect.stack()[1].filename).group()
    # notify_email(f'{str(now)}\n{traceback.format_exc()}', source, ex)
