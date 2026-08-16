# DTM ULTIMATE PINE ↔ PYTHON PARITY REPAIR REPORT

Generated: 2026-08-15T22:09:01.728116

## RESULT

- Source Python files analyzed: **515**
- Initial parity score: **9**
- Final parity score: **9**
- Changes applied: **0**
- Rollbacks: **0**

## ROOT-CAUSE CATEGORIES

- **CANDLE**: 568
- **OHLC**: 464
- **TIMESTAMP**: 369
- **PIVOT_RIGHT_SHIFT**: 9
- **FIB**: 4
- **RMA**: 4
- **EMA**: 4
- **DIVERGENCE**: 2
- **RSI**: 2
- **MACD**: 2
- **ATR**: 2
- **PANDAS_SHIFT**: 1

## FUNCTIONS / CLASSES / PARAMETERS

### `bot.py`
**Classes:** HealthHandler, PrivateExchange, PublicData
**Functions:** __init__, _handle_shutdown, _request, _round_price, _sign, create_order, do_GET, fetch_balance, fetch_ohlcv, log_message, loop, run_health_server, send_telegram, test_connection
**Parameters:** API_KEY, API_SECRET, BASE_URL, HISTORY_BARS, LEVERAGE_MAP, PRICE_PRECISION, STOP_EVENT, SYMBOLS, TARGET_RISK, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TICK_SIZES

### `dtm_bot.py`
**Classes:** TrueTradePrivateExchange, TrueTradePublicData
**Functions:** __init__, _ignore_sigterm, _request, _round_price, _sign, create_order, fetch_balance, fetch_ohlcv, fetch_open_positions, format_iran_time, health, health_check, run_trading_loop, send_telegram_message, test_connection
**Parameters:** API_KEY, API_SECRET, BASE_URL, BIG_CANDLE_AVG_LEN, BIG_CANDLE_MULTIPLIER, ENABLE_HIDDEN, ENABLE_MTF, FIB_TOLERANCE_PCT, FIB_TREND_SEARCH_BARS, FIB_USE_618, FIB_USE_786, HISTORY_BARS, LEFT_BARS, LEVERAGE_MAP, MACD_FAST, MACD_SIG, MACD_SLOW, MAX_OPPOSITE_SHADOW_PCT, MIN_CANDLE_ATR_RATIO, MIN_CONFIRMATIONS, MTF_TIMEFRAME, PRICE_PRECISION, RIGHT_BARS, RSI_LEN, SHADOW_TO_BODY_RATIO, SYMBOLS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TICK_SIZES, TIMEFRAME, TREND_LOOKBACK, TREND_SLOPE_MIN_PCT

### `health_server.py`
**Classes:** HealthHandler
**Functions:** do_GET, log_message
**Parameters:** HOST, PORT

### `parity_env/lib/python3.14/site-packages/_pytest/__init__.py`

### `parity_env/lib/python3.14/site-packages/_pytest/_argcomplete.py`
**Classes:** FastFilesCompleter
**Functions:** __call__, __init__, try_argcomplete

### `parity_env/lib/python3.14/site-packages/_pytest/_code/__init__.py`

### `parity_env/lib/python3.14/site-packages/_pytest/_code/code.py`
**Classes:** Code, ExceptionChainRepr, ExceptionInfo, ExceptionInfoFormatter, ExceptionRepr, Frame, ReprEntry, ReprEntryNative, ReprExceptionInfo, ReprFileLocation, ReprFuncArgs, ReprLocals, ReprTraceback, ReprTracebackNative, TerminalRepr, Traceback, TracebackEntry
**Functions:** __eq__, __getitem__, __init__, __post_init__, __repr__, __str__, _byte_offset_to_character_offset, _get_single_subexc, _getentrysource, _getindent, _getreprcrash, _group_contains, _makepath, _truncate_recursive_traceback, _write_entry_lines, addsection, code, colno, cut, end_colno, end_lineno_relative, errisinstance, eval, exconly, f, f_globals, f_locals, fill_unfilled, filter, filter_excinfo_traceback, filter_traceback, firstlineno, for_later, frame, from_current, from_exc_info, from_exception, from_function, fullsource, get_exconly, get_highlight_arrows_for_line, get_python_framesummary, get_source, getargs, getfirstlinesource, getfslineno, getrepr, getsource, group_contains, ishidden, lineno, locals, match, name, path, recursionindex, relline, repr, repr_args, repr_excinfo, repr_locals, repr_traceback, repr_traceback_entry, source, statement, stringify_exception, tb, toterminal, traceback, type, typename, value, with_repr_style
**Parameters:** E, EXCEPTION_OR_MORE, _PLUGGY_DIR, _PYTEST_DIR

### `parity_env/lib/python3.14/site-packages/_pytest/_code/source.py`
**Classes:** Source
**Functions:** __eq__, __getitem__, __init__, __iter__, __len__, __str__, deindent, findsource, get_statement_startend2, getrawcode, getstatement, getstatementrange, getstatementrange_ast, indent, strip

### `parity_env/lib/python3.14/site-packages/_pytest/_io/__init__.py`

### `parity_env/lib/python3.14/site-packages/_pytest/_io/pprint.py`
**Classes:** PrettyPrinter, _safe_key
**Functions:** __init__, __lt__, _format, _format_dict_items, _format_items, _format_namespace_items, _pprint_bytearray, _pprint_bytes, _pprint_chain_map, _pprint_counter, _pprint_dataclass, _pprint_default_dict, _pprint_deque, _pprint_dict, _pprint_list, _pprint_mappingproxy, _pprint_ordered_dict, _pprint_set, _pprint_simplenamespace, _pprint_str, _pprint_tuple, _pprint_user_dict, _pprint_user_list, _pprint_user_string, _recursion, _repr, _safe_repr, _safe_tuple, _wrap_bytes_repr, pformat

### `parity_env/lib/python3.14/site-packages/_pytest/_io/saferepr.py`
**Classes:** SafeRepr
**Functions:** __init__, _ellipsize, _format_repr_exception, _try_repr_or_str, repr, repr_dict, repr_instance, safeformat, saferepr, saferepr_unlimited
**Parameters:** DEFAULT_REPR_MAX_SIZE

### `parity_env/lib/python3.14/site-packages/_pytest/_io/terminalwriter.py`
**Classes:** TerminalWriter
**Functions:** __init__, _get_pygments_formatter, _get_pygments_lexer, _highlight, _write_source, flush, fullwidth, get_terminal_width, line, markup, sep, should_do_markup, width_of_current_line, write, write_raw
**Parameters:** N

### `parity_env/lib/python3.14/site-packages/_pytest/_io/wcwidth.py`
**Functions:** wcswidth, wcwidth

### `parity_env/lib/python3.14/site-packages/_pytest/_py/__init__.py`

### `parity_env/lib/python3.14/site-packages/_pytest/_py/error.py`
**Classes:** Error, ErrorMaker
**Functions:** __getattr__, __repr__, __str__, _geterrnoclass, checked_call
**Parameters:** P, R

### `parity_env/lib/python3.14/site-packages/_pytest/_py/path.py`
**Classes:** Checkers, FNMatcher, ImportMismatchError, LocalPath, NeverRaised, Stat, Visitor
**Functions:** __add__, __call__, __div__, __eq__, __fspath__, __getattr__, __gt__, __hash__, __init__, __lt__, __ne__, __repr__, __str__, _ensuredirs, _ensuresyspath, _evaluate, _fastjoin, _getbyspec, _gethomedir, _sortlist, _stat, as_cwd, atexit_remove_lockfile, atime, basename, basestarts, bestrelpath, chdir, check, chmod, chown, common, computehash, copy, copychunked, copymode, copystat, create_lockfile, dir, dirname, dirpath, dotfile, dump, endswith, ensure, ensure_dir, exists, ext, file, fnmatch, gen, get_mtime, get_temproot, getgroupid, getuserid, group, is_garbage, isdir, isfile, isimportable, islink, join, link, listdir, load, lstat, make_numbered_dir, map_as_list, mkdir, mkdtemp, mklinkto, mksymlinkto, move, mtime, new, open, owner, parse_num, parts, purebasename, pyimport, pypkgpath, read, read_binary, read_text, readlines, readlink, realpath, rec, relto, remove, rename, samefile, setmtime, size, stat, sysexec, sysfind, try_remove_lockfile, visit, write, write_binary, write_text

