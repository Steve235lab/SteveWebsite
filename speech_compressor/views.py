from django.shortcuts import render


def render_page(request):
    return render(request, 'speech_compressor.html')
