from app.schemas.resume import (
    Resume,
    ResumeProject,
    ResumeEducation,
)

from app.pdf.generator import generate_resume_pdf


resume = Resume(

    name="Sathvik Chiluka",

    summary=(
        "Computer Science undergraduate with experience "
        "building full-stack and GenAI applications using "
        "Python, React, Node.js, LangChain and LangGraph."
    ),

    skills=[
        "Python",
        "JavaScript",
        "React",
        "Node.js",
        "Express.js",
        "MongoDB",
        "Redis",
        "LangChain",
        "LangGraph",
    ],

    projects=[

        ResumeProject(
            name="TestForge",
            description=(
                "Built a real-time online examination "
                "platform using React, Node.js, MongoDB, "
                "Redis and Socket.io."
            ),
            technologies=[
                "React",
                "Node.js",
                "MongoDB",
                "Redis",
                "Socket.io",
            ],
        ),

        ResumeProject(
            name="QuickRental",
            description=(
                "Built a MERN stack car rental application "
                "with Cloudinary for image storage."
            ),
            technologies=[
                "React",
                "Node.js",
                "MongoDB",
                "Cloudinary",
            ],
        ),
    ],

    experience=[],

    education=[
        ResumeEducation(
            institution="Your University",
            degree="B.Tech Computer Science Engineering",
            duration="2023 - 2027",
        )
    ],

    certifications=[
        "Generative AI"
    ],
)


output_path = "resume_test.pdf"

generate_resume_pdf(
    resume,
    output_path
)

print(f"PDF generated successfully: {output_path}")