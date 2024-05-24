import manage
# Test the index route 
def test_index_success(client):
    # Send a GET request to the index endpoint
    response = client.get('/')
    # Verify that the response content type is 'text/html; charset=utf-8'
    assert response.content_type == 'text/html; charset=utf-8'
    # Verify that the response status code is 200 (OK)
    assert response.status_code == 200
    # Verify that the response text contains the expected HTML content
    assert "<h1>General Discussion</h1>" in response.text

def test_index_fail(client):
    # Send a GET request to the index endpoint
    response = client.get('/')
    # Verify that the response content type is 'text/html; charset=utf-8'
    assert response.content_type == 'text/html; charset=utf-8'
    # Verify that the response status code is 200 (OK)
    assert response.status_code == 200
    # Verify that the response text does not contain the expected HTML content
    assert "<h1>My dog is named Athena</h1>" not in response.text

# Test the profile route
def test_profile_success(client):
    # Send a POST request to the login endpoint with form data
    response = client.post("/login", data={
        'email': 'tristanjames3131@gmail.com',
        'password': 'Password'
    })
    # Verify that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Verify that the response location is '/profile'
    assert response.location == '/'
    # Send a GET request to the profile endpoint
    response = client.get('/profile')
    # Verify that the string is found in response.text
    assert '<div class="section profile-heading">' in response.text

def test_profile_fail(client):
    # Send a POST request to the login endpoint with form data
    response = client.post("/login", data={
        'email': 'tristanjames3131@gmail.com',
        'password': 'Password'
    })
    # Verify that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Verify that the response location is '/profile'
    assert response.location == '/'
    response = client.get('/profile')
    # Verify that the string is not found in response.text
    assert "Welcome, Huu Nguyen!" not in response.text

# Test the thread detailed route
def test_thread_detailed_success(client):
    # Send a GET request to the thread detailed endpoint
    response = client.get('/thread_detailed/1')
    # Verify that string is in response.text
    assert '<div class="subforum-icon subforum-column center">' in response.text

def test_thread_detailed_failed(client):
    # Send a GET request to the thread detailed endpoint
    response = client.get('/thread_detailed/1')
    # Verify that string is not in response.text
    assert 'What was your favourite course from term 2?' not in response.text

# Test the add page route
def test_add_page_success(client):
    # Send a GET request to the add page enpoint
    response = client.get('/add')
    # Verify that string is in response.text
    assert '<button type="submit" class="formbold-btn">Add Thread</button>' in response.text

def test_add_page_fail(client):
    # Send a GET request to the add page enpoint
    response = client.get('/add')
    # Verify that string is not in response.text
    assert '<button type="submit" class="formbold-btn">Delete Thread</button>' not in response.text
    
# Test Add Thread
def test_add_post_success(client):
    # Send a POST request to the root endpoint with form data
    response = client.post("/", data={
        'subheading': '1',
        'title': 'Athena',
        'content':'I love my dog'
    })
    # Verify that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Verify that the response location is '/'
    assert response.location == '/'
    
def test_add_post_fail(client):
    # Send a POST request to the root endpoint with form data
    response = client.post("/", data={
        'subheading': '1',
        'title': 'Athena',
        'content':''
    })
    # Verify that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Verify that the response location is '/'
    # Since content is an empty string, redirect back to /add route
    assert response.location == '/add'
    # Resetting database
    manage.run()        




    
    