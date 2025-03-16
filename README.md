# Welcome to the Django User Behavior Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-user-behavior)](https://github.com/lazarus-org/dj-user-behavior/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-user-behavior)](https://pypi.org/project/dj-user-behavior/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-user-behavior)](https://pypi.org/project/dj-user-behavior/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-user-behavior)](https://pypi.org/project/dj-user-behavior/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-user-behavior)](https://github.com/lazarus-org/dj-user-behavior/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-user-behavior)](https://github.com/lazarus-org/dj-user-behavior/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-user-behavior)](https://github.com/lazarus-org/dj-user-behavior)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-user-behavior/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-user-behavior)

[`dj-user-behavior`](https://github.com/lazarus-org/dj-user-behavior/) is a Django package developed by Lazarus to streamline the tracking, management, and analysis of user behavior within Django applications.

This package provides a robust and flexible framework for capturing detailed user interactions, page views, and session data through an optimized API and intuitive model structure.
Designed for scalability and performance, `dj-user-behavior` empowers developers to monitor user engagement, audit system activity, and derive actionable insights with ease, making it an essential tool for data-driven Django projects.

## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2
- Django REST Framework: >= 3.14

> **Note: Version Compatibility**
>
> For `Django >= 5.1`, use Django Rest Framework `3.15+`

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[API Guide](#api-guide)**: Detailed information on available APIs and endpoints.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[Settings](#settings)**: Configuration options and settings you can customize.

---

# Quick Start

This section provides a fast and easy guide to getting the `dj-user-behavior` package up and running in your Django
project.
Follow the steps below to quickly set up the package and start using the package.

## 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-user-behavior
```

**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-user-behavior
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-user-behavior
```

## 2. Install Django REST Framework

You need to install Django REST Framework for API support. If it's not already installed in your project, you can
install it via pip:

**Using pip:**

```bash
$ pip install djangorestframework
```

## 3. Add to Installed Apps

After installing the necessary packages, ensure that both `rest_framework` and `user_behavior` are added to
the `INSTALLED_APPS` in your Django `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework", # Required for API support

    "user_behavior",
    # ...
]
```

### 4. (Optional) Configure API Filters

To enable filtering through the API, install ``django-filter``, include ``django_filters`` in your ``INSTALLED_APPS`` and configure the filter settings.

Install ``django-filter`` using one of the above methods:

**Using pip:**

```bash
$ pip install django-filter
```

Add `django_filters` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
   # ...
   "django_filters",
   # ...
]
```

Then, set the filter class configuration in your ``settings.py``:

```python
USER_BEHAVIOR_API_PAGE_VIEW_FILTERSET_CLASS = "user_behavior.api.filters.PageViewFilter"
USER_BEHAVIOR_API_USER_SESSION_FILTERSET_CLASS = "user_behavior.api.filters.UserSessionFilter"
USER_BEHAVIOR_API_USER_INTERACTION_FILTERSET_CLASS = "user_behavior.api.filters.UserInteractionFilter"
```

You can also define your custom `FilterClass` and reference it in here if needed. This allows you to customize the filtering behavior according to your requirements. for more detailed info, refer to the [Settings](#settings) section.


## 5. Apply Migrations

Run the following command to apply the necessary migrations:

```shell
python manage.py migrate
```

## 6. Add User Behavior API URLs

You can use the API or the Django Template View for Dashboard by Including them in your project’s `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("user_behavior/", include("user_behavior.urls")),
    # ...
]
```

----

# API Guide

# Django User Behavior API Guide

## Overview

The `dj-user-behavior` package provides APIs for tracking and analyzing user behavior within your application. The API exposes three main endpoints:

- **User Sessions**: Tracks user session details.
- **Page Views**: Records the pages visited by users.
- **User Interactions**: Logs user interactions with elements on the website.

---

## Endpoints

### **User Sessions API**

#### **List User Sessions**
- **Endpoint**: `GET /sessions/`
- **Description**: Fetches all user sessions.
- **Response Example**:

```json
{
    "results": [
        {
            "id": 1,
            "session_id": "abc123",
            "user_agent": "Mozilla/5.0",
            "ip_address": "192.168.1.1",
            "start_time": "2025-03-01T12:00:00Z",
            "end_time": null,
            "user_id": "user_123"
        }
    ]
}
```

#### **Retrieve a User Session**
- **Endpoint**: `GET /sessions/{id}/`
- **Description**: Fetches details of a specific user session.
- **Response Fields**:
    - `session_id`: Unique session identifier.
    - `user_agent`: Browser and device details.
    - `ip_address`: IP address of the user.
    - `start_time`: Timestamp of session start.
    - `end_time`: Timestamp of session end (if applicable).
    - `user_id`: Optional user identifier.

#### **Create a User Session**
- **Endpoint**: `POST /sessions/`
- **Payload Example**:

```json
{
    "session_id": "abc123",
    "user_agent": "Mozilla/5.0",
    "ip_address": "192.168.1.1",
    "end_time": "2025-03-01T12:00:00Z",
    "user_id": "user_123"
}
```

---

### **Page Views API**

#### **List Page Views**
- **Endpoint**: `GET /pageviews/`
- **Description**: Retrieves a list of recorded page views.
- **Response Example**:

```json
{
    "results": [
        {
            "id": 1,
            "url": "https://example.com/home",
            "timestamp": "2025-03-01T12:05:00Z",
            "session_id": "abc123",
            "session": {
                "session_id": "abc123",
                "user_agent": "agent",
                "ip_address": "127.0.0.1",
                "start_time": "2025-03-14T14:14:33.522742Z",
                "end_time": null,
                "user_id": "1"
            }
        }
    ]
}
```

#### **Create a Page View**
- **Endpoint**: `POST /pageviews/`
- **Payload Example**:

```json
{
    "url": "https://example.com/home",
    "session_id": "abc123"
}
```

---

### **User Interactions API**

#### **List User Interactions**
- **Endpoint**: `GET /interactions/`
- **Description**: Fetches recorded user interactions.
- **Response Example**:

```json
{
    "results": [
        {
            "id": 1,
            "session": {
                "id": 1,
                "session_id": "1",
                "user_agent": "agent",
                "ip_address": "127.0.0.1",
                "start_time": "2025-03-14T14:14:33.522742Z",
                "end_time": null,
                "user_id": "1"
            },
            "event_type": "click",
            "element": "button#submit",
            "metadata": {}
        }
    ]
}
```

#### **Create a User Interaction**
- **Endpoint**: `POST /interactions/`
- **Payload Example**:

```json
{
    "session_id": "abc123",
    "event_type": "click",
    "element": "button#submit",
    "metadata": {}
}
```

---

## Throttling

The API includes a built-in throttling mechanism that limits the number of requests a user can make based on their role.
You can customize these throttle limits in the settings file.

To specify the throttle rates for users and staff members, add the following in your settings:

```ini
USER_BEHAVIOR_BASE_USER_THROTTLE_RATE = "100/day"
USER_BEHAVIOR_STAFF_USER_THROTTLE_RATE = "60/minute"
```

These settings limit the number of requests users can make within a given timeframe.

**Note:** You can define custom throttle classes for each ViewSet and reference them in your settings.

---

## Ordering, Filtering and Search

The API supports ordering, filtering and searching for all endpoints.

Options include:

- **Ordering**: Results can be ordered by fields dedicated to each ViewSet.

- **Filtering**: By default, the filtering feature is not included. If you want to use this, you need to install `django-filter` first, then add `django_filters` to your `INSTALLED_APPS` and provide the path to each filter class (`"user_behavior.api.filters.PageViewFilter"` or any other). Alternatively, you can use a custom filter class if needed.

- **Search**: You can search for any fields that is used is search fields.

These fields can be customized by adjusting the related configurations in your Django settings.

---

## Pagination

The API supports limit-offset pagination, with minimum, maximum, and default page size limits. This
controls the number of results returned per page.

---

## Permissions

The base permission for all endpoints is ``IsAuthenticated``, meaning users must be logged in to access the API. You can
extend this by passing an extra permission class like ``IsAdminUser`` or creating custom permission classes to implement more specific access control.


---

## Parser Classes

The API supports multiple parser classes that control how data is processed. The default parsers include:

- ``JSONParser``
- ``MultiPartParser``
- ``FormParser``

You can modify parser classes for each ViewSet by updating the API settings to include additional parsers or customize the existing ones
to suit your project.

----

Each feature can be configured through the Django settings file. For further details, refer to the [Settings](#settings)
section.

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of
the Django admin panels for managing user behaviors.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your
Django settings. Otherwise, Django may raise the following error during checks or the ModelAdmin will not accessible in
the Admin panel.

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class
instance

```python
USER_BEHAVIOR_ADMIN_SITE_CLASS = "path.to.your.custom.site"
```

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
USER_BEHAVIOR_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-user-behavior` to use your custom admin site for its Admin interface, preventing any errors and
ensuring a smooth integration with the custom admin interface.

