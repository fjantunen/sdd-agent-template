#!/usr/bin/env python3
"""Save, auto-prune (last 3 versions), and rollback pre-task workspace checkpoints."""

import argparse
import datetime as dt
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile


def git(cwd: pathlib.Path, *args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    """Run a git command in cwd and return the completed process."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        input=input_bytes,
        capture_output=True,
        check=False,
    )


def repo_root() -> pathlib.Path:
    """Resolve the git repository root or fall back to cwd."""
    res = git(pathlib.Path.cwd(), "rev-parse", "--show-toplevel")
    if res.returncode == 0:
        return pathlib.Path(res.stdout.decode().strip())
    return pathlib.Path.cwd()


def checkpoints_dir(root: pathlib.Path) -> pathlib.Path:
    """Return and ensure the .sdd/checkpoints directory."""
    d = root / ".sdd" / "checkpoints"
    d.mkdir(parents=True, exist_ok=True)
    return d


def prune_checkpoints(ckpt_root: pathlib.Path, keep: int = 3) -> list[str]:
    """Keep only the newest `keep` checkpoint directories and delete older ones."""
    dirs = sorted([p for p in ckpt_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    removed: list[str] = []
    if len(dirs) > keep:
        for old in dirs[: len(dirs) - keep]:
            shutil.rmtree(old)
            removed.append(old.name)
    return removed


def cmd_save(root: pathlib.Path, label: str, keep: int) -> int:
    """Save current tracked diff + untracked files (excluding .sdd/) and prune old versions."""
    ckpt_root = checkpoints_dir(root)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    safe_label = re.sub(r"[^a-zA-Z0-9._-]+", "-", label).strip("-") or "ckpt"
    ckpt_dir = ckpt_root / f"{stamp}-{safe_label}"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    diff_res = git(root, "diff", "HEAD")
    if diff_res.returncode == 0 and diff_res.stdout:
        (ckpt_dir / "tracked.patch").write_bytes(diff_res.stdout)

    untracked_res = git(root, "ls-files", "--others", "--exclude-standard")
    untracked_files = [
        line for line in untracked_res.stdout.decode().splitlines()
        if line and not line.startswith(".sdd/") and line != ".sdd"
    ]
    if untracked_files:
        with tarfile.open(ckpt_dir / "untracked.tar.gz", "w:gz") as tar:
            for rel in untracked_files:
                full = root / rel
                if full.exists():
                    tar.add(full, arcname=rel)

    head_res = git(root, "rev-parse", "HEAD")
    manifest = {
        "id": ckpt_dir.name,
        "label": safe_label,
        "created_at": stamp,
        "head": head_res.stdout.decode().strip() if head_res.returncode == 0 else "",
    }
    (ckpt_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    pruned = prune_checkpoints(ckpt_root, keep=keep)
    print(f"Saved checkpoint: {ckpt_dir.name}" + (f" (pruned {len(pruned)})" if pruned else ""))
    return 0


def cmd_rollback(root: pathlib.Path) -> int:
    """Restore workspace to the latest saved checkpoint without touching .sdd/."""
    ckpt_root = checkpoints_dir(root)
    dirs = sorted([p for p in ckpt_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not dirs:
        print("ERROR: No checkpoints available to rollback.", file=sys.stderr)
        return 1

    latest = dirs[-1]
    git(root, "checkout", "--", ".")
    git(root, "clean", "-fd", "-e", ".sdd/")

    patch_file = latest / "tracked.patch"
    if patch_file.exists() and patch_file.stat().st_size > 0:
        apply_res = git(root, "apply", "--whitespace=nowarn", str(patch_file))
        if apply_res.returncode != 0:
            print(f"ERROR: Failed to apply patch: {apply_res.stderr.decode()}", file=sys.stderr)
            return 1

    tar_file = latest / "untracked.tar.gz"
    if tar_file.exists():
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall(root, filter="data")

    print(f"Rolled back workspace to checkpoint: {latest.name}")
    return 0


def cmd_prune(root: pathlib.Path, keep: int) -> int:
    """Prune checkpoints to retain only the newest `keep` versions."""
    removed = prune_checkpoints(checkpoints_dir(root), keep=keep)
    print(f"Pruned {len(removed)} checkpoint(s); kept up to {keep}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SDD pre-task checkpoint manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_save = sub.add_parser("save", help="Save checkpoint and auto-prune")
    p_save.add_argument("label", nargs="?", default="task", help="Checkpoint label (e.g. T1)")
    p_save.add_argument("--keep", type=int, default=3, help="Max checkpoints to retain")

    sub.add_parser("rollback", help="Rollback to latest checkpoint")

    p_prune = sub.add_parser("prune", help="Prune old checkpoints")
    p_prune.add_argument("--keep", type=int, default=3, help="Max checkpoints to retain")

    args = parser.parse_args()
    root = repo_root()
    if args.command == "save":
        return cmd_save(root, args.label, args.keep)
    if args.command == "rollback":
        return cmd_rollback(root)
    if args.command == "prune":
        return cmd_prune(root, args.keep)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
