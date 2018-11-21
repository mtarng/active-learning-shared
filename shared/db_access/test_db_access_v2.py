import unittest
from unittest.mock import patch 
from unittest.mock import Mock

from .db_access_v2 import(
    ImageTagDataAccess,
    ArgumentException,
    ImageTagState,
    generate_test_image_infos
#    _update_images,
#    create_user,
#    get_image_ids_for_new_images,
#    get_new_images
)

class MockConnection:
    def _mock_cursor(self):
        self.fetchCount=5

        def fetchone():
            if (self.fetchCount):
                self.fetchCount = self.fetchCount-1
                return (["A","B"])
            return None

        def execute(query):
            return 

        test = Mock()
        test.execute = execute
        test.fetchone = fetchone
        return test

    def cursor(self):
        return self._mock_cursor()

class MockDBProvider:
    def __init__(self, fail = False):
        self.fail = fail

    def get_connection(self):
        if self.fail:
            raise Exception
        return MockConnection()

class TestImageTagDataAccess(unittest.TestCase):
    def test_connection(self):
        print("Running...")
        data_access = ImageTagDataAccess(MockDBProvider())
        data_access.test_connection()
        self.assertEqual(5, 5)
    
    def test_create_user_empty_string(self):
        with self.assertRaises(ArgumentException):
            data_access = ImageTagDataAccess(MockDBProvider())
            data_access.create_user('')
    
    def test_create_user_db_error(self):
        with self.assertRaises(Exception):
            data_access = ImageTagDataAccess(MockDBProvider(fail=True))
            data_access.create_user('MyUserName')

    def test_update_image_bad_image_state(self):
        with self.assertRaises(TypeError):
            data_access = ImageTagDataAccess(MockDBProvider())
            data_access._update_images((),"I should be an enum",1,None)

    def test_update_image_db_error(self):
        with self.assertRaises(Exception):
            data_access = ImageTagDataAccess(MockDBProvider(fail=True))
            data_access._update_images((),ImageTagState.READY_TO_TAG,1,None)

    def test_get_new_images_bad_request(self):
        with self.assertRaises(ArgumentException):
            data_access = ImageTagDataAccess(MockDBProvider())
            num_of_images = -5
            data_access.get_images_for_tagging(num_of_images, 5)

    def test_add_new_images_user_id_type_error(self):
        with self.assertRaises(TypeError):
            data_access = ImageTagDataAccess(MockDBProvider())
            data_access.add_new_images((),"I should be an integer")

    def test_add_new_images_connection_error(self):
        with self.assertRaises(Exception):
            data_access = ImageTagDataAccess(MockDBProvider(fail=True))
            data_access.add_new_images(generate_test_image_infos(5),10)

 #   def test_add_new_images_cursor_error(self):
 #       with self.assertRaises(Exception):
 #           data_access = ImageTagDataAccess(MockDBProvider(fail=True))
  #          data_access.add_new_images(generate_test_image_infos(5),10)

    def test_update_image_urls_user_id_type_error(self):
        with self.assertRaises(TypeError):
            data_access = ImageTagDataAccess(MockDBProvider())
            data_access.update_image_urls((),"I should be an integer")
 
if __name__ == '__main__':
    unittest.main()
