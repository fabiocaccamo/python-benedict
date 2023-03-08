class ExtrasRequireModuleNotFoundError(ModuleNotFoundError):
    def __init__(self, *, package, target):
        message = (
            f"{package!r} module not found, "
            f"you can install it by running: "
            f"'python -m pip install \"python-benedict[{target}]\"'"
        )
        super().__init__(message)
