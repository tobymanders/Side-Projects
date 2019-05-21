import json
import requests
import twitter
import string

def addCard(word, definition):

        url = "http://localhost:8765"
        payload = {}
        params = {
                'note': {
                        'deckName' : 'English Vocabulary',
                        'modelName' : 'Basic',
                        'fields' : {
                                'Front' : word,
                                'Back' : definition
                        },
                        'tags' : ['english-vocabulary']
                }
        }

        payload['action'] = 'addNote'
        payload['version'] = 6
        payload['params'] = params
        payload = json.dumps(payload)

        res = requests.post(url, payload)
        if json.loads(res.text)['error'] != None:
                pass

def getDef(word):

        word_id = word

        app_id = '6cfc5c5c'
        app_key = '5daf86366c7cb1c61413e4ca35f13590'
        language = 'en'
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key}).json()
        entries = r['results'][0]['lexicalEntries']
        defs = ''
        examples = ''
        for entry in entries:
                partofspeech = "<i>" + entry['lexicalCategory'][0] + ".</i>"
                d = ': '.join((partofspeech, entry['entries'][0]['senses'][0]['definitions'][0]))
                defs = "<br>".join((defs, d))
                examples = "<br>".join((examples, "<i>e.g.</i> \'" + entry['entries'][0]['senses'][0]['examples'][0]['text'] + "\'"))
        answer = defs + '<br>' + examples
        return answer

def getWords():
        api = twitter.Api(
                consumer_key='aTwXMk3Ovfc4Yvyy8BJAqsLuo', 
                consumer_secret='kSJ5CjfgMx8RMa9vV0tCHyUKEDJufoIWkaDMUS5Dq6ED7VovCx', 
                access_token_key='1112533740146835458-n6W28QoFnkFX70czU8oAxwtCsY7VQr', 
                access_token_secret='uwQklIAXVNGyevVBvfThHkur6FZaVm99y2qekTCrZ4GdE')
        statuses = api.GetUserTimeline(screen_name='AnkiVocab')
        words = []
        for status in statuses:
            if '"' in status.text: 
                word = status.text.split('"')[1].replace('”', '').lower()
            else:
                word = status.text.lower()
            print(word)
            for p in string.punctuation:
                word = word.replace(p, '')
            words.append(word)
        return words

def sync():
        url = "http://localhost:8765"
        payload = {}
        params = {}
        payload['action'] = 'sync'
        payload['version'] = 6
        payload['params'] = params
        payload = json.dumps(payload)

        res = requests.post(url, payload)
        

def main():
        words = getWords()
        for word in words:
                try:
                        definition = getDef(word)
                        addCard(word, definition)
                except:
                        pass 
        sync()


if __name__ == '__main__':
        main()
