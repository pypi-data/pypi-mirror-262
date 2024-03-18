# type: ignore
import os
import json
import sys
import shutil
import traceback
from enum import Enum
from httpx import ConnectError
from innertube import InnerTube
from innertube.errors import RequestError
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional

TEST_PATH = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_PATH, "test_data.json")
TEST_ERRS = os.path.join(TEST_PATH, "errors")
ITDE_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, ITDE_PATH)

from itde import extractor  # noqa
from itde import Container  # noqa
from itde import ITDEError  # noqa


if os.path.exists(TEST_ERRS):
    shutil.rmtree(path=TEST_ERRS)

os.mkdir(path=TEST_ERRS)


class TestExtractor:

    def __init__(self) -> None:
        self.__innertube_client = InnerTube("WEB_REMIX")
        self.tlog: List[str] = []
        self.ext_data: Dict[str, Optional[Container]] = {}

        with open(TEST_DATA, mode="r") as file:
            test_data = json.loads(file.read())
        self.__test_sear = test_data["sear"]
        self.__test_brow = test_data["brow"]
        self.__test_next = test_data["next"]
        # self.__test_cont = test_data["cont"]

    def test_search(self) -> None:
        for test in self.__test_sear:
            self.__do_test_wrapper(
                func=lambda: self.__innertube_client.search(
                    query=test["query"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="sear",
                test_name=test["name"],
            )

    def test_browse(self) -> None:
        for test in self.__test_brow:
            self.__do_test_wrapper(
                func=lambda: self.__innertube_client.browse(
                    browse_id=test["browse_id"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="brow",
                test_name=test["name"],
            )

    def test_next(self) -> None:
        for test in self.__test_next:
            self.__do_test_wrapper(
                func=lambda: self.__innertube_client.next(
                    video_id=test["video_id"],
                    playlist_id=test["playlist_id"],
                    params=test["params"],
                    index=test["index"],
                    continuation=test["continuation"],
                ),
                test_type="next",
                test_name=test["name"],
            )

    # def test_continuation(self) -> None:
    #     for test in self.__test_sear:
    #         innertube_data = self.__innertube_client.search(
    #             query=test["query"],
    #             params=test["params"],
    #             continuation=test["continuation"],
    #         )

    def __do_test_wrapper(
        self, func: Callable, test_type: str, test_name: str
    ) -> None:
        name = f"{test_type}_{test_name}"
        tlog = f"{name} {Color.GREEN}[OK]{Color.RESET}"
        try:
            innertube_data = func()
            ext_data = extractor.extract(innertube_data)
            self.ext_data[name] = ext_data
        except (ITDEError, RequestError, ConnectError) as error:
            print(f"{Color.BOLD}{Color.BLUE}+++ {name} +++{Color.RESET}")
            traceback.print_exc()
            tlog = f"{name} {Color.RED}[ERROR]{Color.RESET}"
            if isinstance(error, ITDEError):
                with open(os.path.join(TEST_ERRS, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)  # noqa
        else:
            print(f"{Color.BLUE}{name}{Color.RESET}")
            if ext_data and ext_data.contents:
                for shelf in ext_data.contents:
                    print(f"{Color.LIGHT_GREEN}{shelf.name}{Color.RESET}")
                    for item in shelf:
                        print(f"{str(item)[:200]}")
            else:
                print("None")
            print()
        finally:
            self.tlog.append(tlog)


class Color(Enum):
    GREEN = "\033[92m"
    LIGHT_GREEN = "\033[1;92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    BOLD = "\033[;1m"
    CYAN = "\033[1;36m"
    LIGHT_CYAN = "\033[1;96m"
    LIGHT_GREY = "\033[1;37m"
    DARK_GREY = "\033[1;90m"
    BLACK = "\033[1;30m"
    WHITE = "\033[1;97m"
    INVERT = "\033[;7m"
    RESET = "\033[0m"

    def __str__(self) -> str:
        return self.value


def main():
    test_extractor = TestExtractor()
    test_extractor.test_search()
    test_extractor.test_browse()
    test_extractor.test_next()

    print("----------------")
    for tlog in test_extractor.tlog:
        print(tlog)


if __name__ == "__main__":
    main()
