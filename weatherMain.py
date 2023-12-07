from weatherLogic import *

def main():
    application = QApplication([])
    window = Weather()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()