### `parity_env/lib/python3.14/site-packages/_pytest/_version.py`

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/__init__.py`
**Classes:** AssertionState, DummyRewriteHook, RewriteHook
**Functions:** __init__, call_assertion_pass_hook, callbinrepr, install_importhook, mark_rewrite, pytest_addoption, pytest_assertrepr_compare, pytest_collection, pytest_configure, pytest_runtest_protocol, pytest_sessionfinish, register_assert_rewrite, undo

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_any.py`
**Functions:** _compare_eq_any, _compare_eq_cls

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_mapping.py`
**Functions:** _compare_eq_mapping

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_sequence.py`
**Functions:** _compare_eq_iterable, _compare_eq_sequence

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_set.py`
**Functions:** _both_sets_are_equal, _compare_eq_set, _compare_gt_set, _compare_gte_set, _compare_lt_set, _compare_lte_set, _set_one_sided_diff

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_guards.py`
**Functions:** has_default_eq, isattrs, isiterable, ismapping, isnamedtuple, issequence, isset, istext

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/_typing.py`
**Classes:** _HighlightFunc
**Functions:** __call__

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/compare_text.py`
**Functions:** _compare_eq_text, _diff_text, _diff_text_block, _format_text_block_lines, _notin_text

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/highlight.py`
**Functions:** dummy_highlighter

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/rewrite.py`
**Classes:** AssertionRewriter, AssertionRewritingHook, Sentinel
**Functions:** __init__, _call_assertion_pass, _call_reprcompare, _check_if_assertion_pass_impl, _early_rewrite_bailout, _format_assertmsg, _format_boolop, _get_assertion_exprs, _get_maxsize_for_saferepr, _is_marked_for_rewrite, _read_pyc, _rewrite_test, _saferepr, _should_repr_global_name, _should_rewrite, _warn_already_imported, _write_and_reset, _write_pyc, _write_pyc_fp, assign, builtin, create_module, display, exec_module, explanation_param, find_spec, generic_visit, get_cache_dir, get_data, get_resource_reader, helper, is_rewrite_disabled, mark_rewrite, pop_format_context, push_format_context, rewrite_asserts, run, set_session, traverse_node, try_makedirs, variable, visit_Assert, visit_Attribute, visit_BinOp, visit_BoolOp, visit_Call, visit_Compare, visit_Name, visit_NamedExpr, visit_Starred, visit_UnaryOp
**Parameters:** BINOP_MAP, PYC_EXT, PYC_TAIL, PYTEST_TAG, UNARY_MAP, _SCOPE_END_MARKER

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/truncate.py`
**Functions:** _get_truncation_parameters, _truncate_by_char_count, _truncate_explanation, truncate_if_required
**Parameters:** DEFAULT_MAX_CHARS, DEFAULT_MAX_LINES, USAGE_MSG

### `parity_env/lib/python3.14/site-packages/_pytest/assertion/util.py`
**Functions:** _format_lines, _split_explanation, assertrepr_compare, format_explanation, get_assertion_text_diff_style, validate_assertion_text_diff_style
**Parameters:** ASSERTION_TEXT_DIFF_STYLE_CHOICES, ASSERTION_TEXT_DIFF_STYLE_INI

### `parity_env/lib/python3.14/site-packages/_pytest/cacheprovider.py`
**Classes:** Cache, LFPlugin, LFPluginCollSkipfiles, LFPluginCollWrapper, NFPlugin
**Functions:** __init__, _ensure_cache_dir_and_supporting_files, _get_increasing_order, _getvaluepath, _make_cachedir, _mkdir, cache, cache_dir_from_config, cacheshow, clear_cache, for_config, get, get_last_failed_paths, mkdir, pytest_addoption, pytest_cmdline_main, pytest_collection_modifyitems, pytest_collectreport, pytest_configure, pytest_make_collect_report, pytest_report_collectionfinish, pytest_report_header, pytest_runtest_logreport, pytest_sessionfinish, set, sort_key, warn
**Parameters:** _CACHE_PREFIX_DIRS, _CACHE_PREFIX_VALUES

### `parity_env/lib/python3.14/site-packages/_pytest/capture.py`
**Classes:** CaptureBase, CaptureFixture, CaptureIO, CaptureManager, CaptureResult, DontReadFromInput, EncodedFile, FDCapture, FDCaptureBase, FDCaptureBinary, MultiCapture, NoCapture, SysCapture, SysCaptureBase, SysCaptureBinary, TeeCaptureIO
**Functions:** __enter__, __exit__, __init__, __iter__, __next__, __repr__, _assert_state, _colorama_workaround, _get_multicapture, _is_started, _readline_workaround, _reopen_stdio, _resume, _start, _suspend, _windowsconsoleio_workaround, activate_fixture, buffer, capfd, capfdbinary, capsys, capsysbinary, capteesys, close, deactivate_fixture, disabled, done, encoding, fileno, flush, getvalue, global_and_fixture_disabled, is_capturing, is_globally_capturing, is_started, isatty, item_capture, mode, name, pop_outerr_to_orig, pytest_addoption, pytest_internalerror, pytest_keyboard_interrupt, pytest_load_initial_conftests, pytest_make_collect_report, pytest_runtest_call, pytest_runtest_setup, pytest_runtest_teardown, read, read_global_capture, readable, readlines, readouterr, repr, resume, resume_capturing, resume_fixture, resume_global_capture, seek, seekable, set_fixture, snap, start, start_capturing, start_global_capturing, stop_capturing, stop_global_capturing, suspend, suspend_capturing, suspend_fixture, suspend_global_capture, tell, truncate, unset_fixture, writable, write, writelines, writeorg
**Parameters:** EMPTY_BUFFER

### `parity_env/lib/python3.14/site-packages/_pytest/compat.py`
**Classes:** CallableBool, NotSetType
**Functions:** __bool__, __call__, __init__, ascii_escaped, assert_never, decorator, deprecated, get_default_arg_names, get_real_func, get_user_id, getfuncargnames, getimfunc, getlocation, is_async_function, iscoroutinefunction, legacy_path, num_mock_patch_args, running_on_ci, safe_getattr, safe_isclass, signature
**Parameters:** ERROR, LEGACY_PATH

### `parity_env/lib/python3.14/site-packages/_pytest/config/__init__.py`
**Classes:** ArgsSource, Config, ConftestImportFailure, ExitCode, InvocationParams, PytestPluginManager, _DeprecatedInicfgProxy, cmdline
**Functions:** __delitem__, __getitem__, __init__, __iter__, __len__, __setitem__, __str__, _add_verbosity_ini, _assertion_supported, _check_non_top_pytest_plugins, _checkversion, _configure_python_path, _consider_importhook, _console_main, _decide_args, _do_configure, _ensure_unconfigure, _get_directory, _get_legacy_hook_marks, _get_plugin_specs_as_list, _get_prog_name, _get_unknown_ini_keys, _getconftest_pathlist, _getconftestmodules, _getini, _getini_ini, _getini_toml, _getini_unknown_type, _import_plugin_specs, _importconftest, _is_in_confcutdir, _iter_rewritable_modules, _loadconftestmodules, _main, _mark_plugins_for_rewrite, _prepareconfig, _processopt, _resolve_warning_category, _rget_with_confmod, _set_initial_conftests, _strtobool, _unconfigure_python_path, _validate_args, _validate_config_options, _validate_plugins, _verbosity_ini_name, _warn_about_missing_assertion, _warn_about_skipped_plugins, _warn_or_fail_if_strict, add_cleanup, addinivalue_line, apply_warning_filters, consider_conftest, consider_env, consider_module, consider_pluginarg, consider_preparse, console_main, create_terminal_writer, cwd_relative_nodeid, directory_arg, filename_arg, filter_traceback_for_conftest_import_failure, fromdictargs, get_config, get_plugin_manager, get_terminal_writer, get_verbosity, getini, getoption, getplugin, getvalue, getvalueorskip, hasplugin, import_plugin, inicfg, inipath, issue_config_time_warning, main, notify_exception, parse, parse_hookimpl_opts, parse_hookspec_opts, parse_warning_filter, print_conftest_import_error, print_usage_error, pytest_cmdline_parse, pytest_collection, pytest_configure, pytest_load_initial_conftests, register, rootpath
**Parameters:** ARGS, INCOVATION_DIR, INTERNAL_ERROR, INTERRUPTED, INVOCATION_DIR, MAX_WARNINGS_ERROR, NO_TESTS_COLLECTED, OK, TESTPATHS, TESTS_FAILED, USAGE_ERROR

### `parity_env/lib/python3.14/site-packages/_pytest/config/argparsing.py`
**Classes:** Argument, DropShorterLongHelpFormatter, OptionGroup, OverrideIniAction, Parser, PytestArgumentParser
**Functions:** __call__, __init__, __repr__, _addoption, _addoption_inner, _format_action_invocation, _split_lines, addini, addoption, attrs, default, dest, error, get_ini_default_for_type, getgroup, names, parse, parse_known_and_unknown_args, parse_known_args, processoption, prog, type
**Parameters:** FILE_OR_DIR

### `parity_env/lib/python3.14/site-packages/_pytest/config/exceptions.py`
**Classes:** PrintHelp, UsageError

### `parity_env/lib/python3.14/site-packages/_pytest/config/findpaths.py`
**Classes:** ConfigValue
**Functions:** _parse_ini_config, determine_setup, get_common_ancestor, get_dir_from_path, get_dirs_from_args, get_file_part_from_node_id, is_fs_root, is_option, load_config_dict_from_file, locate_config, make_scalar, parse_override_ini
**Parameters:** CFG_PYTEST_SECTION

### `parity_env/lib/python3.14/site-packages/_pytest/debugging.py`
**Classes:** PdbInvoke, PdbTrace, PytestPdbWrapper, pytestPDB
**Functions:** _enter_pdb, _get_pdb_wrapper_class, _import_pdb_cls, _init_pdb, _is_capturing, _postmortem_exc_or_tb, _validate_usepdb_cls, do_continue, do_debug, do_quit, fin, get_stack, maybe_wrap_pytest_function_for_tracing, post_mortem, pytest_addoption, pytest_configure, pytest_exception_interact, pytest_internalerror, pytest_pyfunc_call, set_trace, setup, wrap_pytest_function_for_tracing, wrapper

### `parity_env/lib/python3.14/site-packages/_pytest/deprecated.py`
**Functions:** check_ispytest
**Parameters:** CLASS_FIXTURE_INSTANCE_METHOD, CONFIG_INICFG, CONSOLE_MAIN, DEPRECATED_EXTERNAL_PLUGINS, FIXTUREDEF_HAS_LOCATION_DEPRECATED, FIXTURE_BASEID_DEPRECATED, FIXTURE_GETFIXTUREVALUE_DURING_TEARDOWN, FIXTURE_NODEID_DEPRECATED, HOOK_LEGACY_MARKING, MONKEYPATCH_LEGACY_NAMESPACE_PACKAGES, PARAMETRIZE_NON_COLLECTION_ITERABLE, PARSEFACTORIES_NODEID_DEPRECATED, PASTEBIN, PRIVATE, YIELD_FIXTURE

### `parity_env/lib/python3.14/site-packages/_pytest/doctest.py`
**Classes:** DoctestItem, DoctestModule, DoctestTextfile, LiteralsOutputChecker, MockAwareDocTestFinder, MultipleDoctestFailures, PytestDoctestRunner, ReprFailDoctest
**Functions:** __init__, _check_all_skipped, _disable_output_capturing_for_darwin, _find_lineno, _from_module, _get_allow_bytes_flag, _get_allow_unicode_flag, _get_checker, _get_continue_on_failure, _get_flag_lookup, _get_number_flag, _get_report_choice, _get_runner, _init_checker_class, _init_runner_class, _initrequest, _is_doctest, _is_main_py, _is_mocked, _is_setup_py, _mock_aware_unwrap, _patch_unwrap_mock_aware, _remove_unwanted_precision, check_output, collect, doctest_namespace, from_parent, get_optionflags, pytest_addoption, pytest_collect_file, pytest_unconfigure, remove_prefixes, report_failure, report_unexpected_exception, reportinfo, repr_failure, runtest, setup, toterminal
**Parameters:** CHECKER_CLASS, DOCTEST_REPORT_CHOICES, DOCTEST_REPORT_CHOICE_CDIFF, DOCTEST_REPORT_CHOICE_NDIFF, DOCTEST_REPORT_CHOICE_NONE, DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE, DOCTEST_REPORT_CHOICE_UDIFF, RUNNER_CLASS

### `parity_env/lib/python3.14/site-packages/_pytest/faulthandler.py`
**Functions:** get_exit_on_timeout_config_value, get_stderr_fileno, get_timeout_config_value, pytest_addoption, pytest_configure, pytest_enter_pdb, pytest_exception_interact, pytest_runtest_protocol, pytest_unconfigure

### `parity_env/lib/python3.14/site-packages/_pytest/fixtures.py`
**Classes:** FixtureDef, FixtureFunctionDefinition, FixtureFunctionMarker, FixtureLookupError, FixtureLookupErrorRepr, FixtureManager, FixtureRequest, FuncFixtureInfo, ParamArgKey, RequestFixtureDef, SubRequest, TopRequest
**Functions:** __call__, __get__, __init__, __post_init__, __repr__, _check_fixturedef_without_param, _check_scope, _eval_scope_callable, _fillfixtures, _fixturemanager, _flush_pending_conftests_to_session, _format_fixturedef_line, _get_active_fixturedef, _get_direct_parametrize_args, _get_fixtures_per_test, _get_fixturestack, _get_wrapped_function, _getautousenames, _getusefixturesnames, _iter_chain, _matchfactories, _pretty_fixture_path, _raise_teardown_lookup_error, _register_fixture, _resolve_args_directness, _scope, _show_fixtures_per_test, _showfixtures_main, _teardown_yield_fixture, addfinalizer, applymarker, cache_key, call_fixture_func, cls, config, deduplicate_names, execute, finish, fixture, fixturenames, formatrepr, function, get_best_relpath, get_param_argkeys, get_parametrize_mark_argnames, get_scope_node, get_scope_package, getfixtureclosure, getfixturedefs, getfixtureinfo, getfixturemarker, getfixturevalue, has_location, instance, is_visibility_more_specific, keywords, module, node, parsefactories, path, process_argname, prune_dependency_tree, pytest_addoption, pytest_cmdline_main, pytest_collection_finish, pytest_collection_modifyitems, pytest_fixture_setup, pytest_generate_tests, pytest_make_collect_report, pytest_plugin_registered, pytest_sessionstart, pytestconfig, raiseerror, register_fixture, reorder_items, reorder_items_atscope, resolve_fixture_function, scope, session, show_fixtures_per_test, showfixtures, sort_by_scope, toterminal, traverse_fixture_closure, write_docstring, write_fixture, write_item, yield_fixture
**Parameters:** _PYTEST_DIR, _V

### `parity_env/lib/python3.14/site-packages/_pytest/freeze_support.py`
**Functions:** _iter_all_modules, freeze_includes

### `parity_env/lib/python3.14/site-packages/_pytest/helpconfig.py`
**Classes:** HelpAction
**Functions:** __call__, __init__, getpluginversioninfo, pytest_addoption, pytest_cmdline_main, pytest_cmdline_parse, pytest_report_header, show_version_verbose, showhelp, unset_tracing

### `parity_env/lib/python3.14/site-packages/_pytest/hookspec.py`
**Functions:** pytest_addhooks, pytest_addoption, pytest_assertion_pass, pytest_assertrepr_compare, pytest_cmdline_main, pytest_cmdline_parse, pytest_collect_directory, pytest_collect_file, pytest_collection, pytest_collection_finish, pytest_collection_modifyitems, pytest_collectreport, pytest_collectstart, pytest_configure, pytest_deselected, pytest_enter_pdb, pytest_exception_interact, pytest_fixture_post_finalizer, pytest_fixture_setup, pytest_generate_tests, pytest_ignore_collect, pytest_internalerror, pytest_itemcollected, pytest_keyboard_interrupt, pytest_leave_pdb, pytest_load_initial_conftests, pytest_make_collect_report, pytest_make_parametrize_id, pytest_markeval_namespace, pytest_plugin_registered, pytest_pycollect_makeitem, pytest_pycollect_makemodule, pytest_pyfunc_call, pytest_report_collectionfinish, pytest_report_from_serializable, pytest_report_header, pytest_report_teststatus, pytest_report_to_serializable, pytest_runtest_call, pytest_runtest_logfinish, pytest_runtest_logreport, pytest_runtest_logstart, pytest_runtest_makereport, pytest_runtest_protocol, pytest_runtest_setup, pytest_runtest_teardown, pytest_runtestloop, pytest_sessionfinish, pytest_sessionstart, pytest_terminal_summary, pytest_unconfigure, pytest_warning_recorded

### `parity_env/lib/python3.14/site-packages/_pytest/junitxml.py`
**Classes:** LogXML, _NodeReporter
**Functions:** __init__, _add_simple, _check_record_param_type, _get_global_properties_node, _opentestcase, _prepare_content, _warn_incompatibility_with_xunit2, _write_content, add_attr_noop, add_attribute, add_global_property, add_property, add_stats, append, append_collect_error, append_collect_skipped, append_error, append_failure, append_pass, append_property, append_skipped, bin_xml_escape, finalize, make_properties_node, mangle_test_address, merge_family, node_reporter, pytest_addoption, pytest_collectreport, pytest_configure, pytest_internalerror, pytest_runtest_logreport, pytest_sessionfinish, pytest_sessionstart, pytest_terminal_summary, pytest_unconfigure, record_func, record_property, record_testreport, record_testsuite_property, record_xml_attribute, repl, to_xml, update_testcase_duration, write_captured_output

### `parity_env/lib/python3.14/site-packages/_pytest/legacypath.py`
**Classes:** LegacyTestdirPlugin, LegacyTmpdirPlugin, TempdirFactory, Testdir
**Functions:** Cache_makedir, Config__getini_unknown_type, Config_inifile, Config_invocation_dir, Config_rootdir, FixtureRequest_fspath, Node_fspath, Node_fspath_set, Session_startdir, TerminalReporter_startdir, __init__, __repr__, __str__, chdir, collect_by_name, copy_example, finalize, genitems, getbasetemp, getinicfg, getitem, getitems, getmodulecol, getnode, getpathnode, inline_genitems, inline_run, inline_runsource, make_hook_recorder, makeconftest, makefile, makeini, makepyfile, makepyprojecttoml, maketxtfile, mkdir, mkpydir, mktemp, monkeypatch, parseconfig, parseconfigure, plugins, popen, pytest_configure, pytest_load_initial_conftests, pytest_plugin_registered, request, run, runitem, runpytest, runpytest_inprocess, runpytest_subprocess, runpython, runpython_c, spawn, spawn_pytest, syspathinsert, test_tmproot, testdir, tmpdir, tmpdir_factory

### `parity_env/lib/python3.14/site-packages/_pytest/logging.py`
**Classes:** ColoredLevelFormatter, DatetimeFormatter, LogCaptureFixture, LogCaptureHandler, LoggingPlugin, PercentStyleMultiline, _FileHandler, _LiveLoggingNullHandler, _LiveLoggingStreamHandler, catching_logs
**Functions:** __enter__, __exit__, __init__, _create_formatter, _disable_loggers, _finalize, _force_enable_logging, _get_auto_indent, _log_cli_enabled, _remove_ansi_escape_sequences, _runtest_for, add_color_level, add_option_ini, at_level, caplog, clear, emit, filtering, format, formatTime, get_log_level_for_setting, get_option_ini, get_records, handleError, handler, messages, pytest_addoption, pytest_collection, pytest_configure, pytest_runtest_call, pytest_runtest_logfinish, pytest_runtest_logreport, pytest_runtest_logstart, pytest_runtest_setup, pytest_runtest_teardown, pytest_runtestloop, pytest_sessionfinish, pytest_sessionstart, pytest_unconfigure, record_tuples, records, reset, set_level, set_log_path, set_when, text
**Parameters:** DEFAULT_LOG_DATE_FORMAT, DEFAULT_LOG_FORMAT, LEVELNAME_FMT_REGEX, _ANSI_ESCAPE_SEQ

### `parity_env/lib/python3.14/site-packages/_pytest/main.py`
**Classes:** CollectionArgument, Dir, FSHookProxy, Failed, Interrupted, Session, _bestrelpath_cache
**Functions:** __getattr__, __init__, __missing__, __repr__, _collect_one_node, _collect_path, _in_venv, _main, _node_location_to_relpath, collect, from_config, from_parent, genitems, gethookproxy, is_ancestor, is_collection_argument_subsumed_by, isinitpath, normalize_collection_arguments, perform_collect, pytest_addoption, pytest_cmdline_main, pytest_collect_directory, pytest_collection, pytest_collection_modifyitems, pytest_collectstart, pytest_ignore_collect, pytest_runtest_logreport, pytest_runtestloop, resolve_collection_argument, search_pypath, shouldfail, shouldstop, startpath, validate_basetemp, wrap_session

### `parity_env/lib/python3.14/site-packages/_pytest/mark/__init__.py`
**Classes:** KeywordMatcher, MarkMatcher
**Functions:** __call__, _parse_expression, deselect_by_keyword, deselect_by_mark, from_item, from_markers, param, pytest_addoption, pytest_cmdline_main, pytest_collection_modifyitems, pytest_configure, pytest_unconfigure

### `parity_env/lib/python3.14/site-packages/_pytest/mark/expression.py`
**Classes:** Expression, ExpressionMatcher, MatcherAdapter, MatcherNameAdapter, Scanner, Token, TokenType
**Functions:** __bool__, __call__, __getitem__, __init__, __iter__, __len__, accept, all_kwargs, and_expr, compile, evaluate, expr, expression, lex, not_expr, reject, single_kwarg
**Parameters:** AND, BUILTIN_MATCHERS, COMMA, EOF, EQUAL, IDENT, IDENT_PREFIX, LPAREN, NOT, OR, RPAREN, STRING

### `parity_env/lib/python3.14/site-packages/_pytest/mark/structures.py`
**Classes:** Mark, MarkDecorator, MarkGenerator, NodeKeywords, ParameterSet, _FilterwarningsMarkDecorator, _HiddenParam, _ParametrizeMarkDecorator, _SkipMarkDecorator, _SkipifMarkDecorator, _UsefixturesMarkDecorator, _XfailMarkDecorator
**Functions:** __call__, __contains__, __delitem__, __getattr__, __getitem__, __init__, __iter__, __len__, __repr__, __setitem__, _for_parametrize, _has_param_ids, _parse_parametrize_args, _parse_parametrize_parameters, args, combined_with, extract_from, get_empty_parameterset_mark, get_unpacked_marks, istestfunc, kwargs, markname, name, normalize_mark_list, param, store_mark, update, with_args
**Parameters:** EMPTY_PARAMETERSET_OPTION, HIDDEN_PARAM, MARK_GEN

### `parity_env/lib/python3.14/site-packages/_pytest/monkeypatch.py`
**Classes:** MonkeyPatch
**Functions:** __init__, annotated_getattr, chdir, context, delattr, delenv, delitem, derive_importpath, monkeypatch, resolve, setattr, setenv, setitem, syspath_prepend, undo
**Parameters:** K, RE_IMPORT_ERROR_NAME, V

### `parity_env/lib/python3.14/site-packages/_pytest/nodes.py`
**Classes:** CollectError, Collector, Directory, FSCollector, File, Item, Node, NodeMeta
**Functions:** __call__, __hash__, __init__, __repr__, _check_initialpaths_for_relpath, _check_item_and_collector_diamond_inheritance, _create, _repr_failure_py, _traceback_filter, add_marker, add_report_section, addfinalizer, collect, from_parent, get_closest_marker, get_fslocation_from_item, getparent, ihook, iter_markers, iter_markers_with_node, iter_parents, listchain, listextrakeywords, listnames, location, nodeid, norm_sep, reportinfo, repr_failure, runtest, setup, teardown, warn
**Parameters:** SEP, _T

### `parity_env/lib/python3.14/site-packages/_pytest/outcomes.py`
**Classes:** Exit, Failed, OutcomeException, Skipped, XFailed, _Exit, _Fail, _Skip, _XFail
**Functions:** __call__, __init__, __repr__, importorskip
**Parameters:** TEST_OUTCOME

### `parity_env/lib/python3.14/site-packages/_pytest/pastebin.py`
**Functions:** create_new_paste, pytest_addoption, pytest_configure, pytest_terminal_summary, pytest_unconfigure, tee_write

### `parity_env/lib/python3.14/site-packages/_pytest/pathlib.py`
**Classes:** CouldNotResolvePathError, ImportMode, ImportPathMismatchError
**Functions:** _force_symlink, _ignore_error, _import_module_using_spec, _is_same, absolutepath, bestrelpath, chmod_rw, cleanup_candidates, cleanup_dead_symlinks, cleanup_numbered_dir, cleanup_on_exit, commonpath, compute_module_name, create_cleanup_lock, ensure_deletable, ensure_extended_length_path, extract_suffixes, find_prefixed, find_suffixes, fnmatch_ex, get_extended_length_path_str, get_lock_path, import_path, insert_missing_modules, is_importable, make_numbered_dir, make_numbered_dir_with_cleanup, maybe_delete_a_numbered_dir, module_name_from_path, on_rm_rf_error, parse_num, parts, register_cleanup_lock_removal, resolve_from_str, resolve_package_path, resolve_pkg_root_and_module_name, rm_rf, safe_exists, samefile_nofollow, scandir, spec_matches_module_path, symlink_or_skip, try_cleanup, visit
**Parameters:** LOCK_TIMEOUT, _IGNORED_ERRORS, _IGNORED_WINERRORS

### `parity_env/lib/python3.14/site-packages/_pytest/pytester.py`
**Classes:** HookRecorder, LineComp, LineMatcher, LsofFdLeakChecker, PytestArg, Pytester, PytesterHelperPlugin, RecordedHookCall, RunResult, SysModulesSnapshot, SysPathsSnapshot, TimeoutExpired, reprec
**Functions:** LineMatcher_fixture, __getattr__, __init__, __repr__, __str__, __take_sys_modules_snapshot, _config_for_test, _dump_lines, _ensure_basetemp, _fail, _finalize, _getlines, _getpytestargs, _log, _log_text, _makefile, _match_lines, _match_lines_random, _no_match_line, _pytest, _sys_snapshot, after, assert_contains, assert_contains_lines, assert_outcomes, assertoutcome, before, chdir, clear, collect_by_name, copy_example, countoutcomes, finish_recording, fnmatch_lines, fnmatch_lines_random, genitems, get_lines_after, get_open_files, get_public_names, getcall, getcalls, getfailedcollections, getfailures, gethookrecorder, getinicfg, getitem, getitems, getmodulecol, getnode, getpathnode, getreports, handle_timeout, inline_genitems, inline_run, inline_runsource, isopen, linecomp, listoutcomes, make_hook_recorder, makeconftest, makefile, makeini, makepyfile, makepyprojecttoml, maketoml, maketxtfile, matching_platform, matchreport, mkdir, mkpydir, no_fnmatch_line, no_re_match_line, parse_summary_nouns, parseconfig, parseconfigure, parseoutcomes, path, popcall, popen, preserve_module, pytest_addoption, pytest_configure, pytest_runtest_protocol, pytester, re_match_lines, re_match_lines_random, restore, run, runitem, runpytest, runpytest_inprocess, runpytest_subprocess, runpython, runpython_c, spawn, spawn_pytest, str, syspathinsert, to_text
**Parameters:** IGNORE_PAM

### `parity_env/lib/python3.14/site-packages/_pytest/pytester_assertions.py`
**Functions:** assert_outcomes, assertoutcome

### `parity_env/lib/python3.14/site-packages/_pytest/python.py`
**Classes:** CallSpec2, Class, DirectParamFixtureDef, Function, FunctionDefinition, IdMaker, Metafunc, Module, Package, PyCollector, PyobjMixin, _EmptyClass
**Functions:** __init__, _ascii_escaped_by_config, _call_with_optional_argument, _complain_multiple_hidden_parameter_sets, _find_parametrized_scope, _genfunctions, _get_first_non_fixture_func, _getinstance, _getobj, _idval, _idval_from_argname, _idval_from_function, _idval_from_hook, _idval_from_value, _idval_from_value_required, _initrequest, _make_error_prefix, _matches_prefix_or_glob_option, _pyfuncitem, _recompute_direct_params_indices, _register_setup_class_fixture, _register_setup_function_fixture, _register_setup_method_fixture, _register_setup_module_fixture, _resolve_ids, _resolve_parameter_set_ids, _strict_parametrization_ids_enabled, _traceback_filter, _validate_ids, _validate_if_using_arg_names, async_fail, classnamefilter, cls, collect, from_parent, funcnamefilter, function, get_direct_param_fixture_func, getmodpath, getparam, hasinit, hasnew, id, importtestmodule, instance, isnosetest, istestclass, istestfunction, make_unique_parameterset_ids, module, newinstance, obj, parametrize, path_matches_patterns, pytest_addoption, pytest_collect_directory, pytest_collect_file, pytest_configure, pytest_generate_tests, pytest_pycollect_makeitem, pytest_pycollect_makemodule, pytest_pyfunc_call, reportinfo, repr_failure, runtest, setmulti, setup, sort_key, xunit_setup_class_fixture, xunit_setup_function_fixture, xunit_setup_method_fixture, xunit_setup_module_fixture
**Parameters:** IGNORED_ATTRIBUTES, _ALLOW_MARKERS

### `parity_env/lib/python3.14/site-packages/_pytest/python_api.py`
**Classes:** ApproxBase, ApproxDecimal, ApproxMapping, ApproxNumpy, ApproxScalar, ApproxSequenceLike, ApproxTimedelta
**Functions:** __bool__, __eq__, __init__, __ne__, __repr__, _approx_scalar, _as_numpy_array, _check_type, _compare_approx, _is_sequence_like, _recursive_sequence_map, _repr_compare, _yield_comparisons, approx, get_value_from_nested_list, is_bool, set_default, tolerance
**Parameters:** DEFAULT_ABSOLUTE_TOLERANCE, DEFAULT_RELATIVE_TOLERANCE

### `parity_env/lib/python3.14/site-packages/_pytest/raises.py`
**Classes:** AbstractRaises, NotChecked, RaisesExc, RaisesGroup, ResultHolder
**Functions:** __enter__, __exit__, __init__, __repr__, _check_check, _check_exceptions, _check_expected, _check_match, _check_raw_type, _check_type, _exception_type_name, _match_pattern, _parse_exc, _parse_excgroup, _repr_expected, _unroll_exceptions, backquote, expected_type, fail_reason, get_result, has_result, is_fully_escaped, matches, no_match_for_actual, no_match_for_expected, possible_match, raises, repr_callable, set_result, unescape
**Parameters:** E, P, _REGEX_NO_FLAGS

### `parity_env/lib/python3.14/site-packages/_pytest/recwarn.py`
**Classes:** WarningsChecker, WarningsRecorder
**Functions:** __enter__, __exit__, __getitem__, __init__, __iter__, __len__, clear, deprecated_call, found_str, list, matches, pop, recwarn, warns
**Parameters:** P, T

### `parity_env/lib/python3.14/site-packages/_pytest/reports.py`
**Classes:** BaseReport, CollectErrorRepr, CollectReport, TestReport
**Functions:** __getattr__, __init__, __repr__, _format_exception_group_all_skipped_longrepr, _format_failed_longrepr, _from_json, _get_verbose_word_with_markup, _report_kwargs_from_json, _report_to_json, _report_unserialization_failure, _to_json, caplog, capstderr, capstdout, count_towards_summary, deserialize_repr_crash, deserialize_repr_entry, deserialize_repr_traceback, failed, from_item_and_call, fspath, get_sections, getworkerinfoline, head_line, location, longreprtext, passed, pytest_report_from_serializable, pytest_report_to_serializable, serialize_exception_longrepr, serialize_repr_crash, serialize_repr_entry, serialize_repr_traceback, skipped, toterminal

### `parity_env/lib/python3.14/site-packages/_pytest/runner.py`
**Classes:** CallInfo, SetupState
**Functions:** __init__, __repr__, _update_current_test_var, addfinalizer, call_and_report, check_interactive_exception, collect, collect_one_node, from_call, get_reraise_exceptions, is_node_active, pytest_addoption, pytest_make_collect_report, pytest_report_teststatus, pytest_runtest_call, pytest_runtest_makereport, pytest_runtest_protocol, pytest_runtest_setup, pytest_runtest_teardown, pytest_sessionfinish, pytest_sessionstart, pytest_terminal_summary, result, runtestprotocol, setup, show_test_item, teardown_exact

### `parity_env/lib/python3.14/site-packages/_pytest/scope.py`
**Classes:** Scope
**Functions:** __lt__, from_user, next_higher, next_lower
**Parameters:** HIGH_SCOPES, _ALL_SCOPES, _SCOPE_INDICES

### `parity_env/lib/python3.14/site-packages/_pytest/setuponly.py`
**Functions:** _show_fixture_action, pytest_addoption, pytest_cmdline_main, pytest_fixture_post_finalizer, pytest_fixture_setup

### `parity_env/lib/python3.14/site-packages/_pytest/setupplan.py`
**Functions:** pytest_addoption, pytest_cmdline_main, pytest_fixture_setup

### `parity_env/lib/python3.14/site-packages/_pytest/skipping.py`
**Classes:** Skip, Xfail
**Functions:** evaluate_condition, evaluate_skip_marks, evaluate_xfail_marks, nop, pytest_addoption, pytest_configure, pytest_report_teststatus, pytest_runtest_call, pytest_runtest_makereport, pytest_runtest_setup

### `parity_env/lib/python3.14/site-packages/_pytest/stash.py`
**Classes:** Stash, StashKey
**Functions:** __contains__, __delitem__, __getitem__, __init__, __len__, __setitem__, get, setdefault
**Parameters:** D, T

### `parity_env/lib/python3.14/site-packages/_pytest/stepwise.py`
**Classes:** StepwiseCacheInfo, StepwisePlugin
**Functions:** __init__, _load_cached_info, empty, last_cache_date, pytest_addoption, pytest_collection_modifyitems, pytest_configure, pytest_report_collectionfinish, pytest_runtest_logreport, pytest_sessionfinish, pytest_sessionstart, update_date_to_now
**Parameters:** STEPWISE_CACHE_DIR

### `parity_env/lib/python3.14/site-packages/_pytest/subtests.py`
**Classes:** Captured, CapturedLogs, SubtestContext, SubtestReport, Subtests, _SubTestContextManager
**Functions:** __enter__, __exit__, __init__, __post_init__, _from_json, _new, _sub_test_description, _to_json, capturing_logs, capturing_output, head_line, pytest_addoption, pytest_configure, pytest_report_from_serializable, pytest_report_teststatus, pytest_report_to_serializable, subtests, test

### `parity_env/lib/python3.14/site-packages/_pytest/terminal.py`
**Classes:** MoreQuietAction, TerminalProgressPlugin, TerminalReporter, TestShortLogReport, WarningReport
**Functions:** __call__, __init__, _add_stats, _build_collect_only_summary_stats_line, _build_normal_summary_stats_line, _determine_main_color, _determine_show_progress_info, _emit_progress, _folded_skips, _format_trimmed, _get_line_with_reprcrash_message, _get_main_color, _get_max_warnings, _get_node_id_with_markup, _get_progress_information_message, _get_raw_skip_reason, _get_reports_to_display, _get_teardown_reports, _getcrashline, _getfailureheadline, _handle_teardown_sections, _is_last_item, _locationline, _outrep_summary, _plugin_nameversions, _printcollecteditems, _report_keyboardinterrupt, _set_main_color, _width_of_current_line, _write_progress_information_filling_space, _write_progress_information_if_past_edge, _write_report_lines_from_hooks, build_summary_stats_line, collapsed_location_report, ensure_newline, flush, format_node_duration, format_session_duration, get_location, getreportopt, getreports, hasopt, line, mkrel, mywriter, no_header, no_summary, pluralize, print_teardown_sections, pytest_addoption, pytest_collection, pytest_collection_finish, pytest_collectreport, pytest_configure, pytest_deselected, pytest_internalerror, pytest_keyboard_interrupt, pytest_plugin_registered, pytest_report_header, pytest_report_teststatus, pytest_runtest_logreport, pytest_runtest_logstart, pytest_runtestloop, pytest_sessionfinish, pytest_sessionstart, pytest_terminal_summary, pytest_unconfigure, pytest_warning_recorded, report_collect, reported_progress, rewrite, section, short_test_summary, show_simple, show_skipped, show_skipped_folded, show_skipped_unfolded, show_xfailed, show_xpassed, showfspath, showheader, showlongtestinfo, summary_errors, summary_failures, summary_failures_combined, summary_passes, summary_passes_combined, summary_stats, summary_warnings, summary_xfailures, summary_xpasses, verbosity, wrap_write, write, write_ensure_prefix, write_fspath_result, write_line, write_raw, write_sep
**Parameters:** KNOWN_TYPES, REPORT_COLLECTING_RESOLUTION, _REPORTCHARS_DEFAULT

### `parity_env/lib/python3.14/site-packages/_pytest/terminalprogress.py`
**Functions:** pytest_configure

### `parity_env/lib/python3.14/site-packages/_pytest/threadexception.py`
**Classes:** ThreadExceptionMeta
**Functions:** cleanup, collect_thread_exception, pytest_configure, pytest_runtest_call, pytest_runtest_setup, pytest_runtest_teardown, thread_exception_hook

### `parity_env/lib/python3.14/site-packages/_pytest/timing.py`
**Classes:** Duration, Instant, MockTiming
**Functions:** as_utc, elapsed, patch, seconds, sleep, time

### `parity_env/lib/python3.14/site-packages/_pytest/tmpdir.py`
**Classes:** TempPathFactory
**Functions:** __init__, _ensure_relative_to_basetemp, _mk_tmp, from_config, get_user, getbasetemp, mktemp, pytest_addoption, pytest_configure, pytest_runtest_makereport, pytest_sessionfinish, tmp_path, tmp_path_factory
**Parameters:** MAXVAL

### `parity_env/lib/python3.14/site-packages/_pytest/tracemalloc.py`
**Functions:** tracemalloc_message

### `parity_env/lib/python3.14/site-packages/_pytest/unittest.py`
**Classes:** TestCaseFunction, TwistedVersion, UnitTestCase
**Functions:** _addexcinfo, _get_twisted_version, _getinstance, _handle_twisted_exc_info, _is_skipped, _obtain_errors_and_skips, _register_unittest_setup_class_fixture, _register_unittest_setup_method_fixture, _register_unittest_skip_fixture, _testcase, _traceback_filter, addDuration, addError, addExpectedFailure, addFailure, addSkip, addSubTest, addSuccess, addUnexpectedSuccess, add_skip, collect, newinstance, process_teardown_exceptions, pytest_configure, pytest_pycollect_makeitem, pytest_runtest_makereport, pytest_runtest_protocol, runtest, setup, startTest, stopTest, store_raw_exception_info, teardown, unittest_setup_class_fixture, unittest_setup_method_fixture, unittest_skip_fixture
**Parameters:** TWISTED_RAW_EXCINFO_ATTR

### `parity_env/lib/python3.14/site-packages/_pytest/unraisableexception.py`
**Classes:** UnraisableMeta
**Functions:** cleanup, collect_unraisable, gc_collect_harder, pytest_configure, pytest_runtest_call, pytest_runtest_setup, pytest_runtest_teardown, pytest_unconfigure, unraisable_hook

### `parity_env/lib/python3.14/site-packages/_pytest/warning_types.py`
**Classes:** PytestAssertRewriteWarning, PytestCacheWarning, PytestCollectionWarning, PytestConfigWarning, PytestDeprecationWarning, PytestExperimentalApiWarning, PytestFDWarning, PytestRemovedIn10Warning, PytestReturnNotNoneWarning, PytestUnhandledThreadExceptionWarning, PytestUnknownMarkWarning, PytestUnraisableExceptionWarning, PytestWarning, UnformattedWarning
**Functions:** format, simple, warn_explicit_for
**Parameters:** _W

### `parity_env/lib/python3.14/site-packages/_pytest/warnings.py`
**Functions:** catch_warnings_for_item, pytest_collection, pytest_configure, pytest_load_initial_conftests, pytest_runtest_protocol, pytest_sessionfinish, pytest_terminal_summary, warning_record_to_str

### `parity_env/lib/python3.14/site-packages/iniconfig/__init__.py`
**Classes:** IniConfig, SectionWrapper
**Functions:** __contains__, __getitem__, __init__, __iter__, get, items, lineof, parse
**Parameters:** _D, _T

### `parity_env/lib/python3.14/site-packages/iniconfig/_parse.py`
**Classes:** ParsedLine
**Functions:** _parseline, iscommentline, parse_ini_data, parse_lines
**Parameters:** COMMENTCHARS

### `parity_env/lib/python3.14/site-packages/iniconfig/_version.py`
**Parameters:** COMMIT_ID, TYPE_CHECKING, VERSION_TUPLE

### `parity_env/lib/python3.14/site-packages/iniconfig/exceptions.py`
**Classes:** ParseError
**Functions:** __init__, __str__

### `parity_env/lib/python3.14/site-packages/packaging/__init__.py`

### `parity_env/lib/python3.14/site-packages/packaging/_elffile.py`
**Classes:** EIClass, EIData, ELFFile, ELFInvalid, EMachine
**Functions:** __init__, _read, interpreter
**Parameters:** C32, C64, I386, S390, X8664

### `parity_env/lib/python3.14/site-packages/packaging/_manylinux.py`
**Classes:** _GLibCVersion
**Functions:** _get_glibc_version, _get_manylinux_module, _glibc_version_string, _glibc_version_string_confstr, _glibc_version_string_ctypes, _have_compatible_abi, _is_compatible, _is_linux_armhf, _is_linux_i686, _parse_elf, _parse_glibc_version, platform_tags
**Parameters:** EF_ARM_ABIMASK, EF_ARM_ABI_FLOAT_HARD, EF_ARM_ABI_VER5, _ALLOWED_ARCHS

### `parity_env/lib/python3.14/site-packages/packaging/_musllinux.py`
**Classes:** _MuslVersion
**Functions:** _get_musl_version, _parse_musl_version, platform_tags

### `parity_env/lib/python3.14/site-packages/packaging/_parser.py`
**Classes:** Node, Op, ParsedRequirement, Value, Variable
**Functions:** __getstate__, __init__, __repr__, __setstate__, __str__, _parse_extras, _parse_extras_list, _parse_full_marker, _parse_marker, _parse_marker_atom, _parse_marker_item, _parse_marker_op, _parse_marker_var, _parse_requirement, _parse_requirement_details, _parse_requirement_marker, _parse_specifier, _parse_version_many, _restore_value, parse_marker, parse_requirement, process_env_var, process_python_str, serialize

### `parity_env/lib/python3.14/site-packages/packaging/_ranges.py`
**Classes:** BoundaryKind, BoundaryVersion, LowerBound, UpperBound
**Functions:** __eq__, __gt__, __hash__, __init__, __lt__, __repr__, _base_dev0, _is_family, _lowest_release_at_or_above, _make_above_after_locals, _make_above_after_posts, _make_below_after_locals, _nearest_release_above_prerelease, _next_prefix_dev0, _order_key, above, below, bounds_for_spec, coerce_version, filter_by_ranges, intersect_ranges, intersect_specifier_bounds, least_version_above, matches_bounds_only, range_is_empty, ranges_are_prerelease_only, resolve_prereleases, standard_ranges, trim_release, wildcard_ranges
**Parameters:** AFTER_LOCALS, AFTER_POSTS

### `parity_env/lib/python3.14/site-packages/packaging/_structures.py`
**Classes:** InfinityType, NegativeInfinityType
**Functions:** __repr__

### `parity_env/lib/python3.14/site-packages/packaging/_tokenizer.py`
**Classes:** ParserSyntaxError, Token, Tokenizer
**Functions:** __init__, __str__, check, consume, enclosing_tokens, expect, raise_syntax_error, read

### `parity_env/lib/python3.14/site-packages/packaging/dependency_groups.py`
**Classes:** CyclicDependencyGroup, DependencyGroupInclude, DependencyGroupResolver, DuplicateGroupNames, InvalidDependencyGroupObject
**Functions:** __dir__, __init__, __reduce__, __repr__, _normalize_group_names, _normalize_name, _parse_group, _resolve, lookup, resolve, resolve_dependency_groups
**Parameters:** _NORMALIZE_PATTERN

### `parity_env/lib/python3.14/site-packages/packaging/direct_url.py`
**Classes:** ArchiveInfo, DirInfo, DirectUrl, DirectUrlValidationError, VcsInfo, _DirectUrlRequiredKeyError, _FromMappingProtocol
**Functions:** __dir__, __init__, __str__, _file_url_has_absolute_path, _from_dict, _get, _get_object, _get_required, _json_dict_factory, _strip_auth_from_netloc, _strip_url, from_dict, to_dict, validate
**Parameters:** _PEP610_USER_PASS_ENV_VARS_REGEX, _T

### `parity_env/lib/python3.14/site-packages/packaging/errors.py`
**Classes:** ExceptionGroup, _ErrorCollector
**Functions:** __dir__, __init__, __repr__, collect, error, finalize, on_exit

### `parity_env/lib/python3.14/site-packages/packaging/licenses/__init__.py`
**Classes:** InvalidLicenseExpression
**Functions:** __dir__, canonicalize_license_expression

### `parity_env/lib/python3.14/site-packages/packaging/licenses/_spdx.py`
**Classes:** SPDXException, SPDXLicense
**Parameters:** VERSION

### `parity_env/lib/python3.14/site-packages/packaging/markers.py`
**Classes:** Environment, InvalidMarker, Marker, UndefinedComparison, UndefinedEnvironmentName
**Functions:** __and__, __dir__, __eq__, __getstate__, __hash__, __init__, __or__, __repr__, __setstate__, __str__, _cached_default_environment, _eval_op, _evaluate_markers, _format_full_version, _format_marker, _from_markers, _lookup_environment, _normalize, _normalize_extra_values, _normalize_extras, _pep440_python_full_version, _repair_python_full_version, default_environment, evaluate
**Parameters:** MARKERS_ALLOWING_SET, MARKERS_REQUIRING_VERSION

### `parity_env/lib/python3.14/site-packages/packaging/metadata.py`
**Classes:** InvalidMetadata, Metadata, RFC822Message, RFC822Policy, RawMetadata, _Validator
**Functions:** __dir__, __get__, __init__, __reduce__, __set_name__, _get_payload, _invalid_metadata, _parse_keywords, _parse_project_urls, _process_description_content_type, _process_dynamic, _process_import_names, _process_license_expression, _process_license_files, _process_metadata_version, _process_name, _process_provides_extra, _process_requires_dist, _process_requires_python, _process_summary, _process_version, _write_metadata, as_bytes, as_rfc822, from_email, from_raw, header_store_parse, parse_email
**Parameters:** T, _DICT_FIELDS, _EMAIL_TO_RAW_MAPPING, _LINE_BOUNDARY_RE, _LIST_FIELDS, _NOT_FOUND, _RAW_TO_EMAIL_MAPPING, _REQUIRED_ATTRS, _STRING_FIELDS, _VALID_METADATA_VERSIONS

### `parity_env/lib/python3.14/site-packages/packaging/pylock.py`
**Classes:** Package, PackageArchive, PackageDirectory, PackageSdist, PackageVcs, PackageWheel, Pylock, PylockSelectError, PylockUnsupportedVersionError, PylockValidationError, _FromMappingProtocol, _PylockRequiredKeyError
**Functions:** __dir__, __init__, __str__, _from_dict, _get, _get_as, _get_object, _get_required, _get_required_as, _get_required_sequence_of_objects, _get_sequence, _get_sequence_as, _get_sequence_of_objects, _path_name, _toml_dict_factory, _toml_key, _toml_value, _url_name, _validate_hashes, _validate_normalized_name, _validate_path_url, filename, from_dict, is_direct, is_valid_pylock_path, select, to_dict, validate
**Parameters:** _PYLOCK_FILE_NAME_RE, _T, _T2

### `parity_env/lib/python3.14/site-packages/packaging/ranges.py`
**Classes:** VersionRange, _SetOp
**Functions:** __and__, __contains__, __dir__, __eq__, __hash__, __invert__, __new__, __or__, __repr__, __sub__, _arbitrary_active, _bound_version_str, _build, _canonical_floor, _canonicalize, _check_policy_compat, _clean_lower, _combine_literals, _complement_ranges, _decompose_dev0_gap, _detect_equal_wildcard, _detect_not_equal, _dev_family_anchor, _encode_gap, _encode_gaps, _encode_interval, _encode_lower, _encode_upper, _epoch_floor_lower, _filter_with_admission, _format_intervals, _format_lower, _format_upper, _from_specifier_set, _has_literals, _is_dev0_version, _is_plain, _matches_literal, _merged_region, _predecessor_boundary, _same_releases, _struct_admits, _tighten_no_prereleases, _union_ranges, _with_policy, admit, complement, contains, difference, empty, filter, full, intersection, is_disjoint, is_empty, is_subset, is_superset, singleton, to_specifier_set, union
**Parameters:** DIFFERENCE, INTERSECTION, T, UNION, _MAX_EXCLUSION_RUN

### `parity_env/lib/python3.14/site-packages/packaging/requirements.py`
**Classes:** InvalidRequirement, Requirement
**Functions:** __dir__, __eq__, __getstate__, __hash__, __init__, __repr__, __setstate__, __str__, _iter_parts

### `parity_env/lib/python3.14/site-packages/packaging/specifiers.py`
**Classes:** BaseSpecifier, InvalidSpecifier, Specifier, SpecifierSet
**Functions:** __and__, __contains__, __dir__, __eq__, __getstate__, __hash__, __init__, __iter__, __len__, __repr__, __setstate__, __str__, _apply_prereleases_filter, _canonical_spec, _canonical_specs, _check_arbitrary_unsatisfiable, _check_relation_operand, _fast_match, _get_ranges, _get_spec_version, _pep440_filter_prereleases, _require_spec_version, _str, _to_ranges, _validate_pre, _validate_spec, contains, filter, is_disjoint, is_subset, is_superset, is_unsatisfiable, operator, prereleases, to_range, version
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/packaging/tags.py`
**Classes:** InvalidTag, Tag, TooManyTagsError, UnsortedTagsError
**Functions:** __dir__, __eq__, __getstate__, __hash__, __init__, __repr__, __setstate__, __str__, _abi3_applies, _abi3t_applies, _compute_32_bit_interpreter, _cpython_abis, _emscripten_platforms, _generic_abi, _generic_platforms, _get_config_var, _is_threaded_cpython, _linux_platforms, _mac_arch, _mac_binary_formats, _normalize_string, _py_interpreter_range, _version_nodot, abi, android_platforms, compatible_tags, cpython_tags, create_compatible_tags_selector, generic_tags, interpreter, interpreter_name, interpreter_version, ios_platforms, mac_platforms, parse_tag, platform, platform_tags, pure_python_tags, selector, sys_tags
**Parameters:** _32_BIT_INTERPRETER, _T

