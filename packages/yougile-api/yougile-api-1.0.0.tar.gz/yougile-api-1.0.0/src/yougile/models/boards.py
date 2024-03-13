from pydantic import BaseModel

class BoardController_search(BaseModel):
    '''
    Получить список
    
    token:str - Токен (Обязательно)
    includeDeleted:bool - По умолчанию, если объект был отмечен как удаленный, то он не будет найден. Поставьте true, чтобы удаленные объекты возвращались (Необязательно)
    limit:int - Количество элементов, которые хочется получить. Максимум 1000 (По умолчанию = 50)
    offset:int - Индекс первого элемента страницы (По умолчанию = 0)
    projectId:str - ID проекта (Необязательно)
    title:str - Имя доски (Необязательно)
    
    https://ru.yougile.com/api-v2#/operations/BoardController_search
    '''
    _method:str = 'get'
    _url:str = '/api-v2/boards'
    token:str
    _url_params:tuple = ('includeDeleted','limit','offset','projectId','title')
    includeDeleted:bool|None = None
    limit:int=50
    offset:int=0
    projectId:str|None = None
    title:str|None = None
    
class BoardController_create(BaseModel):
    '''
    Создать
    
    token:str - Токен (Обязательно)
    title:str - Название доски (Обязательно)
    projectId:str - Id проекта, в котором находится доска (Обязательно)
    stickers:dict - Стикеры доски (Необязательно)
    
    https://ru.yougile.com/api-v2#/operations/BoardController_create
    '''
    _method:str = 'post'
    _url:str = '/api-v2/boards'
    token:str
    title:str
    projectId:str
    stickers:dict

class BoardController_get(BaseModel):
    '''
    Получить по ID
    
    token:str - Токен (Обязательно)
    id:str - ID доски (Обязательно)
    
    https://ru.yougile.com/api-v2#/operations/BoardController_get
    '''
    _method:str = 'get'
    _url:str = '/api-v2/boards/{id}'
    token:str
    _url_parse:tuple = ('id',)
    id:str
    
class BoardController_update(BaseModel):
    '''
    Изменить
    
    token:str - Токен (Обязательно)
    id:str - ID доски (Обязательно)
    
    https://ru.yougile.com/api-v2#/operations/BoardController_update
    '''
    _method:str = 'put'
    _url:str = '/api-v2/boards/{id}'
    token:str
    _url_parse:tuple = ('id',)
    id:str
    deleted:bool
    title:str
    projectId:str
    stickers:dict