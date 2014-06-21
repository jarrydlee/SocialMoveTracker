from django.shortcuts import render
from system.models import *
import requests

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'posts':posts
    })


def search(request):
    baseUrl = 'https://search-proxy.massrelevance.com/search.json'

    movies = [
        'Ride%20Along',
        'Endless%20Love',
        'Non-Stop',
        'Neighbors%20movie',
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

    def scrape():
        url = 'https://search-proxy.massrelevance.com/search.json?filter.text=search%20party?filter.text=movie&filter.start=-24h&filter.finish=0&view.entities=true&view.entities.limit=100'
        r = requests.get(url)
        rJson = r.json()
        for tweet in rJson['views']['entities']['data']:
            post = Post(
                post_id = tweet['raw']['id'],
                text = tweet['raw']['text'],
                label = '',
                positive = 0,
                negative = 0,
                neutral = 0,
            )

            post.save()

    scrape()

    return render(request, 'index.html')


    #for title in movies:
     #   options = '?filter.text=' + title + '&filter.start=-24h&filter.finish=0&view.entities=true&view.entities.limit=100'