### `parity_env/lib/python3.14/site-packages/packaging/utils.py`
**Classes:** InvalidName, InvalidSdistFilename, InvalidWheelFilename
**Functions:** __dir__, canonicalize_name, canonicalize_version, is_normalized_name, parse_sdist_filename, parse_wheel_filename

### `parity_env/lib/python3.14/site-packages/packaging/version.py`
**Classes:** InvalidVersion, Version, _BaseVersion, _TrimmedRelease, _Version, _VersionReplace
**Functions:** __dir__, __eq__, __ge__, __getstate__, __gt__, __hash__, __init__, __le__, __lt__, __ne__, __replace__, __repr__, __setstate__, __str__, _cmpkey, _deprecated, _key, _parse_letter_version, _parse_local_version, _str, _validate_dev, _validate_epoch, _validate_local, _validate_post, _validate_pre, _validate_release, _version, base_version, decorator, dev, epoch, from_parts, is_devrelease, is_postrelease, is_prerelease, local, major, micro, minor, normalize_pre, parse, post, pre, public, release, wrapper
**Parameters:** VERSION_PATTERN, _LETTER_NORMALIZATION, _LOCAL_PATTERN, _LOCAL_STR_RANK, _PRE_RANK, _PRE_RANK_DEV_ONLY, _PRE_RANK_STABLE, _SIMPLE_VERSION_INDICATORS, _STABLE_SUFFIX, _VERSION_PATTERN, _VERSION_PATTERN_OLD

### `parity_env/lib/python3.14/site-packages/pip/__init__.py`
**Functions:** main

### `parity_env/lib/python3.14/site-packages/pip/__main__.py`

### `parity_env/lib/python3.14/site-packages/pip/__pip-runner__.py`
**Classes:** PipImportRedirectingFinder
**Functions:** find_spec, version_str
**Parameters:** PIP_SOURCES_ROOT, PYTHON_REQUIRES

### `parity_env/lib/python3.14/site-packages/pip/_internal/__init__.py`
**Functions:** main

### `parity_env/lib/python3.14/site-packages/pip/_internal/build_env.py`
**Classes:** BuildEnvironment, BuildEnvironmentInstaller, ExtraEnviron, InprocessBuildEnvironmentInstaller, NoOpBuildEnvironment, SubprocessBuildEnvironmentInstaller, _Prefix
**Functions:** __enter__, __exit__, __init__, _dedup, _deprecation_constraint_check, _get_system_sitepackages, _install_impl, _make_resolver, check_requirements, cleanup, get_runnable_pip, install, install_requirements

### `parity_env/lib/python3.14/site-packages/pip/_internal/cache.py`
**Classes:** Cache, CacheEntry, EphemWheelCache, SimpleWheelCache, WheelCache
**Functions:** __init__, _get_cache_path_parts, _get_candidates, _hash_dict, get, get_cache_entry, get_ephem_path_for_link, get_path_for_link, record_download_origin
**Parameters:** ORIGIN_JSON_NAME

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/autocompletion.py`
**Functions:** auto_complete_paths, autocomplete, get_path_completion_type

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/base_command.py`
**Classes:** Command
**Functions:** __init__, _inner_run, _main, _run_wrapper, add_options, handler_map, main, parse_args, pip_version_check, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/cmdoptions.py`
**Classes:** PipOption
**Functions:** _convert_python_version, _get_format_control, _get_release_control, _handle_all_releases, _handle_config_settings, _handle_dependency_group, _handle_merge_hash, _handle_no_binary, _handle_no_cache_dir, _handle_only_binary, _handle_only_final, _handle_python_version, _handle_src, _handle_uploaded_prior_to, _package_name_option_check, _path_option_check, add_target_python_options, all_releases, build_constraints, check_build_constraints, check_dist_restriction, check_list_path_option, check_release_control_exclusive, constraints, editable, exists_action, extra_index_url, find_links, make_option_group, make_target_python, no_binary, only_binary, only_final, prefer_binary, raise_option_error, requirements, requirements_from_scripts, trusted_host, uploaded_prior_to
**Parameters:** ALWAYS_ENABLED_FEATURES, TYPES, TYPE_CHECKER

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/command_context.py`
**Classes:** CommandContextMixIn
**Functions:** __init__, enter_context, main_context
**Parameters:** _T

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/index_command.py`
**Classes:** IndexGroupCommand, SessionCommandMixin
**Functions:** __init__, _build_session, _create_truststore_ssl_context, _get_index_urls, _pip_self_version_check_emit, _pip_self_version_check_fetch, get_default_session, pip_version_check, should_exclude_prerelease

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/main.py`
**Functions:** main

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/main_parser.py`
**Functions:** create_main_parser, identify_python_interpreter, parse_command

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/parser.py`
**Classes:** ConfigOptionParser, CustomOptionParser, PrettyHelpFormatter, UpdatingDefaultsHelpFormatter
**Functions:** __init__, _get_ordered_configuration_items, _update_defaults, check_default, error, expand_default, format_description, format_epilog, format_heading, format_option, format_option_strings, format_usage, get_default_values, indent_lines, insert_option_group, option_list_all, print_help

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/progress_bars.py`
**Functions:** _raw_progress_bar, _rich_download_progress_bar, _rich_install_progress_bar, get_download_progress_renderer, get_install_progress_renderer, write_progress
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/req_command.py`
**Classes:** RequirementCommand
**Functions:** __init__, _build_package_finder, configure_tempdir_registry, determine_resolver_variant, get_requirements, make_requirement_preparer, make_resolver, parse_constraint_files, should_ignore_regular_constraints, trace_basic_info, with_cleanup, wrapper
**Parameters:** KEEPABLE_TEMPDIR_TYPES

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/spinners.py`
**Classes:** InteractiveSpinner, NonInteractiveSpinner, RateLimiter, SpinnerInterface, _PipRichSpinner
**Functions:** __init__, __rich_console__, __rich_measure__, _update, _write, finish, hidden_cursor, open_rich_spinner, open_spinner, ready, render, reset, spin
**Parameters:** HIDE_CURSOR, SHOW_CURSOR

### `parity_env/lib/python3.14/site-packages/pip/_internal/cli/status_codes.py`
**Parameters:** ERROR, NO_MATCHES_FOUND, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/__init__.py`
**Functions:** create_command, get_similar_commands

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/cache.py`
**Classes:** CacheCommand
**Functions:** _cache_dir, _find_http_files, _find_wheels, add_options, format_for_abspath, format_for_human, get_cache_dir, get_cache_info, handler_map, list_cache_items, purge_cache, remove_cache_items, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/check.py`
**Classes:** CheckCommand
**Functions:** run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/completion.py`
**Classes:** CompletionCommand
**Functions:** add_options, run
**Parameters:** BASE_COMPLETION, COMPLETION_SCRIPTS

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/configuration.py`
**Classes:** ConfigurationCommand
**Functions:** _determine_editor, _determine_file, _get_n_args, _save_configuration, add_options, get_name, handler_map, list_config_values, list_values, open_in_editor, print_config_file_values, print_env_var_values, run, set_name_value, unset_name

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/debug.py`
**Classes:** DebugCommand
**Functions:** add_options, ca_bundle_info, create_vendor_txt_map, get_module_from_module_name, get_vendor_version_from_module, run, show_actual_vendor_versions, show_sys_implementation, show_tags, show_value, show_vendor_versions

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/download.py`
**Classes:** DownloadCommand
**Functions:** add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/freeze.py`
**Classes:** FreezeCommand
**Functions:** _dev_pkgs, _should_suppress_build_backends, add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/hash.py`
**Classes:** HashCommand
**Functions:** _hash_of_file, add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/help.py`
**Classes:** HelpCommand
**Functions:** run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/index.py`
**Classes:** IndexCommand
**Functions:** _build_package_finder, add_options, get_available_package_versions, handler_map, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/inspect.py`
**Classes:** InspectCommand
**Functions:** _dist_to_dict, add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/install.py`
**Classes:** InstallCommand
**Functions:** _arg_refers_to_pip, _determine_conflicts, _eagerly_import_modules, _handle_target_dir, _prevent_further_imports, _prevent_import_hook, _warn_about_conflicts, add_options, create_os_error_message, decide_user_install, get_lib_location_guesses, installed_packages_summary, pip_version_check, run, site_packages_writable
**Parameters:** _IMPORT_AUDIT_HOOK_INSTALLED

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/list.py`
**Classes:** ListCommand, _DistWithLatestInfo
**Functions:** _build_package_finder, add_options, format_for_columns, format_for_json, get_not_required, get_outdated, get_uptodate, iter_packages_latest_infos, latest_info, output_package_listing, output_package_listing_columns, pip_version_check, run, wheel_build_tag

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/lock.py`
**Classes:** LockCommand
**Functions:** add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/search.py`
**Classes:** SearchCommand, TransformedHit
**Functions:** add_options, get_installed_distribution, highest_version, print_dist_installation_info, print_results, run, search, transform_hits

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/show.py`
**Classes:** ShowCommand, _PackageInfo
**Functions:** _get_requiring_packages, add_options, normalize_project_url_label, print_results, run, search_packages_info

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/uninstall.py`
**Classes:** UninstallCommand
**Functions:** add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/commands/wheel.py`
**Classes:** WheelCommand
**Functions:** add_options, run

