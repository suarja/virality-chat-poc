"""
Batch processing utilities for tracking accounts and errors.
"""
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BatchTracker:
    """Manages account tracking and error handling for batch processing."""

    def __init__(self, dataset_name: str):
        """Initialize batch tracker for a specific dataset."""
        self.dataset_name = dataset_name
        self.dataset_dir = Path("data") / f"dataset_{dataset_name}"
        self.source_file = self.dataset_dir / "source.txt"
        self.errors_file = self.dataset_dir / "errors.txt"

        # Create dataset directory and files if they don't exist
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self.source_file.touch(exist_ok=True)
        self.errors_file.touch(exist_ok=True)

    def load_processed_accounts(self) -> List[str]:
        """Load list of already processed accounts."""
        if self.source_file.exists():
            with open(self.source_file) as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def load_error_accounts(self) -> Dict[str, List[Dict]]:
        """Load accounts with errors and their error details."""
        errors = {}
        if self.errors_file.exists():
            with open(self.errors_file) as f:
                for line in f:
                    if line.strip():
                        try:
                            account, phase, timestamp, error = line.strip().split("|")
                            if account not in errors:
                                errors[account] = []
                            errors[account].append({
                                'phase': phase,
                                'timestamp': timestamp,
                                'error': error
                            })
                        except ValueError:
                            logger.warning(
                                f"Invalid error entry: {line.strip()}")
        return errors

    def mark_account_processed(self, account: str):
        """Mark an account as successfully processed."""
        with open(self.source_file, "a") as f:
            f.write(f"{account}\n")
        logger.info(f"✅ Marked account {account} as processed")

    def log_error(self, account: str, phase: str, error: str):
        """Log an error for an account in a specific phase."""
        timestamp = datetime.now().isoformat()
        with open(self.errors_file, "a") as f:
            f.write(f"{account}|{phase}|{timestamp}|{error}\n")
        logger.error(f"❌ Error in {phase} for {account}: {error}")

    def get_next_batch(self, available_accounts: List[str], batch_size: int) -> List[str]:
        """Get next batch of unprocessed accounts."""
        processed = set(self.load_processed_accounts())
        return [acc for acc in available_accounts if acc not in processed][:batch_size]

    def get_failed_accounts(self, phase: Optional[str] = None) -> List[str]:
        """Get list of accounts that failed in a specific phase or any phase."""
        errors = self.load_error_accounts()
        if phase:
            return [acc for acc, errs in errors.items()
                    if any(e['phase'] == phase for e in errs)]
        return list(errors.keys())

    def summarize_progress(self) -> Dict:
        """Get summary of processing progress."""
        processed = self.load_processed_accounts()
        errors = self.load_error_accounts()

        return {
            'total_processed': len(processed),
            'total_errors': len(errors),
            'accounts_with_errors': list(errors.keys()),
            'error_phases': {
                'scraping': len(self.get_failed_accounts('scraping')),
                'analysis': len(self.get_failed_accounts('analysis')),
                'features': len(self.get_failed_accounts('features'))
            }
        }

    def mark_account_failed(self, account: str, phase: str, error: str):
        """Mark an account as failed to prevent infinite loops."""
        self.log_error(account, phase, error)
        # Also add to source.txt to prevent reprocessing
        with open(self.source_file, "a") as f:
            f.write(f"{account}\n")
        logger.warning(
            f"⚠️  Marked account {account} as failed in {phase} phase")