# User Behavior Admin Panel

The `dj-user-behavior` package provides comprehensive admin interfaces for managing user behavior records—`UserSession`, `PageView`, and `UserInteraction`—within the Django admin panel. These interfaces, built with the `AdminPermissionControlMixin`, offer powerful tools for administrators to view, filter, and search user activity data efficiently. Below are the features and functionalities of each admin interface.

---

## UserSession Admin Panel

The `UserSessionAdmin` class provides an admin interface for managing user session records.

### Features

#### List Display

The list view for user session records includes the following fields:

- **Session ID**: The unique identifier for the session.
- **User Agent**: The user agent string of the client device.
- **IP Address**: The IP address of the client.
- **Start Time**: The timestamp when the session began.
- **End Time**: The timestamp when the session ended (if applicable).
- **User ID**: The identifier of the associated user.

#### List Display Links

By default, the `Session ID` field is a clickable link to the detailed view of each session record (configurable via Django admin defaults).

#### Filtering

Admins can filter the list of user session records based on:

- **Start Time**: Filter by the session start time.
- **End Time**: Filter by the session end time (if set).
- **User ID**: Filter by the associated user identifier.

#### Search Functionality

Admins can search for user session records using:

- **Session ID**: Search by session identifier.
- **User Agent**: Search by user agent string.
- **IP Address**: Search by client IP address.
- **User ID**: Search by user identifier.

