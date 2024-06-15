from django.conf import settings

# 连接库
conn = settings.MONGO_CLIENT['test']


class User(object):

    # 使用哪个集合
    db = conn['user']
    @classmethod
    def insert(cls, **params):
        print(params)
        return cls.db.insert_one(params)

    @classmethod
    def get_all(cls, **params):
        return list(cls.db.find(params))

    @classmethod
    def get_one(cls, **params):
        return cls.db.find_one(params)

    @classmethod
    def update(cls, _id, **params):
        # 不加$set会覆盖
        cls.db.update_one({'_id': _id}, {'$set': params})
        print(f'params:{params}')
