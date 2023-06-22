"""
This suite contains tests described in the docs/functional.md file under the
section "No flags"

Directory structure here is as follows:
    .
    ├── srcA
    └── SrcDir
"""

import pytest


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


def test_code_if_src_doesnt_replace_not_writeable_dst(vfs):
    """
    Verify cp sets return code to 1 while trying to copy file that can not be
    writeable
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Goodbye!")
    dst_file.chmod(0o444)
    code, *_ = vfs.call_copy(src=vfs.srcA.name, dst=dst_file.name)
    assert code == 1


def test_msg_if_src_doesnt_replace_not_writeable_dst(vfs):
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


@pytest.mark.parametrize(
    "path_prefix",
    [".", "..", "SrcDir"],
    ids=["this dir", "parent dir", "child dir"],
)
def test_code_if_src_copied_as_relative(vfs, path_prefix):
    """
    Verify cp returns status code 0 if src is copied as relative
    path
    """
    src_path = f"{path_prefix}/srcA"
    src_file = vfs.root_dir / path_prefix / "srcA"
    src_file.write_text("Thanks for all the fish!")
    code, *_ = vfs.call_copy(src=src_path, dst="dstA")
    assert code == 0


@pytest.mark.parametrize(
    "path_prefix",
    [".", "..", "SrcDir"],
    ids=["this dir", "parent dir", "child dir"],
)
def test_dst_exists_if_src_copied_as_relative(vfs, path_prefix):
    """
    Verify cp returns status code 0 if src is copied as relative
    path
    """
    src_path = f"{path_prefix}/srcA"
    src_file = vfs.root_dir / path_prefix / "srcA"
    src_file.write_text("Thanks for all the fish!")
    vfs.call_copy(src=src_path, dst="dstA")
    assert (vfs.root_dir / "dstA").exists()


def test_code_if_src_copied_as_absolute(vfs):
    """
    Verify cp returns code 0 on success if src is copied as absolute path
    """
    code, *_ = vfs.call_copy(src=vfs.srcA.absolute(), dst="dstA")
    assert code == 0


def test_dst_exists_if_src_copied_as_absolute(vfs):
    """
    Verify cp creates destination file on success if src is copied as absolute
    path
    """
    vfs.call_copy(src=vfs.srcA.absolute(), dst="dstA")
    assert (vfs.root_dir / "dstA").exists()


@pytest.mark.parametrize(
    "relative_path",
    [".", "..", "SrcDir"],
    ids=["this dir", "parent dir", "child dir"],
)
def test_code_if_dst_copied_as_relative(vfs, relative_path):
    """
    Verify cp returns code 0 on success if destination is relative path
    """
    dst_path = f"{relative_path}/dstA"
    (vfs.root_dir / dst_path).parent.mkdir(parents=True, exist_ok=True)
    code, *_ = vfs.call_copy(src=vfs.srcA.name, dst=dst_path)
    assert code == 0


@pytest.mark.parametrize(
    "relative_path",
    [".", "..", "SrcDir"],
    ids=["this dir", "parent dir", "child dir"],
)
def test_dst_exists_if_dst_copied_as_relative(vfs, relative_path):
    """
    Verify destination file created on success if destination is relative path
    """
    dst_path = f"{relative_path}/dstA"
    (vfs.root_dir / dst_path).parent.mkdir(parents=True, exist_ok=True)
    vfs.call_copy(src=vfs.srcA.name, dst=dst_path)
    assert (vfs.root_dir / relative_path / "dstA").exists()


def test_code_if_dst_copied_as_absolute(vfs):
    """
    Verify cp returns code 0 on success if destination is absolute path
    """
    dst_path = (vfs.root_dir / "dstA").absolute()
    code, *_ = vfs.call_copy(src=vfs.srcA.name, dst=dst_path)
    assert code == 0


def test_dst_exists_if_dst_copied_as_absolute(vfs):
    """
    Verify destination file is created on success if destination is absolute
    path
    """
    dst_path = (vfs.root_dir / "dstA").absolute()
    vfs.call_copy(src=vfs.srcA.name, dst=dst_path)
    assert dst_path.exists()


def test_code_file_copied_to_directory_with_no_name(vfs):
    """
    Verify cp returns code 0 if file is copied to the directory, no name is
    specified
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(exist_ok=True)
    code, *_ = vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}/")
    assert code == 0


