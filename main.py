from piedmont import Piedmont
from piedmont import logger

pie = Piedmont()


@pie.bridge('message')
def handler(data):
    pie.send('response', '123')


if __name__ == "__main__":
    # logger.set_dev_mode()
    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        print('Exit.')
        exit(0)
