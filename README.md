# Shivdhan Shirgole - Django Portfolio

Same structure and design as the Vijay resume website (multi-page, Bootstrap 5, header/footer includes),
with Shivdhan's content and a contact form that sends **two emails**:
one to the admin (shivdhanshirgole2808@gmail.com) and a "Thank you for contacting me" mail to the visitor.

## Folder structure
```
portfolio_django/
├── manage.py
├── resume_project/            project settings (settings.py, urls.py, wsgi.py, asgi.py)
├── portfolio/                 the app
│   ├── models.py              ContactMessage (mail tracking) + Project
│   ├── views.py               home, about, skills, projects, education, contact, send_contact_message
│   ├── urls.py                page URLs
│   ├── forms.py               contact form validation
│   ├── emails.py              sends admin mail + visitor thank-you mail
│   ├── email_backends.py      Brevo HTTPS email (for Render free plan)
│   ├── context_processors.py  email / phone / github shown on every page
│   ├── admin.py               /admin: messages (mail sent? errors?) and projects
│   ├── tests.py               python manage.py test
│   └── migrations/            database tables + the 6 starter projects
├── templates/
│   ├── base.html              Bootstrap, fonts, header, footer, flash messages
│   ├── includes/              header.html, footer.html
│   ├── portfolio/             home, about, skills, projects, education, contact
│   └── emails/                admin_notification.html, user_confirmation.html
├── static/
│   ├── css/style.css          the design
│   ├── js/script.js           menu, form counter, scroll effects
│   └── images/                put your photo here (optional)
├── run_local.bat              double-click: setup + start website (Windows)
├── create_admin.bat           double-click: create /admin login
├── test_email.bat             double-click: send a test email
├── requirements-local.txt     packages for your PC
├── requirements.txt           packages for Render (live)
├── .env.example               copy to .env and fill passwords (never upload .env)
└── render.yaml, build.sh      live deployment on Render
```

## Run on your PC (Windows)
1. Delete any old `venv` folder and any old `db.sqlite3`.
2. Double-click `run_local.bat` and open http://127.0.0.1:8000
3. Double-click `create_admin.bat`, then open http://127.0.0.1:8000/admin
4. Open `.env`, fill `EMAIL_HOST_PASSWORD` (Gmail App Password), run `test_email.bat`.

## Edit your content
- Projects: /admin -> Projects (add, hide, reorder).
- Skills, education, about, experience: edit the files in `templates/portfolio/`.
- Email / phone / GitHub shown on the site: `.env` (`PUBLIC_EMAIL`, `PUBLIC_PHONE`, `GITHUB_URL`).