#### Pagination

The admin list view displays **10 records per page** by default (Django admin default, unless overridden).

#### Read-Only Fields

The following field is marked as read-only in the detailed view:

- **Start Time**: The session start time (cannot be edited).

#### Fieldsets

The detailed view organizes fields into collapsible sections:

- **Main Section**: `session_id`, `user_agent`, `ip_address`, `user_id`.
- **Timestamps (Collapsed)**: `start_time`, `end_time`.

---

## PageView Admin Panel

The `PageViewAdmin` class provides an admin interface for managing page view records.

### Features

#### List Display

The list view for page view records includes the following fields:

- **Session**: The associated user session.
- **URL**: The URL of the visited page.
- **Timestamp**: The time the page was viewed.

#### List Display Links

By default, the `Session` field is a clickable link to the detailed view of each page view record (configurable via Django admin defaults).

#### Filtering

Admins can filter the list of page view records based on:

- **Timestamp**: Filter by the time the page was viewed.

#### Search Functionality

Admins can search for page view records using:

- **URL**: Search by the page URL.
- **Session ID**: Search by the `session_id` of the associated session (via `session__session_id`).

#### Autocomplete Fields

- **Session**: Provides an autocomplete dropdown for selecting the associated `UserSession`, improving usability when editing.

#### Pagination

