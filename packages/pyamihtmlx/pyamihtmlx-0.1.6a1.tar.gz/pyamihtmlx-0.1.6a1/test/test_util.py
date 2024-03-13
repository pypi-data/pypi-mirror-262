# test util

import csv
import logging
import re
import shutil
import sys
import unittest
from pathlib import Path

from pyamihtmlx.file_lib import FileLib
from pyamihtmlx.util import EnhancedRegex
from pyamihtmlx.util import Util, GithubDownloader, ArgParseBuilder, AmiArgParser, AmiArgParseException
from pyamihtmlx.xml_lib import Templater

from test.resources import Resources
from test.test_all import AmiAnyTest

# local


logger = logging.getLogger("py4ami_test_util")


class TestUtil(AmiAnyTest):
    # def __init__(self):
    sys_argv_save = None

    # @classmethod
    # def setUp(cls):
    #     """save args as they will be edited"""
    #     cls.sys_argv_save = sys.argv
    #
    # @classmethod
    # def tearDown(cls):
    #     """restore args"""
    #     sys.argv = cls.sys_argv_save

    @classmethod
    @unittest.skip("not working properly, I think some tests change the args...")
    # TODO fix args - some  tests change the args
    def test_add_argstr(cls):
        # this is a hack as normally there is only one element
        # sys.argv = sys.argv[1:]
        # assert sys.argv[1:] == []
        cmd = "--help foo bar plinge"
        Util.add_sys_argv_str(cmd)
        assert sys.argv[1:] == ["--help", "foo", "bar", "plinge"]

    @classmethod
    @unittest.skip("not working properly")
    # TODO fix args
    def test_add_args(cls):
        # this is a hack as normally there is only one element
        sys.argv = sys.argv[1:]
        # assert sys.argv[1:] == []
        args = ["--help", "foox", "barx", "plingex"]
        Util.add_sys_argv(args)
        assert sys.argv[1:] == ["--help", "foox", "barx", "plingex"]

    @classmethod
    def test_copy_anything(cls):
        src = Resources.TEST_CLIMATE_10_SVG_DIR
        dst = Path(AmiAnyTest.TEMP_DIR, "tempzz")
        if dst.exists():
            shutil.rmtree(dst)
        FileLib.copyanything(src, dst)
        assert Path(dst).exists()

    def test_create_name_value(self):
        """tests parsing of PyAMI flags
        """
        name, value = Util.create_name_value("foo=bar")
        assert name, value == ("foo", "bar")
        name, value = Util.create_name_value("foo")
        assert name, value == ("foo", True)
        try:
            arg = "foo=bar=plugh"
            Util.create_name_value(arg)
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve == "too many delimiters in {arg}")
        try:
            arg = "foo bar"
            _, v = Util.create_name_value(arg)
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve) == "arg [foo bar] may not contain whitespace"

        Util.create_name_value("foo/bar")
        assert name, value == "foo/bar"

        Util.create_name_value("foo/bar", delim="/")
        assert name, value == ("foo", "bar")

        assert Util.create_name_value("") is None

        arg = "foo bar"
        try:
            _, v = Util.create_name_value(arg, delim=" ")
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve) == f"arg [{arg}] may not contain whitespace"

    def test_read_csv(self):
        """use Python csv to select column values"""
        csv_file = Path(Resources.TEST_RESOURCES_DIR, "eoCompound", "compound_enzyme.csv")
        assert csv_file.exists(), f"{csv_file} should exist"
        with open(str(csv_file), newline='') as csvfile:
            row_values = [["isopentenyl diphosphate", "COMPOUND"],
                          ["dimethylallyl diphosphate", "COMPOUND"],
                          ["hemiterpene", "COMPOUND"]]
            reader = csv.DictReader(csvfile)

            for i, row in enumerate(reader):
                if i < 3:
                    assert row['NAME'] == row_values[i][0]
                    assert row['TYPE'] == row_values[i][1]

    def test_select_csv_field_by_type(self):
        """select value in column of csv file by value of defining column
        """
        csv_file = Path(Resources.TEST_RESOURCES_DIR, "eoCompound", "compound_enzyme.csv")
        assert csv_file.exists(), f"{csv_file} should exist"
        selector_column = "TYPE"
        column_with_values = "NAME"
        selector_value = "COMPOUND"

        values = Util.extract_csv_fields(csv_file, column_with_values, selector_column, selector_value)
        assert len(values) == 89
        assert values[:3] == ['isopentenyl diphosphate', 'dimethylallyl diphosphate', 'hemiterpene']

        selector_value = "ENZYME"
        values = Util.extract_csv_fields(csv_file, column_with_values, selector_column, selector_value)
        assert len(values) == 92
        assert values[:3] == ['isomerase', 'GPP synthase', 'FPP synthase']

    def test_create_arg_parse(self):
        arg_parse_file = Path(Resources.TEST_RESOURCES_DIR, "arg_parse.json")
        arg_parse_builder = ArgParseBuilder()
        arg_dict = arg_parse_builder.create_arg_parse(arg_dict_file=arg_parse_file)

    def test_range_list_contains_int(self):
        """does a range or range list contain an int"""
        # single
        rangex = range(1, 3)
        assert not Util.range_list_contains_int(0, rangex)
        assert Util.range_list_contains_int(1, rangex)
        assert not Util.range_list_contains_int(3, rangex)
        # list
        range_list = [range(1, 3), range(5, 9)]
        assert not Util.range_list_contains_int(0, range_list)
        assert Util.range_list_contains_int(1, range_list)
        assert not Util.range_list_contains_int(3, range_list)
        assert not Util.range_list_contains_int(4, range_list)
        assert Util.range_list_contains_int(5, range_list)
        assert not Util.range_list_contains_int(9, range_list)
        assert not Util.range_list_contains_int(10, range_list)
        # None
        range_list = None
        assert not Util.range_list_contains_int(0, range_list)
        range_list = range(1, 3)
        assert not Util.range_list_contains_int(None, range_list)

    def test_get_file_from_url(self):
        url = None
        assert Util.get_file_from_url(url) is None
        url = "https://foo.bar/plugh/bloop.xml"
        assert Util.get_file_from_url(url) == "bloop.xml"

    @unittest.skip("NYI")
    def test_make_id_from_match_and_idgen(self):
        """idgen is of the form <grouo>some text<group>
        where groups correspond to named capture groups in regex
        """
        idgen = "12/CMA.34"
        components = ["", ("decision", "\\d+"), "/", ("type", "CP|CMA|CMP"), "\\.", ("session", "\\d+"), ""]
        enhanced_regex = EnhancedRegex(components=components)
        id = enhanced_regex.make_id(idgen)
        assert id == "12_CMA_34"

    # ABANDONED
    # def test_make_regex_with_capture_groups(self):
    #     """idgen is of the form <grouo>some text<group>
    #     where groups correspond to named capture groups in regex
    #     """
    #     enhanced_regex = EnhancedRegex()
    #     components = ["", ("decision", "\d+"), "/", ("type", "CP|CMA|CMP"), "\.", ("session", "\d+"), ""]
    #     regex = enhanced_regex.make_regex_with_capture_groups(components)
    #     assert regex == '(?P<decision>\\d+)/(?P<type>CP|CMA|CMP)\\.(?P<session>\\d+)'

    def test_make_components_from_regex(self):
        """splits regex with capture groups into its components
        """
        regex = '(?P<decision>\\d+)/(?P<type>CP|CMA|CMP)\\.(?P<session>\\d+)'
        re_parser = EnhancedRegex(regex=regex)
        components = re_parser.make_components_from_regex(regex)
        assert len(components) == 7
        assert components[1] == '(?P<decision>\\d+)'
        assert components[3] == '(?P<type>CP|CMA|CMP)'
        unittest.TestCase().assertListEqual(components,
            ['', '(?P<decision>\\d+)','/','(?P<type>CP|CMA|CMP)','\\.', '(?P<session>\\d+)', ''])


