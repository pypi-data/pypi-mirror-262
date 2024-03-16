###############################################################################################
# Guardian API Client
# Submits a model URI to the Guardian API for scanning and checking scan status.
#
# Usage:
# python guardian.py <base_url> <model_uri> [--threshold <threshold>] [--block-on-errors] [--log-level <log-level>] | echo ?
#
# Arguments:
#  base_url: The base URL of the Guardian API.
#  model_uri: The model URI to scan.
#  --threshold: The threshold level. If the scan result exceeds this threshold, the script will exit with code 1.
# --block-on-errors: Block on scan errors. Default is False.
# --report-only: Report only, do not evaluate scan results. Default is False.
#  --log-level: The log level. Default is "info".
#
# Exit Codes:
#  0 - Scan successful and no issues > threshold
#  1 - Scan successful but with issues >= threshold
#  2 - Scan failed (for any other reason)
#
# Example:
#  python guardian.py https://api.guardian.example.com s3://bucket/key --threshold high || echo $?
###############################################################################################


import json
import sys
import argparse

from guardian_clients.python.api import GuardianAPIClient

import click

CRITICAL = "CRITICAL"
INFO = "info"


@click.command()
@click.argument("base_url", required=True)
@click.argument("model_uri", required=True)
@click.option(
    "--threshold",
    default=CRITICAL,
    type=str,
    required=False,
    help="The threshold level at or above which scan fails (CRITICAL, HIGH, MEDIUM, LOW)",
)
@click.option(
    "--block-on-scan-errors",
    is_flag=True,
    help="Block if the scanning process failed on an incomplete scan",
)
@click.option(
    "--report-only",
    is_flag=True,
    help="Generate a JSON report only without evaluating scan results",
)
@click.option("--silent", is_flag=True, help="Do not print anything to stdout")
@click.option(
    "--log-level",
    default=INFO,
    type=str,
    required=False,
    help="Logging level if not silent (critical, error, info, debug)",
)
def cli(
    base_url: str,
    model_uri: str,
    threshold: str = CRITICAL,
    block_on_scan_errors: bool = True,
    report_only: bool = False,
    silent: bool = True,
    log_level: str = INFO,
) -> None:
    main(base_url, model_uri, threshold, block_on_scan_errors, report_only, silent, log_level) 

def main(
    base_url: str,
    model_uri: str,
    threshold: str = CRITICAL,
    block_on_scan_errors: bool = True,
    report_only: bool = False,
    silent: bool = True,
    log_level: str = INFO,
) -> None:
    try:
        guardian = GuardianAPIClient(
            base_url, log_level=log_level if not silent else CRITICAL
        )

        response = guardian.scan(model_uri)

        http_status_code = response.get("http_status_code")
        if not http_status_code or http_status_code != 200:
            print(
                f"Error: Scan failed with status code: {http_status_code}, message: {response.get('error')}"
            )
            sys.exit(2)

        if report_only:
            print(json.dumps(response["scan_status_json"], indent=4))

        else:
            if response["scan_status_json"]["status"] != "FINISHED":
                print(
                    f"Error: Scan failed with code: {response['scan_status_json']['error_code']}, message: {response['scan_status_json']['error_message']}"
                )
                sys.exit(2)

            reason, blocked = guardian.evaluate(
                response["scan_status_json"],
                threshold=threshold,
                block_on_scan_errors=block_on_scan_errors,
            )
            if blocked:
                print(f"Error: {reason}")
                sys.exit(1)
    except ValueError as e:
        print("Error: Invalid arguments", e)
        sys.exit(2)
    except Exception as e:
        print("Error: Scan submission failed", e)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Submit a URI to an API and check status."
    )
    parser.add_argument("base_url", type=str, help="The base URL of the API.")
    parser.add_argument("model_uri", type=str, help="The model URI to scan.")
    parser.add_argument(
        "--threshold",
        type=str,
        choices=["low", "high", "medium", CRITICAL],
        help="The threshold level.",
        default=CRITICAL,
    )
    parser.add_argument(
        "--block-on-scan-errors",
        action="store_true",
        help="Block on scan errors.",
        default=True,
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Report only, do not block on errors.",
        default=False,
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Do not print anything to stdout.",
        default=False,
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=[CRITICAL, "error", INFO, "debug"],
        help="The log level.",
        default=INFO,
    )

    args = parser.parse_args()

    main(
        base_url=args.base_url,
        model_uri=args.model_uri,
        threshold=args.threshold,
        block_on_scan_errors=args.block_on_scan_errors,
        report_only=args.report_only,
        silent=args.silent,
        log_level=args.log_level,
    )
