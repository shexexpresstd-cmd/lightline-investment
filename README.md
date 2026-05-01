# Lightline Investment Website

A modern, dynamic Python Flask web application with SQLite database for managing an investment company website.

## Features

- **Dynamic Website** - Home, About, Services, Portfolio, Contact pages
- **SQLite Database** - Stores contacts, subscribers, services, portfolio, team, testimonials
- **Admin Dashboard** - Manage all content from the admin panel
- **Responsive Design** - Mobile & desktop optimized
- **Dynamic Animations** - CSS animations, parallax effects, particle system
- **API Endpoints** - Contact form & newsletter subscriptions via JSON API

## Dynamic Elements

### CSS Animations
- Floating particles background
- Card hover effects with 3D tilt
- Gradient background animations
- Smooth scroll reveal animations
- Magnetic button effects
- Parallax scrolling

### JavaScript Interactions
- Counter animations (stats)
- Scroll-triggered reveals
- Form validation & submission
- Mobile menu toggle
- Image lazy loading
- Smooth scrolling

## Project Structure

```
lightline-investment/
├── app.py              # Flask application
├── lightline_investment.db  # SQLite database (auto-created)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── about.html      # About page
│   ├── services.html   # Services page
│   ├── portfolio.html  # Portfolio page
│   ├── contact.html    # Contact page
│   ├── error.html      # Error page
│   └── admin/          # Admin templates
│       ├── login.html
│       ├── dashboard.html
│       ├── contacts.html
│       ├── services.html
│       ├── portfolio.html
│       └── subscribers.html
└── assets/             # Static assets
    ├── css/
    ├── js/
    └── images/
```

## Installation

1. **Install dependencies:**
   ```bash
   pip install flask
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   - Local: http://127.0.0.1:5000
   - Admin: http://127.0.0.1:5000/admin

## Database Tables

- **contacts** - Contact form submissions
- **subscribers** - Newsletter subscribers
- **services** - Investment services offered
- **portfolio** - Investment projects
- **team** - Team members
- **testimonials** - Client testimonials
- **stats** - Statistics to display

## API Endpoints

- `POST /api/contact` - Submit contact form
- `POST /api/subscribe` - Newsletter subscription

## Admin Features

- Dashboard with stats overview
- Manage contacts (mark as read, delete)
- Add/edit/delete services
- Add/remove portfolio items
- View subscribers list
