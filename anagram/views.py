import itertools

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from .models import WordBuilding, Letter
from .forms import *
# Create your views here.

#openai.api_key = settings.OPENAI_API_KEY


def generate_words_from_letters(letters, no_of_words):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""give the results in a python list for example [['Words','Dictionary meaning'], ['Words','meaning'],]
                    Generate {no_of_words} lettered words from this letter {letters}""",
            temperature=0.7,
        )

        return response['choices'][0]['text']
    except Exception as e:
        print(e)

def generate_three_five_lettered_words(letters):
    import nltk
    nltk.download('words')
    from nltk.corpus import words
    
    valid_words = set(words.words())
    possible_words = set()
    for length in range(3, 6):
        for combination in itertools.permutations(letters, length):
            word = ''.join(combination).lower()
            print(word)
            possible_words.add(word)
    print(possible_words)
    results = [word for word in possible_words if word in valid_words]
    #print(results)
    return results


def generate_words(letters, length):
    import nltk
    #nltk.download('words')
    #nltk.download('wordnet')
    from nltk.corpus import words, wordnet
    
    valid_words = set(words.words())
    possible_words = set()
    for combination in itertools.permutations(letters, length):
        word = ''.join(combination).lower()
        #print(word)
        possible_words.add(word)
    #print(possible_words)
    results = [word for word in possible_words if word in valid_words]
    #print(results)
    
    meanings = {word: wordnet.synsets(word) for word in results}
    formatted_meanings = {word: [synset.definition() for synset in synsets] for word, synsets in meanings.items()}
    #print(meanings)
    print(formatted_meanings)
                          
    return formatted_meanings


def home(request):
    if request.method == "POST":
        form = WordsForm(request.POST)
        if form.is_valid():
            #input_text = form.cleaned_data['letters']
            no_of_words = form.cleaned_data['number_of_letters']
            letter_list = form.cleaned_data['letter_list']

            print(no_of_words, letter_list)

            #results = [['ERA','MEANING - ERA ERA'], ['EAR','MEANING - EAR'], ['BEAM','MEANING - BEAM'], ['BARE','MEANING - BARE'], ['AMBER','MEANING - AMBER']]
            #results = generate_words_from_letters(input_text, no_of_words)
            #letters = 'r E A b m'.split() #['r','e','a','b','m']

            #letters = input_text.split(',')
            letters = letter_list
            print(letters)
            print(type(letters))
            results = generate_words(letters, int(no_of_words))
            print(results)
            if results:
                request.session['results'] = results
                print(request.session['results'])

                obj_list = []
                for result in results:
                    obj = WordBuilding(
                            words=result,
                            letter=Letter.objects.get_or_create(letter=letter_list)[0],
                    )

                    obj_list.append(obj)
                save_data = WordBuilding.objects.bulk_create(obj_list)
                
                return redirect('anagram:results-page')
                """
                context = {}
                context['results'] = request.session['results']
                #context['results'] = results
                return render(request, 'anagram/results.html', context)
                """
            else:
                messages.error(
                    request, "Oops!!! we could not generate any words for you, please try again.."
                )
    else:
        form = WordsForm()
    context = {"form": form}
    return render(request, 'anagram/index.html', context)

def word_result(request):
    if 'results' in request.session:
        context = {}
        context['results'] = request.session['results']
        #context['results'] = results
        return render(request, 'anagram/results.html', context)
    else:
        return redirect('anagram:home')
