import httplib  
import json
import traceback

class PocketUrl(object): 
    
    application_name = 'pyBatchUrl'
    consumer_key = '36822-6df058ece34310d6dceda601'
    
    pocket_url = 'getpocket.com'
    request_token_url = '/v3/oauth/request'
    authorize_url = '/v3/oauth/authorize'
    add_url = '/v3/add'
    fetch_url = '/v3/get'
    
    content_Type = 'application/json; charset=UTF-8'
    x_Accept = 'application/json'    
    http_method = 'POST'
    http_response_ok = 200
    pocket_status_added = 1
    
    def __init__(self):
        self.request_token = None
        self.access_token = None
        
        
    def connectHost(self,url,body,header):
        requests = httplib.HTTPSConnection(self.pocket_url)        
        requests.request(self.http_method,url,body, header)        
        response = requests.getresponse()
        return (response.status,response.read())

    def getRequestToken(self):
        headers = {"content-type": self.content_Type,
                   "X-Accept": self.x_Accept}
        params ={
            'consumer_key':self.consumer_key,
            'redirect_uri': ('%s:authorizationFinished' %(self.application_name))
        }
        status,response = self.connectHost(self.request_token_url,json.dumps(params), headers)
        results = json.JSONDecoder().decode(response)        
        requestToken =results['code']    
        return requestToken
    
    def getAccessToken(self):        
        headers = {"content-type": self.content_Type,
                   "X-Accept": self.x_Accept}
        params ={
            'consumer_key':self.consumer_key,
            'code': self.request_token
        }
        status,response = self.connectHost(self.authorize_url,json.dumps(params), headers)        
        results = json.JSONDecoder().decode(response)                
        requestToken =results['access_token']    
        return requestToken

    def Authenticate(self):
        if(self.request_token is None):
            self.request_token = self.getRequestToken()              
        outputURL = "https://%s/auth/authorize?request_token=%s&redirect_uri=%s:authorizationFinished" %(self.pocket_url, self.request_token,self.application_name)    
        return outputURL
    
    
    def AddPage(self,url,title):
        if(self.request_token is None):
            self.request_token = self.getRequestToken()
        if(self.access_token is None):
            self.access_token = self.getAccessToken()
            
        headers = {"content-type": self.content_Type,
                   "X-Accept": self.x_Accept}
        params ={
            'consumer_key':self.consumer_key,
            'access_token': self.access_token,
            'url' : url            
        }            
        status,response = self.connectHost(self.add_url,json.dumps(params), headers)
        results = json.JSONDecoder().decode(response)                           
        status =results['status']          
        return status,results
    
    def FetchPages(self,count):        
        if(self.request_token is None):
            self.request_token = self.getRequestToken()
        if(self.access_token is None):
            self.access_token = self.getAccessToken()
            
        headers = {"content-type": self.content_Type,
                   "X-Accept": self.x_Accept}
        params ={
            'consumer_key':self.consumer_key,
            'access_token': self.access_token,
            'count' : count,
            "detailType":"simple"
        }            
        status,response = self.connectHost(self.fetch_url,json.dumps(params), headers)
        results = json.JSONDecoder().decode(response)                           
        status =results['status']     
        return status, results
    
if __name__ == '__main__':
    try:
        pu = PocketUrl();
        tobrowser = pu.Authenticate();
        pu.AddPage('http://www.baidu.com',None)
        pu.fetch_url(1);
    except Exception as exc:           
        print("app catch: %s\n" % ( exc));   
        info = traceback.format_exc()
        print(info)
    print("done"); 
          


