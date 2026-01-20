import boto3
import logging
from botocore.exceptions import ClientError

LOG_RETENTION_DAYS = 365

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logs_client = boto3.client("logs")


def lambda_handler(event, context):
    paginator = logs_client.get_paginator("describe_log_groups")

    updated = []
    skipped = []
    failed = []

    logger.info("Starting CloudWatch Log Group retention enforcement")

    for page in paginator.paginate():
        for log_group in page.get("logGroups", []):
            log_group_name = log_group["logGroupName"]

            # Retention missing == Never Expire
            if "retentionInDays" not in log_group:
                try:
                    logs_client.put_retention_policy(
                        logGroupName=log_group_name, retentionInDays=LOG_RETENTION_DAYS
                    )

                    updated.append(log_group_name)
                    logger.info(
                        f"Retention updated to {LOG_RETENTION_DAYS} days for log group: {log_group_name}"
                    )

                except ClientError as e:
                    failed.append(log_group_name)
                    logger.error(
                        f"FAILED to update retention for log group: {log_group_name} | Error: {e}"
                    )
            else:
                skipped.append(log_group_name)

    logger.info(
        f"Retention enforcement complete | "
        f"updated={len(updated)}, skipped={len(skipped)}, failed={len(failed)}"
    )

    return {
        "status": "completed",
        "retention_days": LOG_RETENTION_DAYS,
        "updated_log_groups": updated,
        "skipped_log_groups_count": len(skipped),
        "failed_log_groups": failed,
    }
