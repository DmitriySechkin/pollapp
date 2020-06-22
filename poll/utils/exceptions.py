class Error(Exception):
    """
    Base Error, all other Errors thrown by Parser should inherit from this
    """

    def __init__(self, value=None):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __unicode__(self):
        return f"{self.value}"


class NoFindQuestionByID(Error):
    """
    The exception is thrown when there is no requested section in the config file
    """

    def __init__(self, question_id):
        err_text = f"Не найден объект Question по id {question_id}!"
        super(NoFindQuestionByID, self).__init__(err_text)


class NoFindChoiceInTableById(Error):

    def __init__(self, choice_id):
        err_text = f"В БД не найден объект Choice по id {choice_id}!"
        super(NoFindChoiceInTableById, self).__init__(err_text)
