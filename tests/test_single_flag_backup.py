"""
This suite contains tests ftom the docs/functional.md -> "Single-flag cases" ->
"--backup"
"""
import os

import pytest


@pytest.mark.parametrize("opt", ["none", "off"])
@pytest.mark.parametrize("backup_exists", [False, True])
def test_backup_none_no_backup_option(vfs, opt, backup_exists):
    """
    Verify backup won't be created if called 'cp --backup={opt}' and backup
    exists: '{backup_exists}'
    """
    expected_backups = 1 if backup_exists else 0
    if backup_exists:
        (vfs.root_dir / "dstA~").write_text("This is faked backup")
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    collected_files = []
    for _, __, files in os.walk(vfs.root_dir):
        collected_files.extend(filter(lambda x: "dstA~" in x, files))
        collected_files.extend(filter(lambda x: "dstA.~" in x, files))
    assert len(collected_files) == expected_backups


@pytest.mark.parametrize("opt", ["none", "off"])
@pytest.mark.parametrize("backup_exists", [False, True])
def test_backup_none_dst_content_option(vfs, opt, backup_exists):
    """
    Verify backup won't be created if called 'cp --backup={opt}' and backup
    exists: '{backup_exists}'
    """
    if backup_exists:
        (vfs.root_dir / "dstA~").write_text("This is faked backup")
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()


@pytest.mark.parametrize(
    "opt",
    ["numbered", "t", "existing", "nil", "simple", "never"],
    ids=[
        "numbered long",
        "numbered short",
        "existing long",
        "existing short",
        "simple long",
        "simple short",
    ],
)
def test_cp_ignores_backups_if_no_dest_file(vfs, opt):
    """
    Verify cp will create destination file if it is missing, ignoring existing
    backups.
    """
    (vfs.root_dir / "dstA~").write_text("Faked simple backup")
    (vfs.root_dir / "dstA.~1~").write_text("Faked numbered backup")
    vfs.call_copy(vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    collected_files = []
    for _, _, files in os.walk(vfs.root_dir):
        collected_files.extend(filter(lambda x: "dstA" in x, files))
    assert len(collected_files) == 3


@pytest.mark.parametrize(
    "opt",
    ["numbered", "t", "existing", "nil", "simple", "never"],
    ids=[
        "numbered long",
        "numbered short",
        "existing long",
        "existing short",
        "simple long",
        "simple short",
    ],
)
def test_cp_ignores_backups_if_no_dest_file_dst_content(vfs, opt):
    """
    Verify cp will create destination file if it is missing, ignoring existing
    backups.
    """
    (vfs.root_dir / "dstA~").write_text("Faked simple backup")
    (vfs.root_dir / "dstA.~1~").write_text("Faked numbered backup")
    vfs.call_copy(vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()


@pytest.mark.parametrize("opt", ["numbered", "t"])
@pytest.mark.parametrize("backups", [0, 1], ids=["no backup", "backup exists"])
def test_backup_numbered_backup_option(vfs, opt, backups):
    """
    Verify numebred backup create correct amount of backups on
    'cp --backup={opt}' if '{backups}' backups are in destination.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if backups > 0:
        (vfs.root_dir / "dstA.~1~").write_text("Faked destination")
    expected_backups = backups + 1
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    collected_files = []
    for _, __, files in os.walk(vfs.root_dir):
        collected_files.extend(filter(lambda x: "dstA.~" in x, files))
    assert len(collected_files) == expected_backups


@pytest.mark.parametrize("opt", ["numbered", "t"])
@pytest.mark.parametrize("backups", [0, 1], ids=["no backup", "backup exists"])
def test_backup_numbered_backup_option_dst_content(vfs, opt, backups):
    """
    Verify numebred backup create correct amount of backups on
    'cp --backup={opt}' if '{backups}' backups are in destination.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if backups > 0:
        (vfs.root_dir / "dstA.~1~").write_text("Faked destination")
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()


@pytest.mark.parametrize("opt", ["existing", "nil"])
@pytest.mark.parametrize(
    "s_backups, n_backups, next_s_backup",
    [
        (0, 0, True),
        (1, 0, True),
        (0, 1, False),
        (1, 1, False),
    ],
    ids=[
        "neither simple nor numbered backup in destination",
        "simple backup in destination exists",
        "numbered backup in destination",
        "both simple and numbered backup in destination",
    ],
)
def test_backup_existing_backup_option(
    vfs, opt, s_backups, n_backups, next_s_backup
):
    """
    Verify simple backup will be created if no numbered backups are already in
    the destination directory. Extra numbered backup will be created otherwise.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if s_backups > 0:
        (vfs.root_dir / "dstA~").write_text("Faked simple backup")
    if n_backups > 0:
        (vfs.root_dir / "dstA.~1~").write_text("Faked numbered backup")

    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")

    exp_numbered_backups = n_backups if next_s_backup else n_backups + 1
    exp_simple_backups = 1 if next_s_backup else s_backups
    numbered_backups = []
    simple_backups = []
    for _, __, files in os.walk(vfs.root_dir):
        numbered_backups.extend(filter(lambda x: "dstA.~" in x, files))
        simple_backups.extend(filter(lambda x: "dstA~" in x, files))
    assert (
        len(simple_backups) == exp_simple_backups
        and len(numbered_backups) == exp_numbered_backups
    )


@pytest.mark.parametrize("opt", ["existing", "nil"])
@pytest.mark.parametrize(
    "s_backups, n_backups",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
    ],
    ids=[
        "neither simple nor numbered backup in destination",
        "simple backup in destination exists",
        "numbered backup in destination",
        "both simple and numbered backup in destination",
    ],
)
def test_backup_existing_backup_option_dst_content(
    vfs, opt, s_backups, n_backups
):
    """
    Verify simple backup will be created if no numbered backups are already in
    the destination directory. Extra numbered backup will be created otherwise.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if s_backups > 0:
        (vfs.root_dir / "dstA~").write_text("Faked simple backup")
    if n_backups > 0:
        (vfs.root_dir / "dstA.~1~").write_text("Faked numbered backup")

    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()


@pytest.mark.parametrize("opt", ["existing", "nil"])
@pytest.mark.parametrize(
    "s_backups", [0, 1], ids=["no simple backups", "one simple backup"]
)
def test_backup_simple_backup_option(vfs, opt, s_backups):
    """
    Verify one and only one simple backup will be created if called
    'cp --backup={opt}' and '{s_backups}' backups exist in destination.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if s_backups > 0:
        (vfs.root_dir / "dstA~").write_text("Faked simple backup")

    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")

    simple_backups = []
    for _, __, files in os.walk(vfs.root_dir):
        simple_backups.extend(filter(lambda x: "dstA~" in x, files))
    assert len(simple_backups) == 1


@pytest.mark.parametrize("opt", ["existing", "nil"])
@pytest.mark.parametrize(
    "s_backups", [0, 1], ids=["no simple backups", "one simple backup"]
)
def test_backup_simple_backup_option_dst_content(vfs, opt, s_backups):
    """
    Verify one and only one simple backup will be created if called
    'cp --backup={opt}' and '{s_backups}' backups exist in destination.
    """
    (vfs.root_dir / "dstA").write_text("Faked destination")
    if s_backups > 0:
        (vfs.root_dir / "dstA~").write_text("Faked simple backup")

    vfs.call_copy(src=vfs.srcA, dst="dstA", flags=f"--backup={opt}")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()
