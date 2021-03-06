from annoying.decorators import render_to, ajax_request
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Course, Lesson, Problem, Submission


@render_to('index.html')
def index(request):
    return {
        'title_course': Course.objects.get(slug='test')
    }


@render_to('lesson.html')
def lesson(request, course_slug, lesson_slug):
    return {
        'lesson': Lesson.objects.get(slug=lesson_slug, course__slug=course_slug)
    }


@ensure_csrf_cookie  # TODO enable csrf cookie for all views
@render_to('problem.html')
def problem(request, course_slug, lesson_slug, problem_slug):
    problem = Problem.objects.get(slug=problem_slug, lesson__slug=lesson_slug, lesson__course__slug=course_slug)

    return {
        'problem': problem,
        'submissions': problem.submissions.filter(user=request.user)
    }


# TODO django-rest-framework
@ajax_request
def create_submission(request, course_slug, lesson_slug, problem_slug):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Cannot save submission for anonymous user')

    problem = Problem.objects.get(slug=problem_slug, lesson__slug=lesson_slug, lesson__course__slug=course_slug)
    submission = Submission.objects.create(problem=problem, user=request.user, code=request.POST.get('code'))

    return {
        'id': submission.id,
        'date': submission.date_string(),
    }


# TODO django-rest-framework
@ajax_request
def get_submission(request, course_slug, lesson_slug, problem_slug, id):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Cannot get submission for anonymous user')

    submission = Submission.objects.get(id=int(id))
    # TODO check slugs
    if not submission.user == request.user:
        return HttpResponseBadRequest('Cannot get submission for different user')

    return {
        'id': submission.id,
        'date': submission.date_string(),
        'code': submission.code,
    }
