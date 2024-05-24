# Test login post
def test_login_post_success(client):
        # Send a POST request to the login endpoint with form data
        response = client.post("/login", data={
            'email': 'tristanjames3131@gmail.com',
            'password': 'Password'
        })
        # Verify that the response status code is 302 (Redirect)
        assert response.status_code == 302
        # Verify that the response location is '/profile'
        assert response.location == '/'

def test_login_post_fail(client):
        # Send a POST request to the login endpoint with form data
        # email and password are not in database
        response = client.post("/login", data={
            'email': 'random@gmail.com',
            'password': '123456'
        })
        # Verify that the response status code is 302 (Redirect)
        assert response.status_code == 200

