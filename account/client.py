"""Provide the Client class for a financial institution.

Author: Jashandeep Kaur
"""

from email_validator import validate_email


class Client:
    """Represent a client with an identifier, name, and email address."""

    def __init__(
        self,
        client_id: int,
        name: str,
        email_address: str
    ):
        """Initialize a client with a validated email address.

        Args:
            client_id (int): The client's positive identifier.
            name (str): The client's name. Surrounding whitespace
                is removed.
            email_address (str): The client's email address.
                Surrounding whitespace is removed before validation.

        Raises:
            ValueError: If client_id is less than or equal to zero,
                or name is blank after stripping whitespace.
            EmailNotValidError: If the email address is invalid.
        """
        if client_id <= 0:
            raise ValueError(
                "client_id must be a value greater than zero."
            )

        name = name.strip()

        if name == "":
            raise ValueError(
                "name cannot be an empty string."
            )

        email_address = email_address.strip()
        email_info = validate_email(
            email_address,
            check_deliverability=False
        )

        self.__client_id = client_id
        self.__name = name
        self.__email_address = email_info.normalized

    @property
    def client_id(self) -> int:
        """Return the client's identifier as an int."""
        return self.__client_id

    @property
    def name(self) -> str:
        """Return the client's name as a str."""
        return self.__name

    @property
    def email_address(self) -> str:
        """Return the validated, normalized email address as a str."""
        return self.__email_address

    @email_address.setter
    def email_address(self, value: str) -> None:
        """Validate and update the client's email address.

        Args:
            value (str): The new email address. Surrounding
                whitespace is removed before validation.

        Raises:
            EmailNotValidError: If the new email address is invalid.
                The existing address remains unchanged.
        """
        value = value.strip()

        email_info = validate_email(
            value,
            check_deliverability=False
        )

        self.__email_address = email_info.normalized

    def __str__(self) -> str:
        """Return the client's name, bracketed ID, and email address."""
        return (
            f"{self.__name} [{self.__client_id}] - "
            f"{self.__email_address}"
        )