### `parity_env/lib/python3.14/site-packages/pip/_internal/configuration.py`
**Classes:** Configuration
**Functions:** __init__, __repr__, _construct_parser, _dictionary, _disassemble_key, _ensure_have_load_only, _get_parser_to_modify, _load_config_files, _load_environment_vars, _load_file, _mark_as_modified, _normalize_name, _normalized_keys, get_configuration_files, get_environ_vars, get_file_to_edit, get_value, get_values_in_config, items, iter_config_files, load, save, set_value, unset_value
**Parameters:** CONFIG_BASENAME, ENV_NAMES_IGNORED, OVERRIDE_ORDER, VALID_LOAD_ONLY

### `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/__init__.py`
**Functions:** make_distribution_for_install_requirement

### `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/base.py`
**Classes:** AbstractDistribution
**Functions:** __init__, build_tracker_id, get_metadata_distribution, prepare_distribution_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/installed.py`
**Classes:** InstalledDistribution
**Functions:** build_tracker_id, get_metadata_distribution, prepare_distribution_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/sdist.py`
**Classes:** SourceDistribution
**Functions:** _get_build_requires_editable, _get_build_requires_wheel, _install_build_reqs, _prepare_build_backend, _raise_conflicts, _raise_missing_reqs, build_tracker_id, get_metadata_distribution, prepare_distribution_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/wheel.py`
**Classes:** WheelDistribution
**Functions:** build_tracker_id, get_metadata_distribution, prepare_distribution_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/exceptions.py`
**Classes:** BadCommand, BestVersionAlreadyInstalled, BuildDependencyInstallError, CommandError, ConfigurationError, ConfigurationFileCouldNotBeLoaded, DiagnosticPipError, DirectoryUrlHashUnsupported, DistributionNotFound, ExternallyManagedEnvironment, FailedToPrepareCandidate, HashError, HashErrors, HashMismatch, HashMissing, HashUnpinned, IncompleteDownloadError, InstallWheelBuildError, InstallationError, InstallationSubprocessError, InvalidEggFragment, InvalidInstalledPackage, InvalidPyProjectBuildRequires, InvalidSchemeCombination, InvalidWheel, InvalidWheelFilename, LegacyDistutilsInstall, MetadataGenerationFailed, MetadataInconsistent, MetadataInvalid, MissingPyProjectBuildRequires, NetworkConnectionError, NoneMetadataError, PipError, PreviousBuildDirError, RequirementsFileParseError, ResolutionTooDeepError, UninstallMissingRecord, UnsupportedPythonVersion, UnsupportedWheel, UserInstallationInvalid, VcsHashUnsupported
**Functions:** __bool__, __init__, __repr__, __rich_console__, __str__, _hash_comparison, _is_kebab_case, _iter_externally_managed_error_keys, _prefix_with_indent, _requirement_name, append, body, from_config, hash_then_or
**Parameters:** _DEFAULT_EXTERNALLY_MANAGED_ERROR

### `parity_env/lib/python3.14/site-packages/pip/_internal/index/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/index/collector.py`
**Classes:** CacheablePageContent, CollectedSources, HTMLLinkParser, IndexContent, LinkCollector, ParseLinks, _NotAPIContent, _NotHTTP
**Functions:** __call__, __eq__, __hash__, __init__, __str__, _ensure_api_header, _ensure_api_response, _get_encoding_from_headers, _get_index_content, _get_simple_response, _handle_get_simple_fail, _make_index_content, _match_vcs_scheme, collect_sources, create, fetch_response, find_links, get_href, handle_starttag, parse_links, with_cached_index_content, wrapper, wrapper_wrapper

### `parity_env/lib/python3.14/site-packages/pip/_internal/index/package_finder.py`
**Classes:** BestCandidateResult, CandidateEvaluator, CandidatePreferences, LinkEvaluator, LinkType, PackageFinder
**Functions:** __init__, __post_init__, _check_link_requires_python, _extract_version_from_fragment, _find_name_version_sep, _format_versions, _log_skipped_link, _should_install_candidate, _sort_key, _sort_links, client_cert, compute_best_candidate, create, custom_cert, evaluate_link, evaluate_links, filter_unallowed_hashes, find_all_candidates, find_best_candidate, find_links, find_requirement, get_applicable_candidates, get_install_candidate, get_version_sort_key, index_urls, make_candidate_evaluator, make_link_evaluator, prefer_binary, process_project_url, proxy, release_control, requires_python_skipped_reasons, search_scope, set_prefer_binary, set_release_control, sort_best_candidate, target_python, trusted_hosts, uploaded_prior_to

### `parity_env/lib/python3.14/site-packages/pip/_internal/index/sources.py`
**Classes:** LinkSource, _FlatDirectorySource, _FlatDirectoryToUrls, _IndexDirectorySource, _LocalFileSource, _RemoteFileSource
**Functions:** __init__, _is_html_file, _scan_directory, build_source, file_links, link, page_candidates, project_name_to_urls

### `parity_env/lib/python3.14/site-packages/pip/_internal/locations/__init__.py`
**Functions:** _log_context, _looks_like_bpo_44860, _looks_like_deb_system_dist_packages, _looks_like_debian_scheme, _looks_like_msys2_mingw_scheme, _looks_like_red_hat_lib, _looks_like_red_hat_patched_platlib_purelib, _looks_like_red_hat_scheme, _looks_like_slackware_scheme, _should_use_sysconfig, _warn_if_mismatch, _warn_mismatched, get_bin_prefix, get_bin_user, get_platlib, get_purelib, get_scheme
**Parameters:** _MISMATCH_LEVEL, _USE_SYSCONFIG

### `parity_env/lib/python3.14/site-packages/pip/_internal/locations/_distutils.py`
**Functions:** distutils_scheme, get_bin_prefix, get_platlib, get_purelib, get_scheme

### `parity_env/lib/python3.14/site-packages/pip/_internal/locations/_sysconfig.py`
**Functions:** _infer_home, _infer_prefix, _infer_user, _should_use_osx_framework_prefix, get_bin_prefix, get_platlib, get_purelib, get_scheme
**Parameters:** _AVAILABLE_SCHEMES, _HOME_KEYS

### `parity_env/lib/python3.14/site-packages/pip/_internal/locations/base.py`
**Functions:** change_root, get_major_minor_version, get_src_prefix, is_osx_framework
**Parameters:** USER_CACHE_DIR

### `parity_env/lib/python3.14/site-packages/pip/_internal/main.py`
**Functions:** main

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/__init__.py`
**Classes:** Backend
**Functions:** _emit_pkg_resources_deprecation_if_needed, _should_use_importlib_metadata, get_default_environment, get_directory_distribution, get_environment, get_metadata_distribution, get_wheel_distribution, select_backend

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/_json.py`
**Functions:** json_name, msg_to_json, sanitise_header
**Parameters:** METADATA_FIELDS

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/base.py`
**Classes:** BaseDistribution, BaseEntryPoint, BaseEnvironment, FilesystemWheel, MemoryWheel, RequiresEntry, Wheel
**Functions:** __init__, __repr__, __str__, _add_egg_info_requires, _convert_installed_files_path, _iter_declared_entries_from_legacy, _iter_declared_entries_from_record, _iter_distributions, _iter_egg_info_dependencies, _iter_egg_info_extras, _iter_requires_txt_entries, _metadata_impl, as_zipfile, canonical_name, default, direct_url, editable, editable_project_location, from_directory, from_metadata_file_contents, from_paths, from_wheel, get_distribution, group, in_site_packages, in_usersite, info_location, installed_as_egg, installed_by_distutils, installed_location, installed_with_dist_info, installed_with_setuptools_egg_info, installer, is_file, iter_all_distributions, iter_declared_entries, iter_dependencies, iter_distutils_script_names, iter_entry_points, iter_installed_distributions, iter_provided_extras, iter_raw_dependencies, local, location, metadata, metadata_dict, metadata_version, name, raw_name, raw_version, read_text, requested, requires_python, setuptools_filename, value, version

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/__init__.py`
**Parameters:** NAME

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_compat.py`
**Classes:** BadMetadata, BasePath
**Functions:** __init__, __str__, get_dist_canonical_name, get_info_location, name, parent, parse_name_and_version_from_info_directory

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_dists.py`
**Classes:** Distribution, WheelDistribution
**Functions:** __init__, _metadata_impl, canonical_name, from_directory, from_metadata_file_contents, from_wheel, from_zipfile, info_location, installed_location, is_file, iter_dependencies, iter_distutils_script_names, iter_entry_points, iter_provided_extras, iterdir, locate_file, location, raw_version, read_text, version

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_envs.py`
**Classes:** Environment, _DistributionFinder
**Functions:** __init__, _find_impl, _iter_distributions, _looks_like_wheel, default, find, find_legacy_editables, from_paths, get_distribution

### `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/pkg_resources.py`
**Classes:** Distribution, EntryPoint, Environment, InMemoryMetadata
**Functions:** __init__, _extra_mapping, _iter_distributions, _metadata_impl, _search_distribution, canonical_name, default, from_directory, from_metadata_file_contents, from_paths, from_wheel, get_distribution, get_metadata, get_metadata_lines, has_metadata, info_location, installed_by_distutils, installed_location, is_file, iter_dependencies, iter_distutils_script_names, iter_entry_points, iter_provided_extras, location, metadata_isdir, metadata_listdir, raw_version, read_text, run_script, version
**Parameters:** NAME

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/candidate.py`
**Classes:** InstallationCandidate
**Functions:** __init__, __str__

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/direct_url.py`
**Classes:** DirectUrl
**Functions:** from_json, is_local_editable, to_dict_compat, to_json
**Parameters:** DIRECT_URL_METADATA_NAME

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/format_control.py`
**Classes:** FormatControl
**Functions:** __eq__, __init__, __repr__, disallow_binaries, get_allowed_formats, handle_mutual_excludes

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/index.py`
**Classes:** PackageIndex
**Functions:** __init__, _url_for_path

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/installation_report.py`
**Classes:** InstallationReport
**Functions:** __init__, _install_req_to_dict, to_dict

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/link.py`
**Classes:** Link, LinkHash, MetadataFile, _CleanResult
**Functions:** __eq__, __hash__, __init__, __lt__, __post_init__, __repr__, __str__, _absolute_link_url, _clean_file_url_path, _clean_link, _clean_url_path, _clean_url_path_part, _egg_fragment, _ensure_quoted_url, as_dict, as_hashes, ext, file_path, filename, find_hash_url_fragment, from_element, from_json, has_hash, hash, hash_name, is_existing_dir, is_file, is_hash_allowed, is_vcs, is_wheel, is_yanked, links_equivalent, metadata_link, netloc, path, redacted_url, scheme, show_url, splitext, subdirectory_fragment, supported_hashes, url, url_without_fragment
**Parameters:** _SUPPORTED_HASHES

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/release_control.py`
**Classes:** ReleaseControl
**Functions:** allows_prereleases, get_ordered_args, handle_mutual_excludes

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/scheme.py`
**Classes:** Scheme
**Parameters:** SCHEME_KEYS

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/search_scope.py`
**Classes:** SearchScope
**Functions:** create, get_formatted_locations, get_index_urls_locations, mkurl_pypi_url

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/selection_prefs.py`
**Classes:** SelectionPreferences

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/target_python.py`
**Classes:** TargetPython
**Functions:** __init__, format_given, get_sorted_tags, get_unsorted_tags

### `parity_env/lib/python3.14/site-packages/pip/_internal/models/wheel.py`
**Classes:** Wheel
**Functions:** __init__, find_most_preferred_tag, get_formatted_file_tags, support_index_min, supported

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/auth.py`
**Classes:** Credentials, KeyRingBaseProvider, KeyRingCliProvider, KeyRingNullProvider, KeyRingPythonProvider, MultiDomainBasicAuth
**Functions:** PATH_as_shutil_which_determines_it, __call__, __init__, _get_index_url, _get_keyring_auth, _get_new_credentials, _get_password, _get_url_and_credentials, _prompt_for_password, _set_password, _should_save_password_to_keyring, get_auth_info, get_keyring_provider, handle_401, keyring_provider, save_auth_info, save_credentials, use_keyring, warn_on_401
**Parameters:** KEYRING_DISABLED

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/cache.py`
**Classes:** SafeFileCache
**Functions:** __init__, _get_cache_path, _write, _write_from_io, _write_to_file, delete, get, get_body, is_from_cache, set, set_body, set_body_from_io, suppressed_cache_errors

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/download.py`
**Classes:** Downloader, _FileDownload
**Functions:** __call__, __init__, _attempt_resumes_or_redownloads, _cache_resumed_download, _get_http_response_etag_or_last_modified, _get_http_response_filename, _get_http_response_size, _http_get, _http_get_resume, _log_download, _process_response, batch, is_incomplete, parse_content_disposition, reset_file, sanitize_content_filename, write_chunk

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/lazy_wheel.py`
**Classes:** HTTPRangeRequestUnsupported, LazyZipOverHTTP
**Functions:** __enter__, __exit__, __init__, _check_zip, _download, _merge, _stay, _stream_response, close, closed, dist_from_wheel_url, mode, name, read, readable, seek, seekable, tell, truncate, writable

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/session.py`
**Classes:** CacheControlAdapter, HTTPAdapter, InsecureCacheControlAdapter, InsecureHTTPAdapter, LocalFSAdapter, PipSession, _SSLContextAdapterMixin
**Functions:** __init__, add_trusted_host, cert_verify, close, init_poolmanager, is_secure_origin, iter_secure_origins, looks_like_ci, proxy_manager_for, request, send, update_index_urls, user_agent
**Parameters:** CI_ENVIRONMENT_VARIABLES

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/utils.py`
**Functions:** raise_for_status, response_chunks
**Parameters:** DOWNLOAD_CHUNK_SIZE

### `parity_env/lib/python3.14/site-packages/pip/_internal/network/xmlrpc.py`
**Classes:** PipXmlrpcTransport
**Functions:** __init__, request

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/build_tracker.py`
**Classes:** BuildTracker, TrackerId
**Functions:** __enter__, __exit__, __init__, _entry_path, add, cleanup, get_build_tracker, remove, track, update_env_context_manager

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/metadata.py`
**Functions:** generate_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/metadata_editable.py`
**Functions:** generate_editable_metadata

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/wheel.py`
**Functions:** build_wheel_pep517

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/wheel_editable.py`
**Functions:** build_wheel_editable

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/check.py`
**Classes:** PackageDetails
**Functions:** _create_whitelist, _simulate_installation_of, check_install_conflicts, check_package_set, check_unsupported, create_package_set_from_installed

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/freeze.py`
**Classes:** FrozenRequirement, _EditableInfo
**Functions:** __str__, _format_as_name_version, _get_editable_info, canonical_name, freeze, from_dist

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/install/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/install/wheel.py`
**Classes:** File, MissingCallableSuffix, PipScriptMaker, ScriptFile, ZipBackedFile
**Functions:** __init__, _fs_to_record_path, _generate_file, _getinfo, _install_wheel, _normalized_outrows, _raise_for_invalid_entrypoint, _record_to_fs_path, assert_no_path_traversal, csv_io_kwargs, data_scheme_file_maker, fix_script, get_console_script_specs, get_csv_rows_for_installed, get_entrypoints, install_wheel, is_data_scheme_path, is_dir_path, is_entrypoint_wrapper, is_script_scheme_path, make, make_data_scheme_file, make_root_scheme_file, message_about_scripts_not_on_PATH, pyc_output_path, pyc_source_file_paths, record_installed, rehash, req_error_context, root_scheme_file_maker, save, wheel_root_is_purelib

### `parity_env/lib/python3.14/site-packages/pip/_internal/operations/prepare.py`
**Classes:** File, RequirementPreparer
**Functions:** __init__, __post_init__, _check_download_dir, _complete_partial_requirements, _ensure_link_req_src_dir, _fetch_metadata_only, _fetch_metadata_using_lazy_wheel, _fetch_metadata_using_link_data_attr, _get_linked_req_hashes, _get_prepared_distribution, _log_preparing_link, _prepare_linked_requirement, get_file_url, get_http_url, prepare_editable_requirement, prepare_installed_requirement, prepare_linked_requirement, prepare_linked_requirements_more, save_linked_requirement, unpack_url, unpack_vcs_link

### `parity_env/lib/python3.14/site-packages/pip/_internal/pyproject.py`
**Functions:** _is_list_of_str, load_pyproject_toml, make_pyproject_path

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/__init__.py`
**Classes:** InstallationResult
**Functions:** _validate_requirements, install_given_reqs

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/constructors.py`
**Classes:** RequirementParts
**Functions:** _get_url_from_path, _looks_like_path, _parse_direct_url_editable, _parse_pip_syntax_editable, _parse_req_string, _pylock_hashes_to_hash_options, _set_requirement_extras, _strip_extras, check_first_requirement_in_file, convert_extras, deduce_helpful_msg, install_req_drop_extras, install_req_extend_extras, install_req_from_editable, install_req_from_line, install_req_from_link_and_ireq, install_req_from_parsed_requirement, install_req_from_pylock_package, install_req_from_req_string, parse_editable, parse_req_from_editable, parse_req_from_line, with_source

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/pep723.py`
**Classes:** PEP723Exception
**Functions:** __init__, pep723_metadata
**Parameters:** REGEX

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_dependency_group.py`
**Functions:** _build_resolvers, _load_pyproject, _resolve_all_groups, parse_dependency_groups

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_file.py`
**Classes:** OptionParsingError, ParsedLine, ParsedRequirement, RequirementsFileParser
**Functions:** __init__, _decode_req_file, _parse_and_recurse, _parse_file, break_args_options, build_parser, expand_env_variables, get_file_content, get_line_parser, handle_line, handle_option_line, handle_requirement_line, ignore_comments, is_editable, join_lines, parse, parse_line, parse_requirements, parser_exit, preprocess, requirement
**Parameters:** COMMENT_RE, DEFAULT_ENCODING, ENV_VAR_RE, PEP263_ENCODING_RE, SCHEME_RE, SUPPORTED_OPTIONS_EDITABLE_REQ_DEST, SUPPORTED_OPTIONS_REQ_DEST

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_install.py`
**Classes:** InstallRequirement
**Functions:** __init__, __repr__, __str__, _clean_zip_name, _get_archive_name, _has_option, _set_requirement, archive, assert_source_matches_version, check_if_exists, check_invalid_constraint_type, editable_sanity_check, ensure_build_location, ensure_has_source_dir, ensure_pristine_source_checkout, format_debug, from_path, get_dist, has_hash_options, hashes, install, is_direct, is_pinned, is_wheel, is_wheel_from_cache, load_pyproject_toml, match_markers, metadata, name, needs_unpacked_archive, prepare_metadata, pyproject_toml_path, set_dist, setup_py_path, specifier, supports_pyproject_editable, uninstall, unpacked_source_directory, update_editable, warn_on_mismatching_name

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_set.py`
**Classes:** RequirementSet
**Functions:** __init__, __repr__, __str__, add_named_requirement, add_unnamed_requirement, all_requirements, get_requirement, has_requirement, requirements_to_install

### `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_uninstall.py`
**Classes:** StashedUninstallPathSet, UninstallPathSet, UninstallPthEntries
**Functions:** __init__, _allowed_to_proceed, _display, _get_directory_stash, _get_file_stash, _permitted, _script_names, _unique, add, add_pth, can_rollback, commit, compact, compress_for_output_listing, compress_for_rename, from_dist, iter_scripts_to_remove, norm_join, remove, rollback, stash, uninstallation_paths, unique

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/base.py`
**Classes:** BaseResolver
**Functions:** get_installation_order, resolve

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/legacy/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/legacy/resolver.py`
**Classes:** Resolver
**Functions:** __init__, _add_requirement_to_set, _check_dist_requires_python, _check_skip_installed, _find_requirement_link, _get_dist_for, _is_upgrade_allowed, _populate_link, _resolve_one, _set_req_to_reinstall, add_req, get_installation_order, resolve, schedule

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/base.py`
**Classes:** Candidate, Constraint, Requirement
**Functions:** __and__, __bool__, _match_link, empty, format_for_error, format_name, from_ireq, get_candidate_lookup, get_install_requirement, is_editable, is_installed, is_satisfied_by, iter_dependencies, name, project_name, source_link, version

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/candidates.py`
**Classes:** AlreadyInstalledCandidate, EditableCandidate, ExtrasCandidate, LinkCandidate, RequiresPythonCandidate, _InstallRequirementBackedCandidate
**Functions:** __eq__, __hash__, __init__, __repr__, __str__, _check_metadata_consistency, _make_install_req_from_dist, _prepare, _prepare_distribution, as_base_candidate, format_for_error, get_install_requirement, is_editable, is_installed, iter_dependencies, make_install_req_from_editable, make_install_req_from_link, name, project_name, source_link, version
**Parameters:** REQUIRES_PYTHON_IDENTIFIER

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/factory.py`
**Classes:** CollectedRootRequirements, ConflictCause, Factory
**Functions:** __init__, _fail_if_link_is_unsupported_wheel, _get_installed_candidate, _get_locked_installation_candidate, _has_any_candidates, _iter_candidates_from_constraints, _iter_explicit_candidates_from_base, _iter_found_candidates, _make_base_candidate_from_link, _make_candidate_from_dist, _make_candidate_from_link, _make_extras_candidate, _make_requirements_from_install_req, _report_requires_python_error, _report_single_requirement_conflict, collect_root_requirements, describe_trigger, find_candidates, force_reinstall, get_dist_to_uninstall, get_installation_error, get_wheel_cache_entry, is_pinned, iter_index_candidate_infos, make_requirement_from_candidate, make_requirements_from_spec, make_requires_python_requirement, text_join
**Parameters:** C

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py`
**Classes:** FoundCandidates
**Functions:** __bool__, __getitem__, __init__, __iter__, __len__, _iter_built, _iter_built_with_inserted, _iter_built_with_prepended

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/provider.py`
**Classes:** PipProvider
**Functions:** __init__, _eligible_for_upgrade, _get_with_identifier, constraints, find_matches, get_dependencies, get_preference, identify, is_satisfied_by, narrow_requirement_selection
**Parameters:** D, V, _CONFLICT_PRIORITY_THRESHOLD

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/reporter.py`
**Classes:** PipDebuggingReporter, PipReporter
**Functions:** __init__, adding_requirement, ending, ending_round, pinning, rejecting_candidate, starting, starting_round

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/requirements.py`
**Classes:** ExplicitRequirement, RequiresPythonRequirement, SpecifierRequirement, SpecifierWithoutExtrasRequirement, UnsatisfiableRequirement
**Functions:** __eq__, __hash__, __init__, __repr__, __str__, _equal, format_for_error, get_candidate_lookup, is_satisfied_by, name, project_name