The admin list view displays **10 records per page** by default (Django admin default, unless overridden).

#### Read-Only Fields

The following field is marked as read-only in the detailed view:

- **Timestamp**: The time the page was viewed (cannot be edited).

#### Fieldsets

The detailed view organizes fields into collapsible sections:

- **Main Section**: `session`, `url`.
- **Timestamp (Collapsed)**: `timestamp`.

---

## UserInteraction Admin Panel

The `UserInteractionAdmin` class provides an admin interface for managing user interaction records.

### Features

#### List Display

The list view for user interaction records includes the following fields:

- **Session**: The associated user session.
- **Event Type**: The type of interaction (e.g., `CLICK`, `SCROLL`).
- **Element**: The DOM element interacted with (e.g., `#submit-button`).
- **Timestamp**: The time the interaction occurred.

#### List Display Links

By default, the `Session` field is a clickable link to the detailed view of each interaction record (configurable via Django admin defaults).

#### Filtering

Admins can filter the list of user interaction records based on:

- **Event Type**: Filter by interaction type (e.g., `CLICK`, `SCROLL`).
- **Timestamp**: Filter by the time the interaction occurred.

#### Search Functionality

Admins can search for user interaction records using:

- **Element**: Search by the DOM element identifier.
- **Session ID**: Search by the `session_id` of the associated session (via `session__session_id`).

#### Autocomplete Fields

- **Session**: Provides an autocomplete dropdown for selecting the associated `UserSession`, enhancing usability when editing.

#### Pagination

The admin list view displays **10 records per page** by default (Django admin default, unless overridden).

#### Read-Only Fields

The following field is marked as read-only in the detailed view:

- **Timestamp**: The time the interaction occurred (cannot be edited).

#### Fieldsets

The detailed view organizes fields into collapsible sections:

- **Main Section**: `session`, `event_type`, `element`.
- **Metadata (Collapsed)**: `metadata` (JSON field for additional data).
- **Timestamp (Collapsed)**: `timestamp`.

----

# Settings

This section outlines the available settings for configuring the `dj-user-behavior` package. You can customize these
settings in your Django project's `settings.py` file to tailor the behavior of the system monitor to your
needs.

## Example Settings

Below is an example configuration with default values:

