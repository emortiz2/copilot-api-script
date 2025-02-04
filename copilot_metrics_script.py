import os
import logging
import psycopg2
import requests

from datetime import date, timedelta
from dotenv import load_dotenv
from psycopg2.extras import execute_values
from typing import Any, Dict, Optional

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
GITHUB_COPILOT_API_URL = "https://api.github.com/orgs/SquareTrade/copilot/metrics"
GITHUB_COPILOT_TOKEN = os.getenv("GITHUB_TOKEN")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_PATH = os.getenv("DB_PATH")


def get_github_headers() -> Dict[str, str]:
    """Generate headers dynamically to avoid global token exposure."""
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_COPILOT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_copilot_metrics() -> Optional[Dict[str, Any]]:
    """Fetch Copilot metrics from GitHub API."""

    headers = get_github_headers()
    params = {"since": (date.today() - timedelta(days=1))}
    # params = {"since": "2025-02-01"}

    try:
        response = requests.get(
            GITHUB_COPILOT_API_URL, headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching copilot metrics data: {e}")
        return None


def add_copilot_metrics(response: Dict[str, Any]) -> None:
    """Update Copilot metrics data into the database."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, options=f"-c search_path={DB_PATH}"
        )
        cursor = connection.cursor()

        for data in response:
            # Insert Daily Usage Metrics
            daily_usage_metrics_query = """
            INSERT INTO copilot_daily_metrics (metric_date, total_active_users, total_engaged_users)
            VALUES (%s, %s, %s)
            """
            copilot_metrics_data = (
                data["date"],
                data["total_active_users"],
                data["total_engaged_users"],
            )
            cursor.execute(daily_usage_metrics_query, copilot_metrics_data)

            # Insert IDE Chat Metrics
            ide_chat_metrics_query = """
            INSERT INTO copilot_ide_chat_metrics (metric_date, editor_name, model_name, total_chats, is_custom_model, total_engaged_users, total_chat_copy_events, total_chat_insertion_events)
            VALUES %s
            """
            ide_chat_metrics_data = []
            for editor in data["copilot_ide_chat"]["editors"]:
                for model in editor["models"]:
                    ide_chat_metrics_data.append(
                        (
                            data["date"],
                            editor["name"],
                            model["name"],
                            model["total_chats"],
                            model["is_custom_model"],
                            model["total_engaged_users"],
                            model["total_chat_copy_events"],
                            model["total_chat_insertion_events"],
                        )
                    )
            execute_values(cursor, ide_chat_metrics_query, ide_chat_metrics_data)

            # Insert IDE Code Completion Engagement
            ide_code_completion_engagement_query = """

            INSERT INTO copilot_ide_code_completion_engagement (metric_date, editor_name, total_engaged_users)
            VALUES %s
            """
            ide_code_completion_engagement_data = []
            for editor in data["copilot_ide_code_completions"]["editors"]:
                ide_code_completion_engagement_data.append(
                    (data["date"], editor["name"], editor["total_engaged_users"])
                )
            logger.info(f"Code completion engagement data: {ide_code_completion_engagement_data}")
            execute_values(cursor, ide_code_completion_engagement_query, ide_code_completion_engagement_data)

            # Insert IDE Code Completion Metrics
            ide_code_completion_metrics_query = """
            INSERT INTO copilot_ide_code_completion_metrics (metric_date, editor_name, model_name, is_custom_model, language_name, total_engaged_users, total_code_acceptances, total_code_suggestions, total_code_lines_accepted, total_code_lines_suggested)
            VALUES %s
            """
            ide_code_completion_metrics_data = []
            for editor in data["copilot_ide_code_completions"]["editors"]:
                for model in editor["models"]:
                    for language in model["languages"]:
                        ide_code_completion_metrics_data.append(
                            (
                                data["date"],
                                editor["name"],
                                model["name"],
                                model["is_custom_model"],
                                language["name"],
                                language["total_engaged_users"],
                                language["total_code_acceptances"],
                                language["total_code_suggestions"],
                                language["total_code_lines_accepted"],
                                language["total_code_lines_suggested"],
                            )
                        )
            logger.info(f"Code completions data: {ide_code_completion_metrics_data}")
            execute_values(
                cursor, ide_code_completion_metrics_query, ide_code_completion_metrics_data
            )

            connection.commit()
            logger.info(f"Copilot metrics are updated successfully for {data['date']}")
    except Exception as e:
        logger.error(
            f"Error updating copilot metrics data into the database for {data['date']}: {e}"
        )
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


data = fetch_copilot_metrics()
print(data)
if data:
    add_copilot_metrics(data)