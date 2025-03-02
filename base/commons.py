class BaseClass:
    def tick(self) -> None:
        # Run any maintenance tasks and checks (about every 5 seconds)
        pass

    def required_config() -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        pass


class address:
    def __init__(self, address: str):
        split_address = address.strip().split(".")

        # Data Validation
        if len(split_address) != 4:
            raise ValueError()

        for value in split_address:

            if not value.isdigit():
                raise ValueError()

            elif len(value) > 3:
                raise ValueError()

            elif int(value) < 0 or int(value) > 255:
                raise ValueError()

        self.address = [int(value) for value in split_address]

    def is_multicast(self) -> bool:
        if self.address[0] >= 224 and self.address[0] <= 239:
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.address[0]}.{self.address[1]}.{self.address[2]}.{self.address[3]}"
        )


class url:
    def __init__(self, url: str):
        self.url = url

    def __str__(self) -> str:
        return self.url
