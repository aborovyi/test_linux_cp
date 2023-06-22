"""
This suite contains tests for section docs/functional.md -> single-flag cases
-> "--archive"
"""
import os

import pytest


@pytest.mark.parametrize(
    "flag", ["-a", "--archive"], ids=["short flag", "long flag"]
)
def test_code_copy_all_dir_as_archive(vfs, flag):
    """
    Verify cp returns code 0 on copying complete directory if called with
    flag '{flag}'.
    """
    src_dir = vfs.root_dir / "SrcDir"
    dst_dir = vfs.root_dir / "DstDir"
    code, *_ = vfs.call_copy(src=src_dir, dst=dst_dir, flags=flag)
    assert code == 0


@pytest.mark.parametrize(
    "flag", ["-a", "--archive"], ids=["short flag", "long flag"]
)
def test_content_copy_all_dir_as_archive(vfs, flag):
    """
    Verify cp copies complete directory if called with flag '{flag}'.
    """
    src_dir = vfs.root_dir / "SrcDir"
    dst_dir = vfs.root_dir / "DstDir"

    vfs.call_copy(src=src_dir, dst=dst_dir, flags=flag)

    src_content = []
    for _, dirnames, filenames in os.walk(src_dir):
        src_content.append([dirnames, filenames])
    dst_content = []
    for _, dirnames, filenames in os.walk(dst_dir):
        dst_content.append([dirnames, filenames])
    assert src_content == dst_content
