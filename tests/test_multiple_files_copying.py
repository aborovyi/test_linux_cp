"""
Verify multiple files copying functionality
"""
import os
from pathlib import Path

import pytest


def test_code_multiple_files_explicit_name_copied_to_same_dir(vfs):
    """
    Verify cp returns code 0 on succesfull copying multiple files indicated by
    explicit names.
    """
    src_files = " ".join([vfs.srcA.name, vfs.srcB.name])
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(parents=True, exist_ok=True)
    code, *_ = vfs.call_copy(src=src_files, dst=f"{dst_dir}")
    assert code == 0


def test_dst_exist_multiple_files_explicit_name_copied_to_same_dir(vfs):
    """
    Verify cp creates files on succesfull copying multiple files indicated by
    explicit names.
    """
    src_files = " ".join([vfs.srcA.name, vfs.srcB.name])
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(parents=True, exist_ok=True)
    vfs.call_copy(src=src_files, dst=f"{dst_dir}")
    assert all((dst_dir / x).exists() for x in [vfs.srcA.name, vfs.srcB.name])


def test_code_multiple_files_explicit_name_copied_to_nonexisting_dir(vfs):
    """
    Verify cp returns code 1 if copying multiple explicit files to non-existing
    directory.
    """
    src_files = " ".join([vfs.srcA.name, vfs.srcB.name])
    dst_dir = vfs.root_dir / "DstDir"
    code, *_ = vfs.call_copy(src=src_files, dst=f"{dst_dir}/")
    assert code == 1


def test_msg_multiple_files_explicit_name_copied_to_nonexisting_dir(vfs):
    """
    Verify cp prints to stderr message about non-existing directory.
    """
    src_files = " ".join([vfs.srcA.name, vfs.srcB.name])
    dst_dir = vfs.root_dir / "DstDir"
    *_, stderr = vfs.call_copy(src=src_files, dst=f"{dst_dir}/")
    assert stderr == bytes(
        f"cp: target '{dst_dir}/': No such file or directory\n",
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    "src_file_1, src_file_2",
    [("srcK", "srcA"), ("srcA", "srcK")],
    ids=["first_doesn't exist", "second doesn't exist"],
)
def test_code_multiple_files_second_is_missing(vfs, src_file_1, src_file_2):
    """
    Verify cp returns code 1 if it is requested to copy non-existing file.
    """
    src_files = [str(vfs.root_dir / x) for x in [src_file_1, src_file_2]]
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(parents=True, exist_ok=True)
    code, *_ = vfs.call_copy(src=" ".join(src_files), dst=dst_dir)
    assert code == 1


@pytest.mark.parametrize(
    "src_file_1, src_file_2",
    [("srcK", "srcA"), ("srcA", "srcK")],
    ids=["first_doesn't exist", "second doesn't exist"],
)
def test_msg_multiple_files_second_is_missing(vfs, src_file_1, src_file_2):
    """
    Verify cp returns code 1 if it is requested to copy non-existing file.
    """
    src_files = [str(vfs.root_dir / x) for x in [src_file_1, src_file_2]]
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(parents=True, exist_ok=True)
    *_, stderr = vfs.call_copy(src=" ".join(src_files), dst=dst_dir)
    assert stderr == bytes(
        f"cp: cannot stat '{vfs.root_dir / 'srcK'}': "
        "No such file or directory\n",
        encoding="utf-8",
    )


def test_code_multiple_files_mask_applies(vfs):
    """
    Verify cp returns code 0 if there are any files that correspond to the
    mask, and are copied
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    code, *_ = vfs.call_copy(src="src*", dst=dst_dir)
    assert code == 0


def test_dst_exists_multiple_files_mask_applies(vfs):
    """
    Verify files that correspond to mask were copied to the destination.
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    vfs.call_copy(src="src*", dst=dst_dir)
    source_files = [
        Path(x) for x in os.listdir(vfs.root_dir) if Path(x).is_file()
    ]
    assert all((dst_dir / x.name).exists() for x in source_files)


def test_code_multiple_files_mask_doesnt_apply(vfs):
    """
    Verify cp returns code 1 if there are no files that correspond to the mask.
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    code, *_ = vfs.call_copy(src="spam*", dst=dst_dir)
    assert code == 1


def test_msg_multiple_files_mask_doesnt_apply(vfs):
    """
    Verify cp report an error if mask coudn't be applied to the files
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    *_, stderr = vfs.call_copy(src="spam*", dst=dst_dir)
    assert stderr == bytes(
        "cp: cannot stat 'spam*': No such file or directory\n",
        encoding="utf-8",
    )
