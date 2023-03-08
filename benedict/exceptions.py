class ExtrasRequireModuleNotFoundError(ModuleNotFoundError):
    def __init__(self, *, target):
        message = (
            f"Extras require '[{target}]' module not found, "
            f"you can install it by running: "
            f"'python -m pip install \"python-benedict[{target}]\"'"
        )
        super().__init__(message)
