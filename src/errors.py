class Error(Exception):
    """
    错误类
    """
    pass


class InputError(Error):
    """
    用于报告输入空文件的错误
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
