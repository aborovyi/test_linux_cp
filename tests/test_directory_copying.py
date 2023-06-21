"""
This suite contains cases described under docs/functional.md -> "No flags" ->
"Copying directory to directory"
"""


def test_code_copy_dir_to_existing_dir_omiting(vfs):
    """
    Verify cp returns code 1 if copying existing dir into existing dir w/o
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    code, *_ = vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir)
    assert code == 1


def test_msg_copy_dir_to_existing_dir_omiting(vfs):
    """
    Verify cp reports an error if copying existing dir into existing dir w/o
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    *_, stderr = vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir)
    assert stderr == bytes(
        f"cp: -r not specified; omitting directory '{vfs.root_dir}/SrcDir'\n",
        encoding="utf-8",
    )


def test_code_copy_dir_to_existing_dir(vfs):
    """
    Verify cp returns code 0 if copying existing dir into existing dir with
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    code, *_ = vfs.call_copy(
        src=vfs.root_dir / "SrcDir", dst=dst_dir, flags="-r"
    )
    assert code == 0


def test_dst_exists_copy_dir_to_existing_dir(vfs):
    """
    Verify cp creates directory if copying existing dir into existing dir with
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir()
    vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir, flags="-r")
    assert (dst_dir / "SrcDir").exists()


def test_code_copy_dir_to_nonexisting_dir_no_flag_r(vfs):
    """
    Verify cp returns code 1 if copying existing dir into non-existing dir w/o
    flag -r
    """
    dst_dir = vfs.root_dir / "DstDir"
    code, *_ = vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir)
    assert code == 1


def test_msg_copy_dir_to_nonexisting_dir_no_flag_r(vfs):
    """
    Verify cp reports an error if copying existing dir into existing dir w/o
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    *_, stderr = vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir)
    assert stderr == bytes(
        f"cp: -r not specified; omitting directory '{vfs.root_dir}/SrcDir'\n",
        encoding="utf-8",
    )


def test_code_copy_dir_to_nonexisting_dir_with_flag_r(vfs):
    """
    Verify cp returns code 0 if copying existing dir into non-existing dir with
    flag -r
    """
    dst_dir = vfs.root_dir / "DstDir"
    code, *_ = vfs.call_copy(
        src=vfs.root_dir / "SrcDir", dst=dst_dir, flags="-r"
    )
    assert code == 0


def test_dst_exists_copy_dir_to_nonexisting_dir_no_flag_r(vfs):
    """
    Verify cp reports an error if copying existing dir into existing dir w/o
    flag "-r"
    """
    dst_dir = vfs.root_dir / "DstDir"
    vfs.call_copy(src=vfs.root_dir / "SrcDir", dst=dst_dir, flags="-r")
    assert dst_dir.exists()
