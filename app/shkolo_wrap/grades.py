import re

from app import CourseCRUD, GradeCRUD, GradeCreate, Grade, Course, GradeSchema
from app.shkolo_wrap.user import get_class_id

# GRADE_BTN_REGEX = r"<button[^>]*class=\"[^\"]*grade[^>]*>(\d+)<\/button>"
PUPIL_ID_PATTERN = r'<input id="pupil_id_field"[^>]*value="(\d+)"'
CLASS_ID_PATTERN = r'<input id="class_year_id_field"[^>]*value="(\d+)"'
TABLE_PATTERN = r'<table[^>]*id="tableGrades"[^>]*>(.*?)</table>'
COURSE_GRADES_REGEX = (
    r'data-course-id="(\d+)"[\s\S]*?<td>\s*<i[^>]*></i>\s*([^<]+)</td>'   # Capture course_id and course_name
    r'|id="grade_(\d+)"[^>]*>(\d+)'                                       # Capture grade_id and grade_value
)

async def process_grades(source: str, pupil_id):
    # async with session.get(f"https://app.shkolo.bg/ajax/diary/getGradesForPupil?pupil_id={pupil_id}") as resp:
    #     content = (await resp.read()).decode()

    table_match = re.search(TABLE_PATTERN, source, re.DOTALL)

    if not table_match:
        raise ValueError("Grades table not found")

    table = table_match.group(1)
    matches = re.findall(COURSE_GRADES_REGEX, table)

    grades = [match for match in matches if not match[0]]
    grade_count = await Grade.all().count()

    if grade_count == len(grades):
        return

    class_id = await get_class_id()

    course_id = None
    courses = []
    grades = []
    for match in matches:
        if match[0]:  # Captured a course_id
            course_id = match[0]
            course_name = match[1].strip()

            courses.append(Course(id=course_id, name=course_name, year_class_id=class_id))
        else:  # Captured a grade id and value
            grades.append(Grade(
                id=match[2], value=match[3], course_id=course_id, pupil_id=pupil_id
            ))

    await Course.bulk_create(courses, ignore_conflicts=True)
    grades_db = await Grade.bulk_create(grades, ignore_conflicts=True)
