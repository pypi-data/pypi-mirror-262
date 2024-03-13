class QasePytestOptions:
    
    @staticmethod
    def addoptions(parser, group, added=[]):

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-mode",
            dest="qase_mode",
            default="off",
            help="Define Qase reporter mode: `off`, `report` or `testops`"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-environment",
            dest="qase_environment",
            help="Define environment slug or ID from TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-debug",
            dest="qase_debug",
            type="bool",
            default=False,
            help="Enable debug mode"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-execution-plan-path",
            dest="qase_execution_plan_path",
            default="qase_execution_plan.json",
            help="Path to file with execution plan"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-project",
            dest="qase_testops_project",
            help="Project code in Qase TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-api-token",
            dest="qase_testops_api_token",
            help="API token for Qase TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-api-host",
            dest="qase_testops_api_host",
            default="qase.io",
            help="API host for Qase TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-plan-id",
            dest="qase_testops_plan_id",
            help="Test Plan ID in Qase TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-run-id",
            dest="qase_testops_run_id",
            help="Test Run ID in Qase TestOps"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-run-title",
            "qase_testops_run_title",
            help="Define title for autocreated Test Run. If not set, will be used autogenerated title"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-run-description",
            dest="qase_testops_run_description",
            default="",
            help="Define description for autocreated Test Run"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-run-complete",
            dest="qase_testops_run_complete",
            type="bool",
            default=False,
            help="Complete run after tests execution"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-bulk",
            dest="qase_testops_bulk",
            type="bool",
            default=True,
            help="Send results in bulk after tests execution or one by one after each test"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-batch",
            dest="qase_testops_batch",
            default=200,
            help="Define batch size for bulk sending. Default: 200"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-testops-defect",
            dest="qase_testops_defect",
            type="bool",
            default=False,
            help="Create defect if test failed"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-report-driver",
            dest="qase_report_driver",
            default="local",
            help="Define report driver: `local`. More options coming soon."
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-report-connection-local-path",
            dest="qase_report_connection_local_path",
            default="./build/qase-report",
            help="Define local path for report directory"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-report-connection-local-format",
            dest="qase_report_connection_local_format",
            default="json",
            help="Define local format for report directory: `json` or `jsonp`"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-framework-pytest-capture-logs",
            dest="qase_framework_pytest_capture_logs",
            type="bool",
            default=False,
            help="Capture logs on fail for each test"
        )

        QasePytestOptions.add_option_ini(
            parser,
            group,
            "--qase-framework-pytest-capture-http",
            dest="qase_framework_pytest_capture_http",
            type="bool",
            default=False,
            help="Capture http requests for each test and save them as steps"
        )
    
    @staticmethod
    def add_option_ini(parser, group, option, dest, default=None, type=None, **kwargs):
        # We are going to add options that were not added before through the manager
        try:
            parser.addini(
                dest,
                default=default,
                type=type,
                help="default value for " + option,
            )
            group.addoption(option, dest=dest, default=default, action="store", **kwargs)
        except ValueError:
            pass