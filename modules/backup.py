import gzip
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from py_libs.Command import Command
from py_libs.InputValidator import InputValidator
from py_libs.Print import Print
from py_libs.Select import Select

BACKUP_DIR = Path("./backups")
# Сколько автоименованных бэкапов (backup_<db>_*) оставлять
KEEP_AUTO_BACKUPS = 4


def _load_env() -> dict[str, str]:
    env_file = Path(".env")
    if not env_file.exists():
        raise RuntimeError(".env file not found!")

    env: dict[str, str] = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        env[key] = value

    for key in ("DB_USERNAME", "DB_NAME"):
        if not env.get(key):
            raise RuntimeError(f"{key} is not set in .env")
    return env


def _find_container() -> str:
    names = Command.run_quiet(
        "docker ps --filter name=postgres --format '{{.Names}}'"
    ).splitlines()
    if not names:
        raise RuntimeError(
            "Postgres container not found (docker ps --filter name=postgres)."
        )
    return names[0]


def _psql(container: str, user: str, sql: str):
    result = subprocess.run(
        ["docker", "exec", container, "psql", "-U", user, "-d", "postgres",
         "-c", sql],
    )
    if result.returncode != 0:
        raise RuntimeError(f"psql failed: {sql}")


def backup_export():
    env = _load_env()
    db_user, db_name = env["DB_USERNAME"], env["DB_NAME"]
    container = _find_container()
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    name = InputValidator.get_string("Enter backup name: ", allow_empty=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{name}_{timestamp}" if name else f"backup_{db_name}_{timestamp}"
    safe_name = re.sub(r"[^A-Za-z0-9_-]", "", name.replace(" ", "_"))
    backup_file = BACKUP_DIR / f"{safe_name}.sql.gz"

    Print.info(f"Creating backup of database: {db_name}\nContainer: {container}")
    proc = subprocess.Popen(
        ["docker", "exec", container, "pg_dump", "-U", db_user, "-d", db_name],
        stdout=subprocess.PIPE,
    )
    assert proc.stdout is not None
    with gzip.open(backup_file, "wb") as gz:
        shutil.copyfileobj(proc.stdout, gz)
    proc.wait()

    with gzip.open(backup_file, "rb") as gz:
        empty = not gz.read(1)
    if proc.returncode != 0 or empty:
        backup_file.unlink(missing_ok=True)
        raise RuntimeError("❌ Backup failed!")

    size_kb = backup_file.stat().st_size / 1024
    Print.success(f"✅ Backup successful: {backup_file}\nSize: {size_kb:.1f}K")

    # Удалить старые автоименованные бэкапы, оставив последние KEEP_AUTO_BACKUPS
    auto = sorted(
        BACKUP_DIR.glob(f"backup_{db_name}_*.sql.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for old in auto[KEEP_AUTO_BACKUPS:]:
        old.unlink(missing_ok=True)


def backup_import():
    env = _load_env()
    db_user, db_name = env["DB_USERNAME"], env["DB_NAME"]
    container = _find_container()

    if not BACKUP_DIR.is_dir():
        raise RuntimeError(f"{BACKUP_DIR} directory not found!")

    # Новые сверху
    files = sorted(
        BACKUP_DIR.glob("*.sql.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        raise RuntimeError(f"No backup files found in {BACKUP_DIR}")

    options = [
        f"{datetime.fromtimestamp(f.stat().st_mtime):%Y-%m-%d %H:%M}  {f.name}"
        for f in files
    ]
    selected = Select.select_fzf_one(options)
    if not selected:
        Print.warning("No backup selected.")
        return
    backup_file = files[options.index(selected)]

    Print.warning(
        f"Database:  {db_name}\nContainer: {container}\nBackup:    {backup_file}\n\n"
        "⚠️  WARNING: This will DROP and recreate the database!"
    )
    answer = InputValidator.get_string("Continue? (yes/no): ", allow_empty=True)
    if answer != "yes":
        Print.info("Restore cancelled.")
        return

    print("Disconnecting active connections...")
    _psql(
        container, db_user,
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
        f"WHERE datname = '{db_name}' AND pid <> pg_backend_pid();",
    )
    print("Dropping database...")
    _psql(container, db_user, f'DROP DATABASE IF EXISTS "{db_name}";')
    print("Creating database...")
    _psql(container, db_user, f'CREATE DATABASE "{db_name}";')

    print("Restoring data...")
    proc = subprocess.Popen(
        ["docker", "exec", "-i", container, "psql", "-U", db_user, "-d", db_name],
        stdin=subprocess.PIPE,
    )
    assert proc.stdin is not None
    with gzip.open(backup_file, "rb") as gz:
        shutil.copyfileobj(gz, proc.stdin)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("❌ Restore failed!")

    Print.success("✅ Restore completed successfully!")


def backup():
    choice = Select.select_fzf_one(["Export", "Import", "Back"])
    if choice == "Export":
        backup_export()
    elif choice == "Import":
        backup_import()
