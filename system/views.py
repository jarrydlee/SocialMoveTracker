from django.shortcuts import render
from system.models import *
from django.db import IntegrityError
import requests

# Create your views here.


def home(request):
    posts = Post.objects.all()
    keywords = Keyword.objects.all()

    test = Post.objects.get(id=1).keyword
    print(test.word)
    return render(request, 'test.html', {
        'posts':posts,
        'keywords':keywords
    })


def search(request):
    baseUrl = 'https://search-proxy.massrelevance.com/search.json'

    movies = [
        'Ride%20Along',
        'Endless%20Love',
        'Non-Stop',
        'Neighbors',
        'A%20Million%20Ways%20to%20die%20in%20the%20west',
        'Mrs%20Brown\'s%20Boys',
        'The%20Purge',
        'Get%20on%20up',
        'Lucy',
        'As%20above%20so%20below',
        'the%20loft',
        'search%20party',
        'Ouija'
    ]

    def scrape(title):
        #define variables
        pagination = ''

        # Creating keywords
        keyword = Keyword(
            word = title
        )
        keyword.save()

        for x in range(1,5):
            # Creating post object
            url = 'https://search-proxy.massrelevance.com/search.json?filter.text="'+ title +'"%20movie&filter.start=-24h&filter.finish=0&view.entities=true&view.entities.limit=100&'+ pagination
            r = requests.get(url)
            rJson = r.json()

            for tweet in rJson['views']['entities']['data']:
                post = Post(
                    post_id = tweet['raw']['id'],
                    text = tweet['raw']['text'],
                    label = '',
                    keyword = keyword,
                    positive = 0,
                    negative = 0,
                    neutral = 0,
                )
                try:
                    post.save()
                except IntegrityError as e:
                    print('duplicate post')

    for title in movies:

        scrape(title)

    return render(request, 'index.html')




