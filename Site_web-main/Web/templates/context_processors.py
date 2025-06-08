from datetime import datetime

def current_time(request):
        now = datetime.now()
        return {'current_time': now}
    
