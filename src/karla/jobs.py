"""Job management for Karla."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class Job(BaseModel):
    """A scraping job configuration."""

    name: str
    query: str
    region: str
    cities: list[str] = []
    schema: str = "default"
    sources: list[str] = []
    status: str = "pending"
    created: str = ""
    updated: str = ""


class JobManager:
    """Manages job configurations stored as YAML files."""

    def __init__(self, jobs_dir: Optional[Path] = None):
        if jobs_dir is None:
            jobs_dir = Path.home() / ".karla" / "jobs"
        self.jobs_dir = jobs_dir
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

    def _job_path(self, name: str) -> Path:
        return self.jobs_dir / f"{name}.yaml"

    def create(
        self,
        name: str,
        query: str,
        region: str,
        cities: list[str] = None,
        schema: str = "default",
        sources: list[str] = None,
    ) -> Job:
        """Create a new job."""
        now = datetime.utcnow().isoformat()

        job = Job(
            name=name,
            query=query,
            region=region,
            cities=cities or [],
            schema=schema,
            sources=sources or [],
            status="pending",
            created=now,
            updated=now,
        )

        self._save(job)
        return job

    def get(self, name: str) -> Optional[Job]:
        """Get a job by name."""
        path = self._job_path(name)
        if not path.exists():
            return None

        with open(path) as f:
            data = yaml.safe_load(f)
            return Job(**data)

    def list_all(self) -> list[Job]:
        """List all jobs."""
        jobs = []
        for path in self.jobs_dir.glob("*.yaml"):
            with open(path) as f:
                data = yaml.safe_load(f)
                jobs.append(Job(**data))
        return sorted(jobs, key=lambda j: j.created, reverse=True)

    def update(self, name: str, **kwargs) -> Optional[Job]:
        """Update a job."""
        job = self.get(name)
        if not job:
            return None

        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)

        job.updated = datetime.utcnow().isoformat()
        self._save(job)
        return job

    def delete(self, name: str) -> bool:
        """Delete a job."""
        path = self._job_path(name)
        if path.exists():
            path.unlink()
            return True
        return False

    def _save(self, job: Job) -> None:
        """Save a job to disk."""
        path = self._job_path(job.name)
        with open(path, "w") as f:
            yaml.dump(job.model_dump(), f, default_flow_style=False)
