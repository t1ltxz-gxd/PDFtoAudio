from main import get_documents
from unittest import main, TestCase
import asyncio


class TestSaveMp3(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_main(self):
        asyncio.run(get_documents(file_path="data/pdf"))


if __name__ == "__main__":
    main()
