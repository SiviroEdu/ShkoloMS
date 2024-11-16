import re
import time

from app import Feedback, FeedbackEnum, CourseCRUD
from app.shkolo_wrap.user import get_class_id

FEEDBACKS_REGEX = re.compile(
    r'<tr class="compactTableRow ">\s*'
    r'<td class="numVal">\s*\d+\s*</td>\s*<td>\s*'
    r'<i[^>]+></i>\s*([^<]+)</td>\s*<td class="numVal">'
    r'<button[^>]*>(\d+)</button></td>\s*<td class="numVal">'
    r'<button[^>]*>(\d+)</button></td>',  # Capture praises count
    re.MULTILINE
)

async def process_feedbacks(source: str, pupil_id: int):
    matches = re.findall(FEEDBACKS_REGEX, source)

    class_id = await get_class_id()

    feedbacks = []
    for course_name, remarks, praises in matches:
        course_name = course_name.strip()
        remarks = int(remarks)
        praises = int(praises)

        if course_name == "Общи отзиви" or not (remarks or praises):
            continue

        course_id = (await CourseCRUD.get_by(
            year_class_id=class_id, name=course_name
        )).id

        feedbacks += [
            Feedback(
                amount=remarks,
                type=FeedbackEnum.REMARKS,
                pupil_id=pupil_id,
                course_id=course_id
            ), Feedback(
                amount=praises,
                type=FeedbackEnum.PRAISES,
                pupil_id=pupil_id,
                course_id=course_id
            )
        ]

    await Feedback.bulk_create(
        feedbacks, update_fields=("amount",), on_conflict=("course_id", "pupil_id", "type")
    )
