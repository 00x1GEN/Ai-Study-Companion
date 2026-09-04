from sqlalchemy import select
from app.core.database import SessionLocal, ensure_extensions
from app.core.security import hash_password
from app.models import User, Course, Flashcard, Quiz, QuizQuestion
from app.services.gamification_service import seed_badges

def run():
    ensure_extensions()
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "student@aspira.test"))
        if not user:
            user = User(name="Demo Student", email="student@aspira.test", password_hash=hash_password("password123"))
            db.add(user); db.commit(); db.refresh(user)
        course = db.scalar(select(Course).where(Course.owner_id == user.id, Course.title == "Data Structures and Algorithms"))
        if not course:
            course = Course(
                owner_id=user.id,
                title="Data Structures and Algorithms",
                description="Lists, stacks, queues, trees, hashing and algorithmic thinking.",
            )
            db.add(course); db.commit(); db.refresh(course)
        if not db.scalar(select(Flashcard).where(Flashcard.course_id == course.id, Flashcard.user_id == user.id)):
            db.add_all([
                Flashcard(course_id=course.id, user_id=user.id, question="What principle does a stack use?", answer="LIFO — Last In, First Out."),
                Flashcard(course_id=course.id, user_id=user.id, question="What principle does a queue use?", answer="FIFO — First In, First Out."),
            ])
        if not db.scalar(select(Quiz).where(Quiz.course_id == course.id)):
            quiz = Quiz(course_id=course.id, title="Structures Quick Check")
            db.add(quiz); db.flush()
            db.add_all([
                QuizQuestion(quiz_id=quiz.id, question="Which structure uses FIFO?", option_a="Stack", option_b="Queue", option_c="Tree", option_d="Hash table", correct_index=1, explanation="Queue uses First In, First Out."),
                QuizQuestion(quiz_id=quiz.id, question="Which operation removes from a stack?", option_a="Pop", option_b="Enqueue", option_c="Merge", option_d="Hash", correct_index=0, explanation="Pop removes the top element from a stack."),
            ])
        seed_badges(db)
        db.commit()
        print("Seed complete.")

if __name__ == "__main__":
    run()
