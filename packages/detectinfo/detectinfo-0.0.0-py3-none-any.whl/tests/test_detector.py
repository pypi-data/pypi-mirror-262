from sensitive_info_detector.detector import check_for_secrets


def test_secrets_present():

    # Test whether sensitive information is correctly identified when present in a file.

    file_path = "/home/user/sensitive_info_detector/sensitive_info_detector/demo.txt"
    assert check_for_secrets(file_path) == True


# Test whether the function correctly identifies the absence of sensitive information in a file.
def test_no_secrets_present():

    file_path = (
        "/home/user/sensitive_info_detector/sensitive_info_detector/demonosecrets.txt"
    )
    check_for_secrets(file_path) == False


# Test whether the function handles the case where the specified file is not found .
def test_file_not_found():

    file_path = "non_existent_file.txt"
    assert check_for_secrets(file_path) == False
