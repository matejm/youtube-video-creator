
class Logger:
    @staticmethod
    def log(data):
        print('[LOG] {}'.format(data))

    @staticmethod
    def warn(data):
        print('[WARN] {}'.format(data))

    @staticmethod
    def error(data):
        print('[ERROR] {}'.format(data))
