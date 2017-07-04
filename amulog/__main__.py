#!/usr/bin/env python
# coding: utf-8

"""
Interface to use some functions about Log DB from CLI.
"""

import sys
import logging
import argparse
from collections import namedtuple
from collections import defaultdict

from . import common
from . import config

_logger = logging.getLogger(__package__)


def get_targets(ns, conf):
    if ns.recur:
        targets = common.recur_dir(ns.files)
    else:
        targets = common.rep_dir(ns.files)
    return targets


def get_targets_opt(ns, conf):
    if len(ns.files) == 0:
        l_path = config.getlist(conf, "general", "src_path")
        if conf.getboolean("general", "src_recur"):
            targets = common.recur_dir(l_path)
        else:
            targets = common.rep_dir(l_path)
    else:
        targets = get_targets(ns, conf)
    return targets


def generate_testdata(ns):
    from . import testlog
    if ns.conf_path is None:
        conf_path = testlog.DEFAULT_CONFIG
    else:
        conf_path = ns.conf_path
    testlog.generate_testdata(conf_path, ns.file, ns.seed)


def db_make(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    targets = get_targets_opt(ns, conf)
    from . import log_db

    timer = common.Timer("db-make", output = _logger)
    timer.start()
    log_db.process_files(conf, targets, True)
    timer.stop()


def db_make_init(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    targets = get_targets_opt(ns, conf)
    from . import log_db

    timer = common.Timer("db-make-init", output = _logger)
    timer.start()
    log_db.process_init_data(conf, targets)
    timer.stop()


def db_add(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    targets = get_targets(ns, conf)
    from . import log_db

    timer = common.Timer("db-add", output = _logger)
    timer.start()
    log_db.process_files(conf, targets, False)
    timer.stop()


def db_update(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    targets = get_targets(ns, conf)
    from . import log_db

    timer = common.Timer("db-update", output = _logger)
    timer.start()
    log_db.process_files(conf, targets, False, diff = True)
    timer.stop()


def db_anonymize(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db
    
    timer = common.Timer("db-anonymize", output = _logger)
    timer.start()
    log_db.anonymize(conf)
    timer.stop()


def reload_area(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db
    log_db.reload_area(conf)


def show_db_info(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    log_db.info(conf)


def show_lt(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    log_db.dump_lt(conf)


def show_ltg(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    log_db.show_lt(conf)


def show_lt_import(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    log_db.show_lt_import(conf)


def show_lt_words(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    d = log_db.agg_words(conf, target = "all")
    print(common.cli_table(sorted(d.items(), key = lambda x: x[1],
                                  reverse = True)))


def show_lt_descriptions(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    d = log_db.agg_words(conf, target = "description")
    print(common.cli_table(sorted(d.items(), key = lambda x: x[1],
                                  reverse = True)))


def show_lt_variables(ns):
    import re

    def repl_var(d):
        reobj = re.compile(r"[0-9]+")
        keys = list(d.keys())
        for k in keys:
            new_k = reobj.sub("\d", k)
            if k == new_k:
                pass
            else:
                d[new_k] += d.pop(k)


    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    d = log_db.agg_words(conf, target = "variable")
    if ns.repld:
        repl_var(d)
    print(common.cli_table(sorted(d.items(), key = lambda x: x[1],
                                  reverse = True)))


def show_host(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    log_db.show_all_host(conf)


def show_log(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db

    d = _parse_condition(ns.conditions)
    ld = log_db.LogData(conf)
    for e in ld.iter_lines(**d):
        print(e.restore__line())


def dump_crf_train(ns):
    conf = config.open_config(ns.conf_path)
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import log_db
    from . import lt_crf

    d = _parse_condition(ns.conditions)
    ld = log_db.LogData(conf)
    iterobj = ld.iter_lines(**d)
    print(lt_crf.make_crf_train(conf, iterobj))


def _parse_condition(condition):
    d = {}
    for arg in ns.conditions:
        if not "=" in arg:
            raise SyntaxError
        key = arg.partition("=")[0]
        if key == "ltid":
            d["ltid"] = int(arg.partition("=")[-1])
        elif key == "gid":
            d["ltgid"] = int(arg.partition("=")[-1])
        elif key == "top_date":
            date_string = arg.partition("=")[-1]
            d["top_dt"] = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        elif key == "end_date":
            date_string = arg.partition("=")[-1]
            d["end_dt"] = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        elif key == "date":
            date_string = arg.partition("=")[-1]
            d["top_dt"] = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            d["end_dt"] = top_dt + datetime.timedelta(days = 1)
        elif key == "host":
            d["host"] = arg.partition("=")[-1]
        elif key == "area":
            d["area"] = arg.partition("=")[-1]
    return d


def measure_crf(ns):
    conf = config.open_config(ns.conf_path,
                              ex_defaults = ["data/measure_crf.conf"])
    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(conf, logger = _logger, lv = lv)
    from . import lt_crf

    ma = lt_crf.MeasureAccuracy(conf)
    if len(ma.results) == 0:
        raise ValueError("No measure results found")
    print(ma.info())
    print()
    print(ma.result())


def measure_crf_multi(ns):
    from . import lt_crf

    def process_measure_crf(conf, conf_name):
        _logger.info("process {0} start".format(conf_name))
        output = "result_" + conf_name
        ma = lt_crf.MeasureAccuracy(conf)
        if len(ma.results) == 0:
            raise ValueError("No measure results found")
        buf = []
        buf.append(ma.info())
        buf.append("")
        buf.append(ma.result())
        with open(output, "w") as f:
            f.write("\n".join(buf))
        print("> {0}".format(output))
        _logger.info("process {0} finished".format(conf_name))


    ex_defaults = ["data/measure_crf.conf"]
    l_conf = [config.open_config(conf_path,
                                 ex_defaults = ["data/measure_crf.conf"])
              for conf_path in ns.confs]
    l_conf_name = ns.confs[:]
    if ns.configset is not None:
        l_conf += config.load_config_group(ns.configset, ex_defaults)
        l_conf_name += config.read_config_group(ns.configset)
    if len(l_conf) == 0:
        sys.exit("No configuration file is given")
    diff_keys = ns.diff
    diff_keys.append(("log_template_crf.model_filename"))
    config.check_all_diff(ns.confs, diff_keys, l_conf)

    lv = logging.DEBUG if ns.debug else logging.INFO
    config.set_common_logging(l_conf[0], logger = _logger, lv = lv)

    import multiprocessing
    timer = common.Timer("measure_crf_multi task", output = _logger)
    timer.start()
    l_process = [multiprocessing.Process(name = args[1],
                                         target = process_measure_crf,
                                         args = args)
                 for args in zip(l_conf, l_conf_name)]
    common.mprocess_queueing(l_process, ns.pal)
    timer.stop()


def conf_defaults(ns):
    config.show_default_config()


def conf_diff(ns):
    files = ns.files[:]
    if ns.configset:
        files += config.read_config_group(ns.configset)
    config.show_config_diff(files)


def conf_minimum(ns):
    config.config_minimum(ns.conf_path)


def conf_shadow(ns):
    cond = {}
    incr = []
    for rule in ns.rules:
        if "=" in rule:
            key, val = rule.split("=")
            cond[key] = val
        else:
            incr.append(rule)
    l_conf_name = config.config_shadow(n = ns.number, cond = cond, incr = incr,
                                       fn = ns.conf_path, output = ns.output,
                                       ignore_overwrite = ns.force)

    if ns.configset is not None:
        config.dump_config_group(ns.configset, l_conf_name)
        print(ns.configset)


# common argument settings
OPT_DEBUG = [["--debug"],
             {"dest": "debug", "action": "store_true",
              "help": "set logging level to debug (default: info)"}]
OPT_CONFIG = [["-c", "--config"],
              {"dest": "conf_path", "metavar": "CONFIG", "action": "store",
               #"default": config.DEFAULT_CONFIG,
               "default": None,
               "help": "configuration file path for amulog"}]
OPT_CONFIG_SET = [["-s", "--configset"],
                  {"dest": "configset", "metavar": "CONFIG_SET",
                   "default": None,
                   "help": "use config group definition file"}]
OPT_RECUR = [["-r", "--recur"],
             {"dest": "recur", "action": "store_true",
              "help": "recursively search files to process"}]
OPT_TERM = [["-t", "--term"],
            {"dest": "dt_range",
             "metavar": "DATE1 DATE2", "nargs": 2,
             "help": ("datetime range, start and end in %Y-%M-%d style."
                      "(optional; defaultly use all data in database)")}]
ARG_FILE = [["file"],
             {"metavar": "PATH", "action": "store",
              "help": "filepath to output"}]
ARG_FILES = [["files"],
             {"metavar": "PATH", "nargs": "+",
              "help": "files or directories as input"}]
ARG_FILES_OPT = [["files"],
                 {"metavar": "PATH", "nargs": "*",
                  "help": ("files or directories as input "
                           "(optional; defaultly read from config")}]
ARG_DBSEARCH = [["conditions"],
                {"metavar": "CONDITION", "nargs": "+",
                 "help": ("Conditions to search log messages. "
                          "Example: show-log gid=24 date=2012-10-10 ..., "
                          "Keys: ltid, gid, date, top_date, end_date, "
                          "host, area")}]


# argument settings for each modes
# description, List[args, kwargs], func
# defined after functions because these settings use functions
DICT_ARGSET = {
    "testdata": ["Generate test log data.",
                 [OPT_DEBUG, ARG_FILE,
                  [["-c", "--config"],
                   {"dest": "conf_path", "metavar": "CONFIG",
                    "action": "store", "default": None,
                    "help": ("configuration file path for testlog "
                             "(different from that for amulog)")}],
                  [["-s", "--seed"],
                   {"dest": "seed", "metavar": "INT", "action": "store",
                    "default": 0,
                    "help": "seed value to generate random values"}]],
                 generate_testdata],
    "db-make": [("Initialize database and add log data. "
                 "This fuction works incrementaly."),
                [OPT_CONFIG, OPT_DEBUG, OPT_RECUR, ARG_FILES_OPT],
                db_make],
    "db-make-init": [("Initialize database and add log data "
                      "for given dataset. "
                      "This function does not consider "
                      "to add other data afterwards."),
                     [OPT_CONFIG, OPT_DEBUG, OPT_RECUR,
                      ARG_FILES_OPT],
                     db_make_init],
    "db-add": ["Add log data to existing database.",
               [OPT_CONFIG, OPT_DEBUG, OPT_RECUR, ARG_FILES],
               db_add],
    "db-update": [("Add newer log data (seeing timestamp range) "
                   "to existing database."),
                  [OPT_CONFIG, OPT_DEBUG, OPT_RECUR, ARG_FILES],
                  db_update],
    "db-anonymize": [("Remove variables in log messages. "
                      "(Not anonymize hostnames; to be added)"),
                     [OPT_CONFIG, OPT_DEBUG],
                     db_anonymize],
    "db-reload-area": ["Reload area definition file from config.",
                       [OPT_CONFIG, OPT_DEBUG],
                       reload_area],
    "show-db-info": ["Show abstruction of database status.",
                     [OPT_CONFIG, OPT_DEBUG, OPT_TERM],
                     show_db_info],
    "show-lt": ["Show all log templates in database.",
                [OPT_CONFIG, OPT_DEBUG],
                show_lt],
    "show-ltg": ["Show all log template groups and their members in database.",
                 [OPT_CONFIG, OPT_DEBUG],
                 show_ltg],
    "show-lt-import": ["Output log template definitions in lt_import format.",
                       [OPT_CONFIG, OPT_DEBUG],
                       show_lt_import],
    "show-host": ["Show all hostnames in database.",
                  [OPT_CONFIG, OPT_DEBUG],
                  show_host],
    "show-lt-word": ["Show words and their counts in all messages",
                     [OPT_CONFIG, OPT_DEBUG],
                     show_lt_words],
    "show-lt-description": ["Show description words and their counts",
                            [OPT_CONFIG, OPT_DEBUG],
                            show_lt_descriptions],
    "show-lt-variable": ["Show variable words and their counts",
                         [OPT_CONFIG, OPT_DEBUG,
                          [["-d", "--digit"],
                           {"dest": "repld", "action": "store_true",
                            "help": "replace digit to \d"}]],
                         show_lt_variables],
    "show-log": ["Show log messages that satisfy given conditions in args.",
                 [OPT_CONFIG, OPT_DEBUG, ARG_DBSEARCH],
                 show_log],
    "dump-crf-train": ["Output CRF training file for given conditions.",
                       [OPT_CONFIG, OPT_DEBUG, ARG_DBSEARCH],
                       dump_crf_train],
    "measure-crf": ["Measure accuracy of CRF-based log template estimation.",
                    [OPT_DEBUG,
                     [["-c", "--config"],
                      {"dest": "conf_path", "metavar": "CONFIG",
                       "action": "store", "default": None,
                       "help": "Extended config file for measure-lt"}],],
                    measure_crf],
    "measure-crf-multi": ["Multiprocessing of measure-crf.",
                          [OPT_DEBUG, OPT_CONFIG_SET,
                           [["-p", "--pal"],
                            {"dest": "pal", "action": "store",
                             "type": int, "default": 1,
                             "help": "number of processes"}],
                           [["-d", "--diff"],
                            {"dest": "diff", "action": "append",
                             "default": [],
                             "help": ("check configs that given option values "
                                      "are all different. This option can "
                                      "be specified multiple times. "
                                      "Example: -d general.import -d ...")}],
                           [["confs"],
                            {"metavar": "CONFIG", "nargs": "*",
                             "help": "configuration files"}]],
                          measure_crf_multi],
    "conf-defaults": ["Show default configurations.",
                     [],
                     conf_defaults],
    "conf-diff": ["Show differences of 2 configuration files.",
                  [OPT_CONFIG_SET,
                   [["files"],
                    {"metavar": "FILENAME", "nargs": "*",
                     "help": "configuration file"}]],
                   conf_diff],
    "conf-minimum": ["Remove default options and comments.",
                     [OPT_CONFIG],
                     conf_minimum],
    "conf-shadow": ["Copy configuration files.",
                    [OPT_CONFIG,
                     [["-f", "--force"],
                      {"dest": "force", "action": "store_true",
                       "help": "Ignore overwrite of output file"}],
                     [["-n", "--number"],
                      {"dest": "number", "metavar": "INT",
                       "action": "store", "type": int, "default": 1,
                       "help": "number of files to generate"}],
                     [["-o", "--output"],
                      {"dest": "output", "metavar": "FILENAME",
                       "action": "store", "type": str, "default": None,
                       "help": "basic output filename"}],
                     [["-s", "--configset"],
                      {"dest": "configset", "metavar": "CONFIG_SET",
                       "default": None,
                       "help": ("define config group ",
                                "and dump it in given filename")}],
                     [["rules"],
                      {"metavar": "RULES", "nargs": "*",
                       "help": ("Rules to replace options. You can indicate "
                                "option, or option and its value with =. "
                                "You can use both of them together. "
                                "For example: \"general.import=hoge.conf "
                                "general.logging\"")}]],
                    conf_shadow],
}

USAGE_COMMANDS = "\n".join(["  {0}: {1}".format(key, val[0])
                            for key, val in DICT_ARGSET.items()])
USAGE = ("usage: {0} MODE [options and arguments] ...\n\n"
         "mode:\n".format(
        sys.argv[0])) + USAGE_COMMANDS


if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit(USAGE)
    mode = sys.argv[1]
    if mode in ("-h", "--help"):
        sys.exit(USAGE)
    commandline = sys.argv[2:]

    desc, l_argset, func = DICT_ARGSET[mode]
    ap = argparse.ArgumentParser(prog = " ".join(sys.argv[0:2]),
                                 description = desc)
    for args, kwargs in l_argset:
        ap.add_argument(*args, **kwargs)
    ns = ap.parse_args(commandline)
    func(ns)

