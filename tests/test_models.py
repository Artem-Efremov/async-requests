import pytest
import models


@pytest.mark.parametrize(
    'name, expected', [
        # Valid names
        ('Kassulke', True), ('Glover', True), ('Kling', True), ('Palma', True),
        ('Larson', True), ('Batz', True), ('Mills', True), ('Abshire', True), 
        ('Heidenreich', True), ('Horacio', True),
        # Invalid names
        ('PhD', False), ('MD', False), ('Prof.', False), ('Miss', False), 
        ('Mr.', False), ('Dr.', False), ('Sr.', False), ('I', False),
        ('DDS', False), ('II', False), ('IV', False), ('DVM', False), 
        ('Ms.', False), ('Mrs.', False)
    ]
)
def test_fakename_is_valid_name(name, expected):
    test_obj = models.FakeName()
    assert test_obj.is_valid_name(name) == expected



@pytest.mark.parametrize(
    'fullname, expected', [
        ('Dr. Eldred Crooks DDS', ['Eldred', 'Crooks']),
        ('Prof. Taya Kassulke', ['Taya', 'Kassulke']),
        ('Mister Casimir Harvey', ['Mister', 'Casimir', 'Harvey'])
    ]
)
def test_fakename_split_fullname(fullname, expected):
    test_obj = models.FakeName(fullname=fullname)
    assert sorted(test_obj.split_fullname()) == sorted(expected)
