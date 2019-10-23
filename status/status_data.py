def logs(status, message, link=None):
    log = {
        "code": status,
        "message": message
    }
    if link is not None:
        log["link"] = link

    return log


def HTTP_400_BAD_REQUEST(self):
    error = {}
    if self[0] == 100:
        message = "Unknown error"
        error = logs('400_BAD_REQUEST', message)
    # 200:
    elif self[0] == 200:
        try:
            message = self[1]
        except:
            message = "Not data completed"
        error = logs('400_BAD_REQUEST', message)
    # 300:
    elif self[0] == 300:
        message = "Empty Database"
        error = logs('400_BAD_REQUEST', message)

    return error


def HTTP_404_NOT_FOUND(self):
    error = {}
    if self[0] == 100:
        message = "Not found record in database"
        error = logs('404_NOT_FOUND', message)
        try:
            error['message'] += " uuid: " + self[1]
        except:
            pass
    return error
