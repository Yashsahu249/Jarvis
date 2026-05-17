import os
import re
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Any
from loguru import logger
from app.core.config import settings


class RepoService:
    def __init__(self):
        self.base_dir = Path(settings.MEMORY_DB_PATH).parent / "repos"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.repos: dict[str, dict[str, Any]] = {}
        self._load_existing()

    def _load_existing(self):
        if self.base_dir.exists():
            for item in self.base_dir.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    repo_id = item.name
                    self.repos[repo_id] = {
                        "id": repo_id,
                        "name": repo_id,
                        "url": self._get_remote_url(item),
                        "local_path": str(item),
                        "branch": self._get_branch(item),
                        "description": None,
                        "last_analyzed": None,
                        "size_bytes": self._get_dir_size(item),
                        "file_count": self._count_files(item),
                    }

    def _get_remote_url(self, repo_path: Path) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else "local"
        except Exception:
            return "local"

    def _get_branch(self, repo_path: Path) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def _get_dir_size(self, path: Path) -> int:
        total = 0
        for f in path.rglob("*"):
            if f.is_file():
                try:
                    total += f.stat().st_size
                except OSError:
                    pass
        return total

    def _count_files(self, path: Path) -> int:
        return sum(1 for f in path.rglob("*") if f.is_file())

    async def clone(self, url: str, name: str | None = None, branch: str | None = None, depth: int | None = None) -> dict:
        repo_name = name or url.rstrip("/").split("/")[-1].replace(".git", "")
        repo_id = re.sub(r"[^a-zA-Z0-9_-]", "_", repo_name)
        dest = self.base_dir / repo_id

        if dest.exists():
            logger.warning(f"Repo {repo_id} already exists at {dest}")
            return self.repos.get(repo_id, {"id": repo_id, "name": repo_name, "local_path": str(dest)})

        import asyncio
        cmd = ["git", "clone"]
        if branch:
            cmd.extend(["-b", branch])
        if depth:
            cmd.extend(["--depth", str(depth)])
        cmd.extend([url, str(dest)])

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                raise RuntimeError(f"Clone failed: {stderr.decode()}")

            repo_info = {
                "id": repo_id,
                "name": repo_name,
                "url": url,
                "local_path": str(dest),
                "branch": branch or self._get_branch(dest),
                "description": None,
                "last_analyzed": None,
                "size_bytes": self._get_dir_size(dest),
                "file_count": self._count_files(dest),
            }
            self.repos[repo_id] = repo_info
            logger.info(f"Cloned repo {repo_id} from {url}")
            return repo_info
        except Exception as e:
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            raise RuntimeError(f"Failed to clone {url}: {e}")

    def list_repos(self) -> list[dict]:
        return list(self.repos.values())

    def get_repo(self, repo_id: str) -> dict | None:
        return self.repos.get(repo_id)

    def get_structure(self, repo_id: str, path: str = "") -> list[dict]:
        repo = self.repos.get(repo_id)
        if not repo:
            raise ValueError(f"Repo {repo_id} not found")

        base = Path(repo["local_path"])
        if path:
            target = base / path
        else:
            target = base

        if not target.exists() or not str(target).startswith(str(base)):
            raise ValueError(f"Invalid path: {path}")

        items = []
        try:
            for item in sorted(target.iterdir()):
                if item.name.startswith(".git"):
                    continue
                items.append({
                    "path": str(item.relative_to(base)),
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "language": self._detect_language(item.name) if item.is_file() else None,
                })
        except PermissionError:
            pass
        return items

    def get_file(self, repo_id: str, file_path: str) -> dict:
        repo = self.repos.get(repo_id)
        if not repo:
            raise ValueError(f"Repo {repo_id} not found")

        full_path = Path(repo["local_path"]) / file_path
        if not full_path.exists() or not full_path.is_file():
            raise ValueError(f"File not found: {file_path}")
        if not str(full_path).startswith(str(Path(repo["local_path"]))):
            raise ValueError("Path traversal detected")

        content = full_path.read_text(encoding="utf-8", errors="replace")
        return {
            "path": file_path,
            "name": full_path.name,
            "content": content,
            "size": full_path.stat().st_size,
            "language": self._detect_language(full_path.name),
            "extension": full_path.suffix,
        }

    async def analyze(self, repo_id: str, task: str, files: list[str] | None = None, context: str | None = None) -> dict:
        repo = self.repos.get(repo_id)
        if not repo:
            raise ValueError(f"Repo {repo_id} not found")

        from app.services.llm_service import llm_service

        code_context = ""
        if files:
            for f in files[:5]:
                try:
                    file_data = self.get_file(repo_id, f)
                    code_context += f"\n--- {f} ---\n{file_data['content'][:3000]}\n"
                except Exception:
                    pass
        else:
            structure = self.get_structure(repo_id)
            code_context = "\n".join([s["path"] for s in structure[:50]])

        prompt = (
            f"Repository: {repo['name']}\n"
            f"Task: {task}\n"
            f"Context: {context or ''}\n\n"
            f"Repository structure/files:\n{code_context}\n\n"
            f"Provide a detailed analysis based on the task."
        )

        messages = [{"role": "user", "content": prompt}]
        analysis = await llm_service.chat(messages, temperature=0.3)

        repo["last_analyzed"] = __import__("datetime").datetime.now().isoformat()
        return {"repo_id": repo_id, "task": task, "analysis": analysis}

    async def search(self, repo_id: str, query: str, file_pattern: str | None = None, max_results: int = 20) -> dict:
        repo = self.repos.get(repo_id)
        if not repo:
            raise ValueError(f"Repo {repo_id} not found")

        base = Path(repo["local_path"])
        results = []
        search_terms = query.lower().split()

        patterns = [f"*{file_pattern}" if file_pattern else "*"]
        from pathlib import Path as P
        for pat in patterns:
            for file_path in base.rglob(pat):
                if file_path.is_file() and ".git" not in file_path.parts:
                    try:
                        relative = str(file_path.relative_to(base))
                        content = file_path.read_text(encoding="utf-8", errors="replace")
                        lines = content.split("\n")
                        for i, line in enumerate(lines, 1):
                            line_lower = line.lower()
                            if all(term in line_lower for term in search_terms):
                                results.append({
                                    "file": relative,
                                    "line": i,
                                    "content": line.strip()[:200],
                                    "score": sum(line_lower.count(t) for t in search_terms),
                                })
                    except Exception:
                        continue

        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:max_results]

        return {
            "repo_id": repo_id,
            "query": query,
            "total_results": len(results),
            "results": results,
            "file_pattern": file_pattern,
        }

    def remove(self, repo_id: str) -> bool:
        repo = self.repos.pop(repo_id, None)
        if repo:
            dest = Path(repo["local_path"])
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
                return True
        return False

    def _detect_language(self, filename: str) -> str:
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".rs": "rust",
            ".go": "go",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".r": "r",
            ".m": "matlab",
            ".sql": "sql",
            ".html": "html",
            ".css": "css",
            ".scss": "scss",
            ".less": "less",
            ".json": "json",
            ".xml": "xml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".md": "markdown",
            ".txt": "text",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            ".fish": "shell",
            ".env": "dotenv",
            ".dockerfile": "dockerfile",
        }
        return ext_map.get(Path(filename).suffix.lower(), "unknown")


repo_service = RepoService()
