# Django Authentication API

A comprehensive Django-based authentication system that provides JWT token-based authentication with various user management features.

## Features

- JWT Token-based Authentication
- User Registration and Login
- Password Management (Reset, Change, Forgot)
- Token Management (Access and Refresh Tokens)
- Session Management
- Token Blacklisting for Security

## Authentication Endpoints

### User Authentication

#### Login
`POST /api/v1/auth/login_credentials`
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
Returns access and refresh tokens upon successful authentication.

#### Register
`POST /api/v1/auth/register_credentials`
```json
{
    "username": "new_username",
    "email": "user@example.com",
    "password": "your_password"
}
```
Creates a new user account and returns access and refresh tokens.

### Token Management

#### Get Access Token
`POST /api/v1/auth/access_token`
```json
{
    "refresh_token": "your_refresh_token"
}
```
Generates a new access token using a valid refresh token.

#### Get Refresh Token
`POST /api/v1/auth/refresh_token`
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
Generates a new refresh token.

### Password Management

#### Forgot Password
`POST /api/v1/auth/forgot_password`
```json
{
    "email": "your_email@example.com"
}
```
Sends a password reset link to the user's email.

#### Reset Password
`POST /api/v1/auth/reset_password`
```json
{
    "token": "reset_token_from_email",
    "new_password": "your_new_password"
}
```
Resets the password using the token received via email.

#### Change Password
`POST /api/v1/auth/change_password`
```json
{
    "current_password": "your_current_password",
    "new_password": "your_new_password"
}
```
Changes the password for an authenticated user.

### Session Management

#### Logout
`POST /api/v1/auth/logout`
```json
{
    "refresh_token": "your_refresh_token"
}
```
Logs out the user and blacklists the refresh token.

#### Get Session Info
`GET /api/v1/auth/session`

Returns current user session information.

#### Get Tokens
`GET /api/v1/auth/tokens`

Returns new access and refresh tokens for the authenticated user.

## Security Features

- Token Blacklisting for logged-out sessions
- Secure password reset flow
- Email verification for password reset
- JWT token expiration
- Protected routes using authentication middleware

## Authentication Flow

1. User registers or logs in
2. System provides access and refresh tokens
3. Access token is used for API requests
4. When access token expires, use refresh token to get new access token
5. For logout, refresh token is blacklisted

## Setup Requirements

1. Configure environment variables:
   - `FRONTEND_URL`: For password reset links
   - `DEFAULT_FROM_EMAIL`: For sending emails
   - JWT settings in Django settings

2. Database migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found

Error responses include a detail message explaining the error.