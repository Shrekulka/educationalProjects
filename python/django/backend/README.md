# Django 4.2 Blog Project

## Project Overview

This project is a fully functional blog developed using Django 4.2. It demonstrates best practices in Django development 
and includes a wide range of features characteristic of modern web applications. The project serves as an educational 
resource for learning Django and related technologies, as well as a foundation for creating fully-fledged web 
applications.

## Key Features

1. **Blog System:**
   - Create, edit, and delete articles with a rich text editor (CKEditor 5) for advanced content formatting
   - Categorize articles using a tree structure (MPTT) for easy navigation
   - Tagging system for improved search and grouping of related articles
   - Display related articles based on tags
   
2. **User System:**
   - Registration with email confirmation to protect against spam
   - Authentication (login/logout) with the ability to log in using either email or username
   - User profiles with editing capabilities and password change
   - Password recovery system via email
   
3. **Comments:**
   - Tree structure for comments (MPTT) for convenient discussions
   - Ability to reply to comments while maintaining hierarchy
   - Comment moderation
   - Add comments without page reload using AJAX
   
4. **Search:**
   - Full-text search using built-in PostgreSQL capabilities for fast and efficient content searching
   
5. **Additional Features:** 
   - Like/dislike system for content rating without page reload (AJAX)
   - Blog subscription for updates
   - Contact form to communicate with site administration using CAPTCHA for spam protection
   - Sitemap (sitemap.xml) for improved SEO
   - RSS feed for convenient tracking of new publications
   - View counter for articles
   - Display of popular articles for the last 7 days and daily
   
6. **Administrative Features:**
   - Enhanced Django admin panel
   - Automatic database backups using Celery Beat
7. **Technical Features:**
   - Asynchronous tasks using Celery for handling long operations (sending emails, creating backups)
   - Caching using Redis to improve performance
   - Project dockerization for easy deployment and scaling
   - Nginx configuration as a proxy server for handling static files and load balancing
   - PostgreSQL as the primary database
   - Gunicorn as the WSGI server for the production environment
   - SSL setup with Certbot for secure HTTPS connections

## Installation and Launch