### `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/resolver.py`
**Classes:** Resolver
**Functions:** __init__, _req_set_item_sorter, get_installation_order, get_topological_weights, resolve, visit

### `parity_env/lib/python3.14/site-packages/pip/_internal/self_outdated_check.py`
**Classes:** SelfCheckState, UpgradePrompt
**Functions:** __init__, __rich__, _compute_upgrade_prompt, _get_current_remote_pip_version, _get_statefile_name, get, key, pip_self_version_check_emit, pip_self_version_check_fetch, set
**Parameters:** _WEEK

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/_jaraco_text.py`
**Functions:** _, _nonblank, drop_comment, join_continuation, yield_lines

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/_log.py`
**Classes:** VerboseLogger
**Functions:** getLogger, init_logging, verbose
**Parameters:** VERBOSE

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/appdirs.py`
**Functions:** _macos_user_config_dir, site_config_dirs, user_cache_dir, user_config_dir

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/compat.py`
**Functions:** get_path_uid, has_tls, open_text_resource
**Parameters:** WINDOWS

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/compatibility_tags.py`
**Functions:** _android_platforms, _custom_manylinux_platforms, _expand_allowed_platforms, _get_custom_interpreter, _get_custom_platforms, _get_python_version, _ios_platforms, _mac_platforms, get_supported, version_info_to_nodot

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/datetime.py`
**Functions:** parse_iso_datetime, today_is_later_than

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/deprecation.py`
**Classes:** PipDeprecationWarning
**Functions:** _showwarning, deprecated, install_warning_logger
**Parameters:** DEPRECATION_MSG_PREFIX

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/direct_url_helpers.py`
**Functions:** direct_url_as_pep440_direct_reference, direct_url_for_editable, direct_url_from_link

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/egg_link.py`
**Functions:** _egg_link_names, egg_link_path_from_location, egg_link_path_from_sys_path

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/entrypoints.py`
**Functions:** _wrapper, get_best_invocation_for_this_pip, get_best_invocation_for_this_python
**Parameters:** _EXECUTABLE_NAMES

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/filesystem.py`
**Functions:** _subdirs_without_generic, _test_writable_dir_win, adjacent_tmp_file, check_path_owner, copy_directory_permissions, directory_size, file_size, find_files, format_directory_size, format_file_size, subdirs_without_files, subdirs_without_wheels, test_writable_dir

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/filetypes.py`
**Functions:** is_archive_file
**Parameters:** ARCHIVE_EXTENSIONS, WHEEL_EXTENSION

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/glibc.py`
**Functions:** glibc_version_string, glibc_version_string_confstr, glibc_version_string_ctypes, libc_ver

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/hashes.py`
**Classes:** Hashes, MissingHashes
**Functions:** __and__, __bool__, __eq__, __hash__, __init__, _raise, check_against_chunks, check_against_file, check_against_path, digest_count, has_one_of, is_hash_allowed
**Parameters:** FAVORITE_HASH, STRONG_HASHES

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/logging.py`
**Classes:** BetterRotatingFileHandler, BrokenStdoutLoggingError, ExcludeLoggerFilter, IndentedRenderable, IndentingFormatter, MaxLevelFilter, PipConsole, RichPipStreamHandler
**Functions:** __init__, __rich_console__, _is_broken_pipe_error, _open, capture_logging, emit, filter, format, get_console, get_indentation, get_message_start, handleError, indent_log, on_broken_pipe, setup_logging

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/misc.py`
**Classes:** ConfiguredBuildBackendHookCaller, HiddenText, StreamWrapper
**Functions:** __eq__, __init__, __repr__, __str__, _check_no_input, _get_netloc, _onerror_ignore, _onerror_reraise, _redact_netloc, _transform_url, ask, ask_input, ask_password, ask_path_exists, backup_dir, build_editable, build_netloc, build_sdist, build_url_from_netloc, build_wheel, check_externally_managed, display_path, encoding, ensure_dir, enum, format_size, from_stream, get_pip_version, get_prog, get_requires_for_build_editable, get_requires_for_build_sdist, get_requires_for_build_wheel, hash_file, hide_url, hide_value, is_console_interactive, is_installable_dir, is_local, normalize_path, normalize_version_info, pairwise, parse_netloc, partition, prepare_metadata_for_build_editable, prepare_metadata_for_build_wheel, protect_pip_from_modification_on_windows, read_chunks, redact_auth_from_requirement, redact_auth_from_url, redact_netloc, remove_auth_from_url, renames, rmtree, rmtree_errorhandler, split_auth_from_netloc, split_auth_netloc_from_url, splitext, strtobool, tabulate, warn_if_run_as_root, write_output
**Parameters:** FILE_CHUNK_SIZE, T

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/packaging.py`
**Functions:** check_requires_python, get_requirement

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/pylock.py`
**Functions:** _get_pylock_path_or_url_content, _is_url, _package_dist_url, _pylock_package_from_install_requirement, is_valid_pylock_filename, package_archive_requirement_url, package_directory_requirement_url, package_sdist_requirement_url, package_vcs_requirement_url, package_wheel_requirement_url, pylock_from_install_requirements, select_from_pylock_path_or_url
**Parameters:** _SCHEME_RE

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/retry.py`
**Functions:** retry, retry_wrapped, wrapper
**Parameters:** P, T

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/subprocess.py`
**Functions:** call_subprocess, format_command_args, make_command, reveal_command_args, runner, runner_with_spinner_message

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/temp_dir.py`
**Classes:** AdjacentTempDirectory, TempDirectory, TempDirectoryTypeRegistry, _Default
**Functions:** __enter__, __exit__, __init__, __repr__, _create, _generate_names, cleanup, get_delete, global_tempdir_manager, onerror, path, set_delete, tempdir_registry
**Parameters:** LEADING_CHARS, _T

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/unpacking.py`
**Functions:** _get_default_mode_plus_executable, _untar, _untar_without_filter, _unzip, current_umask, has_leading_dir, is_symlink_target_in_tar, is_within_directory, pip_filter, set_extracted_file_to_default_mode_plus_executable, split_leading_dir, unpack_file, untar_file, unzip_file, zip_item_is_executable
**Parameters:** SUPPORTED_EXTENSIONS

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/urls.py`
**Functions:** path_to_url, url_to_path

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/virtualenv.py`
**Functions:** _get_pyvenv_cfg_lines, _no_global_under_legacy_virtualenv, _no_global_under_venv, _running_under_legacy_virtualenv, _running_under_venv, running_under_virtualenv, virtualenv_no_global
**Parameters:** _INCLUDE_SYSTEM_SITE_PACKAGES_REGEX

### `parity_env/lib/python3.14/site-packages/pip/_internal/utils/wheel.py`
**Functions:** check_compatibility, parse_wheel, read_wheel_metadata_file, wheel_dist_info_dir, wheel_metadata, wheel_version
**Parameters:** VERSION_COMPATIBLE

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/bazaar.py`
**Classes:** Bazaar
**Functions:** fetch_new, get_base_rev_args, get_remote_url, get_revision, get_url_rev_and_auth, is_commit_id_equal, switch, update

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/git.py`
**Classes:** Git
**Functions:** _git_remote_to_pip_url, _should_fetch, fetch_new, get_base_rev_args, get_current_branch, get_git_version, get_remote_url, get_repository_root, get_revision, get_revision_sha, get_subdirectory, get_url_rev_and_auth, has_commit, is_commit_id_equal, is_immutable_rev_checkout, looks_like_hash, resolve_revision, run_command, should_add_vcs_url_prefix, switch, update, update_submodules
**Parameters:** GIT_VERSION_REGEX, HASH_REGEX, SCP_REGEX

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/mercurial.py`
**Classes:** Mercurial
**Functions:** fetch_new, get_base_rev_args, get_remote_url, get_repository_root, get_requirement_revision, get_revision, get_subdirectory, is_commit_id_equal, switch, update

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/subversion.py`
**Classes:** Subversion
**Functions:** __init__, _get_svn_url_rev, call_vcs_version, fetch_new, get_base_rev_args, get_netloc_and_auth, get_remote_call_options, get_remote_url, get_revision, get_url_rev_and_auth, get_vcs_version, is_commit_id_equal, make_rev_args, should_add_vcs_url_prefix, switch, update

### `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/versioncontrol.py`
**Classes:** RemoteNotFoundError, RemoteNotValidError, RevOptions, VcsSupport, VersionControl
**Functions:** __init__, __iter__, __repr__, _is_local_repository, all_schemes, arg_rev, backends, compare_urls, dirnames, fetch_new, find_path_to_project_root_from_repo_root, get_backend, get_backend_for_dir, get_backend_for_scheme, get_base_rev_args, get_netloc_and_auth, get_remote_url, get_repository_root, get_requirement_revision, get_revision, get_src_requirement, get_subdirectory, get_url_rev_and_auth, get_url_rev_options, is_commit_id_equal, is_immutable_rev_checkout, is_repository_directory, is_url, make_new, make_rev_args, make_rev_options, make_vcs_requirement_url, normalize_url, obtain, register, run_command, should_add_vcs_url_prefix, switch, to_args, to_display, unpack, unregister, update

### `parity_env/lib/python3.14/site-packages/pip/_internal/wheel_builder.py`
**Functions:** _build_one, _build_one_inside_env, _contains_egg_info, _get_cache_dir, _should_cache, _verify_one, build

### `parity_env/lib/python3.14/site-packages/pip/_vendor/__init__.py`
**Functions:** vendored
**Parameters:** DEBUNDLED, WHEEL_DIR

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/_cmd.py`
**Functions:** get_args, get_session, main, setup_logging

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/adapter.py`
**Classes:** CacheControlAdapter
**Functions:** __init__, _update_chunk_length, build_response, close, send

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/cache.py`
**Classes:** BaseCache, DictCache, SeparateBodyBaseCache
**Functions:** __init__, close, delete, get, get_body, set, set_body

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/caches/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/caches/file_cache.py`
**Classes:** FileCache, SeparateBodyFileCache, _FileCacheMixin
**Functions:** __init__, _delete, _fn, _write, delete, encode, get, get_body, set, set_body, url_to_file_path

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/caches/redis_cache.py`
**Classes:** RedisCache
**Functions:** __init__, clear, close, delete, get, set

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/controller.py`
**Classes:** CacheController
**Functions:** __init__, _cache_set, _load_from_cache, _urlnorm, cache_response, cache_url, cached_request, conditional_headers, parse_cache_control, parse_uri, update_cached_response
**Parameters:** PERMANENT_REDIRECT_STATUSES, URI

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/filewrapper.py`
**Classes:** CallbackFileWrapper
**Functions:** __getattr__, __init__, __is_fp_closed, _close, _safe_read, read

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/heuristics.py`
**Classes:** BaseHeuristic, ExpiresAfter, LastModified, OneDayCache
**Functions:** __init__, apply, datetime_to_header, expire_after, update_headers, warning
**Parameters:** TIME_FMT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/serialize.py`
**Classes:** Serializer
**Functions:** _loads_v4, dumps, loads, prepare_response, serialize

### `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/wrapper.py`
**Functions:** CacheControl

### `parity_env/lib/python3.14/site-packages/pip/_vendor/certifi/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/certifi/__main__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/certifi/core.py`
**Functions:** contents, exit_cacert_ctx, where
**Parameters:** _CACERT_CTX, _CACERT_PATH

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/__init__.py`
**Classes:** DistlibException, NullHandler
**Functions:** createLock, emit, handle

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/compat.py`
**Classes:** BaseConfigurator, CertificateError, ChainMap, Container, ConvertingDict, ConvertingList, ConvertingTuple, OrderedDict, ZipExtFile, ZipFile
**Functions:** __bool__, __contains__, __delitem__, __enter__, __eq__, __exit__, __getitem__, __init__, __iter__, __len__, __missing__, __ne__, __reduce__, __repr__, __reversed__, __setitem__, _access_check, _dnsname_match, _get_normal_name, _recursive_repr, as_tuple, cache_from_source, callable, cfg_convert, clear, configure_custom, convert, copy, decorating_function, detect_encoding, ext_convert, find_cookie, fromkeys, fsdecode, fsencode, get, items, iteritems, iterkeys, itervalues, keys, match_hostname, new_child, open, parents, pop, popitem, python_implementation, quote, read_or_stop, resolve, setdefault, update, valid_ident, values, viewitems, viewkeys, viewvalues, which, wrapper
**Parameters:** CONVERT_PATTERN, DIGIT_PATTERN, DOT_PATTERN, IDENTIFIER, INDEX_PATTERN, WORD_PATTERN

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/resources.py`
**Classes:** Resource, ResourceBase, ResourceCache, ResourceContainer, ResourceFinder, ZipResourceFinder
**Functions:** __init__, _adjust_path, _find, _is_directory, _make_path, allowed, as_stream, bytes, file_path, find, finder, finder_for_path, get, get_bytes, get_cache_info, get_resources, get_size, get_stream, is_container, is_stale, iterator, register_finder, resources, size

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/scripts.py`
**Classes:** ScriptMaker
**Functions:** __init__, _build_shebang, _copy_script, _fix_jython_executable, _get_alternate_executable, _get_launcher, _get_script_text, _get_shebang, _is_shell, _make_script, _write_script, dry_run, enquote_executable, get_manifest, get_script_filenames, make, make_multiple
**Parameters:** DISTLIB_PACKAGE, FIRST_LINE_RE, SCRIPT_TEMPLATE, WRAPPERS, _DEFAULT_MANIFEST

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/util.py`
**Classes:** CSVBase, CSVReader, CSVWriter, Cache, Configurator, EventMixin, ExportEntry, FileOperator, HTTPSConnection, HTTPSHandler, HTTPSOnlyHandler, Progress, PyPIRCFile, SafeTransport, Sequencer, ServerProxy, SubprocessMixin, Transport, cached_property
**Functions:** ETA, __enter__, __eq__, __exit__, __get__, __getitem__, __init__, __iter__, __repr__, _conn_maker, _csv_open, _get_external_data, _iglob, _init_record, _load_pypirc, _store_pypirc, add, add_node, byte_compile, chdir, check_path, clear, commit, configure_custom, connect, convert, convert_path, copy_file, copy_stream, dot, ensure_dir, ensure_removed, ensure_slash, extract_by_key, extraction_filter, format_duration, get_cache_base, get_executable, get_export_entry, get_extras, get_host_platform, get_package_data, get_platform, get_process_umask, get_project_data, get_rel_path, get_resources_dests, get_steps, get_subscribers, get_versions, http_open, https_open, iglob, in_venv, inc_convert, increment, is_step, is_string_sequence, is_writable, make_connection, marker, marker_and, marker_expr, marker_var, maximum, newer, next, normalize_name, parse_credentials, parse_marker, parse_name_and_version, parse_requirement, path_to_cache_dir, percentage, prefix_to_dir, proceed, publish, read, read_exports, read_stream, reader, record_as_written, remove, remove_node, resolve, rollback, run_command, set_mode, socket_timeout, speed, split_filename, start, stop, strong_connections, strongconnect, tempdir, unarchive, update, value, write_binary_file, write_exports, write_text_file, writerow, zip_dir
**Parameters:** AND, ARCHIVE_EXTENSIONS, COMPARE_OP, DEFAULT_REALM, DEFAULT_REPOSITORY, ENTRY_RE, IDENTIFIER, MARKER_OP, NAME_VERSION_RE, NON_SPACE, OR, PROJECT_NAME_AND_VERSION, PYTHON_VERSION, RICH_GLOB, STRING_CHUNK, UNITS, VERSION_IDENTIFIER, _CHECK_MISMATCH_SET, _CHECK_RECURSIVE_GLOB, _TARGET_TO_PLAT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distro/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distro/__main__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/distro/distro.py`
**Classes:** InfoDict, LinuxDistribution, VersionDict, cached_property
**Functions:** __get__, __init__, __repr__, _debian_version, _distro_release_info, _lsb_release_info, _os_release_info, _oslevel_info, _parse_distro_release_content, _parse_distro_release_file, _parse_lsb_release_content, _parse_os_release_content, _parse_uname_content, _to_str, _uname_info, build_number, codename, distro_release_attr, distro_release_info, id, info, like, linux_distribution, lsb_release_attr, lsb_release_info, main, major_version, minor_version, name, normalize, os_release_attr, os_release_info, oslevel_info, uname_attr, uname_info, version, version_parts
**Parameters:** NORMALIZED_DISTRO_ID, NORMALIZED_LSB_ID, NORMALIZED_OS_ID, _DISTRO_RELEASE_BASENAMES, _DISTRO_RELEASE_BASENAME_PATTERN, _DISTRO_RELEASE_CONTENT_REVERSED_PATTERN, _DISTRO_RELEASE_IGNORE_BASENAMES, _OS_RELEASE_BASENAME, _UNIXCONFDIR, _UNIXUSRLIBDIR

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/codec.py`
**Classes:** Codec, IncrementalDecoder, IncrementalEncoder, StreamReader, StreamWriter
**Functions:** _buffer_decode, _buffer_encode, decode, encode, search_function

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/compat.py`
**Functions:** ToASCII, ToUnicode, nameprep

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/core.py`
**Classes:** IDNABidiError, IDNAError, InvalidCodepoint, InvalidCodepointContext
**Functions:** _combining_class, _is_script, _punycode, _unot, alabel, check_bidi, check_hyphen_ok, check_initial_combiner, check_label, check_nfc, decode, encode, ulabel, uts46_remap, valid_contextj, valid_contexto, valid_label_length, valid_string_length

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/idnadata.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/intranges.py`
**Functions:** _decode_range, _encode_range, intranges_contain, intranges_from_list

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/package_data.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/uts46data.py`
**Functions:** _seg_0, _seg_1, _seg_10, _seg_11, _seg_12, _seg_13, _seg_14, _seg_15, _seg_16, _seg_17, _seg_18, _seg_19, _seg_2, _seg_20, _seg_21, _seg_22, _seg_23, _seg_24, _seg_25, _seg_26, _seg_27, _seg_28, _seg_29, _seg_3, _seg_30, _seg_31, _seg_32, _seg_33, _seg_34, _seg_35, _seg_36, _seg_37, _seg_38, _seg_39, _seg_4, _seg_40, _seg_41, _seg_42, _seg_43, _seg_44, _seg_45, _seg_46, _seg_47, _seg_48, _seg_49, _seg_5, _seg_50, _seg_51, _seg_52, _seg_53, _seg_54, _seg_55, _seg_56, _seg_57, _seg_58, _seg_59, _seg_6, _seg_60, _seg_61, _seg_62, _seg_63, _seg_64, _seg_65, _seg_66, _seg_67, _seg_68, _seg_69, _seg_7, _seg_70, _seg_71, _seg_72, _seg_73, _seg_74, _seg_75, _seg_76, _seg_77, _seg_78, _seg_79, _seg_8, _seg_80, _seg_81, _seg_82, _seg_83, _seg_9

### `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/__init__.py`
**Functions:** pack, packb, unpack

