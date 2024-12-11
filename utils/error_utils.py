class SQLError(Exception):
    """数据库异常类"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
