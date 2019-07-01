# Built-in libraries
import asyncio
import time
import urllib3
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer, timeit

# Installed libraries
import requests

# Local libraries
from models import FakeName
import settings

# Exeptions
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError


def get_response(session, url):
    with session.get(url) as response:
        if response.status_code == 200:
            return response


def is_valid_json_response(response):
    try:
        return response and response.json().get('name')
    except JSONDecodeError as e:
        print('FAILED:: {}'.format(e))
        return False


def fetch_fakename(session, url):
    name_obj = FakeName(start=default_timer())
    for _ in range(int(settings.FAILED_LOAD_RETRIES)): # Restart if request was failed
        name_obj.retries += 1
        try:
            response = get_response(session, url)
            if is_valid_json_response(response):
                name_obj.fullname = response.json().get('name')
                name_obj.name_received_time = default_timer()
                return name_obj
        except ConnectionError as e:
            print('FAILED:: {}'.format(e))
        finally:
            time.sleep(settings.FAILED_LOAD_DELAY)


def create_asynchronous_tasks(loop, exec_func, executor=None, *args, **kwargs):
    return [
        loop.run_in_executor(
            executor,
            exec_func,
            *args
        )
        for _ in range(settings.DEFAULT_REQUESTS_COUNT)
    ]


async def get_fakename_asynchronous():
    with ThreadPoolExecutor(max_workers=settings.CONCURRENT_REQUESTS_COUNT) as executor:
        with requests.Session() as session:
            session.verify = False
            session.timeout = settings.DEFAULT_TIMEOUT
            loop = asyncio.get_event_loop()
            tasks = create_asynchronous_tasks(loop, fetch_fakename, executor,
                 session, settings.BASE_URL)
            return await asyncio.gather(*tasks)


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
    print('{} MOST COMMON WORDS'.format(settings.MOST_COMMON_WORDS_COUNT), 
        end='\n\n', file=output)
    common = Counter(fake_names).most_common(settings.MOST_COMMON_WORDS_COUNT)
    print("{0:<30} {1:>20}".format("Word", "Count"), file=output)
    for name, count in common:
        print("{0:<30} {1:>20}".format(name, count), file=output)


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_fakename_asynchronous())
    loop.run_until_complete(future)
    names_obj_list = future.result()
    process_names(names_obj_list)


if __name__ == '__main__':
    
    DEFAULT_OUTPUT = 'outputs/timed_output_{0}.txt'.format(time.strftime('%Y-%m-%d_%H-%M-%S'))

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with open(DEFAULT_OUTPUT, 'a') as output:
        elapsed = '{:5.2f}s'.format(
            timeit('main()', 'from __main__ import main', number=1))
        
        format_pat = "{0:<30} {1:>20}"
        resume_tuple = [
            ("Total names received:", settings.DEFAULT_REQUESTS_COUNT),
            ("Concurrent request count:", settings.CONCURRENT_REQUESTS_COUNT),
            ("Most common words count:", settings.MOST_COMMON_WORDS_COUNT), 
            ("Total time elapsed:", elapsed)
        ]
            
        print('\n' + '='*51, end='\n\n', file=output)
        for k, v in resume_tuple:
            print(format_pat.format(k, v), file=output)