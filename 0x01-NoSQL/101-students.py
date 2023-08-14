#!/usr/bin/env python3
"""101-students module"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    students = mongo_collection.find()

    student_scores = []
    for student in students:
        scores = [topic['score'] for topic in student['topics']]
        average_score = sum(scores) / len(scores) if len(scores) > 0 else 0
        student_scores.append(
            {'_id': student['_id'], 'name': student['name'],
             'averageScore': average_score})

    sorted_students = sorted(
        student_scores, key=lambda x: x['averageScore'], reverse=True)

    return sorted_students
