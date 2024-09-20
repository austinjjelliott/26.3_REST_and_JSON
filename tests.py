from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data and push an app context."""
        # Set up an app context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a test client
        self.client = app.test_client()

        # Drop and create all tables
        db.drop_all()
        db.create_all()

        # Add demo data
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions and pop the app context."""
        db.session.rollback()
        self.app_context.pop()

    def test_list_cupcakes(self):
        with self.client as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with self.client as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with self.client as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2, follow_redirects = True)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)





# from unittest import TestCase

# from app import app
# from models import db, Cupcake

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

# db.drop_all()
# db.create_all()


# CUPCAKE_DATA = {
#     "flavor": "TestFlavor",
#     "size": "TestSize",
#     "rating": 5,
#     "image": "http://test.com/cupcake.jpg"
# }

# CUPCAKE_DATA_2 = {
#     "flavor": "TestFlavor2",
#     "size": "TestSize2",
#     "rating": 10,
#     "image": "http://test.com/cupcake2.jpg"
# }


# class CupcakeViewsTestCase(TestCase):
#     """Tests for views of API."""

#     def setUp(self):
#         """Make demo data."""

#         Cupcake.query.delete()

#         cupcake = Cupcake(**CUPCAKE_DATA)
#         db.session.add(cupcake)
#         db.session.commit()

#         self.cupcake = cupcake

#     def tearDown(self):
#         """Clean up fouled transactions."""

#         db.session.rollback()

#     def test_list_cupcakes(self):
#         with app.test_client() as client:
#             resp = client.get("/api/cupcakes")

#             self.assertEqual(resp.status_code, 200)

#             data = resp.json
#             self.assertEqual(data, {
#                 "cupcakes": [
#                     {
#                         "id": self.cupcake.id,
#                         "flavor": "TestFlavor",
#                         "size": "TestSize",
#                         "rating": 5,
#                         "image": "http://test.com/cupcake.jpg"
#                     }
#                 ]
#             })

#     def test_get_cupcake(self):
#         with app.test_client() as client:
#             url = f"/api/cupcakes/{self.cupcake.id}"
#             resp = client.get(url)

#             self.assertEqual(resp.status_code, 200)
#             data = resp.json
#             self.assertEqual(data, {
#                 "cupcake": {
#                     "id": self.cupcake.id,
#                     "flavor": "TestFlavor",
#                     "size": "TestSize",
#                     "rating": 5,
#                     "image": "http://test.com/cupcake.jpg"
#                 }
#             })

#     def test_create_cupcake(self):
#         with app.test_client() as client:
#             url = "/api/cupcakes"
#             resp = client.post(url, json=CUPCAKE_DATA_2)

#             self.assertEqual(resp.status_code, 201)

#             data = resp.json

#             # don't know what ID we'll get, make sure it's an int & normalize
#             self.assertIsInstance(data['cupcake']['id'], int)
#             del data['cupcake']['id']

#             self.assertEqual(data, {
#                 "cupcake": {
#                     "flavor": "TestFlavor2",
#                     "size": "TestSize2",
#                     "rating": 10,
#                     "image": "http://test.com/cupcake2.jpg"
#                 }
#             })

#             self.assertEqual(Cupcake.query.count(), 2)


# # BUT NOTICE THAT THIS DID DELETE YOUR DATABASE AND IT MADE YOU HAVE TO RUN SEED FILE AGAIN! FYI!! 
# # # # This is the CHATGPT test for first test .... since the ones above gave me this error:  RuntimeError: Working outside of application context.
# # This typically means that you attempted to use functionality that needed
# # the current application. To solve this, set up an application context
# # with app.app_context(). See the documentation for more information.
# # import unittest
# # from app import app  # Assuming your app is in `app.py`
# # from models import db, Cupcake

# # class CupcakeTestCase(unittest.TestCase):
# #     def setUp(self):
# #         """Set up test client and application context."""
# #         # Ensure the app context is set up properly for the tests
# #         self.client = app.test_client()
# #         self.app_context = app.app_context()
# #         self.app_context.push()

# #         # Create all tables and set up initial data
# #         db.create_all()

# #     def tearDown(self):
# #         """Clean up after tests."""
# #         db.session.remove()
# #         db.drop_all()
# #         self.app_context.pop()

# #     def test_get_all_cupcakes(self):
# #         """Test retrieving all cupcakes."""
# #         response = self.client.get('/api/cupcakes')
# #         self.assertEqual(response.status_code, 200)
# #         data = response.json
# #         # Assuming some cupcakes exist, adjust based on your data
# #         self.assertIsInstance(data['cupcakes'], list)
