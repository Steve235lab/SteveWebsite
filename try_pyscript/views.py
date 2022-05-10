from django.shortcuts import render


def repl_terminal(request):
    return render(request, 'repl_terminal.htm')