### Prerequisites
- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)
- Git

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/Shrekulka/educationalProjects.git
    cd educationalProjects/python/django/backend
    ```
   
2. Create a .env.dev file in the docker/env/ directory and fill it with the necessary environment variables.
   Example content for the file:
    ```bash
    SECRET_KEY='your_secret_key'
    DEBUG=1
    ALLOWED_HOSTS='127.0.0.1 localhost'
    CSRF_TRUSTED_ORIGINS='http://127.0.0.1 http://localhost'
    POSTGRES_DB='your_db_name'
    POSTGRES_USER='your_db_user'
    POSTGRES_PASSWORD='your_db_password'
    POSTGRES_HOST='postgres'
    POSTGRES_PORT=5432
    REDIS_LOCATION='redis://redis:6379/1'
    CELERY_BROKER_URL='redis://redis:6379/0'
    CELERY_RESULT_BACKEND='redis://redis:6379/0'
    RECAPTCHA_PUBLIC_KEY='your_public_key'
    RECAPTCHA_PRIVATE_KEY='your_private_key'
    EMAIL_HOST='your_email_host'
    EMAIL_PORT=your_email_port
    EMAIL_USE_TLS=1
    EMAIL_HOST_USER='your_email'
    EMAIL_HOST_PASSWORD='your_email_password'
    ```
   
3. Modify the settings in settings.py to work with the environment variables.

4. Build the Docker images:
    ```bash
    docker compose -f docker-compose.dev.yml build
    ```
   
5. Launch the containers:
    ```bash
    docker compose -f docker-compose.dev.yml up
    ```
   
6. After successful launch, create a superuser:
    ```bash
    docker exec -it django sh
    python manage.py createsuperuser
    ```
   
7. The project will be available at http://localhost or http://127.0.0.1.

## Usage

- The admin panel is available at http://localhost/admin/
- Use the superuser credentials to log in.
- In the admin panel, you can create articles, categories, and tags, as well as manage users and comments.
- On the main page of the site, you will see a list of published articles.
- To create a new article, log in and use the corresponding form.
- Users can register, leave comments, like/dislike posts, and subscribe for updates.

## Development

The project uses Docker to create an isolated development environment. All necessary services (Django, PostgreSQL,
Redis, Celery) run in separate containers.

### To make changes to the code:

1. Modify the necessary files.

2. If you added new dependencies, update the requirements.txt file.

3. Rebuild the Docker images:
    ```bash
    docker compose -f docker-compose.dev.yml build
    ```
4. Restart the containers:
    ```bash
    docker compose -f docker-compose.dev.yml up
    ```
   
**To apply database migrations:**
bash docker exec -it django sh python manage.py makemigrations python manage.py migrate

### Deployment
**To deploy in a production environment:**
- Create a .env.prod file with the appropriate settings.
- Use docker-compose.prod.yml to build and launch the containers.
- Configure Nginx as a reverse proxy server.
- Set up SSL certificates for HTTPS connection.

## Project Structure

```bash
📁 backend                                        # Root directory of the project
│
├── 📁 backend/                                   # Main directory of the Django project
│   │
│   ├── __init__.py                               # Empty file marking the directory as a Python package
│   │
│   ├── asgi.py                                   # Entry point for ASGI-compatible web servers to run the project
│   │
│   ├── celery.py                                 # Celery configuration for asynchronous tasks and background processes
│   │
│   ├── settings.py                               # Main settings file of the Django project
│   │
│   ├── urls.py                                   # Main URL routing file, defining paths for the entire project
│   │   
│   └── wsgi.py                                   # Entry point for WSGI-compatible web servers to run the project
│   
├── 📁 cache/                                     # Directory for storing cache files
│   │ 
│   └── 2ee1e42baa1c3f47432251297a32790b.djcache  # Django cache file
│ 
├── 📁 docker/                                    # Directory with Docker configurations for project containerization
│   │
│   ├── 📁 env/                                   # Directory for environment variable files
│   │   │
│   │   ├── .env.dev                              # Environment variables file for development environment
│   │   │   
│   │   └── .env.prod                             # Environment variables file for production environment
│   │
│   ├── 📁 logs/                                  # Directory for storing Docker container logs
│   │   │
│   │   └── ...                                   # Various log files
│   │   
│   ├── 📁 nginx/                                 # Directory with Nginx configurations for request proxying
│   │   │
│   │   ├── 📁dev/                                # Nginx for development environment
│   │   │   │
│   │   │   └── django.conf                       # Nginx configuration for development environment
│   │   │   
│   │   └── 📁prod/                               # Nginx for production environment
│   │       │
│   │       └── django.conf                       # Nginx configuration for production environment
│   │ 
│   └── 📁 redis/                                 # Directory with Redis configuration (used for caching and Celery 
│       │                                         # queues)
│       └── 📁 data/                              # Subdirectory for storing Redis data
│           │
│           └── dump.rdb                          # Redis data dump file
│    
├── 📁 fixtures/                                  # Directory with database fixtures (initial data)
│   │
│   ├── 📁 blog/                                  # Fixtures for the blog application
│   │   │
│   │   ├── article.json                          # Initial data for blog articles
│   │   │
│   │   ├── category.json                         # Initial data for blog categories
│   │   │   
│   │   └── comment.json                          # Initial data for comments
│   │   
│   └── 📁 system/                                # Fixtures for the system application
│       │
│       ├── feedback.json                         # Initial data for feedback
│       │   
│       └── profile.json                          # Initial data for user profiles
│    
├── 📁 media/                                     # Directory for storing user media files
│   │
│   ├── 📁 articles_images/                       # Images related to blog articles
│   │   │   
│   │   └── ...                                   # Various article images
│   │   
│   └── 📁 images/                                # General directory for various types of images
│       │
│       ├── 📁 avatars/                           # User avatar images
│       │   │      
│       │   └── ...                               # Avatar files
│       │
│       └── 📁 thumbnails/                        # Image thumbnails
│           │
│           └── ...                               # Thumbnail files
│ 
├── 📁 modules/                                   # Directory with project modules (applications)
│   │
│   ├── 📁 blog/                                  # Blog application
│   │   │
│   │   ├── 📁 migrations/                        # Database migrations for the blog application
│   │       │
│   │       │   └── ...                           # Migration files
│   │       │
│   │   ├── 📁 templates/                         # HTML templates for the blog application
│   │   │   │
│   │   │   └── 📁 blog/                          # Blog application directory
│   │   │       │
│   │   │       ├── 📁 articles/                  # Templates for article pages
│   │   │       │   │
│   │   │       │   ├── articles_create.html      # Template for article creation page
│   │   │       │   │
│   │   │       │   ├── articles_delete.html      # Template for article deletion page
│   │   │       │   │
│   │   │       │   ├── articles_detail.html      # Template for article detail view page
│   │   │       │   │
│   │   │       │   ├── articles_func_list.html   # Template for functional article list
│   │   │       │   │
│   │   │       │   ├── articles_list.html        # Template for general article list
│   │   │       │   │
│   │   │       │   └── articles_update.html      # Template for article update page
│   │   │       │   
│   │   │       └── 📁 comments/                  # Templates for comments
│   │   │           │
│   │   │           └── comments_list.html        # Template for comments list
│   │   │
│   │   ├── 📁 templatetags/                      # Custom template tags and filters
│   │   │   │
│   │   │   ├── __init__.py                       # Initialization of the template tags package
│   │   │   │   
│   │   │   └── blog_tags.py                      # Definitions of custom tags for the blog
│   │   │
│   │   ├── __init__.py                           # Initialization of the blog application
│   │   │
│   │   ├── admin.py                              # Admin panel settings for blog models
│   │   │
│   │   ├── apps.py                               # Blog application configuration
│   │   │
│   │   ├── feeds.py                              # Blog RSS feed settings
│   │   │
│   │   ├── forms.py                              # Definitions of forms for the blog (creating/editing articles, etc.)
│   │   │
│   │   ├── models.py                             # Definitions of data models for the blog (articles, categories, 
│   │   │                                         # comments)
│   │   ├── sitemaps.py                           # Blog sitemap settings
│   │   │
│   │   ├── tests.py                              # Unit tests for the blog application
│   │   │
│   │   ├── urls.py                               # URL routes for the blog application
│   │   │   
│   │   └── views.py                              # Views (request handling logic) for the blog
│   │ 
│   ├── 📁 services/                              # General services and utilities for the project
│   │   │
│   │   ├── 📁 management/                        # Directory for custom Django management commands
│   │   │   │   
│   │   │   └── 📁 commands/                      # Custom Django management commands
│   │   │       │
│   │   │       ├── __init__.py                   # Initialization of the commands package
│   │   │       │   
│   │   │       └── dbackup.py                    # Command for creating a database backup
│   │   │
│   │   ├── __init__.py                           # Initialization of the services package
│   │   │
│   │   ├── email.py                              # Functions for working with email
│   │   │
│   │   ├── mixins.py                             # Mixins for code reuse
│   │   │
│   │   ├── tasks.py                              # Definitions of Celery asynchronous tasks
│   │   │   
│   │   └── utils.py                              # General utilities and helper functions
│   │ 
│   ├── 📁 system/                                # System application (user profiles, authentication, etc.)
│   │   │
│   │   ├── 📁 migrations/                        # Database migrations for the system application
│   │   │   │
│   │   │   └── ...                               # Migration files
│   │   │
│   │   ├── 📁 templates/                         # HTML templates for the system application
│   │   │   │
│   │   │   └── 📁 system/                        # Subdirectory with application name to prevent naming conflicts
│   │   │       │
│   │   │       ├── 📁 email/                           # Email templates
│   │   │       │   │
│   │   │       │   ├── activate_email_send.html        # Template for account activation email
│   │   │       │   │
│   │   │       │   ├── feedback_email_send.html        # Template for feedback email
│   │   │       │   │
│   │   │       │   ├── password_reset_mail.html        # Template for password reset email
│   │   │       │   │
│   │   │       │   └── password_subject_reset_mail.txt # Subject for password reset email
│   │   │       │
│   │   │       ├── 📁 errors/                          # Error page templates
│   │   │       │   │
│   │   │       │   └── error_page.html                 # General error page template
│   │   │       │   
│   │   │       ├── 📁 registration/                    # Templates for registration and authentication
│   │   │       │   │
│   │   │       │   ├── email_confirmation_failed.html  # Template for email confirmation failure page
│   │   │       │   │
│   │   │       │   ├── email_confirmation_sent.html    # Template for email confirmation sent page
│   │   │       │   │
│   │   │       │   ├── email_confirmed.html            # Template for successful email confirmation page
│   │   │       │   │
│   │   │       │   ├── user_login.html                 # Template for login page
│   │   │       │   │
│   │   │       │   ├── user_password_change.html       # Template for password change page
│   │   │       │   │
│   │   │       │   ├── user_password_reset.html        # Template for password reset page
│   │   │       │   │
│   │   │       │   ├── user_password_set_new.html      # Template for setting a new password page
│   │   │       │   │
│   │   │       │   └── user_register.html              # Template for registration page
│   │   │       │   
│   │   │       ├── feedback.html                       # Template for feedback page
│   │   │       │   
│   │   │       ├── profile_detail.html                 # Template for profile detail view page
│   │   │       │   
│   │   │       └── profile_edit.html                   # Template for profile edit page
│   │   │
│   │   ├── __init__.py                                 # Initialization of the system application
│   │   │
│   │   ├── admin.py                                    # Admin panel settings for the system application
│   │   │
│   │   ├── apps.py                                     # Configuration for the system application
│   │   │
│   │   ├── backends.py                                 # Custom authentication backends
│   │   │
│   │   ├── forms.py                                    # Definitions of forms for the system application
│   │   │
│   │   ├── middleware.py                               # Custom middleware
│   │   │
│   │   ├── models.py                                   # Definitions of data models for the system application
│   │   │
│   │   ├── tests.py                                    # Unit tests for the system application
│   │   │
│   │   ├── urls.py                                     # URL routes for the system application
│   │   │   
│   │   └── views.py                                    # Views (request handling logic) for the system application
│   └── __init__.py                                     # Initialization of the modules package
│ 
├── 📁 static/                                          # Directory for static files (CSS, JavaScript, images)
│   │
│   ├── 📁 css/                                         # CSS files
│   │   │
│   │   └── 📁 bootstrap/                               # CSS files for the Bootstrap framework
│   │       │
│   │       └── ...                                     # Various Bootstrap CSS files
│   │
│   ├── 📁 favicon/                                     # Directory for favicon files (site icons)
│   │   │
│   │   └── ...                                         # Various sizes and formats of favicons
│   │
│   ├── 📁 fonts/                                       # Directory for fonts
│   │   │
│   │   └── ...                                         # Font files (e.g., .woff, .ttf)
│   │
│   └── 📁 js/                                          # JS files
│       │
│       ├── 📁 bootstrap/                               # JavaScript files for the Bootstrap framework
│       │   │
│       │   └── ...                                     # Various Bootstrap JS files
│       │
│       └── 📁 custom/                                  # Directory for custom JavaScript files
│           │
│           ├── backend.js                              # Custom JS for backend functionality
│           │
│           ├── comments.js                             # JS for handling comments (e.g., AJAX submission)
│           │
│           ├── profile.js                              # JS for user profile functionality
│           │
│           └── ratings.js                              # JS for rating system (e.g., likes/dislikes)
│
├── 📁 staticfiles/                                     # Directory for collected static files (used in production)
│   └── ...                                             # Collected and optimized static files
│
├── 📁 templates/                                       # Directory for general project templates
│   │
│   ├── 📁 includes/                                    # Directory for include templates (page parts)
│   │   │
│   │   ├── latest_comments.html                        # Template for displaying latest comments
│   │   │
│   │   └── messages.html                               # Template for displaying system messages (e.g., errors, 
│   │                                                   # notifications)
│   ├── header.html                                     # Template for the header part of the page
│   │
│   ├── main.html                                       # Main page template (base layout)
│   │
│   ├── pagination.html                                 # Template for pagination
│   │
│   └── sidebar.html                                    # Template for the sidebar
│
├── 📁 venv/                                            # Directory for the Python virtual environment
│   │
│   └── ...                                             # Files and directories of the virtual environment
│
├── celerybeat-schedule                                 # Celery Beat schedule file (task scheduler)
│   
├── celerybeat-schedule.db                              # Celery Beat schedule database
│   
├── database-2024-06-28-09-07-13.json                   # Database backup file (dump in JSON format)
│   
├── db.json                                             # Current database dump in JSON format
│   
├── db.sqlite3                                          # SQLite database file (used for development)
│   
├── docker-compose.dev.yml                              # Docker Compose configuration for the development environment
│   
├── docker-compose.prod.yml                             # Docker Compose configuration for the production environment
│   
├── Dockerfile                                          # Instructions for building the Docker image of the project
│   
├── manage.py                                           # Django command-line utility for managing the project
│   
├── .gitignore                                          # File specifying files and directories to ignore in Git
│   
├── README.md                                           # Project documentation file with installation and usage 
│                                                       # instructions
├── requirements.txt                                    # List of Python project dependencies         
│      
├── 📁External Libraries/                               # Directory displayed in IDE (e.g., PyCharm)
│   │                                                   # Shows installed external Python libraries
│   └── ...                                             # Contains multiple subfolders and files of external libraries
│   
└── 📁 Scratches and Consoles/                          # IDE-specific directory (e.g., PyCharm)
    │                                                   # Used for temporary files and console sessions
    └── ...                                             # Contains various temporary files and scripts
```