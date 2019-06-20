# Built-in libraries
import asyncio
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer, timeit

# Installed libraries
import requests

# Exeptions
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError


DEFAULT_REQUESTS_COUNT = 100
CONCURRENT_REQUESTS_COUNT = 10
DEFAULT_TIMEOUT = 3

FAILED_LOAD_RETRIES = 5
FAILED_LOAD_DELAY = 0.5

DEFAULT_OUTPUT = 'timed_output_{0}.txt'.format(time.strftime('%Y-%m-%d_%H-%M-%S'))

MOST_COMMON_WORDS_COUNT = 10


class FakeName:
    
    INITIAL_TIME = default_timer()
    MINUS_WORDS = ['Miss', 'PhD']

    def __init__(self, start=None, finish=None, fullname=None):
        self.start_request_time = start
        self.name_received_time = finish
        self.fullname = fullname
        self.retries = 0

    @staticmethod
    def is_valid_name(name):
        return (
            '.' not in name 
            and name
            and not name.isupper() 
            and name not in FakeName.MINUS_WORDS
        )

    def split_fullname(self):
        names = self.fullname.split(' ')
        filtered_names = list(filter(FakeName.is_valid_name, names))
        if len(filtered_names) != 2:
            print('INVALID NAME LENGTH:: ', self.fullname, filtered_names)
        return filtered_names


def fetch_fakename(session, url):
    name_obj = FakeName(start=default_timer())
    for _ in range(int(FAILED_LOAD_RETRIES)): # Restart if request was failed
        name_obj.retries += 1
        try:
            with session.get(url) as response:
                if response.status_code == 200:
                    name_obj.fullname = response.json().get('name')
                    name_obj.name_received_time = default_timer()
                    return name_obj
        except (ConnectionError, JSONDecodeError) as e:
            print('FAILED:: {}'.format(e))
        finally:
            time.sleep(FAILED_LOAD_DELAY)


async def get_fakename_asynchronous():

    base_url = 'https://api.namefake.com/'

    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS_COUNT) as executor:
        with requests.Session() as session:
            session.verify = False
            session.timeout = DEFAULT_TIMEOUT
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch_fakename,
                    *(session, base_url)
                )
                for _ in range(DEFAULT_REQUESTS_COUNT)
            ]
    names_obj_list = list(await asyncio.gather(*tasks))
    process_names(names_obj_list)


def process_names(names_obj_list):
    
    pat = "{0:<30} {1:>20} {2:>20} {3:>20}"
    print(pat.format("Full name", "Retries", "Response time", "Completed at"), file=output)

    fake_names = []
    for name_obj in sorted(names_obj_list, key=lambda item: (
                        item.start_request_time, item.name_received_time)):
        response_time = '{:5.2f}s'.format(
            name_obj.name_received_time - name_obj.start_request_time)
        completed_at_time = '{:5.2f}s'.format(
            name_obj.name_received_time - name_obj.INITIAL_TIME)
        print(pat.format(name_obj.fullname, name_obj.retries, response_time,
            completed_at_time, name_obj.INITIAL_TIME), file=output)
        fake_names.extend(name_obj.split_fullname())

    print('\n' + '='*93, end='\n\n', file=output)
    print('{} MOST COMMON WORDS'.format(MOST_COMMON_WORDS_COUNT), 
        end='\n\n', file=output)
    common = Counter(fake_names).most_common(MOST_COMMON_WORDS_COUNT)
    print("{0:<30} {1:>20}".format("Word", "Count"), file=output)
    for name, count in common:
        print("{0:<30} {1:>20}".format(name, count), file=output)


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_fakename_asynchronous())
    loop.run_until_complete(future)


if __name__ == '__main__':
    with open(DEFAULT_OUTPUT, 'a') as output:
        elapsed = '{:5.2f}s'.format(
            timeit('main()', 'from __main__ import main', number=1))
        
        format_pat = "{0:<30} {1:>20}"
        resume_tuple = [
            ("Total names received:", DEFAULT_REQUESTS_COUNT),
            ("Concurrent request count:", CONCURRENT_REQUESTS_COUNT),
            ("Most common words count:", MOST_COMMON_WORDS_COUNT), 
            ("Total time elapsed:", elapsed)
        ]
            
        print('\n' + '='*51, end='\n\n', file=output)
        for k, v in resume_tuple:
            print(format_pat.format(k, v), file=output)