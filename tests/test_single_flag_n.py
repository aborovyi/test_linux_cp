"""
This suite contains tests for section docs/functional.md -> single-flag cases
-> "-n"
"""


def test_code_flag_n_destination_is_missing(vfs):
    """
    Verify cp returns code 0 if destination is missing
    """
    code, *_ = vfs.call_copy(src=vfs.srcA, dst="dstA", flags="-n")
    assert code == 0


def test_dst_content_flag_n_destination_is_missing(vfs):
    """
    Verify cp copies file if destination is missing
    """
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags="-n")
    assert (vfs.root_dir / "dstA").read_text() == vfs.srcA.read_text()


def test_code_flag_n_destination_is_present(vfs):
    """
    Verify cp returns code 0 if destination is present
    """
    dst_file = vfs.root_dir / "dstA"
    dst_file.write_text("It's not the end")
    code, *_ = vfs.call_copy(src=vfs.srcA, dst="dstA", flags="-n")
    assert code == 0


def test_dst_content_flag_n_destination_is_present(vfs):
    """
    Verify cp omits the file if destination is present
    """
    dst_file = vfs.root_dir / "dstA"
    reference_text = "It's not the end"
    dst_file.write_text(reference_text)
    vfs.call_copy(src=vfs.srcA, dst="dstA", flags="-n")
    assert (vfs.root_dir / "dstA").read_text() == reference_text
