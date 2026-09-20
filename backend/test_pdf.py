from app.pdf.generator import generate_resume_pdf
from app.schemas.resume import Resume, ResumeHeader, ResumeProject, ResumeExperience, ResumeEducation

resume = Resume(
    header=ResumeHeader(
        name="SATHVIK CHILUKA",
        email="sathvikchiluka@gmail.com",
        phone="+91 9100780395",
        linkedin_url="linkedin.com/in/sathvik",
        github_url="github.com/Sathvik3819"
    ),
    summary="Full-stack software engineer dedicated to designing, developing, and maintaining secure, highly scalable applications. Proficient in building robust RESTful APIs...",
    skills=["JavaScript, Python, C", "React.js, HTML5, CSS3", "Node.js, Express.js", "MongoDB, Redis"],
    projects=[
        ResumeProject(
            name="TestForge - Real-Time Online Examination Platform",
            description="- Designed and developed a scalable online examination platform.\n- Built secure RESTful APIs.\n- Implemented Redis-based session management.",
            technologies=["React.js", "Node.js", "Redis", "Socket.io", "MongoDB"]
        )
    ],
    experience=[
        ResumeExperience(
            company="Some Company",
            role="Software Engineer Intern",
            duration="Jun 2024 - Aug 2024",
            description=["Developed X using Y.", "Improved performance by Z."]
        )
    ],
    education=[
        ResumeEducation(
            institution="Indian Institute of Information Technology, Sri City",
            degree="Bachelor of Technology in Computer Science",
            duration="2023 - 2027",
            grade="5.0"
        )
    ],
    certifications=["NPTEL Elite Certification"]
)

generate_resume_pdf(resume, "resume_test.pdf", "modern")
print("Generated resume_test.pdf")
