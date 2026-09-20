from app.pdf.generator import generate_resume_pdf
from app.schemas.resume import Resume, ResumeHeader, ResumeProject, ResumeExperience, ResumeEducation

resume = Resume(
    header=ResumeHeader(
        name="Sathvik Chiluka",
        email="sathvikchiluka@gmail.com",
        phone="+91-9100780395",
        linkedin_url="https://linkedin.com/in/sathvik",
        github_url="https://github.com/Sathvik3819"
    ),
    summary="Computer Science undergraduate specializing in backend engineering with experience developing scalable REST APIs, authentication systems, Redis-backed session management, and real-time applications using Node.js, Express.js, MongoDB, Redis, and Socket.io.",
    skills=["Languages: JavaScript, Python, C", "Backend: Node.js, Express.js, REST APIs, JWT Authentication, Socket.io", "Databases: MongoDB, Redis, SQL", "Tools: Git, GitHub, Postman, Cloudinary", "Core CS: Data Structures & Algorithms, DBMS, Operating Systems, Computer Networks"],
    projects=[
        ResumeProject(
            name="TestForge - Real-Time Online Examination Platform",
            description="- Developed a scalable online examination platform supporting secure concurrent exam sessions.\n- Built REST APIs for authentication, exam management, submissions, and monitoring.\n- Implemented Redis-backed session and timer management for reliable exam execution.",
            technologies=["MERN Stack", "Redis", "Socket.io"],
            github_url="https://github.com/Sathvik3819/TestForge"
        )
    ],
    experience=[],
    education=[
        ResumeEducation(
            institution="Indian Institute of Information Technology, Sri City",
            degree="B.Tech in Computer Science",
            duration="2023-2027"
        ),
        ResumeEducation(
            institution="Sri Chaitanya Junior College",
            degree="Class XII",
            duration="2022"
        )
    ],
    certifications=["Solved 100+ Data Structures and Algorithms problems across coding platforms."]
)

generate_resume_pdf(resume, "resume_test2.pdf", "modern")
print("Generated resume_test2.pdf")
