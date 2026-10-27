from django.db import migrations

PROJECTS = [
    ("🎓", "Django", "Online Job Portal",
     "College placement portal connecting students with recruiters.",
     "Role-based access for Admin, Recruiter and Student\nSecure auth, job posting, search/filtering and applications\nNormalized relational schema with a responsive Bootstrap UI",
     "Python, Django, MySQL, Bootstrap", ""),
    ("📝", "Live", "MPSC Quiz Web App",
     "Marathi-language quiz platform for MPSC exam preparation.",
     "Subject-wise banks: Polity, Economy, Science, Current Affairs\nFirebase Authentication with email verification\nInstant scoring engine, mobile-friendly, hosted on GitHub Pages",
     "JavaScript, Firebase, HTML/CSS", "https://shivdhan739.github.io/Mpsc-Quiz/"),
    ("🏦", "Live", "ApexVolt Digital Banking",
     "Futuristic neon fintech website covering accounts, cards and digital banking.",
     "Fully responsive with Flexbox/Grid and CSS animations\nCross-browser, UX and accessibility focused\nGit version-controlled workflow, deployed on GitHub Pages",
     "HTML5, CSS3, JavaScript", "https://shivdhan739.github.io/ApexVolt/"),
    ("🛠", "Live", "Happy Home Services",
     "Home-services booking platform for plumbing, electrical, cleaning and appliance repair.",
     "Responsive front end with Bootstrap\nNode.js backend with MongoDB and MySQL integration\nDeployed online",
     "Node.js, MongoDB, MySQL", ""),
    ("👁", "Computer Vision", "Face Recognition Attendance",
     "Automated attendance with real-time face detection and recognition.",
     "OpenCV recognition pipeline\nFlask web interface for reports\nAttendance records stored in MySQL",
     "Python, OpenCV, Flask, MySQL", ""),
    ("📈", "Machine Learning", "Crime Rate Prediction",
     "ML model that forecasts crime trends from historical data.",
     "Data cleaning, analysis and Matplotlib visualization\nPandas and Scikit-learn modelling\nIntegrated into a Django web application",
     "Django, Pandas, Scikit-learn", ""),
]


def seed(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    if Project.objects.exists():
        return
    for i, (emoji, tag, title, desc, points, tech, link) in enumerate(PROJECTS, start=1):
        Project.objects.create(emoji=emoji, tag=tag, title=title, description=desc,
                               points=points, tech=tech, link=link, order=i)


class Migration(migrations.Migration):

    dependencies = [("portfolio", "0001_initial")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
