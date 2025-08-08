from pptx import Presentation

# Create a new presentation
prs = Presentation()

# Define slides content
slides = [
    {
        "title": "Welcome to InstaCore",
        "content": [
            "Institute Management System",
            "A Modern Web-Based Platform for Institutes",
            "Presented by Team InstaCore"
        ]
    },
    {
        "title": "With due respect to",
        "content": [
            "Instructor: [Insert Sir's Name]",
            "",
            "Team Members:",
            "- Khalid Mahmud – Team Leader & Backend Developer",
            "- Humaira Akter – Designer & UI/UX",
            "- Mehedi Alam – Co-Leader & Full-stack Developer",
            "- Shakil Ahmed – Developer & QA"
        ]
    },
    {
        "title": "Project Overview",
        "content": [
            "InstaCore – Institute Management System",
            "A responsive, secure, and scalable web-based platform",
            "Designed to modernize institute operations",
            "Addresses outdated systems with enhanced UX and APIs"
        ]
    },
    {
        "title": "Core Features (Phase 1)",
        "content": [
            "1. Landing page with login & signup",
            "2. Custom authentication with Django",
            "3. Email verification for signup",
            "4. OTP verification before account deletion",
            "5. User-specific dashboards",
            "6. Profile management: edit, change password, delete",
            "7. Role-aware navigation & fixed footer"
        ]
    },
    {
        "title": "How It Works – User Flow",
        "content": [
            "1. Visit index → login or signup",
            "2. Signup → verify email → login",
            "3. Dashboard → manage profile, password, account",
            "4. OTP required before account deletion",
            "5. Logout securely"
        ]
    },
    {
        "title": "Tech Stack",
        "content": [
            "Backend: Django (Custom User Model, OTP, Email Verification)",
            "Frontend: HTML, CSS, JavaScript",
            "Database: SQLite (Dev), PostgreSQL (Production)",
            "Upcoming: Django REST Framework for API integration"
        ]
    },
    {
        "title": "Project Timeline",
        "content": [
            "11 Aug – Present idea, mockups, and plan",
            "17 Aug – Complete frontend and authentication",
            "21 Aug – Add CRUD operations & APIs",
            "24 Aug – Finalize all features and submit"
        ]
    },
    {
        "title": "Future Plans",
        "content": [
            "• Role-based dashboards (Admin, Teacher, Student)",
            "• Announcements & notifications module",
            "• Attendance & results tracking",
            "• Public API documentation"
        ]
    },
    {
        "title": "Mockup Preview",
        "content": [
            "• Landing Page",
            "• Login Page",
            "• Dashboard",
            "• Profile Page",
            "All designs are mobile-friendly and intuitive."
        ]
    },
    {
        "title": "Conclusion",
        "content": [
            "InstaCore: Secure, Flexible, Future-Ready",
            "A real-world solution for institute management",
            "Meets DiPTi requirements and beyond",
            "Q&A session with our team now begins"
        ]
    },
    {
        "title": "Q&A",
        "content": [
            "We’re ready to take your questions!",
            "Thank you for your time and attention."
        ]
    }
]

# Function to create slides
def add_bullet_slide(prs, title, content):
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = title
    content_placeholder = slide.placeholders[1]
    content_placeholder.text = content[0]
    for line in content[1:]:
        p = content_placeholder.text_frame.add_paragraph()
        p.text = line

# Add slides
for slide in slides:
    add_bullet_slide(prs, slide["title"], slide["content"])

# Save the file
prs.save("InstaCore_Presentation.pptx")
print("Presentation saved as InstaCore_Presentation.pptx")
