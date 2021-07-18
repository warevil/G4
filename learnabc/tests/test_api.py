from ..app import app
from ..database import Base, get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class UserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    @staticmethod
    def disconnect():
        db = TestingSessionLocal()
        Base.metadata.drop_all(bind=db.get_bind())

    @classmethod
    def tearDownClass(cls):
        cls.disconnect()

    def test_create_user(self):
        response = self.client.post(
            "/user/",
            json={
                "name": "user_test",
                "email": "ut@test.com",
                "password": "pwd"
            },
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['name'] == "user_test"

    def test_login(self):

        # Test success login

        response = self.client.post(
            '/login',
            data={
                'username': 'ut@test.com',
                'password': 'pwd'
            },
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('access_token'))
        self.access_token = data.get('access_token')
        self.assertEqual(data.get('token_type'), 'bearer')

        # Test invalid password

        response = self.client.post(
            '/login',
            data={
                'username': 'ut@test.com',
                'password': 'jakia2'
            },
        )

        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get('detail'), 'Incorrect password')

        # Test invalid credentials
        response = self.client.post(
            '/login',
            data={
                'username': 'the_nobodies@gmail.com',
                'password': 'pwd'
            },
        )

        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get('detail'), 'Invalid Credentials')

    def test_get_user(self):
        # Existing user

        response = self.client.get(
            '/user/byemail/ut@test.com',
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('name'), 'user_test')
        self.assertEqual(data.get('email'), 'ut@test.com')
        self.assertEqual(len(data.get('courses_created')), 0)
        self.assertEqual(len(data.get('inscriptions')), 0)

        # Non existing user

        response = self.client.get(
            '/user/byemail/nobodie@test.com',
        )

        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data.get('detail'), "User with the email nobodie@test.com is not available")

    # def test_create_course(self):

    #     # Authenticated user
    #     print('token', self.access_token)
    #     response = self.client.post(
    #         '/course/',
    #         headers={
    #             'Content-Type': 'application/json',
    #             'Authorization': f'Bearer {self.access_token}'
    #         },
    #         data={
    #             'name': 'test course',
    #             'description': 'desc test course',
    #         }
    #     )

    #     data = response.json()

    #     self.assertTrue(data.get('id'))
    #     self.assertEqual(type(data.get('id')), 'int')

    #     # Non authenticated user

    #     response = self.client.post(
    #         '/course/',
    #         data={
    #             'name': 'test course',
    #             'description': 'desc test course',
    #         }
    #     )

    #     data = response.json()

    #     self.assertEqual(data.get('detail'), 'Not authenticated')


def ln(f): return getattr(UserTestCase, f).__code__.co_firstlineno
def cmp(a, b): return (a > b) - (a < b)
def lncmp(_, a, b): return cmp(ln(a), ln(b))


unittest.TestLoader.sortTestMethodsUsing = lncmp