```python
# Admin Settings
USER_BEHAVIOR_ADMIN_SITE_CLASS = None
USER_BEHAVIOR_ADMIN_HAS_ADD_PERMISSION = True
USER_BEHAVIOR_ADMIN_HAS_CHANGE_PERMISSION = True
USER_BEHAVIOR_ADMIN_HAS_DELETE_PERMISSION = True
USER_BEHAVIOR_ADMIN_HAS_MODULE_PERMISSION = True

# Throttle Settings
USER_BEHAVIOR_BASE_USER_THROTTLE_RATE = "30/minute"
USER_BEHAVIOR_STAFF_USER_THROTTLE_RATE = "100/minute"

# Global API Settings
USER_BEHAVIOR_API_ALLOW_LIST = True
USER_BEHAVIOR_API_ALLOW_RETRIEVE = True
USER_BEHAVIOR_API_ALLOW_CREATE = True
USER_BEHAVIOR_API_EXTRA_PERMISSION_CLASS = None
USER_BEHAVIOR_API_PAGINATION_CLASS = "user_behavior.api.paginations.DefaultLimitOffSetPagination"
USER_BEHAVIOR_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]

# PageView API Settings
USER_BEHAVIOR_API_PAGE_VIEW_SERIALIZER_CLASS = None
USER_BEHAVIOR_API_PAGE_VIEW_ORDERING_FIELDS = ["timestamp"]
USER_BEHAVIOR_API_PAGE_VIEW_SEARCH_FIELDS = ["url", "session__session_id"]
USER_BEHAVIOR_API_PAGE_VIEW_THROTTLE_CLASSES = "user_behavior.api.throttlings.RoleBasedUserRateThrottle"
USER_BEHAVIOR_API_PAGE_VIEW_PAGINATION_CLASS = "user_behavior.api.paginations.DefaultLimitOffSetPagination"
USER_BEHAVIOR_API_PAGE_VIEW_EXTRA_PERMISSION_CLASS = None
USER_BEHAVIOR_API_PAGE_VIEW_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
USER_BEHAVIOR_API_PAGE_VIEW_FILTERSET_CLASS = None

# UserSession API Settings
USER_BEHAVIOR_API_USER_SESSION_SERIALIZER_CLASS = None
USER_BEHAVIOR_API_USER_SESSION_ORDERING_FIELDS = ["start_time", "end_time"]
USER_BEHAVIOR_API_USER_SESSION_SEARCH_FIELDS = ["session_id", "user_agent", "ip_address"]
USER_BEHAVIOR_API_USER_SESSION_THROTTLE_CLASSES = "user_behavior.api.throttlings.RoleBasedUserRateThrottle"
USER_BEHAVIOR_API_USER_SESSION_PAGINATION_CLASS = "user_behavior.api.paginations.DefaultLimitOffSetPagination"
USER_BEHAVIOR_API_USER_SESSION_EXTRA_PERMISSION_CLASS = None
USER_BEHAVIOR_API_USER_SESSION_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
USER_BEHAVIOR_API_USER_SESSION_FILTERSET_CLASS = None

# UserInteraction API Settings
USER_BEHAVIOR_API_USER_INTERACTION_SERIALIZER_CLASS = None
USER_BEHAVIOR_API_USER_INTERACTION_ORDERING_FIELDS = ["timestamp"]
USER_BEHAVIOR_API_USER_INTERACTION_SEARCH_FIELDS = ["session__session_id", "element"]
USER_BEHAVIOR_API_USER_INTERACTION_THROTTLE_CLASSES = "user_behavior.api.throttlings.RoleBasedUserRateThrottle"
USER_BEHAVIOR_API_USER_INTERACTION_PAGINATION_CLASS = "user_behavior.api.paginations.DefaultLimitOffSetPagination"
USER_BEHAVIOR_API_USER_INTERACTION_EXTRA_PERMISSION_CLASS = None
USER_BEHAVIOR_API_USER_INTERACTION_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
USER_BEHAVIOR_API_USER_INTERACTION_FILTERSET_CLASS = None
```

# Settings Overview

This section provides a detailed explanation of the available settings in the `dj-user-behavior` package. You can configure these settings in your Django project's `settings.py` file to tailor the behavior of the system to your needs.

## Admin Settings

### `USER_BEHAVIOR_ADMIN_SITE_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Specifies a custom AdminSite class to be applied to the admin interface for enhanced customization.

---

### `USER_BEHAVIOR_ADMIN_HAS_ADD_PERMISSION`
**Type**: `bool`

**Default**: `True`

**Description**: Determines whether users have permission to add new records in the admin panel.

---

### `USER_BEHAVIOR_ADMIN_HAS_CHANGE_PERMISSION`
**Type**: `bool`

**Default**: `True`

**Description**: Controls whether users can modify existing records in the admin panel.

---

### `USER_BEHAVIOR_ADMIN_HAS_DELETE_PERMISSION`
**Type**: `bool`

**Default**: `True`

**Description**: Specifies if users have permission to delete records in the admin panel.

---

### `USER_BEHAVIOR_ADMIN_HAS_MODULE_PERMISSION`
**Type**: `bool`

**Default**: `True`

**Description**: Determines whether users have module-level permissions in the admin panel.

---

## Throttle Settings

### `USER_BEHAVIOR_BASE_USER_THROTTLE_RATE`
**Type**: `str`