def test_dst_exists_file_copied_to_directory_with_no_name(vfs):
    """
    Verify cp creates a file if file is copied to the directory, no name is
    specified
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(exist_ok=True)
    vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}/")
    assert (dst_dir / vfs.srcA.name).exists()


def test_code_file_copied_to_directory_wo_slash(vfs):
    """
    Verify cp returns code 0 if file is copied to the directory that doesn't
    end, with slash destination filename is not specified.
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(exist_ok=True)
    code, *_ = vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}")
    assert code == 0


def test_dst_exists_file_copied_to_directory_wo_slash(vfs):
    """
    Verify cp creates a file if file is copied to the directory that doesn't
    end, with slash destination filename is not specified.
    """
    dst_dir = vfs.root_dir / "DstDir"
    dst_dir.mkdir(exist_ok=True)
    vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}")
    assert (dst_dir / vfs.srcA.name).exists()


def test_code_file_copied_to_directory_with_name(vfs):
    """
    Verify cp returns code 0 if file is copied to the directory no name is
    specified
    """
    dst_file = vfs.root_dir / "DstDir" / "dstA"
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    code, *_ = vfs.call_copy(src=vfs.srcA, dst=dst_file)
    assert code == 0


def test_dst_exists_file_copied_to_directory_with_name(vfs):
    """
    Verify cp creates a file if file is copied to the directory no name is
    specified
    """
    dst_file = vfs.root_dir / "DstDir" / "dstA"
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    vfs.call_copy(src=vfs.srcA, dst=dst_file)
    assert dst_file.exists()


def test_code_error_on_missing_dst_dir(vfs):
    """
    Verify cp returns a code 1 on error if destination directory doesn't exist
    """
    dst_dir = vfs.root_dir / "temp_dir"
    code, *_ = vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}/")
    assert code == 1


def test_msg_error_on_missing_dst_dir(vfs):
    """
    Verify cp error message if destination directory doesn't exist
    """
    dst_dir = vfs.root_dir / "temp_dir"
    *_, stderr = vfs.call_copy(src=vfs.srcA, dst=f"{dst_dir}/")
    assert stderr == bytes(
        f"cp: cannot create regular file '{dst_dir}/': Not a directory\n",
        encoding="utf-8",
    )


@pytest.mark.chattr
def test_code_on_dst_file_has_attr_i(vfs):
    """
    Verify cp returns status code 1, if destination file exists and has
    attribute flag "i".
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Autobots, roll out!")
    vfs.set_attr(file=dst_file, attr="+i")
    code, *_ = vfs.call_copy(src=vfs.srcA, dst=dst_file)
    vfs.set_attr(file=dst_file, attr="-i")
    assert code == 1


@pytest.mark.chattr
def test_msg_on_dst_file_has_attr_i(vfs):
    """
    Verify cp reports an error if destination file exists and has attribute
    flag "i".
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("Autobots, roll out!")
    vfs.set_attr(file=dst_file, attr="+i")
    *_, stderr = vfs.call_copy(src=vfs.srcA, dst=dst_file)
    vfs.set_attr(file=dst_file, attr="-i")
    assert stderr == bytes(
        f"cp: cannot create regular file '{dst_file}': "
        "Operation not permitted\n",
        encoding="utf-8",
    )


@pytest.mark.chattr
def test_dst_remains_on_dst_file_has_attr_i(vfs):
    """
    Verify cp reports an error if destination file exists and has attribute
    flag "i".
    """
    dst_file = vfs.root_dir / "dstA"
    reference_content = "Autobots, roll out!"
    dst_file.write_text(reference_content)
    vfs.set_attr(file=dst_file, attr="+i")
    vfs.call_copy(src=vfs.srcA, dst=dst_file)
    vfs.set_attr(file=dst_file, attr="-i")
    dst_content = dst_file.read_text()
    assert dst_content == reference_content
