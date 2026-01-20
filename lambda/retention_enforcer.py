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
                        "Updated retention policy",
                        extra={
                            "log_group": log_group_name,
                            "retention_days": LOG_RETENTION_DAYS,
                        },
                    )

                except ClientError as e:
                    failed.append({"log_group": log_group_name, "error": str(e)})
                    logger.error(
                        "Failed to update retention policy",
                        extra={"log_group": log_group_name, "error": str(e)},
                    )
            else:
                skipped.append(log_group_name)

    logger.info(
        "Retention enforcement complete",
        extra={
            "updated_count": len(updated),
            "skipped_count": len(skipped),
            "failed_count": len(failed),
        },
    )

    return {
        "status": "completed",
        "retention_days": LOG_RETENTION_DAYS,
        "updated_log_groups": updated,
        "skipped_log_groups_count": len(skipped),
        "failed": failed,
    }