**Default**: `"30/minute"`

**Description**: Defines the throttle rate for regular users (requests per time unit).

---

### `USER_BEHAVIOR_STAFF_USER_THROTTLE_RATE`
**Type**: `str`

**Default**: `"100/minute"`

**Description**: Defines the throttle rate for staff users (requests per time unit).

---

## Global API Settings

### `USER_BEHAVIOR_API_ALLOW_LIST`
**Type**: `bool`

**Default**: `True`

**Description**: Enables or disables listing of API resources.

---

### `USER_BEHAVIOR_API_ALLOW_RETRIEVE`
**Type**: `bool`

**Default**: `True`

**Description**: Allows retrieving specific records through the API.

---

### `USER_BEHAVIOR_API_ALLOW_CREATE`
**Type**: `bool`

**Default**: `True`

**Description**: Enables or disables the creation of new records via the API.

---

### `USER_BEHAVIOR_API_EXTRA_PERMISSION_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Specifies additional permission classes for API access control.

---

### `USER_BEHAVIOR_API_PAGINATION_CLASS`
**Type**: `str`

**Default**: `"user_behavior.api.paginations.DefaultLimitOffSetPagination"`

**Description**: Defines the pagination class for API responses.

---

### `USER_BEHAVIOR_API_PARSER_CLASSES`
**Type**: `List[str]`

**Default**:
```python
[
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
```

**Description**: Specifies parsers for handling different request data formats.

---

## PageView API Settings

### `USER_BEHAVIOR_API_PAGE_VIEW_SERIALIZER_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the serializer class for page view API responses.

---

### `USER_BEHAVIOR_API_PAGE_VIEW_ORDERING_FIELDS`
**Type**: `List[str]`

**Default**: `['timestamp']`

**Description**: Specifies fields for ordering results in the page view API.

---

### `USER_BEHAVIOR_API_PAGE_VIEW_SEARCH_FIELDS`
**Type**: `List[str]`

**Default**: `['url', 'session__session_id']`

**Description**: Defines fields that can be searched within the page view API.

---

### `USER_BEHAVIOR_API_PAGE_VIEW_THROTTLE_CLASSES`
**Type**: `str`

**Default**: `"user_behavior.api.throttlings.RoleBasedUserRateThrottle"`

**Description**: Specifies the throttle class for page view API requests.

---

## UserSession API Settings

### `USER_BEHAVIOR_API_USER_SESSION_SERIALIZER_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the serializer class for user session API responses.

---

### `USER_BEHAVIOR_API_USER_SESSION_ORDERING_FIELDS`
**Type**: `List[str]`

**Default**: `['start_time', 'end_time']`

**Description**: Specifies ordering fields for user session API results.

---

### `USER_BEHAVIOR_API_USER_SESSION_SEARCH_FIELDS`
**Type**: `List[str]`

**Default**: `['session_id', 'user_agent', 'ip_address']`

**Description**: Defines searchable fields in the user session API.

---

### `USER_BEHAVIOR_API_USER_SESSION_THROTTLE_CLASSES`
**Type**: `str`

**Default**: `"user_behavior.api.throttlings.RoleBasedUserRateThrottle"`

**Description**: Specifies the throttle class for user session API requests.

---

## UserInteraction API Settings

### `USER_BEHAVIOR_API_USER_INTERACTION_SERIALIZER_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the serializer class for user interaction API responses.

---

### `USER_BEHAVIOR_API_USER_INTERACTION_ORDERING_FIELDS`
**Type**: `List[str]`

**Default**: `['timestamp']`

**Description**: Specifies ordering fields for user interaction API results.

---

### `USER_BEHAVIOR_API_USER_INTERACTION_SEARCH_FIELDS`
**Type**: `List[str]`

**Default**: `['session__session_id', 'element']`

**Description**: Defines searchable fields in the user interaction API.

---

