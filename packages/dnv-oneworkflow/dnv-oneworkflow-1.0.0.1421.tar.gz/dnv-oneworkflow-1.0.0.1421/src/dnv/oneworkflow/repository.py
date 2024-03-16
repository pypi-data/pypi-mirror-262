from enum import Enum, unique


@unique
class Repository(str, Enum):
    """
    An enumeration representing different package repositories. This enum is used to
    differentiate between various package repositories based on their deployment stages:
    development, testing, and production.

    Attributes:
        DEV (str): Identifier for the development repository. This repository typically
            contains packages that are currently under development and are used for developer
            testing.
        TEST (str): Identifier for the test repository. This repository typically contains
            packages that have passed the development stage and are used for further testing by
            testers.
        PROD (str): Identifier for the production repository. This repository typically
            contains packages that have passed all stages of testing and are ready for use by
            customers and end users.
    """

    DEV = "devpeuwst01owapps"
    TEST = "tstpeuwst01owapps"
    PROD = "prdpeuwst01owapps"
