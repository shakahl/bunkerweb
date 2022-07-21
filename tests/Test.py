from abc import ABC, abstractmethod
from sys import stderr
from time import time, sleep
from requests import get
from traceback import format_exc
from shutil import copytree
from os.path import isdir, join
from os import mkdir, makedirs, walk, chmod, rename
from re import sub, search, MULTILINE
from datetime import datetime
from subprocess import run
from logger import log

class Test(ABC) :

    def __init__(self, name, kind, timeout, tests) :
        self._name = name
        self.__kind = kind
        self.__timeout = timeout
        self.__tests = tests
        log("TEST", "ℹ️", "instiantiated with " + str(len(tests)) + " tests and timeout of " + str(timeout) + "s for " + self._name)

    # Class method
    # called once before running all the different tests for a given integration
    def init() :
        try :
            if not isdir("/tmp/bw-data") :
                mkdir("/tmp/bw-data")
            run("sudo chmod 777 /tmp/bw-data", shell=True)
            rm_dirs = ["configs", "plugins", "www"]
            for rm_dir in rm_dirs :
                if isdir(rm_dir) :
                    run("sudo rm -rf /tmp/bw-data/" + rm_dir, shell=True)
            if not isdir("/tmp/tests") :
                mkdir("/tmp/tests")
        except :
            log("TEST", "❌", "exception while running Test.init()\n" + format_exc())
            return False
        return True

    # Class method
    # called once all tests ended
    def end() :
        return True

    # called before starting the tests
    # must be override if specific actions needs to be done
    def _setup_test(self) :
        try :
            rm_dirs = ["configs", "plugins", "www"]
            for rm_dir in rm_dirs :
                if isdir("/tmp/bw-data/" + rm_dir) :
                    run("sudo rm -rf /tmp/bw-data/" + rm_dir + "/*", shell=True)
            if isdir("/tmp/tests/" + self._name) :
                run("sudo rm -rf /tmp/tests/" + self._name, shell=True)
            copytree("./examples/" + self._name, "/tmp/tests/" + self._name)
        except :
            log("TEST", "❌", "exception while running Test._setup_test()\n" + format_exc())
            return False
        return True

    # called after running the tests
    def _cleanup_test(self) :
        try :
            run("sudo rm -rf /tmp/tests/" + self._name, shell=True)
        except :
            log("TEST", "❌", "exception while running Test._cleanup_test()\n" + format_exc())
            return False
        return True

    # run all the tests
    def run_tests(self) :
        if not self._setup_test() :
            return False
        start = time()
        while time() < start + self.__timeout :
            all_ok = True
            for test in self.__tests :
                ok = self.__run_test(test)
                sleep(1)
                if not ok :
                    all_ok = False
                    break
            if all_ok :
                elapsed = str(int(time() - start))
                log("TEST", "ℹ️", "success (" + elapsed + "/" + str(self.__timeout) + "s)")
                return self._cleanup_test()
            log("TEST", "⚠️", "tests not ok, retrying in 1s ...")
        self._debug_fail()
        self._cleanup_test()
        log("TEST", "❌", "failed (timeout = " + str(self.__timeout) + "s)")
        return False

    # run a single test
    def __run_test(self, test) :
        try :
            if test["type"] == "string" :
                ex_url = test["url"]
                for ex_domain, test_domain in self._domains.items() :
                    if search(ex_domain, ex_url) :
                        ex_url = sub(ex_domain, test_domain, ex_url)
                        break
                r = get(ex_url, timeout=5)
                return test["string"].casefold() in r.text.casefold()
        except :
            #log("TEST", "❌", "exception while running test of type " + test["type"] + " on URL " + ex_url + "\n" + format_exc())
            return False
        raise(Exception("unknow test type " + test["type"]))

    # called when tests fail : typical case is to show logs
    def _debug_fail(self) :
        pass

    def replace_in_file(path, old, new) :
        with open(path, "r") as f :
            content = f.read()
        content = sub(old, new, content, flags=MULTILINE)
        with open(path, "w") as f :
            f.write(content)

    def replace_in_files(path, old, new) :
        for root, dirs, files in walk(path) :
            for name in files :
                Test.replace_in_file(join(root, name), old, new)

    def rename(path, old, new) :
        for root, dirs, files in walk(path) :
            for name in dirs + files :
                full_path = join(root, name)
                new_path = sub(old, new, full_path)
                if full_path != new_path :
                    rename(full_path, new_path)