### `USER_BEHAVIOR_API_USER_INTERACTION_THROTTLE_CLASSES`
**Type**: `str`

**Default**: `"user_behavior.api.throttlings.RoleBasedUserRateThrottle"`

**Description**: Specifies the throttle class for user interaction API requests.

---

### `USER_BEHAVIOR_API_USER_INTERACTION_FILTERSET_CLASS`
**Type**: `Optional[str]`

**Default**: `None`

**Description**: Defines the filter class for user interaction API responses.

---

This overview should help you understand and customize the settings for the `dj-user-behavior` package as needed.

---

### UserSession ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `UserSessionViewSet`:

- **`session_id`**: Unique identifier for the session (orderable, searchable, filterable).
  - **Description**: A string representing the session’s unique ID (e.g., `"test_session_123"`).
- **`user_agent`**: The user agent string of the client device (searchable, filterable).
  - **Description**: Captures the browser or device information (e.g., `"Mozilla/5.0 ..."`).
- **`ip_address`**: The IP address of the client (searchable, filterable).
  - **Description**: The network address of the user (e.g., `"192.168.1.1"`).
- **`start_time`**: The timestamp when the session began (orderable, filterable).
  - **Description**: A datetime marking the session start (e.g., `"2025-03-15T09:59:00+00:00"`).
- **`end_time`**: The timestamp when the session ended, if applicable (orderable, filterable).
  - **Description**: A datetime marking the session end, nullable (e.g., `null` or `"2025-03-15T10:59:00+00:00"`).
- **`user_id`**: The identifier of the associated user (searchable, filterable).
  - **Description**: A string linking the session to a user (e.g., `"user123"`).

---

### PageView ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `PageViewViewSet`:

- **`id`**: Unique identifier of the page view (orderable, filterable).
  - **Description**: An integer primary key for the page view record (e.g., `1`).
- **`session`**: The associated user session (searchable via `session__session_id`, filterable).
  - **Description**: A foreign key to `UserSession`, typically represented by `session_id` in searches (e.g., `"test_session_123"`).
- **`url`**: The URL of the visited page (searchable, filterable).
  - **Description**: The full URL viewed by the user (e.g., `"https://example.com/test-page"`).
- **`timestamp`**: The time the page was viewed (orderable, filterable).
  - **Description**: A datetime of when the page view occurred (e.g., `"2025-03-15T10:00:00+00:00"`).

---

### UserInteraction ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `UserInteractionViewSet`:

- **`id`**: Unique identifier of the user interaction (orderable, filterable).
  - **Description**: An integer primary key for the interaction record (e.g., `1`).
- **`session`**: The associated user session (searchable via `session__session_id`, filterable via `session__id`).
  - **Description**: A foreign key to `UserSession`, searchable by `session_id` (e.g., `"test_session_123"`).
- **`event_type`**: The type of interaction (orderable, filterable).
  - **Description**: An enum value (e.g., `"CLICK"`, `"SCROLL"`) from `EventType`.
- **`element`**: The DOM element interacted with (searchable, filterable).
  - **Description**: A string identifying the element (e.g., `"#submit-button"`).
- **`timestamp`**: The time the interaction occurred (orderable, filterable).
  - **Description**: A datetime of when the interaction happened (e.g., `"2025-03-15T10:02:00+00:00"`).
- **`metadata`**: Additional JSON data about the interaction (filterable).
  - **Description**: A JSON field with key-value pairs (e.g., `{"x_coord": 100, "y_coord": 200}`), filterable via custom `filter_metadata` (e.g., `metadata__x_coord=100`).

----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-user-behavior`.

### Final Notes:

- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python
  versions.
- **API Integration**: The package is designed for flexibility, allowing you to customize many features based on your
  application's needs.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for
  more details.

If you encounter any issues or have feedback, please reach out via
our [GitHub Issues page](https://github.com/lazarus-org/dj-user-behavior/issues).
