"""Install the skill only; never configure Hermes or access QQ."""
import argparse
import os
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    home = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
    parser.add_argument("--skills-dir", type=Path, default=home / "skills", help="Current profile's skills directory")
    parser.add_argument("--dry-run", action="store_true", help="Print destination without writing files")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "qzone-archive"
    target = args.skills_dir.expanduser().resolve() / "qzone-archive"
    if args.dry_run:
        print("Would install: " + str(target))
        return
    try:
        shutil.copytree(source, target)
    except OSError as error:
        parser.exit(1, "Installation refused or failed: " + str(error) + "\n")
    print("Installed: " + str(target))
    print("Start a new Hermes session and load qzone-archive.")


if __name__ == "__main__":
    main()
