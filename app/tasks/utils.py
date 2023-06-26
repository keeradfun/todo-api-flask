from .models import Tasks


def filter_generator(data):
    print(data)
    args = []
    if 'title' in data:
        args.append(Tasks.title.like(data['title']))

    if 'description' in data:
        args.append(Tasks.title.like(data['description']))

    if 'deadline' in data:
        args.append(Tasks.deadline == data['deadline'])

    if 'status' in data:
        args.append(Tasks.status == data['status'])

    print(args)
    return args
