import sys


def main():
    print("Yet another Git implementation in Python.")


if __name__ == "__main__":
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print(e, file=sys.stderr)
    sys.exit(rc)
