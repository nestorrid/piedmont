from piedmont import Piedmont
from piedmont import storage
from piedmont import logger

pie = Piedmont(debug=True)


@pie.bridge('message')
def handler(data):
    pie.send('response', '123')


if __name__ == "__main__":
    pie.start()