### `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/exceptions.py`
**Classes:** BufferFull, ExtraData, FormatError, OutOfData, StackError, UnpackException
**Functions:** __init__, __str__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/ext.py`
**Classes:** ExtType, Timestamp
**Functions:** __eq__, __hash__, __init__, __ne__, __new__, __repr__, from_bytes, from_datetime, from_unix, from_unix_nano, to_bytes, to_datetime, to_unix, to_unix_nano

### `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/fallback.py`
**Classes:** BytesIO, Packer, Unpacker
**Functions:** __init__, __iter__, __next__, _check_type_strict, _consume, _get_data_from_buffer, _get_extradata, _got_extradata, _pack, _pack_array_header, _pack_bin_header, _pack_map_header, _pack_map_pairs, _pack_raw_header, _read, _read_header, _reserve, _unpack, bytes, feed, getbuffer, getvalue, newlist_hint, pack, pack_array_header, pack_ext_type, pack_map_header, pack_map_pairs, read_array_header, read_bytes, read_map_header, reset, skip, tell, unpack, unpackb, write
**Parameters:** DEFAULT_RECURSE_LIMIT, EX_CONSTRUCT, EX_READ_ARRAY_HEADER, EX_READ_MAP_HEADER, EX_SKIP, L, TYPE_ARRAY, TYPE_BIN, TYPE_EXT, TYPE_IMMEDIATE, TYPE_MAP, TYPE_RAW, _MSGPACK_HEADERS, _NO_FORMAT_USED, _USING_STRINGBUILDER

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_elffile.py`
**Classes:** EIClass, EIData, ELFFile, ELFInvalid, EMachine
**Functions:** __init__, _read, interpreter
**Parameters:** C32, C64, I386, S390, X8664

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_manylinux.py`
**Classes:** _GLibCVersion
**Functions:** _get_glibc_version, _glibc_version_string, _glibc_version_string_confstr, _glibc_version_string_ctypes, _have_compatible_abi, _is_compatible, _is_linux_armhf, _is_linux_i686, _parse_elf, _parse_glibc_version, platform_tags
**Parameters:** EF_ARM_ABIMASK, EF_ARM_ABI_FLOAT_HARD, EF_ARM_ABI_VER5, _ALLOWED_ARCHS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_musllinux.py`
**Classes:** _MuslVersion
**Functions:** _get_musl_version, _parse_musl_version, platform_tags

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_parser.py`
**Classes:** Node, Op, ParsedRequirement, Value, Variable
**Functions:** __getstate__, __init__, __repr__, __setstate__, __str__, _parse_extras, _parse_extras_list, _parse_full_marker, _parse_marker, _parse_marker_atom, _parse_marker_item, _parse_marker_op, _parse_marker_var, _parse_requirement, _parse_requirement_details, _parse_requirement_marker, _parse_specifier, _parse_version_many, _restore_value, parse_marker, parse_requirement, process_env_var, process_python_str, serialize

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_structures.py`
**Classes:** InfinityType, NegativeInfinityType
**Functions:** __repr__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_tokenizer.py`
**Classes:** ParserSyntaxError, Token, Tokenizer
**Functions:** __init__, __str__, check, consume, enclosing_tokens, expect, raise_syntax_error, read

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/dependency_groups.py`
**Classes:** CyclicDependencyGroup, DependencyGroupInclude, DependencyGroupResolver, DuplicateGroupNames, InvalidDependencyGroupObject
**Functions:** __dir__, __init__, __repr__, _normalize_group_names, _normalize_name, _parse_group, _resolve, lookup, resolve, resolve_dependency_groups
**Parameters:** _NORMALIZE_PATTERN

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/direct_url.py`
**Classes:** ArchiveInfo, DirInfo, DirectUrl, DirectUrlValidationError, VcsInfo, _DirectUrlRequiredKeyError, _FromMappingProtocol
**Functions:** __dir__, __init__, __str__, _from_dict, _get, _get_object, _get_required, _json_dict_factory, _strip_auth_from_netloc, _strip_url, from_dict, to_dict, validate
**Parameters:** _PEP610_USER_PASS_ENV_VARS_REGEX, _T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/errors.py`
**Classes:** ExceptionGroup, _ErrorCollector
**Functions:** __dir__, __init__, __repr__, collect, error, finalize, on_exit

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/licenses/__init__.py`
**Classes:** InvalidLicenseExpression
**Functions:** __dir__, canonicalize_license_expression

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/licenses/_spdx.py`
**Classes:** SPDXException, SPDXLicense
**Parameters:** VERSION

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/markers.py`
**Classes:** Environment, InvalidMarker, Marker, UndefinedComparison, UndefinedEnvironmentName
**Functions:** __and__, __dir__, __eq__, __getstate__, __hash__, __init__, __or__, __repr__, __setstate__, __str__, _eval_op, _evaluate_markers, _format_full_version, _format_marker, _from_markers, _normalize, _normalize_extra_values, _normalize_extras, _repair_python_full_version, default_environment, evaluate
**Parameters:** MARKERS_ALLOWING_SET, MARKERS_REQUIRING_VERSION

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/metadata.py`
**Classes:** InvalidMetadata, Metadata, RFC822Message, RFC822Policy, RawMetadata, _Validator
**Functions:** __dir__, __get__, __init__, __set_name__, _get_payload, _invalid_metadata, _parse_keywords, _parse_project_urls, _process_description_content_type, _process_dynamic, _process_import_names, _process_license_expression, _process_license_files, _process_metadata_version, _process_name, _process_provides_extra, _process_requires_dist, _process_requires_python, _process_summary, _process_version, _write_metadata, as_bytes, as_rfc822, from_email, from_raw, header_store_parse, parse_email
**Parameters:** T, _DICT_FIELDS, _EMAIL_TO_RAW_MAPPING, _LIST_FIELDS, _NOT_FOUND, _RAW_TO_EMAIL_MAPPING, _REQUIRED_ATTRS, _STRING_FIELDS, _VALID_METADATA_VERSIONS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/pylock.py`
**Classes:** Package, PackageArchive, PackageDirectory, PackageSdist, PackageVcs, PackageWheel, Pylock, PylockSelectError, PylockUnsupportedVersionError, PylockValidationError, _FromMappingProtocol, _PylockRequiredKeyError
**Functions:** __dir__, __init__, __str__, _from_dict, _get, _get_as, _get_object, _get_required, _get_required_as, _get_required_sequence_of_objects, _get_sequence, _get_sequence_as, _get_sequence_of_objects, _path_name, _toml_dict_factory, _toml_key, _toml_value, _url_name, _validate_hashes, _validate_normalized_name, _validate_path_url, filename, from_dict, is_direct, is_valid_pylock_path, select, to_dict, validate
**Parameters:** _PYLOCK_FILE_NAME_RE, _T, _T2

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/requirements.py`
**Classes:** InvalidRequirement, Requirement
**Functions:** __dir__, __eq__, __getstate__, __hash__, __init__, __repr__, __setstate__, __str__, _iter_parts

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/specifiers.py`
**Classes:** BaseSpecifier, InvalidSpecifier, Specifier, SpecifierSet, _BoundaryKind, _BoundaryVersion, _LowerBound, _UpperBound
**Functions:** __and__, __contains__, __dir__, __eq__, __getstate__, __hash__, __init__, __iter__, __len__, __lt__, __repr__, __setstate__, __str__, _base_dev0, _canonical_spec, _canonical_specs, _check_arbitrary_unsatisfiable, _check_prerelease_only_ranges, _coerce_version, _compare_arbitrary, _compare_compatible, _compare_equal, _compare_greater_than, _compare_greater_than_equal, _compare_less_than, _compare_less_than_equal, _compare_not_equal, _earliest_prerelease, _filter_versions, _get_operator, _get_ranges, _get_spec_version, _get_wildcard_split, _intersect_ranges, _is_family, _is_not_suffix, _left_pad, _nearest_non_prerelease, _next_prefix_dev0, _numeric_prefix_len, _operator_cost, _pep440_filter_prereleases, _post_base, _public_version, _range_is_empty, _require_spec_version, _standard_ranges, _str, _to_ranges, _trim_release, _validate_pre, _validate_spec, _version_join, _version_split, _wildcard_ranges, contains, filter, is_unsatisfiable, operator, prereleases, version
**Parameters:** AFTER_LOCALS, AFTER_POSTS, T, _NEG_INF, _POS_INF

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/tags.py`
**Classes:** Tag, UnsortedTagsError
**Functions:** __dir__, __eq__, __getstate__, __hash__, __init__, __repr__, __setstate__, __str__, _abi3_applies, _abi3t_applies, _compute_32_bit_interpreter, _cpython_abis, _emscripten_platforms, _generic_abi, _generic_platforms, _get_config_var, _is_threaded_cpython, _linux_platforms, _mac_arch, _mac_binary_formats, _normalize_string, _py_interpreter_range, _version_nodot, abi, android_platforms, compatible_tags, cpython_tags, create_compatible_tags_selector, generic_tags, interpreter, interpreter_name, interpreter_version, ios_platforms, mac_platforms, parse_tag, platform, platform_tags, selector, sys_tags
**Parameters:** _32_BIT_INTERPRETER, _T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/utils.py`
**Classes:** InvalidName, InvalidSdistFilename, InvalidWheelFilename
**Functions:** __dir__, canonicalize_name, canonicalize_version, is_normalized_name, parse_sdist_filename, parse_wheel_filename

### `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/version.py`
**Classes:** InvalidVersion, Version, _BaseVersion, _TrimmedRelease, _Version, _VersionReplace
**Functions:** __dir__, __eq__, __ge__, __getstate__, __gt__, __hash__, __init__, __le__, __lt__, __ne__, __replace__, __repr__, __setstate__, __str__, _cmpkey, _deprecated, _key, _parse_letter_version, _parse_local_version, _str, _validate_dev, _validate_epoch, _validate_local, _validate_post, _validate_pre, _validate_release, _version, base_version, decorator, dev, epoch, from_parts, is_devrelease, is_postrelease, is_prerelease, local, major, micro, minor, normalize_pre, parse, post, pre, public, release, wrapper
**Parameters:** VERSION_PATTERN, _LETTER_NORMALIZATION, _LOCAL_PATTERN, _LOCAL_STR_RANK, _PRE_RANK, _PRE_RANK_DEV_ONLY, _PRE_RANK_STABLE, _SIMPLE_VERSION_INDICATORS, _STABLE_SUFFIX, _VERSION_PATTERN, _VERSION_PATTERN_OLD

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pkg_resources/__init__.py`
**Classes:** ContextualVersionConflict, DefaultProvider, DistInfoDistribution, Distribution, DistributionNotFound, EggInfoDistribution, EggMetadata, EggProvider, EmptyProvider, EntryPoint, Environment, ExtractionError, FileMetadata, IMetadataProvider, IResourceProvider, MemoizedZipManifests, NoDists, NullProvider, PEP440Warning, PathMetadata, PkgResourcesDeprecationWarning, Requirement, RequirementParseError, ResolutionError, ResourceManager, UnknownExtra, VersionConflict, WorkingSet, ZipManifests, ZipProvider, _LoaderProtocol, _ReqExtras, _ZipLoaderModule, manifest_mod
**Functions:** __add__, __bool__, __call__, __contains__, __dir__, __eq__, __ge__, __getattr__, __getitem__, __getstate__, __gt__, __hash__, __iadd__, __init__, __iter__, __le__, __lt__, __ne__, __repr__, __setstate__, __str__, _added_new, _always_object, _build_dep_map, _build_from_requirements, _build_master, _bypass_ensure_directory, _call_aside, _compute_dependencies, _cygwin_patch, _declare_state, _dep_map, _eager_to_zip, _extract_resource, _filter_extras, _find_adapter, _fn, _forgiving_parsed_version, _forgiving_version, _get, _get_date_and_size, _get_eager_resources, _get_metadata, _get_metadata_path, _get_metadata_path_for_display, _get_version, _handle_ns, _has, _index, _initialize, _initialize_master_working_set, _is_current, _is_egg_path, _is_unpacked_egg, _is_zip_egg, _isdir, _listdir, _macos_arch, _macos_vers, _mkstemp, _normalize_cached, _parents, _parse_extras, _parsed_pkg_info, _parts, _read_utf8_with_fallback, _rebuild_mod_path, _register, _reload_version, _resolve_dist, _resource_to_zip, _safe_segment, _set_egg, _set_parent_ns, _setup_prefix, _sget_dict, _sget_object, _sset_dict, _sset_object, _validate_resource_path, _version_from_file, _warn_on_replacement, _warn_unsafe_extraction_path, _zipinfo_name, activate, add, add_entry, as_requirement, best_match, build, can_add, check_version_conflict, cleanup_resources, clone, compatible_platforms, declare_namespace, dist, dist_factory, distributions_from_metadata, egg_name, ensure_directory, evaluate_marker, extraction_error, extras, file_ns_handler, find, find_distributions, find_eggs_in_zip, find_nothing, find_on_path, find_plugins, fixup_namespace_packages, from_filename, from_location, get_build_platform, get_cache_path, get_default_cache, get_distribution, get_entry_info, get_entry_map, get_metadata, get_metadata_lines, get_provider, get_resource_filename, get_resource_stream, get_resource_string, get_supported_platform, has_metadata, has_resource, has_version, hashcmp, insert_on, invalid_marker, is_version_line, issue_warning, iter_entry_points, key, load, load_entry_point, load_module, markers_pass, metadata_isdir, metadata_listdir, non_empty_lines, normalize_path, null_ns_handler, obtain, parse, parse_group, parse_map, parse_requirements, parsed_version, position_in_sys_path, postprocess, register_finder, register_loader_type, register_namespace_handler, remove, report, req, reqs_for_extra, require, required_by, requirers, requirers_str, requires, resolve, resolve_egg_link, resource_exists, resource_filename, resource_isdir, resource_listdir, resource_stream, resource_string, run_script, safe_extra, safe_listdir, safe_name, safe_sys_path_index, safe_version, scan, set_extraction_path, split_sections, subscribe, to_filename, version, with_context, zipinfo
**Parameters:** BINARY_DIST, CHECKOUT_DIST, DEVELOP_DIST, EGG_DIST, EGG_NAME, EQEQ, MODULE, PKG_INFO, PY_MAJOR, SOURCE_DIST, WRITE_SUPPORT, _LOCALE_ENCODING, _PEP440_FALLBACK, _T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/__init__.py`
**Functions:** _set_platform_dir_class, site_cache_dir, site_cache_path, site_config_dir, site_config_path, site_data_dir, site_data_path, site_runtime_dir, site_runtime_path, user_cache_dir, user_cache_path, user_config_dir, user_config_path, user_data_dir, user_data_path, user_desktop_dir, user_desktop_path, user_documents_dir, user_documents_path, user_downloads_dir, user_downloads_path, user_log_dir, user_log_path, user_music_dir, user_music_path, user_pictures_dir, user_pictures_path, user_runtime_dir, user_runtime_path, user_state_dir, user_state_path, user_videos_dir, user_videos_path

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/__main__.py`
**Functions:** main
**Parameters:** PROPS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/android.py`
**Classes:** Android
**Functions:** _android_documents_folder, _android_downloads_folder, _android_folder, _android_music_folder, _android_pictures_folder, _android_videos_folder, site_cache_dir, site_config_dir, site_data_dir, site_runtime_dir, user_cache_dir, user_config_dir, user_data_dir, user_desktop_dir, user_documents_dir, user_downloads_dir, user_log_dir, user_music_dir, user_pictures_dir, user_runtime_dir, user_state_dir, user_videos_dir

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/api.py`
**Classes:** PlatformDirsABC
**Functions:** __init__, _append_app_name_and_version, _first_item_as_path_if_multipath, _optionally_create_directory, iter_cache_dirs, iter_cache_paths, iter_config_dirs, iter_config_paths, iter_data_dirs, iter_data_paths, iter_runtime_dirs, iter_runtime_paths, site_cache_dir, site_cache_path, site_config_dir, site_config_path, site_data_dir, site_data_path, site_runtime_dir, site_runtime_path, user_cache_dir, user_cache_path, user_config_dir, user_config_path, user_data_dir, user_data_path, user_desktop_dir, user_desktop_path, user_documents_dir, user_documents_path, user_downloads_dir, user_downloads_path, user_log_dir, user_log_path, user_music_dir, user_music_path, user_pictures_dir, user_pictures_path, user_runtime_dir, user_runtime_path, user_state_dir, user_state_path, user_videos_dir, user_videos_path

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/macos.py`
**Classes:** MacOS
**Functions:** site_cache_dir, site_cache_path, site_config_dir, site_data_dir, site_data_path, site_runtime_dir, user_cache_dir, user_config_dir, user_data_dir, user_desktop_dir, user_documents_dir, user_downloads_dir, user_log_dir, user_music_dir, user_pictures_dir, user_runtime_dir, user_state_dir, user_videos_dir

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/unix.py`
**Classes:** Unix
**Functions:** _get_user_dirs_folder, _get_user_media_dir, _site_config_dirs, _site_data_dirs, getuid, iter_config_dirs, iter_data_dirs, site_cache_dir, site_cache_path, site_config_dir, site_config_path, site_data_dir, site_data_path, site_runtime_dir, user_cache_dir, user_config_dir, user_data_dir, user_desktop_dir, user_documents_dir, user_downloads_dir, user_log_dir, user_music_dir, user_pictures_dir, user_runtime_dir, user_state_dir, user_videos_dir

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/version.py`
**Parameters:** COMMIT_ID, TYPE_CHECKING, VERSION_TUPLE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/windows.py`
**Classes:** Windows
**Functions:** _append_parts, _pick_get_win_folder, get_win_folder_from_env_vars, get_win_folder_from_registry, get_win_folder_if_csidl_name_not_env_var, get_win_folder_via_ctypes, site_cache_dir, site_config_dir, site_data_dir, site_runtime_dir, user_cache_dir, user_config_dir, user_data_dir, user_desktop_dir, user_documents_dir, user_downloads_dir, user_log_dir, user_music_dir, user_pictures_dir, user_runtime_dir, user_state_dir, user_videos_dir

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/__init__.py`
**Functions:** format, highlight, lex

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/__main__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/console.py`
**Functions:** ansiformat, colorize, reset_color

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/filter.py`
**Classes:** Filter, FunctionFilter
**Functions:** __init__, _apply, apply_filters, filter, simplefilter

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/filters/__init__.py`
**Classes:** CodeTagFilter, ErrorToken, GobbleFilter, KeywordCaseFilter, NameHighlightFilter, RaiseOnErrorTokenFilter, SymbolFilter, TokenMergeFilter, VisibleWhitespaceFilter
**Functions:** __init__, _replace_special, filter, find_filter_class, get_all_filters, get_filter_by_name, gobble, replacefunc
**Parameters:** FILTERS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatter.py`
**Classes:** Formatter
**Functions:** __class_getitem__, __init__, _lookup_style, format, get_style_defs

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatters/__init__.py`
**Classes:** _automodule
**Functions:** __getattr__, _fn_matches, _load_formatters, find_formatter_class, get_all_formatters, get_formatter_by_name, get_formatter_for_filename, load_formatter_from_file

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatters/_mapping.py`
**Parameters:** FORMATTERS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexer.py`
**Classes:** DelegatingLexer, ExtendedRegexLexer, Lexer, LexerContext, LexerMeta, ProfilingRegexLexer, ProfilingRegexLexerMeta, RegexLexer, RegexLexerMeta, _PseudoMatch, _This, _inherit, combined, default, include, words
**Functions:** __call__, __init__, __new__, __repr__, _preprocess_lexer_input, _process_new_state, _process_regex, _process_state, _process_token, add_filter, analyse_text, bygroups, callback, do_insertions, end, get, get_tokendefs, get_tokens, get_tokens_unprocessed, group, groupdict, groups, match_func, process_tokendef, start, streamer, using

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/__init__.py`
**Classes:** _automodule
**Functions:** __getattr__, _fn_matches, _iter_lexerclasses, _load_lexers, find_lexer_class, find_lexer_class_by_name, find_lexer_class_for_filename, get_all_lexers, get_lexer_by_name, get_lexer_for_filename, get_lexer_for_mimetype, get_rating, guess_lexer, guess_lexer_for_filename, load_lexer_from_file, type_sort
**Parameters:** COMPAT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/_mapping.py`
**Parameters:** LEXERS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/python.py`
**Classes:** CythonLexer, DgLexer, NumPyLexer, Python2Lexer, Python2TracebackLexer, PythonConsoleLexer, PythonLexer, PythonTracebackLexer, _PythonConsoleLexerBase, _ReplaceInnerCode
**Functions:** __init__, analyse_text, fstring_rules, get_tokens_unprocessed, innerstring_rules
**Parameters:** EXTRA_KEYWORDS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/modeline.py`
**Functions:** get_filetype_from_buffer, get_filetype_from_line

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/plugin.py`
**Functions:** find_plugin_filters, find_plugin_formatters, find_plugin_lexers, find_plugin_styles, iter_entry_points
**Parameters:** FILTER_ENTRY_POINT, FORMATTER_ENTRY_POINT, LEXER_ENTRY_POINT, STYLE_ENTRY_POINT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/regexopt.py`
**Functions:** make_charset, regex_opt, regex_opt_inner
**Parameters:** CS_ESCAPE, FIRST_ELEMENT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/scanner.py`
**Classes:** EndOfText, Scanner
**Functions:** __init__, __repr__, check, eos, get_char, scan, test

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/sphinxext.py`
**Classes:** PygmentsDoc
**Functions:** document_filters, document_formatters, document_lexers, document_lexers_overview, format_link, run, setup, write_row, write_seperator
**Parameters:** FILTERDOC, FMTERDOC, LEXERDOC, MODULEDOC

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/style.py`
**Classes:** Style, StyleMeta
**Functions:** __iter__, __len__, __new__, colorformat, list_styles, style_for_token, styles_token

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/styles/__init__.py`
**Functions:** get_all_styles, get_style_by_name
**Parameters:** STYLE_MAP, _STYLE_NAME_TO_MODULE_MAP

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/styles/_mapping.py`
**Parameters:** STYLES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/token.py`
**Classes:** _TokenType
**Functions:** __contains__, __copy__, __deepcopy__, __getattr__, __init__, __repr__, is_token_subtype, split, string_to_tokentype
**Parameters:** STANDARD_TYPES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/unistring.py`
**Functions:** _handle_runs, allexcept, combine

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/util.py`
**Classes:** ClassNotFound, Future, OptionError, UnclosingTextIOWrapper
**Functions:** close, docstring_headline, doctype_matches, duplicates_removed, format_lines, get, get_bool_opt, get_choice_opt, get_int_opt, get_list_opt, guess_decode, guess_decode_from_terminal, html_doctype_matches, looks_like_xml, make_analysator, shebang_matches, surrogatepair, terminal_encoding, text_analyse

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_impl.py`
**Classes:** BackendUnavailable, BuildBackendHookCaller, HookMissing, SubprocessRunner, UnsupportedOperation
**Functions:** __call__, __init__, _call_hook, _supported_features, build_editable, build_sdist, build_wheel, default_subprocess_runner, get_requires_for_build_editable, get_requires_for_build_sdist, get_requires_for_build_wheel, norm_and_check, prepare_metadata_for_build_editable, prepare_metadata_for_build_wheel, quiet_subprocess_runner, read_json, subprocess_runner, write_json

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_in_process/__init__.py`
**Functions:** _in_proc_script_path

