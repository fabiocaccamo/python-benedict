class ExtrasRequireModuleNotFoundError(ModuleNotFoundError):
    def __init__(self, *, package, target):
        message = (
            f"Required optional module {package!r} not found, "
            f"consider to install it by running: "
            'python -m pip install "python-benedict[{target}]'
        )
        super().__init__(message)
