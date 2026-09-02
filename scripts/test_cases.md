# Gatekeeper Test Cases

| Feature | Test Case | Expected Result | Actual Result |
|---------|-----------|-----------------|---------------|
| Signup | Create new user | User added, success message | ✅ Pass|
| Login | Valid credentials | Redirect to dashboard | ✅ Pass|
| Login | Wrong password | Error message | ✅ Pass|
| Role Redirect | Admin | Goes to admin_dashboard.py |✅ Pass |
| Role Redirect | Logs | Goes to logs_dashboard.py | ✅ Pass|
| Role Redirect | User | Goes to user_dashboard.py | ✅ Pass|
| Remember Me | Checked | Session expiry = 7 days | ✅ Pass|
| Logout | Click logout | Cookies cleared, back to login | ✅ Pass|
