

class BaseClass():
    def tick(self) -> None:
        # Run any maintance tasks and checks (about every 5 seconds)
        pass
                
    def required_config() -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        pass 