"""
This suite contains tests described in the docs/functional.md file under the
section "No flags"

Directory structure here is as follows:
    .
    └── srcA
"""


def test_returncode_if_cp_wo_arguments(vfs):
    """
    Verify cp returns status code 1 if called w/o arguments.
    """
    code, *_ = vfs.call_copy()
    assert code == 1


def test_msg_if_cp_wo_arguments(vfs):
    """
    Verify cp prints an error if arguments are missing
    """
    *_, std_err = vfs.call_copy()
    exp_msg = (
        b"cp: missing file operand\n"
        b"Try 'cp --help' for more information.\n"
    )
    assert std_err == exp_msg


def test_msg_if_cp_with_src_only(vfs):
    """
    Verify cp prints an error if only src argument is present
    """
    *_, std_err = vfs.call_copy(src=vfs.srcA.name)
    exp_msg = (
        b"cp: missing destination file operand after 'srcA'\n"
        b"Try 'cp --help' for more information.\n"
    )
    assert std_err == exp_msg


def test_return_code_if_cp_with_all_args(vfs):
    """
    Verify cp returns status code 0 if copying was successfull
    """
    code, *_ = vfs.call_copy(vfs.srcA.name, dst="dstA")
    assert code == 0


def test_no_msgs_if_cp_with_all_args(vfs):
    """
    Verify cp returns status code 0 if copying was successfull
    """
    _, stdout, stderr = vfs.call_copy(vfs.srcA.name, dst="dstA")
    assert len(stdout) == len(stderr) == 0


def test_dst_exists_if_cp_with_all_args(vfs):
    """
    Verify cp copies a file if all args are provided
    """
    vfs.call_copy(vfs.srcA.name, dst="dstA")
    assert (vfs.root_dir / "dstA").exists()
