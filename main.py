from piedmont import Piedmont

pie = Piedmont(debug=True)


@pie.bridge('message')
def handler(data):
    pie.send('response', '123')


if __name__ == "__main__":
    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        print('Exit.')
        raise SystemExit(0)
