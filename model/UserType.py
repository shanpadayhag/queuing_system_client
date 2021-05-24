def convertType(string):
    userType = {
        'admin': 1,
        'teacher': 2,
        'student': 3,
    }

    return userType.get(string, 0)