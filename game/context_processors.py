from .forms import CreateGameForm


def create_game_form(request):
    return {
        'create_game_form': CreateGameForm()
    }