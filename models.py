from timeit import default_timer

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