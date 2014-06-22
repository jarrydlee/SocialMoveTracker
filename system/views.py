from datetime import *
from django.http import HttpResponse
from django.shortcuts import render
from system import AppProperties
from system.AppProperties import MovieProperties
from system.models import *
from django.db import IntegrityError
import requests, urllib, time
import json

# Create your views here.

def home(request):

    return render(request, 'index.html')

def test(request):
    posts = Post.objects.all()
    print(len(posts))
    keywords = Keyword.objects.all()
    lineChartData = getLineChartData('ALL')

    return render(request, 'index.html', {
        'posts':posts,
        'keywords':keywords,
        'lineChartData': lineChartData
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
            word = urllib.unquote_plus(title)
        )
        try:
            keyword.save()
        except IntegrityError as e:
            print('duplicate keyword')


        for x in range(0,2):
            # Creating post object
            url = 'https://search-proxy.massrelevance.com/search.json?filter.text="'+ title +'"%20movie&filter.start=-24h&filter.finish=0&view.entities=true&view.entities.limit=100&'+ pagination
            print(url)
            r = requests.get(url)
            rJson = r.json()

            for tweet in rJson['views']['entities']['data']:

                created = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['raw']['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

                semantics = processText(tweet['raw']['text'])
                sentiment = 0 if semantics['sentiment'] == 'Negative' else 1 if semantics['sentiment'] == 'Neutral' else 2

                post = Post(
                    post_id = tweet['raw']['id'],
                    text = tweet['raw']['text'],
                    label = '',
                    keyword = keyword,
                    semantic = sentiment,
                    confidence = semantics['confidence'],
                    created_at = created,
                )
                try:
                    post.save()
                except IntegrityError as e:
                    #print('duplicate post')
                    pass

            paginationText = urllib.quote_plus(rJson['views']['entities']['meta']['pagination']['next_cursor'])

            pagination = 'view.entities.cursor='+ paginationText

    def processText(text):
        data = {'txt':text}
        result = requests.post('http://sentiment.vivekn.com/api/text/', data=data)
        result = json.loads(result.content)
        return result['result']


    for title in movies:
        scrape(title)

    return render(request, 'index.html')

def getLineChartData(movie):
    movieList = [movie]

    def LineDataFunc(movieList, timeDelta):
        return Post.objects.filter(
            keyword.word in movieList
        ).filter(
            created_at > (datetime.now() - timeDelta)
        ).filter(
            created_at < datetime.now()
        ).count()

    if movie == "ALL":
        movieList = MovieProperties().getMovieList()

    res = dict()
    for x in range(1, 7):
        res[str(x)] = LineDataFunc(movieList, timedelta(minutes=(60*x)))

    return res


def getMovieArrow(request):
    # Will return a dictionary with an entry for each movie, key is whether the number
    # of posts has increased or decreased
    movieList = AppProperties.MovieProperties.getMovieList()

    def ArrowFunc(movieTitle):
        numLast = Post.objects.filter(
            keyword.word = movieTitle
        ).filter(
            created_at > (datetime.now() - timedelta(minutes=120))
        ).filter(
            created_at < (datetime.now() - timedelta(minutes=60))
        ).count()

        numNow = Post.objects.filter(
            keyword.word = movieTitle
        ).filter(
            created_at > (datetime.now() - timedelta(minutes=60))
        ).filter(
            created_at < datetime.now()
        ).count()

        if numLast < numNow:
            return 1
        elif numNow < numLast:
            return -1
        else:
            return 0

    res = {movie: ArrowFunc(movie) for movie in movieList}

    res = {"Ride Along": 1, "This Movie": -1}

    return HttpResponse(json.dumps(res))

def getMovieTitles(request):
    movieUtil = MovieProperties()
    return HttpResponse(json.dumps(movieUtil.getMovieList()))



