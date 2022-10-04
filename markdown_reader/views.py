from django.shortcuts import render


def markdown_reader(request):
    return render(request, 'markdown_reader.html')
