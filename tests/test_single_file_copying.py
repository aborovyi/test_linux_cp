"""
This suite contains tests described in the docs/functional.md file under the
section "No flags"

Directory structure here is as follows:
    .
    ├── DstDir
    ├── srcA
    ├── srcB
    ├── SrcDir
    │   ├── srcC
    │   └── SrcSubDir
    │       └── srcD
    └── srcLnk -> srcA
"""


def test_src_exists_dst_missing_same_dir(vfs):
    """
    Verify cp copies existing file to the destination.
    """
    dst_file = vfs.root_dir / "dstA"
    vfs.call_copy(src=vfs.srcA.name, dst="dstA")
    assert dst_file.exists()


def test_src_exists_dst_missing_same_dir_same_file(vfs):
    """
    Verify content for srcA and dstA are the same
    """
    dst_file = vfs.root_dir / "dstA"
    vfs.call_copy(src=vfs.srcA.name, dst=dst_file.name)
    assert vfs.srcA.read_text() == dst_file.read_text()


def test_code_if_src_not_readable_dst_missing(vfs):
    """
    Verify cp return code is 1 if source file is not readable
    """
    vfs.srcA.chmod(000)
    code, *_ = vfs.call_copy(src=vfs.srcA.name, dst="dstA")
    assert code == 1


def test_msg_if_src_not_readable_dst_missing(vfs):
    """
    Verify cp return code is 1 if source file is not readable
    """
    vfs.srcA.chmod(000)
    *_, stderr = vfs.call_copy(src=vfs.srcA.name, dst="dstA")
    assert stderr == b"cp: cannot open 'srcA' for reading: Permission denied\n"


def test_src_replaces_existing_dst(vfs):
    """
    Verify cp replaces destination file with the given source
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Goodbye!")
    vfs.call_copy(src=vfs.srcA.name, dst=dst_file.name)
    src_content = vfs.srcA.read_text()
    dst_content = dst_file.read_text()
    assert src_content == dst_content


def test_code_if_src_doesnt_replace_not_readable_dst(vfs):
    """
    Verify cp sets return code to 1 while trying to copy file that can not be
    writeable
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Goodbye!")
    dst_file.chmod(0o444)
    code, *_ = vfs.call_copy(src=vfs.srcA.name, dst=dst_file.name)
    assert code == 1


def test_msg_if_src_doesnt_replace_not_readable_dst(vfs):
    """
    Verify cp reports error while trying to copy file that can not be
    writeable
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Goodbye!")
    dst_file.chmod(0o444)
    *_, stderr = vfs.call_copy(src=vfs.srcA.name, dst=dst_file.name)
    assert (
        stderr == b"cp: cannot create regular file 'dstA': Permission denied\n"
    )