class TestGithubDownloader(AmiAnyTest):
    # def __init__(self):
    #     pass

    @unittest.skip("VERY LONG, DOWNLOADS")
    def test_explore_main_page(self):
        owner = "petermr"
        repo = "CEVOpen"
        downloader = GithubDownloader(owner=owner, repo=repo, max_level=1)
        page = None
        downloader.make_get_main_url()
        print(f"main page {downloader.main_url}")
        url = downloader.main_url
        if not url:
            print(f"no page {owner}/{repo}")
            return None

        downloader.load_page(url, level=0)


class TestAmiArgParser(AmiAnyTest):

    def test_ami_arg_parse(self):
        """
        test subclassing of argParse
        """
        ami_argparse = AmiArgParser()
        ami_argparse.add_argument("--flt", type=float, nargs=1, help="a float", default=80)
        ami_argparse.add_argument("--str", type=str, nargs=1, help="a string")

        # this works
        arg_dict = ami_argparse.parse_args(["--flt", "3.2"])
        print(f"arg_dict1 {arg_dict}")
        # this fails
        try:
            arg_dict = ami_argparse.parse_args(["--flt", "3.2", "str"])
        except AmiArgParseException as se:
            print(f"arg parse error {se} line: {se.__traceback__.tb_lineno}")
        except Exception as e:
            print(f" error {e}")

        arg_dict = ami_argparse.parse_args(["--flt", "99.2"])
        print(f"arg_dict2 {arg_dict}")

class TestTemplate(AmiAnyTest):


    def test_id_templates(self):
        """Splits files at Decisions"""
        """requires previous test to have been run"""

        template_values = {
            'DecRes': 'Decision',
            'decision': 1,
            'type': "CMA",
            'session': "3",
        }

        template = "{DecRes}_{decision}_{type}_{session}"
        regex = "(?P<DecRes>Decision|Resolution)\\s(?P<decision>\\d+)/(?P<type>CMA|CMP|CP)\\.(?P<session>\\d+)"
        ss = ["Decision 12/CMP.5", "Decision 10/CP.17", "Decision 2/CMA.2", "Decision 4/CCC.9"]
        matched_templates = Templater.get_matched_templates(regex, ss, template)
        assert matched_templates == ['Decision_12_CMP_5', 'Decision_10_CP_17', 'Decision_2_CMA_2', None]

