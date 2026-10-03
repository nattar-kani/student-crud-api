from fastapi import FastAPI, HTTPException, status

from .schemas import StudentCreate, StudentResponse


app = FastAPI(
    title="Student CRUD API",
    description="A simple FastAPI application for managing students",
    version="1.0.0"
)


students: list[StudentResponse] = []

next_student_id = 1


@app.get("/")
def root():
    return {
        "message": "Student CRUD API is running"
    }


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    global next_student_id

    for existing_student in students:
        if existing_student.email == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this email already exists"
            )

    new_student = StudentResponse(
        id=next_student_id,
        **student.model_dump()
    )

    students.append(new_student)

    next_student_id += 1

    return new_student


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students():

    return students


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):

    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentCreate
):

    for index, student in enumerate(students):

        if student.id == student_id:

            for existing_student in students:
                if (
                    existing_student.email == student_data.email
                    and existing_student.id != student_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="A student with this email already exists"
                    )

            updated_student = StudentResponse(
                id=student_id,
                **student_data.model_dump()
            )

            students[index] = updated_student

            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student.id == student_id:
            students.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )