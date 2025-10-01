"""Local Stage 5 dispatcher/worker test script.

This script:
1. Pulls email/topic from CLI args.
2. Ensures a Redis container is running (docker required).
3. Enqueues a Celery task directly to verify worker behavior.

Usage:
    python scripts/run_local_email_test.py --email foo@example.com --topic news

Assumptions:
    - .env defines CELERY_BROKER_URL/RESULT_BACKEND pointing to localhost Redis.
    - Firestore credentials available via GOOGLE_APPLICATION_CREDENTIALS.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

import dotenv

dotenv.load_dotenv(PROJECT_ROOT / ".env")

from tasks.email_tasks import enqueue_send_email  # type: ignore  # noqa: E402


def ensure_redis_container() -> None:
    result = subprocess.run(["docker", "ps", "--filter", "name=local-redis", "--format", "{{.Names}}"], capture_output=True, text=True)
    if "local-redis" in result.stdout:
        print("✅ Redis container already running")
        return

    print("🚀 Starting Redis container...")
    subprocess.run(["docker", "run", "-d", "--name", "local-redis", "-p", "6379:6379", "redis:7"], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dispatch Stage 5 email task locally")
    parser.add_argument("--email", required=True, help="Subscriber email")
    parser.add_argument("--topic", required=True, help="Subscription topic")
    parser.add_argument("--subscription-id", default="local-test-subscription", help="Subscription ID placeholder")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        ensure_redis_container()
    except subprocess.CalledProcessError as exc:
        print("❌ Failed to launch Redis container:", exc)
        sys.exit(1)

    enqueue_send_email(args.email, args.topic, args.subscription_id)
    print(f"Queued Celery task for {args.email} / {args.topic}")


if __name__ == "__main__":
    main()

