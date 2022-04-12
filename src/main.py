from hashlib import new
from trading_bot import *
from configuration import *

if __name__ == '__main__':
    root = Tk()
    app = BOTGUI(root)

    t2 = Thread(target=log_task, args=(app,))

    t2.start()

    app.mainloop()