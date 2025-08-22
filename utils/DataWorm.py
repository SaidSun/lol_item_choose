import datetime

class DataWorm:
    def __init__(self, API_KEY=None, region="europe", start=0, match_count=20):
        if (API_KEY is None):
            raise ValueError("Need to initialize an API key!!!")
        self.key = API_KEY
        self.start = start
        self.match_count = match_count
        self.region="europe"
        
    def search_by_puuid(self, puuid=None):
        if (puuid is None):
            raise ValueError("Puuid can't be None!!!")
        
        params = {
        "start" : self.start,
        "count" : self.match_count,
        "api_key" : self.key
        }
        
        api_url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        successfulGet = 0
        for i in range(5):
            try:
                response = requests.get(api_url, params=urlencode(params))
                response.raise_for_status()
                successfulGet = 1
            
            except requests.exceptions.RequestException as e:
                    print(f"Issue getting summoner data from API: {e}\n {i+1} attempt...")
        
        if (successfulGet):
            return response.json()
        
        else:
            print("Can't get data  from API...")
            return None
        
    def search_by_metadata(self, tagLine=None, gameName=None):
        if ((tagLine is None) or (gameName is None)):
            raise ValueError("Tagline and Gamename must be not None!!!")
        
        params = {
            "api_key": self.key
        }
        api_url = f"https://{self.region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        successfulGet = 0
        
        for i in range(5):
            try:
                response = requests.get(api_url, params=urlencode(params))
                response.raise_for_status()
                successfulGet = 1
                
            except requests.exceptions.RequestException as e:
                print(f"Issue getting summoner data from API: {e}\n {i} attempt...")
        
        if (successfulGet):
            search_by_puuid(response.json()["puuid"])
            
        else:
            print("Can't get data  from API...")
            return None
        
    def set_key(self, API_KEY):
        self.key = API_KEY
    
    def set_region(self, region):
        self.region = region
    
    def set_start(self, start):
        self.start = start
    
    def set_match_count(self, match_count):
        self.match_count = match_count
    
    def recursive_search(self, params, start_puuid=None, start_tag=None, start_name=None):
        """
        params: Dict(month: int(or None), version: str(or None))
        """
        criterion = {
            "month" : datetime.now().month - 1 if datetime.now().month > 1 else 12,
            "version" : None
        }
        
        if not(params["month"] is None):
            criterion["month"] = params["month"]
        
        if not(params["version"] is None):
            criterion["version"] = params["version"]
        
        stillCont = 1
        
        if not(start_puuid is None):
            search_func = search_by_puuid
            search_args = (start_puuid,)
        if (not(start_tag is None) and not(start_name is None) and (start_puuid is None))
            search_func = search_by_metadata
            search_args = (start_tag, start_name,)
        
        else:
            raise ValueError("Searching data must be only by one way!!!")
            
        while(stillCont):
            response_data = search_func(*search_args)
            
