from authbox_setup_version import get_version, increment_version

def test_get_version():
    # version file contain: Version("menu", 1, 0, 31)
    assert get_version('../tests/version_file.py')  == "1.0.31", "Should be 1.0.31"
    
def test_increment_version():
    # version file contain: Version("menu", 1, 0, 31)
    assert increment_version('../tests/version_file.py')  == "1.0.32", "Should be 1.0.32"
    assert increment_version('../tests/version_file.py', major=1)  == "2.0.31", "Should be 2.0.31"
    assert increment_version('../tests/version_file.py', minor=2)  == "1.1.31", "Should be 1.1.31"
    
