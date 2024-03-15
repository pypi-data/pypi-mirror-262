import requests


class TextData:
    """A class to handle text data from either a local file or a web link."""

    def __init__(self, source: str) -> None:
        """
        Initialize the TextData object.

        Args:
            source (str): The source of the text data. It can be a local file path or a web link.
        """
        self.raw_data = self._read_source(source=source)

    def _read_source(self, source: str):
        """
        Read the text data from the specified source.

        Args:
            source (str): The source of the text data.

        Returns:
            str: The content of the text data.
        """
        if source.startswith("http://") or source.startswith("https://"):
            return self._read_from_link(source=source)

        return self._read_local_file(source=source)

    def _read_from_link(self, source: str):
        """
        Read text data from a web link.

        Args:
            source (str): The web link.

        Returns:
            str: The content of the text data from the web link.
        """
        response = requests.get(source)
        response.raise_for_status()
        content = response.text
        return content

    def _read_local_file(self, source: str):
        """
        Read text data from a local file.

        Args:
            source (str): The path to the local file.

        Returns:
            str: The content of the text data from the local file.
        """
        with open(source) as f:
            content = f.read()
        return content
