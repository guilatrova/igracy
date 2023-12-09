from __future__ import annotations


class IGracyException(Exception):
    pass


class AttrMissingSignature(IGracyException):
    def __init__(self, val: str) -> None:
        msg = f"{val} is missing a type annotation. IGracy can't infer it."
        super().__init__(msg)