### `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py`
**Classes:** BackendUnavailable, GotUnsupportedOperation, HookMissing, _BackendPathFinder, _DummyException
**Functions:** __init__, _build_backend, _dist_info_files, _find_already_built_wheel, _get_wheel_metadata_from_wheel, _supported_features, build_editable, build_sdist, build_wheel, find_distributions, find_spec, get_requires_for_build_editable, get_requires_for_build_sdist, get_requires_for_build_wheel, main, prepare_metadata_for_build_editable, prepare_metadata_for_build_wheel, read_json, write_json
**Parameters:** HOOK_NAMES, WHEEL_BUILT_MARKER

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/__init__.py`
**Functions:** _check_cryptography, check_compatibility

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/__version__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/_internal_utils.py`
**Functions:** to_native_string, unicode_is_ascii
**Parameters:** HEADER_VALIDATORS, _HEADER_VALIDATORS_BYTE, _HEADER_VALIDATORS_STR, _VALID_HEADER_NAME_RE_BYTE, _VALID_HEADER_NAME_RE_STR, _VALID_HEADER_VALUE_RE_BYTE, _VALID_HEADER_VALUE_RE_STR

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/adapters.py`
**Classes:** BaseAdapter, HTTPAdapter
**Functions:** SOCKSProxyManager, __getstate__, __init__, __setstate__, _urllib3_request_context, add_headers, build_connection_pool_key_attributes, build_response, cert_verify, close, get_connection, get_connection_with_tls_context, init_poolmanager, proxy_headers, proxy_manager_for, request_url, send
**Parameters:** DEFAULT_POOLBLOCK, DEFAULT_POOLSIZE, DEFAULT_POOL_TIMEOUT, DEFAULT_RETRIES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/api.py`
**Functions:** delete, get, head, options, patch, post, put, request

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/auth.py`
**Classes:** AuthBase, HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
**Functions:** __call__, __eq__, __init__, __ne__, _basic_auth_str, build_digest_header, handle_401, handle_redirect, init_per_thread_state, md5_utf8, sha256_utf8, sha512_utf8, sha_utf8
**Parameters:** A1, A2, CONTENT_TYPE_FORM_URLENCODED, CONTENT_TYPE_MULTI_PART, HA1, HA2, KD

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/certs.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/compat.py`
**Functions:** _resolve_char_detection

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/cookies.py`
**Classes:** CookieConflictError, MockRequest, MockResponse, RequestsCookieJar
**Functions:** __contains__, __delitem__, __getitem__, __getstate__, __init__, __setitem__, __setstate__, _copy_cookie_jar, _find, _find_no_duplicates, add_header, add_unredirected_header, cookiejar_from_dict, copy, create_cookie, extract_cookies_to_jar, get, get_cookie_header, get_dict, get_full_url, get_header, get_host, get_new_headers, get_origin_req_host, get_policy, get_type, getheaders, has_header, host, info, is_unverifiable, items, iteritems, iterkeys, itervalues, keys, list_domains, list_paths, merge_cookies, morsel_to_cookie, multiple_domains, origin_req_host, remove_cookie_by_name, set, set_cookie, unverifiable, update, values

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/exceptions.py`
**Classes:** ChunkedEncodingError, ConnectTimeout, ConnectionError, ContentDecodingError, FileModeWarning, HTTPError, InvalidHeader, InvalidJSONError, InvalidProxyURL, InvalidSchema, InvalidURL, JSONDecodeError, MissingSchema, ProxyError, ReadTimeout, RequestException, RequestsDependencyWarning, RequestsWarning, RetryError, SSLError, StreamConsumedError, Timeout, TooManyRedirects, URLRequired, UnrewindableBodyError
**Functions:** __init__, __reduce__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/help.py`
**Functions:** _implementation, info, main

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/hooks.py`
**Functions:** default_hooks, dispatch_hook
**Parameters:** HOOKS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/models.py`
**Classes:** PreparedRequest, Request, RequestEncodingMixin, RequestHooksMixin, Response
**Functions:** __bool__, __enter__, __exit__, __getstate__, __init__, __iter__, __nonzero__, __repr__, __setstate__, _encode_files, _encode_params, _get_idna_encoded_host, apparent_encoding, close, content, copy, deregister_hook, generate, is_permanent_redirect, is_redirect, iter_content, iter_lines, json, links, next, ok, path_url, prepare, prepare_auth, prepare_body, prepare_content_length, prepare_cookies, prepare_headers, prepare_hooks, prepare_method, prepare_url, raise_for_status, register_hook, text
**Parameters:** CONTENT_CHUNK_SIZE, DEFAULT_REDIRECT_LIMIT, ITER_CHUNK_SIZE, REDIRECT_STATI

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/packages.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/sessions.py`
**Classes:** Session, SessionRedirectMixin
**Functions:** __enter__, __exit__, __getstate__, __init__, __setstate__, close, delete, get, get_adapter, get_redirect_target, head, merge_environment_settings, merge_hooks, merge_setting, mount, options, patch, post, prepare_request, put, rebuild_auth, rebuild_method, rebuild_proxies, request, resolve_redirects, send, session, should_strip_auth

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/status_codes.py`
**Functions:** _init, doc

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/structures.py`
**Classes:** CaseInsensitiveDict, LookupDict
**Functions:** __delitem__, __eq__, __getitem__, __init__, __iter__, __len__, __repr__, __setitem__, copy, get, lower_items

### `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/utils.py`
**Functions:** _parse_content_type_header, _validate_header_part, add_dict_to_cookiejar, address_in_network, atomic_open, check_header_validity, default_headers, default_user_agent, dict_from_cookiejar, dict_to_sequence, dotted_netmask, extract_zipped_paths, from_key_val_list, get_auth_from_url, get_encoding_from_headers, get_encodings_from_content, get_environ_proxies, get_netrc_auth, get_proxy, get_unicode_from_response, guess_filename, guess_json_utf, is_ipv4_address, is_valid_cidr, iter_slices, parse_dict_header, parse_header_links, parse_list_header, prepend_scheme_if_needed, proxy_bypass, proxy_bypass_registry, requote_uri, resolve_proxies, rewind_body, select_proxy, set_environ, should_bypass_proxies, stream_decode_response_unicode, super_len, to_key_val_list, unquote_header_value, unquote_unreserved, urldefragauth
**Parameters:** DEFAULT_ACCEPT_ENCODING, DEFAULT_CA_BUNDLE_PATH, DEFAULT_PORTS, NETRC_FILES, UNRESERVED_SET

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/providers.py`
**Classes:** AbstractProvider, Preference
**Functions:** __lt__, find_matches, get_dependencies, get_preference, identify, is_satisfied_by, narrow_requirement_selection

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/reporters.py`
**Classes:** BaseReporter
**Functions:** adding_requirement, ending, ending_round, pinning, rejecting_candidate, resolving_conflicts, starting, starting_round

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/abstract.py`
**Classes:** AbstractResolver, Result
**Functions:** __init__, resolve

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/criterion.py`
**Classes:** Criterion
**Functions:** __init__, __repr__, iter_parent, iter_requirement

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/exceptions.py`
**Classes:** InconsistentCandidate, RequirementsConflicted, ResolutionError, ResolutionImpossible, ResolutionTooDeep, ResolverException
**Functions:** __init__, __str__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/resolution.py`
**Classes:** Resolution, Resolver
**Functions:** __init__, _add_to_criteria, _attempt_to_pin_criterion, _backjump, _build_result, _extract_causes, _get_preference, _get_updated_criteria, _has_route_to_root, _is_current_pin_satisfying, _patch_criteria, _push_new_state, _remove_information_from_criteria, _rollback_states, _save_state, resolve, state

