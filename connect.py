import psycopg2
import config

forumdb = psycopg2.connect(database=config.db, user=config.user,
                           password=config.password, host=config.host, port=config.port)


def decrator(func):
    def wrapper(*args, **kw):
        global forumdb
        try:
            cur = forumdb.cursor()
            cur.execute('SELECT 1')
            cur.close()
        except psycopg2.OperationalError:
            forumdb = psycopg2.connect(database=config.db, user=config.user,
                                       password=config.password, host=config.host, port=config.port)

        try:
            curs = forumdb.cursor()
            msg, result, curs = func(*args, **kw, curs=curs)
            curs.close()
            forumdb.commit()
            return msg, result
        except:
            msg = dict(zip(("status", "message"), ("ERROR", "操作失败!请稍后重试!")))
            result = None
            forumdb.rollback()
            return msg,result
    return wrapper
