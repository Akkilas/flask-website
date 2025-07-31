<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
  <h2>Welcome, {{ username }} 🎉</h2>
  <p>You have successfully logged in to your dashboard.</p>
  <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