### `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/structs.py`
**Classes:** DirectedGraph, IteratorMapping, RequirementInformation, State, _FactoryIterableView, _SequenceIterableView
**Functions:** __bool__, __contains__, __getitem__, __init__, __iter__, __len__, __repr__, add, build_iter_view, connect, connected, copy, iter_children, iter_edges, iter_parents, remove
**Parameters:** CT, KT, RT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/__init__.py`
**Functions:** get_console, inspect, print, print_json, reconfigure
**Parameters:** _IMPORT_CWD

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/__main__.py`
**Classes:** ColorBox
**Functions:** __rich_console__, __rich_measure__, comparison, make_test_card

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_cell_widths.py`
**Parameters:** CELL_WIDTHS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_emoji_codes.py`
**Parameters:** EMOJI

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_emoji_replace.py`
**Functions:** _emoji_replace, do_replace

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_export_format.py`
**Parameters:** CONSOLE_HTML_FORMAT, CONSOLE_SVG_FORMAT, _SVG_CLASSES_PREFIX, _SVG_FONT_FAMILY

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_extension.py`
**Functions:** load_ipython_extension

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_fileno.py`
**Functions:** get_fileno

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_inspect.py`
**Classes:** Inspect
**Functions:** __init__, __rich__, _first_paragraph, _get_formatted_doc, _get_signature, _make_title, _render, get_object_types_mro, get_object_types_mro_as_strings, is_object_one_of_types, safe_getattr, sort_items

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_log_render.py`
**Classes:** LogRender
**Functions:** __call__, __init__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_loop.py`
**Functions:** loop_first, loop_first_last, loop_last
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_null_file.py`
**Classes:** NullFile
**Functions:** __enter__, __exit__, __iter__, __next__, close, fileno, flush, isatty, read, readable, readline, readlines, seek, seekable, tell, truncate, writable, write, writelines
**Parameters:** NULL_FILE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_palettes.py`
**Parameters:** EIGHT_BIT_PALETTE, STANDARD_PALETTE, WINDOWS_PALETTE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_pick.py`
**Functions:** pick_bool

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_ratio.py`
**Classes:** E, Edge
**Functions:** ratio_distribute, ratio_reduce, ratio_resolve

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_spinners.py`
**Parameters:** SPINNERS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_stack.py`
**Classes:** Stack
**Functions:** push, top
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_timer.py`
**Functions:** timer

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_win32_console.py`
**Classes:** CONSOLE_CURSOR_INFO, CONSOLE_SCREEN_BUFFER_INFO, LegacyWindowsError, LegacyWindowsTerm, WindowsCoordinates
**Functions:** FillConsoleOutputAttribute, FillConsoleOutputCharacter, GetConsoleCursorInfo, GetConsoleMode, GetConsoleScreenBufferInfo, GetStdHandle, SetConsoleCursorInfo, SetConsoleCursorPosition, SetConsoleTextAttribute, SetConsoleTitle, __init__, _get_cursor_size, cursor_position, erase_end_of_line, erase_line, erase_start_of_line, from_param, hide_cursor, move_cursor_backward, move_cursor_down, move_cursor_forward, move_cursor_to, move_cursor_to_column, move_cursor_up, screen_size, set_title, show_cursor, write_styled, write_text
**Parameters:** ANSI_TO_WINDOWS, BRIGHT_BIT, COORD, ENABLE_VIRTUAL_TERMINAL_PROCESSING, STDOUT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_windows.py`
**Classes:** WindowsConsoleFeatures
**Functions:** get_windows_console_features

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_windows_renderer.py`
**Functions:** legacy_windows_render

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_wrap.py`
**Functions:** divide_line, words

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/abc.py`
**Classes:** Foo, RichRenderable
**Functions:** __subclasshook__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/align.py`
**Classes:** Align, VerticalCenter
**Functions:** __init__, __repr__, __rich_console__, __rich_measure__, blank_lines, center, generate_segments, left, right

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/ansi.py`
**Classes:** AnsiDecoder, _AnsiToken
**Functions:** __init__, _ansi_tokenize, decode, decode_line, read
**Parameters:** SGR_STYLE_MAP

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/bar.py`
**Classes:** Bar
**Functions:** __init__, __repr__, __rich_console__, __rich_measure__
**Parameters:** BEGIN_BLOCK_ELEMENTS, END_BLOCK_ELEMENTS, FULL_BLOCK

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/box.py`
**Classes:** Box
**Functions:** __init__, __repr__, __str__, get_bottom, get_plain_headed_box, get_row, get_top, substitute
**Parameters:** BOXES, LEGACY_WINDOWS_SUBSTITUTIONS, PLAIN_HEADED_SUBSTITUTIONS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/cells.py`
**Functions:** cached_cell_len, cell_len, chop_cells, get_character_cell_size, set_cell_size
**Parameters:** _SINGLE_CELLS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/color.py`
**Classes:** Color, ColorParseError, ColorSystem, ColorType
**Functions:** __repr__, __rich__, __rich_repr__, __str__, blend_rgb, default, downgrade, from_ansi, from_rgb, from_triplet, get_ansi_codes, get_truecolor, is_default, is_system_defined, parse, parse_rgb_hex, system
**Parameters:** ANSI_COLOR_NAMES, DEFAULT, EIGHT_BIT, RE_COLOR, STANDARD, TRUECOLOR, WINDOWS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/color_triplet.py`
**Classes:** ColorTriplet
**Functions:** hex, normalized, rgb

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/columns.py`
**Classes:** Columns
**Functions:** __init__, __rich_console__, add_renderable, iter_renderables

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/console.py`
**Classes:** Capture, CaptureError, Console, ConsoleDimensions, ConsoleOptions, ConsoleRenderable, ConsoleThreadLocals, Group, NewLine, NoChange, PagerContext, RenderHook, RichCast, ScreenContext, ScreenUpdate, ThemeContext
**Functions:** __enter__, __exit__, __init__, __repr__, __rich__, __rich_console__, __rich_measure__, _buffer, _buffer_index, _caller_frame_info, _check_buffer, _collect_renderables, _detect_color_system, _enter_buffer, _exit_buffer, _is_jupyter, _render_buffer, _replace, _svg_hash, _theme_stack, _write_buffer, align_append, ascii_only, begin_capture, bell, capture, check_text, clear, clear_live, color_system, control, copy, decorator, detect_legacy_windows, encoding, end_capture, escape_text, export_html, export_svg, export_text, file, get, get_style, get_svg_style, get_windows_console_features, group, height, input, is_alt_screen, is_dumb_terminal, is_terminal, line, log, make_tag, measure, on_broken_pipe, options, out, pager, pop_render_hook, pop_theme, print, print_exception, print_json, process_renderables, push_render_hook, push_theme, render, render_lines, render_str, renderables, reset_height, rule, save_html, save_svg, save_text, screen, set_alt_screen, set_live, set_window_title, show_cursor, size, status, stringify, update, update_dimensions, update_height, update_screen, update_screen_lines, update_width, use_theme, width
**Parameters:** COLOR_SYSTEMS, JUPYTER_DEFAULT_COLUMNS, JUPYTER_DEFAULT_LINES, MAX_WRITE, NO_CHANGE, WINDOWS, _COLOR_SYSTEMS_NAMES, _STDERR_FILENO, _STDIN_FILENO, _STDOUT_FILENO, _STD_STREAMS, _STD_STREAMS_OUTPUT, _TERM_COLORS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/constrain.py`
**Classes:** Constrain
**Functions:** __init__, __rich_console__, __rich_measure__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/containers.py`
**Classes:** Lines, Renderables
**Functions:** __getitem__, __init__, __iter__, __len__, __repr__, __rich_console__, __rich_measure__, __setitem__, append, extend, justify, pop
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/control.py`
**Classes:** Control
**Functions:** __init__, __rich_console__, __str__, alt_screen, bell, clear, escape_control_codes, get_codes, home, move, move_to, move_to_column, show_cursor, strip_control_codes, title

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/default_styles.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/diagnose.py`
**Functions:** report

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/emoji.py`
**Classes:** Emoji, NoEmoji
**Functions:** __init__, __repr__, __rich_console__, __str__, replace
**Parameters:** VARIANTS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/errors.py`
**Classes:** ConsoleError, LiveError, MarkupError, MissingStyle, NoAltScreen, NotRenderableError, StyleError, StyleStackError, StyleSyntaxError

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/file_proxy.py`
**Classes:** FileProxy
**Functions:** __getattr__, __init__, fileno, flush, rich_proxied_file, write

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/filesize.py`
**Functions:** _to_str, decimal, pick_unit_and_suffix

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/highlighter.py`
**Classes:** Highlighter, ISO8601Highlighter, JSONHighlighter, NullHighlighter, RegexHighlighter, ReprHighlighter
**Functions:** __call__, _combine_regex, highlight
**Parameters:** JSON_STR, JSON_WHITESPACE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/json.py`
**Classes:** JSON
**Functions:** __init__, __rich__, from_data

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/jupyter.py`
**Classes:** JupyterMixin, JupyterRenderable
**Functions:** __init__, _render_segments, _repr_mimebundle_, display, escape, print
**Parameters:** JUPYTER_HTML_FORMAT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/layout.py`
**Classes:** ColumnSplitter, Layout, LayoutError, LayoutRender, NoSplitter, RowSplitter, Splitter, _Placeholder
**Functions:** __getitem__, __init__, __rich_console__, __rich_repr__, _make_region_map, add_split, children, divide, get, get_tree_icon, map, recurse, refresh_screen, render, renderable, split, split_column, split_row, summary, tree, unsplit, update

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/live.py`
**Classes:** Live, _RefreshThread
**Functions:** __enter__, __exit__, __init__, _disable_redirect_io, _enable_redirect_io, get_renderable, is_started, process_renderables, refresh, renderable, run, start, stop, update

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/live_render.py`
**Classes:** LiveRender
**Functions:** __init__, __rich_console__, position_cursor, restore_cursor, set_renderable

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/logging.py`
**Classes:** RichHandler
**Functions:** __init__, divide, emit, get_level_text, render, render_message
**Parameters:** FORMAT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/markup.py`
**Classes:** Tag
**Functions:** __str__, _parse, escape, escape_backslashes, markup, pop_style, render
**Parameters:** MARKUP, RE_HANDLER, RE_TAGS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/measure.py`
**Classes:** Measurement
**Functions:** clamp, get, measure_renderables, normalize, span, with_maximum, with_minimum

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/padding.py`
**Classes:** Padding
**Functions:** __init__, __repr__, __rich_console__, __rich_measure__, indent, unpack

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/pager.py`
**Classes:** Pager, SystemPager
**Functions:** _pager, show

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/palette.py`
**Classes:** ColorBox, Palette
**Functions:** __getitem__, __init__, __rich__, __rich_console__, get_color_distance, match

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/panel.py`
**Classes:** Panel
**Functions:** __init__, __rich_console__, __rich_measure__, _subtitle, _title, align_text, fit

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/pretty.py`
**Classes:** BrokenRepr, Node, Pretty, RichFormatter, StockKeepingUnit, Thing, _Line
**Functions:** __call__, __init__, __repr__, __rich_console__, __rich_measure__, __str__, _get_attr_fields, _get_braces_for_array, _get_braces_for_defaultdict, _get_braces_for_deque, _has_default_namedtuple_repr, _ipy_display_hook, _is_attr_object, _is_dataclass_repr, _is_namedtuple, _safe_isinstance, _traverse, check_length, display_hook, expand, expandable, install, is_expandable, iter_attrs, iter_rich_args, iter_tokens, pprint, pretty_repr, render, to_repr, traverse
**Parameters:** _CONTAINERS, _MAPPING_CONTAINERS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/progress.py`
**Classes:** BarColumn, DownloadColumn, FileSizeColumn, MofNCompleteColumn, Progress, ProgressColumn, ProgressSample, RenderableColumn, SpinnerColumn, Task, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, TotalFileSizeColumn, TransferSpeedColumn, _ReadContext, _Reader, _TrackThread
**Functions:** __call__, __enter__, __exit__, __init__, __iter__, __next__, __rich__, _reset, add_task, advance, close, closed, console, elapsed, fileno, finished, get_default_columns, get_renderable, get_renderables, get_table_column, get_time, isatty, make_tasks_table, mode, name, open, percentage, read, readable, readinto, readline, readlines, refresh, remaining, remove_task, render, render_speed, reset, run, seek, seekable, set_spinner, speed, start, start_task, started, stop, stop_task, task_ids, tasks, tell, time_remaining, track, update, wrap_file, writable, write, writelines
**Parameters:** _I

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/progress_bar.py`
**Classes:** ProgressBar
**Functions:** __init__, __repr__, __rich_console__, __rich_measure__, _get_pulse_segments, _render_pulse, percentage_completed, update
**Parameters:** PULSE_SIZE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/prompt.py`
**Classes:** Confirm, FloatPrompt, IntPrompt, InvalidResponse, Prompt, PromptBase, PromptError
**Functions:** __call__, __init__, __rich__, ask, check_choice, get_input, make_prompt, on_validate_error, pre_prompt, process_response, render_default

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/protocol.py`
**Functions:** is_renderable, rich_cast
**Parameters:** _GIBBERISH

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/region.py`
**Classes:** Region

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/repr.py`
**Classes:** Foo, ReprError
**Functions:** __rich_repr__, auto, auto_repr, auto_rich_repr, do_replace, rich_repr
**Parameters:** T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/rule.py`
**Classes:** Rule
**Functions:** __init__, __repr__, __rich_console__, __rich_measure__, _rule_line

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/scope.py`
**Functions:** render_scope, sort_items, test

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/screen.py`
**Classes:** Screen
**Functions:** __init__, __rich_console__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/segment.py`
**Classes:** ControlType, Segment, SegmentLines, Segments
**Functions:** __bool__, __init__, __rich_console__, __rich_repr__, _split_cells, adjust_line_length, align_bottom, align_middle, align_top, apply_style, cell_length, divide, filter_control, get_line_length, get_shape, is_control, line, remove_color, set_shape, simplify, split_and_crop_lines, split_cells, split_lines, strip_links, strip_styles
**Parameters:** BELL, CARRIAGE_RETURN, CLEAR, CURSOR_BACKWARD, CURSOR_DOWN, CURSOR_FORWARD, CURSOR_MOVE_TO, CURSOR_MOVE_TO_COLUMN, CURSOR_UP, DISABLE_ALT_SCREEN, ENABLE_ALT_SCREEN, ERASE_IN_LINE, HIDE_CURSOR, HOME, SET_WINDOW_TITLE, SHOW_CURSOR

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/spinner.py`
**Classes:** Spinner
**Functions:** __init__, __rich_console__, __rich_measure__, render, update

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/status.py`
**Classes:** Status
**Functions:** __enter__, __exit__, __init__, __rich__, console, renderable, start, stop, update

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/style.py`
**Classes:** Style, StyleStack, _Bit
**Functions:** __add__, __bool__, __eq__, __get__, __hash__, __init__, __ne__, __repr__, __rich_repr__, __str__, _add, _make_ansi_codes, _make_color, background_style, bgcolor, chain, clear_meta_and_links, color, combine, copy, current, from_color, from_meta, get_html_style, link, link_id, meta, normalize, null, on, parse, pick_first, pop, push, render, test, transparent_background, update_link, without_color
**Parameters:** NULL_STYLE, STYLE_ATTRIBUTES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/styled.py`
**Classes:** Styled
**Functions:** __init__, __rich_console__, __rich_measure__

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/syntax.py`
**Classes:** ANSISyntaxTheme, PaddingProperty, PygmentsSyntaxTheme, Syntax, SyntaxTheme, _SyntaxHighlightRange
**Functions:** __get__, __init__, __rich_console__, __rich_measure__, __set__, _apply_stylized_ranges, _get_base_style, _get_code_index_for_syntax_position, _get_line_numbers_color, _get_number_styles, _get_syntax, _get_token_color, _numbers_column_width, _process_code, default_lexer, from_path, get_background_style, get_style_for_token, get_theme, guess_lexer, highlight, lexer, line_tokenize, stylize_range, tokens_to_spans
**Parameters:** DEFAULT_THEME, NUMBERS_COLUMN_DEFAULT_PADDING, RICH_SYNTAX_THEMES, WINDOWS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/table.py`
**Classes:** Column, Row, Table, _Cell
**Functions:** __init__, __rich_console__, __rich_measure__, _calculate_column_widths, _collapse_widths, _extra_width, _get_cells, _get_padding_width, _measure_column, _render, add_cell, add_column, add_row, add_section, align_cell, cells, copy, expand, flexible, get_padding, get_row_style, grid, header, padding, render_annotation, row_count

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/terminal_theme.py`
**Classes:** TerminalTheme
**Functions:** __init__
**Parameters:** DEFAULT_TERMINAL_THEME, DIMMED_MONOKAI, MONOKAI, NIGHT_OWLISH, SVG_EXPORT_THEME

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/text.py`
**Classes:** Span, Text
**Functions:** __add__, __bool__, __contains__, __eq__, __getitem__, __init__, __len__, __repr__, __rich_console__, __rich_measure__, __str__, _trim_spans, align, append, append_text, append_tokens, apply_meta, assemble, blank_copy, cell_len, copy, copy_styles, detect_indentation, divide, expand_tabs, extend, extend_style, fit, flatten_spans, from_ansi, from_markup, get_current_style, get_style_at_offset, get_text_at, highlight_regex, highlight_words, iter_text, join, markup, move, on, pad, pad_left, pad_right, plain, remove_suffix, render, right_crop, rstrip, rstrip_end, set_length, spans, split, styled, stylize, stylize_before, truncate, with_indent_guides, wrap

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/theme.py`
**Classes:** Theme, ThemeStack, ThemeStackError
**Functions:** __init__, config, from_file, pop_theme, push_theme, read

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/themes.py`
**Parameters:** DEFAULT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/traceback.py`
**Classes:** Frame, PathHighlighter, Stack, Trace, Traceback, _SyntaxError
**Functions:** __init__, __rich_console__, _guess_lexer, _iter_syntax_lines, _render_stack, _render_syntax_error, bar, error, excepthook, extract, foo, from_exception, get_locals, install, ipy_display_traceback, ipy_excepthook_closure, ipy_show_traceback, render_locals, render_stack, safe_str
**Parameters:** LEXERS, LOCALS_MAX_LENGTH, LOCALS_MAX_STRING, WINDOWS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/tree.py`
**Classes:** Tree
**Functions:** __init__, __rich_console__, __rich_measure__, add, make_guide
**Parameters:** ASCII_GUIDES, TREE_GUIDES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/_parser.py`
**Classes:** DEPRECATED_DEFAULT, Flags, NestedDict, Output, TOMLDecodeError
**Functions:** __init__, add_pending, append_nest_to_list, create_dict_rule, create_list_rule, finalize_pending, get_or_create_nest, is_, is_unicode_scalar_value, key_value_rule, load, loads, make_safe_parse_float, parse_array, parse_basic_str, parse_basic_str_escape, parse_basic_str_escape_multiline, parse_hex_char, parse_inline_table, parse_key, parse_key_part, parse_key_value_pair, parse_literal_str, parse_multiline_str, parse_one_line_basic_str, parse_value, safe_parse_float, set, skip_chars, skip_comment, skip_comments_and_array_ws, skip_until, unset_all
**Parameters:** TYPE_CHECKING

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/_re.py`
**Functions:** cached_tz, match_to_datetime, match_to_localtime, match_to_number
**Parameters:** TYPE_CHECKING

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/_types.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli_w/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli_w/_writer.py`
**Classes:** Context
**Functions:** __init__, dump, dumps, format_decimal, format_inline_array, format_inline_table, format_key_part, format_literal, format_string, gen_table_chunks, is_aot, is_suitable_inline_table
**Parameters:** ARRAY_TYPES, ASCII_CTRL, BARE_KEY_CHARS, COMPACT_ESCAPES, ILLEGAL_BASIC_STR_CHARS, MAX_LINE_LENGTH, TYPE_CHECKING

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_api.py`
**Classes:** SSLContext, TruststoreSSLObject
**Functions:** __class__, __init__, _get_unverified_chain_bytes, _verify_peercerts, cert_store_stats, check_hostname, do_handshake, extract_from_ssl, get_ca_certs, get_ciphers, hostname_checks_common_name, inject_into_ssl, keylog_filename, load_cert_chain, load_default_certs, load_verify_locations, maximum_version, minimum_version, options, post_handshake_auth, protocol, security_level, session_stats, set_alpn_protocols, set_ciphers, set_default_verify_paths, set_npn_protocols, verify_flags, verify_mode, wrap_bio, wrap_socket

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_macos.py`
**Classes:** CFConst
**Functions:** _bytes_to_cf_data_ref, _bytes_to_cf_string, _cf_string_ref_to_str, _configure_context, _der_certs_to_cf_cert_array, _handle_osstatus, _load_cdll, _verify_peercerts_impl, _verify_peercerts_impl_macos_10_13, _verify_peercerts_impl_macos_10_14

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_openssl.py`
**Functions:** _capath_contains_certs, _configure_context, _verify_peercerts_impl
**Parameters:** _CA_FILE_CANDIDATES, _HASHED_CERT_FILENAME_RE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_ssl_constants.py`
**Functions:** _set_ssl_context_verify_mode

### `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_windows.py`
**Classes:** CERT_CHAIN_CONTEXT, CERT_CHAIN_ELEMENT, CERT_CHAIN_ENGINE_CONFIG, CERT_CHAIN_PARA, CERT_CHAIN_POLICY_PARA, CERT_CHAIN_POLICY_STATUS, CERT_CONTEXT, CERT_ENHKEY_USAGE, CERT_SIMPLE_CHAIN, CERT_TRUST_STATUS, CERT_USAGE_MATCH, SSL_EXTRA_CERT_CHAIN_POLICY_PARA
**Functions:** _configure_context, _get_and_verify_cert_chain, _handle_win_error, _verify_peercerts_impl, _verify_using_custom_ca_certs
**Parameters:** AUTHTYPE_SERVER, CERT_CHAIN_POLICY_ALLOW_TESTROOT_FLAG, CERT_CHAIN_POLICY_ALLOW_UNKNOWN_CA_FLAG, CERT_CHAIN_POLICY_IGNORE_ALL_NOT_TIME_VALID_FLAGS, CERT_CHAIN_POLICY_IGNORE_ALL_REV_UNKNOWN_FLAGS, CERT_CHAIN_POLICY_IGNORE_INVALID_BASIC_CONSTRAINTS_FLAG, CERT_CHAIN_POLICY_IGNORE_INVALID_NAME_FLAG, CERT_CHAIN_POLICY_IGNORE_INVALID_POLICY_FLAG, CERT_CHAIN_POLICY_IGNORE_WRONG_USAGE_FLAG, CERT_CHAIN_POLICY_SSL, CERT_CHAIN_POLICY_TRUST_TESTROOT_FLAG, CERT_CHAIN_POLICY_VERIFY_MODE_NONE_FLAGS, CERT_CHAIN_REVOCATION_CHECK_CHAIN, CERT_CHAIN_REVOCATION_CHECK_END_CERT, CERT_STORE_ADD_USE_EXISTING, CERT_STORE_PROV_MEMORY, FORMAT_MESSAGE_FROM_SYSTEM, FORMAT_MESSAGE_IGNORE_INSERTS, HCERTCHAINENGINE, HCERTSTORE, HCRYPTPROV_LEGACY, OID_PKIX_KP_SERVER_AUTH, PCCERT_CHAIN_CONTEXT, PCCERT_CONTEXT, PCERT_CHAIN_CONTEXT, PCERT_CHAIN_ELEMENT, PCERT_CHAIN_ENGINE_CONFIG, PCERT_CHAIN_PARA, PCERT_CHAIN_POLICY_PARA, PCERT_CHAIN_POLICY_STATUS, PCERT_CONTEXT, PCERT_ENHKEY_USAGE, PCERT_SIMPLE_CHAIN, PHCERTCHAINENGINE, PKCS_7_ASN_ENCODING, SECURITY_FLAG_IGNORE_CERT_CN_INVALID, USAGE_MATCH_TYPE_OR, X509_ASN_ENCODING

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/__init__.py`
**Functions:** add_stderr_logger, disable_warnings, request
**Parameters:** _DEFAULT_POOL

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_base_connection.py`
**Classes:** BaseHTTPConnection, BaseHTTPSConnection, ProxyConfig, _ResponseOptions
**Functions:** __init__, close, connect, getresponse, has_connected_to_proxy, is_closed, is_connected, request, set_tunnel
**Parameters:** _TYPE_BODY

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_collections.py`
**Classes:** HTTPHeaderDict, HTTPHeaderDictItemView, HasGettableStringKeys, RecentlyUsedContainer, _Sentinel
**Functions:** __contains__, __delitem__, __eq__, __getitem__, __init__, __ior__, __iter__, __len__, __ne__, __or__, __repr__, __ror__, __setitem__, _copy_from, _has_value_for_header, _prepare_for_method_change, add, clear, copy, discard, ensure_can_construct_http_header_dict, extend, getlist, items, iteritems, itermerged, keys, setdefault
**Parameters:** _DT, _KT, _VT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_request_methods.py`
**Classes:** RequestMethods
**Functions:** __init__, request, request_encode_body, request_encode_url, urlopen
**Parameters:** _TYPE_ENCODE_URL_FIELDS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_version.py`
**Parameters:** COMMIT_ID, TYPE_CHECKING, VERSION_TUPLE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/connection.py`
**Classes:** BaseSSLError, DummyConnection, HTTPConnection, HTTPSConnection, _WrappedAndVerifiedSocket
**Functions:** __init__, __repr__, __str__, _connect_tls_proxy, _get_default_user_agent, _match_hostname, _new_conn, _ssl_wrap_socket_and_match_hostname, _tunnel, _url_from_connection, _wrap_ipv6, _wrap_proxy_error, close, connect, getresponse, has_connected_to_proxy, host, is_closed, is_connected, proxy_is_forwarding, proxy_is_tunneling, putheader, putrequest, request, request_chunked, set_cert, set_tunnel
**Parameters:** RECENT_DATE, _CONTAINS_CONTROL_CHAR_RE, _MAXLINE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/connectionpool.py`
**Classes:** ConnectionPool, HTTPConnectionPool, HTTPSConnectionPool
**Functions:** __enter__, __exit__, __init__, __str__, _close_pool_connections, _get_conn, _get_timeout, _make_request, _new_conn, _normalize_host, _prepare_proxy, _put_conn, _raise_timeout, _url_from_pool, _validate_conn, close, connection_from_url, is_same_host, urlopen
**Parameters:** _TYPE_TIMEOUT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/__init__.py`
**Functions:** inject_into_urllib3

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/connection.py`
**Classes:** EmscriptenHTTPConnection, EmscriptenHTTPSConnection
**Functions:** __init__, close, connect, getresponse, has_connected_to_proxy, is_closed, is_connected, request, set_cert, set_tunnel

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/fetch.py`
**Classes:** _JSPIReadStream, _ReadStream, _RequestError, _StreamingError, _StreamingFetcher, _TimeoutError
**Functions:** __del__, __init__, _get_next_buffer, _is_node_js, _obj_from_dict, _run_sync_with_timeout, _show_streaming_warning, _show_timeout_warning, close, closed, has_jspi, is_closed, is_cross_origin_isolated, is_in_browser_main_thread, is_in_node, is_worker_available, onErr, onMsg, promise_resolver, readable, readinto, seekable, send, send_jspi_request, send_request, send_streaming_request, streaming_ready, wait_for_streaming_ready, writable
**Parameters:** ERROR_EXCEPTION, ERROR_TIMEOUT, HEADERS_TO_IGNORE, NODE_JSPI_ERROR, SUCCESS_EOF, SUCCESS_HEADER, _SHOWN_STREAMING_WARNING, _SHOWN_TIMEOUT_WARNING

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/request.py`
**Classes:** EmscriptenRequest
**Functions:** set_body, set_header

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/response.py`
**Classes:** EmscriptenHttpResponseWrapper, EmscriptenResponse
**Functions:** __init__, _error_catcher, _init_length, close, connection, data, drain_conn, json, read, read_chunked, release_conn, retries, stream, url

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/pyopenssl.py`
**Classes:** PyOpenSSLContext, UnsupportedExtension, WrappedSocket
**Functions:** __init__, _decref_socketios, _dnsname_to_stdlib, _real_close, _send_until_done, _set_ctx_options, _validate_dependencies_met, _verify_callback, close, extract_from_urllib3, fileno, get_subj_alt_name, getpeercert, idna_encode, inject_into_urllib3, load_cert_chain, load_verify_locations, maximum_version, minimum_version, options, recv, recv_into, selected_alpn_protocol, sendall, set_alpn_protocols, set_ciphers, set_default_verify_paths, settimeout, shutdown, verify_flags, verify_mode, version, wrap_socket
**Parameters:** SSL_WRITE_BLOCKSIZE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/socks.py`
**Classes:** SOCKSConnection, SOCKSHTTPConnectionPool, SOCKSHTTPSConnection, SOCKSHTTPSConnectionPool, SOCKSProxyManager, _TYPE_SOCKS_OPTIONS
**Functions:** __init__, _new_conn

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/exceptions.py`
**Classes:** BodyNotHttplibCompatible, ClosedPoolError, ConnectTimeoutError, DecodeError, DependencyWarning, EmptyPoolError, FullPoolError, HTTPError, HTTPWarning, HeaderParsingError, HostChangedError, IncompleteRead, InsecurePlatformWarning, InsecureRequestWarning, InvalidChunkLength, InvalidHeader, LocationParseError, LocationValueError, MaxRetryError, NameResolutionError, NewConnectionError, NotOpenSSLWarning, PoolError, ProtocolError, ProxyError, ProxySchemeUnknown, ProxySchemeUnsupported, ReadTimeoutError, RequestError, ResponseError, ResponseNotChunked, SSLError, SecurityWarning, SystemTimeWarning, TimeoutError, TimeoutStateError, URLSchemeUnknown, UnrewindableBodyError
**Functions:** __init__, __reduce__, __repr__, pool
**Parameters:** GENERIC_ERROR, SPECIFIC_ERROR, _TYPE_REDUCE_RESULT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/fields.py`
**Classes:** RequestField
**Functions:** __init__, _render_part, _render_parts, format_header_param, format_header_param_html5, format_header_param_rfc2231, format_multipart_header_param, from_tuples, guess_content_type, make_multipart, render_headers
**Parameters:** _TYPE_FIELD_VALUE, _TYPE_FIELD_VALUE_TUPLE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/filepost.py`
**Functions:** choose_boundary, encode_multipart_formdata, iter_field_objects
**Parameters:** _TYPE_FIELDS, _TYPE_FIELDS_SEQUENCE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/__init__.py`
**Functions:** extract_from_urllib3, inject_into_urllib3

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/connection.py`
**Classes:** HTTP2Connection, HTTP2Response, _LockedObject
**Functions:** __enter__, __exit__, __init__, _is_illegal_header_value, _is_legal_header_name, _new_h2_conn, close, connect, data, endheaders, get_redirect_location, getresponse, putheader, putrequest, request, send, set_tunnel
**Parameters:** RE_IS_ILLEGAL_HEADER_VALUE, RE_IS_LEGAL_HEADER_NAME, T

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/probe.py`
**Classes:** _HTTP2ProbeCache
**Functions:** __init__, _reset, _values, acquire_and_get, set_and_release
**Parameters:** _HTTP2_PROBE_CACHE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/poolmanager.py`
**Classes:** PoolKey, PoolManager, ProxyManager
**Functions:** __enter__, __exit__, __init__, _default_key_normalizer, _merge_pool_kwargs, _new_pool, _proxy_requires_url_absolute_form, _set_proxy_headers, clear, connection_from_context, connection_from_host, connection_from_pool_key, connection_from_url, proxy_from_url, urlopen
**Parameters:** SSL_KEYWORDS, _DEFAULT_BLOCKSIZE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/response.py`
**Classes:** BaseHTTPResponse, BrotliDecoder, BytesQueueBuffer, ContentDecoder, DeflateDecoder, GzipDecoder, GzipDecoderState, HTTPResponse, MultiDecoder, ZstdDecoder
**Functions:** __init__, __iter__, __len__, _decode, _decompress, _error_catcher, _flush_decoder, _fp_read, _get_decoder, _handle_chunk, _init_decoder, _init_length, _raw_read, _update_chunk_length, close, closed, connection, data, decompress, drain_conn, fileno, flush, get, get_all, get_redirect_location, getheader, getheaders, geturl, has_unconsumed_tail, info, isclosed, json, put, read, read1, read_chunked, readable, readinto, release_conn, retries, shutdown, stream, supports_chunked_reads, tell, url
**Parameters:** CONTENT_DECODERS, FIRST_MEMBER, HAS_ZSTD, OTHER_MEMBERS, REDIRECT_STATUSES, SWALLOW_DATA

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/__init__.py`

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/connection.py`
**Functions:** _has_ipv6, _set_socket_options, allowed_gai_family, create_connection, is_connection_dropped
**Parameters:** HAS_IPV6, _TYPE_SOCKET_OPTIONS

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/proxy.py`
**Functions:** connection_requires_http_tunnel

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/request.py`
**Classes:** ChunksAndContentLength, _TYPE_FAILEDTELL
**Functions:** body_to_chunks, chunk_readable, make_headers, rewind_body, set_file_position
**Parameters:** ACCEPT_ENCODING, SKIPPABLE_HEADERS, SKIP_HEADER, _METHODS_NOT_EXPECTING_BODY, _TYPE_BODY_POSITION

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/response.py`
**Functions:** assert_header_parsing, is_fp_closed, is_response_to_head

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/retry.py`
**Classes:** RequestHistory, Retry
**Functions:** __init__, __repr__, _is_connection_error, _is_method_retryable, _is_read_error, _sleep_backoff, from_int, get_backoff_time, get_retry_after, increment, is_exhausted, is_retry, new, parse_retry_after, sleep, sleep_for_retry
**Parameters:** DEFAULT_ALLOWED_METHODS, DEFAULT_BACKOFF_MAX, DEFAULT_REMOVE_HEADERS_ON_REDIRECT, RETRY_AFTER_STATUS_CODES

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssl_.py`
**Classes:** _TYPE_PEER_CERT_RET_DICT
**Functions:** _is_bpo_43522_fixed, _is_has_never_check_common_name_reliable, _is_key_file_encrypted, _ssl_wrap_socket_impl, assert_fingerprint, create_urllib3_context, is_ipaddress, resolve_cert_reqs, resolve_ssl_version, ssl_wrap_socket
**Parameters:** ALPN_PROTOCOLS, HASHFUNC_MAP, HAS_NEVER_CHECK_COMMON_NAME, IS_PYOPENSSL, OP_NO_COMPRESSION, OP_NO_TICKET, PROTOCOL_TLS, PROTOCOL_TLS_CLIENT, VERIFY_X509_PARTIAL_CHAIN, VERIFY_X509_STRICT, _TYPE_PEER_CERT_RET, _TYPE_VERSION_INFO

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssl_match_hostname.py`
**Classes:** CertificateError
**Functions:** _dnsname_match, _ipaddress_match, match_hostname

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssltransport.py`
**Classes:** SSLTransport
**Functions:** __enter__, __exit__, __init__, _decref_socketios, _ssl_io_loop, _validate_ssl_context_for_tls_in_tls, _wrap_ssl_read, cipher, close, compression, fileno, getpeercert, gettimeout, makefile, read, recv, recv_into, selected_alpn_protocol, send, sendall, settimeout, shared_ciphers, unwrap, version
**Parameters:** SSL_BLOCKSIZE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/timeout.py`
**Classes:** Timeout, _TYPE_DEFAULT
**Functions:** __init__, __repr__, _validate_timeout, clone, connect_timeout, from_float, get_connect_duration, read_timeout, resolve_default_timeout, start_connect
**Parameters:** _TYPE_TIMEOUT

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/url.py`
**Classes:** Url
**Functions:** __new__, __str__, _encode_invalid_chars, _encode_target, _idna_encode, _normalize_host, _remove_path_dot_segments, authority, hostname, netloc, parse_url, request_uri, url
**Parameters:** _BRACELESS_IPV6_ADDRZ_RE, _FRAGMENT_CHARS, _HEX_PAT, _HOST_PORT_PAT, _HOST_PORT_RE, _IPV4_PAT, _IPV4_RE, _IPV6_ADDRZ_PAT, _IPV6_ADDRZ_RE, _IPV6_PAT, _IPV6_RE, _LS32_PAT, _NORMALIZABLE_SCHEMES, _PATH_CHARS, _PERCENT_RE, _QUERY_CHARS, _REG_NAME_PAT, _SCHEME_RE, _SUB_DELIM_CHARS, _TARGET_RE, _UNRESERVED_CHARS, _UNRESERVED_PAT, _URI_RE, _USERINFO_CHARS, _ZONE_ID_PAT, _ZONE_ID_RE

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/util.py`
**Functions:** reraise, to_bytes, to_str

### `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/wait.py`
**Functions:** _have_working_poll, do_poll, poll_wait_for_socket, select_wait_for_socket, wait_for_read, wait_for_socket, wait_for_write

### `parity_env/lib/python3.14/site-packages/pluggy/__init__.py`

### `parity_env/lib/python3.14/site-packages/pluggy/_callers.py`
**Functions:** _multicall, _raise_wrapfail, _warn_teardown_exception, run_old_style_hookwrapper

### `parity_env/lib/python3.14/site-packages/pluggy/_hooks.py`
**Classes:** HookCaller, HookImpl, HookRelay, HookSpec, HookimplMarker, HookimplOpts, HookspecMarker, HookspecOpts, _SubsetHookCaller
**Functions:** __call__, __getattr__, __init__, __repr__, _add_hookimpl, _call_history, _hookimpls, _maybe_apply_history, _remove_plugin, _verify_all_args_are_provided, call_extra, call_historic, get_hookimpls, has_spec, is_historic, normalize_hookimpl_opts, set_specification, setattr_hookimpl_opts, setattr_hookspec_opts, spec, varnames
**Parameters:** _F, _PYPY, _T

### `parity_env/lib/python3.14/site-packages/pluggy/_manager.py`
**Classes:** DistFacade, PluginManager, PluginValidationError
**Functions:** __dir__, __getattr__, __init__, _formatdef, _hookexec, _verify_hook, _warn_for_function, add_hookcall_monitoring, add_hookspecs, after, before, check_pending, enable_tracing, get_canonical_name, get_hookcallers, get_name, get_plugin, get_plugins, has_plugin, is_blocked, is_registered, list_name_plugin, list_plugin_distinfo, load_setuptools_entrypoints, parse_hookimpl_opts, parse_hookspec_opts, project_name, register, set_blocked, subset_hook_caller, traced_hookexec, unblock, undo, unregister

### `parity_env/lib/python3.14/site-packages/pluggy/_result.py`
**Classes:** HookCallError, Result
**Functions:** __init__, exception, excinfo, force_exception, force_result, from_call, get_result

### `parity_env/lib/python3.14/site-packages/pluggy/_tracing.py`
**Classes:** TagTracer, TagTracerSub
**Functions:** __call__, __init__, _format_message, _processmessage, get, setprocessor, setwriter

### `parity_env/lib/python3.14/site-packages/pluggy/_version.py`
**Parameters:** TYPE_CHECKING, VERSION_TUPLE

### `parity_env/lib/python3.14/site-packages/pluggy/_warnings.py`
**Classes:** PluggyTeardownRaisedWarning, PluggyWarning

### `parity_env/lib/python3.14/site-packages/py.py`

### `parity_env/lib/python3.14/site-packages/pytest/__init__.py`

### `parity_env/lib/python3.14/site-packages/pytest/__main__.py`

### `strategy.py`
**Functions:** atr, calculate_signals, ema, macd, pivot_high, pivot_low, rma, rsi
**Parameters:** LEFT_BARS, MACD_FAST, MACD_SIG, MACD_SLOW, RIGHT_BARS, RSI_LEN

### `web.py`
**Functions:** health

## APPLIED REPAIRS

No high-confidence automatic repair was applied.

## IMPORTANT

Automatic repair intentionally refuses to modify pivot/timestamp/state semantics unless the replacement is deterministic and verified.

Backup: `/data/data/com.termux/files/home/dtm-new-bot/parity_lab/ULTIMATE_BACKUP_20260815_220752`