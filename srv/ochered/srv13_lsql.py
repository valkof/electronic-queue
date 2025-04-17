import sqlite3
from logger import get_logger

log = get_logger(__name__)


class SqLite:
    def __init__(self, dbname, params, dparams=None):
        self.dbname = dbname
        self.params = params
        self.dparams = dparams

    def db_execute_trans(dbname, query_list, params=''):
        con = None
        cur = None
        ret = None
        err = None
        try:
            con = sqlite3.connect(dbname, isolation_level=None)
            cur = con.cursor()
            for i in query_list:
                cur.execute(i, params)
            ret = cur.fetchone()
            con.commit()
        except Exception as e:
            con.rollback()
            err = "Error: " + str(e)
            log.debug("SQL: " + err)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        return (ret, err)

    def db_execute_all_trans(dbname, query_list, params=''):
        con = None
        cur = None
        ret = None
        err = None
        try:
            con = sqlite3.connect(dbname, isolation_level=None)
            cur = con.cursor()
            for i in query_list:
                cur.execute(i, params)
            ret = cur.fetchall()
            con.commit()
        except Exception as e:
            con.rollback()
            err = "Error: " + str(e)
            log.debug("SQL: " + err)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        return (ret, err)

    def db_execute(dbname, query, params=''):
        con = None
        cur = None
        ret = None
        err = None
        try:
            con = sqlite3.connect(dbname, isolation_level=None)
            cur = con.cursor()
            ret = cur.execute(query, params)
            con.commit()
        except Exception as e:
            err = "Error: " + str(e)
            log.debug("SQL: " + err)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        return (ret, err)

    def db_execute_rowid(dbname, query, params):
        con = None
        cur = None
        ret = None
        err = None
        try:
            con = sqlite3.connect(dbname, isolation_level=None)
            cur = con.cursor()
            cur.execute(query, params)
            rowid = cur.lastrowid
            if rowid > 0:
                cur.execute("SELECT * FROM " + params["table"] + " WHERE ROWID=?", (rowid,))
            ret = cur.fetchone()
            con.commit()
        except Exception as e:
            err = "Error: " + str(e)
            log.debug("SQL: " + err)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()
        return (ret, err)

    def db_create(self):
        query = """CREATE TABLE IF NOT EXISTS ticket(
               queue_id INT,
               tick_id INT NOT NULL,
               tick_name TEXT,
               kiosk_id INT,
               tick_kiosk TIMESTAMP,
               tick_start TIMESTAMP,
               tick_stop TIMESTAMP,
               place_id INT,
               status INT,
               description TEXT);
               """
        return SqLite.db_execute(self, query)

    def ticket_create(self):
        query = '''
            WITH new AS (
                SELECT DISTINCT COALESCE(max(tick_id)+1, 1) as t
                FROM ticket
                WHERE queue_id=:q AND tick_kiosk>=date('now', 'localtime')
            )
            INSERT INTO ticket
            SELECT :q, new.t, :p || cast(new.t as text), :w,
                datetime('now','localtime'), 0, 0, 0, 0, ''
            FROM new;
            '''
        self.params["table"] = "ticket"
        ret = SqLite.db_execute_rowid(self.dbname, query, self.params)
        if ret[0] is not None:
            ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_next(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        # закрываем текущий талон
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime')
            WHERE place_id=:w
                AND tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0;
            ''')
        # захватываем свободный талон
        query_list.append('''
            UPDATE ticket SET tick_start=datetime('now','localtime'), place_id=:w
            WHERE (queue_id, tick_id, tick_name, kiosk_id, tick_kiosk)=(
                SELECT :q, tick_id, tick_name, kiosk_id, tick_kiosk
                FROM ticket
                WHERE queue_id=:q AND tick_kiosk>=date('now', 'localtime')
                    AND place_id=0 ORDER BY tick_id LIMIT 1);
            ''')
        # ... и возвращаем талон, который захватили.
        query_list.append('''
            SELECT * FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w LIMIT 1
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_nexts(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        # закрываем текущий талон
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime')
            WHERE place_id=:w
                AND tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0;
            ''')
        # захватываем свободный талон
        cSql = '''
            UPDATE ticket SET tick_start=datetime('now','localtime'), place_id=:w
            WHERE (queue_id, tick_id, tick_name, kiosk_id, tick_kiosk)=(
                SELECT queue_id, tick_id, tick_name, kiosk_id, tick_kiosk
                FROM ticket
                WHERE queue_id in ({qq}) AND tick_kiosk>=date('now', 'localtime')
                    AND place_id=0 ORDER BY tick_kiosk, tick_id LIMIT 1);
            '''
        query_list.append(SqLite.prepare_sql(cSql=cSql,
                                             dparams=self.params))
        # ... и возвращаем талон, который захватили.
        query_list.append('''
            SELECT * FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w LIMIT 1
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_current(self):
        query_list = list()
        query_list.append('''
            SELECT * FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_end(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime'), status=1
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w;
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (None,  ret[1])
        return ret

    def ticket_pause(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime')
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w;
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (None,  ret[1])
        return ret

    def queue_len(self):
        query_list = list()
        query_list.append('''
            SELECT count(*) FROM ticket
            WHERE queue_id in (:q)
                AND tick_kiosk>=date('now', 'localtime')
                AND tick_start=0
                AND tick_stop=0 AND place_id=0
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (ret[0][0], ret[1])
        else:
            ret = (0, ret[1])
        return ret

    def ticket_move(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        query_list.append('''
            WITH new AS (
                SELECT COALESCE(
                    (SELECT tick_id
                    FROM ticket
                    WHERE queue_id=:q AND tick_kiosk>=date('now', 'localtime')
                        AND tick_start=0
                        AND tick_stop=0 AND place_id=0
                    ORDER BY 1
                    LIMIT :o, 1),
                    (SELECT MAX(tick_id)
                    FROM ticket
                    WHERE queue_id=:q AND tick_kiosk>=date('now', 'localtime')
                        AND tick_start=0 AND tick_stop=0 AND place_id=0),
                    (SELECT MAX(tick_id)
                    FROM ticket
                    WHERE queue_id=:q
                        AND tick_kiosk>=date('now', 'localtime')),
                    1
                ) tick_id
            )
            INSERT INTO ticket
            SELECT :q, new.tick_id, :t, :w,
                datetime('now','localtime'), 0, 0, 0, 0, :d
            FROM new;
            ''')
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime'), status=2
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w;
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (None,  ret[1])
        return ret

    def ticket_notshowing(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime'), status=-1
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w;
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (None,  ret[1])
        return ret

    def ticket_list_kiosk(self):
        query_list = list()
        query_list.append('''
            SELECT queue_id, tick_id, tick_name, kiosk_id, strftime('%H:%M:%S', tick_kiosk) as tick_kiosk, description FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start=0
                AND tick_stop=0 AND queue_id=:q
                ORDER BY tick_kiosk
            ''')
        ret = SqLite.db_execute_all_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (ret[0],  ret[1])
        #if ret[0] is not None:
        #    ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_list_queue(self):
        query_list = list()
        query_list.append('''
            SELECT queue_id, tick_id, tick_name, kiosk_id,
                strftime('%H:%M:%S', tick_kiosk) as tick_kiosk,
                description
            FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start=0
                AND tick_stop=0 AND queue_id=:q
                ORDER BY tick_id, tick_kiosk
            ''')
        ret = SqLite.db_execute_all_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = (ret[0],  ret[1])
        #if ret[0] is not None:
        #    ret = ((ret[0][2], ret[0][4]),  ret[1])
        return ret

    def ticket_next_by_name(self):
        query_list = list()
        query_list.append("BEGIN TRANSACTION;")
        # закрываем текущий талон
        query_list.append('''
            UPDATE ticket SET tick_stop=datetime('now','localtime')
            WHERE place_id=:w
                AND tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0;
            ''')
        # захватываем свободный талон
        query_list.append('''
            UPDATE ticket SET tick_start=datetime('now','localtime'), place_id=:w
            WHERE (queue_id, tick_id, tick_name, kiosk_id, tick_kiosk)=(
                SELECT :q, tick_id, tick_name, kiosk_id, tick_kiosk
                FROM ticket
                WHERE queue_id=:q AND UPPER(tick_name)=UPPER(:n)
                    AND tick_kiosk>=date('now', 'localtime')
                    AND place_id=0 ORDER BY tick_id LIMIT 1);
            ''')
        # ... и возвращаем талон, который захватили.
        query_list.append('''
            SELECT * FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start>=date('now', 'localtime')
                AND tick_stop=0 AND place_id=:w LIMIT 1
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = ((ret[0][2], ret[0][4], ret[0][9]),  ret[1])
        return ret

    def ticket_check_new(self):
        query_list = list()
        query_list.append('''
            SELECT count(*) FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start=0
                AND tick_stop=0
                AND queue_id=:q
            ''')
        ret = SqLite.db_execute_trans(self.dbname, query_list, self.params)
        if ret[0] is not None:
            ret = ((ret[0][0]),  ret[1])
        return ret

    def ticket_list_queues(self):
        cSql = '''
            SELECT queue_id, tick_id, tick_name, kiosk_id,
                strftime('%H:%M:%S', tick_kiosk) as tick_kiosk, description
            FROM ticket
            WHERE tick_kiosk>=date('now', 'localtime')
                AND tick_start=0
                AND tick_stop=0 AND queue_id in ({qq})
                ORDER BY tick_kiosk, tick_id;
            '''
        query_list = list()
        query_list.append(SqLite.prepare_sql(cSql=cSql,
                                             dparams=self.dparams))
        ret = SqLite.db_execute_all_trans(self.dbname,
                                          query_list, self.params)
        if ret[0] is None or len(ret[0]) == 0:
            ret = (None, ret[1])
        else:
            pass
        return ret

    def prepare_sql(cSql='', dparams={}):
        if dparams:
            for key, value in dparams.items():
                cSql = cSql.replace('{'+key+'}', value)
        else:
            pass
        return cSql


if __name__ == '__main__':
    from srv13_vars import V
    v = V()
    #s = SqLite(v.sD, {'q': 1})
    #ret = s.ticket_list_kiosk()
    # s = SqLite(v.sD, {'q': '1'})
    #ret = s.ticket_next_by_name()
    #s = SqLite(v.sD, params={'w': '7', 'qq': '1, 2, 3'}, dparams={'qq': '1, 2, 3'})
    #ret = s.ticket_list_queues()
    # s = SqLite(v.sD)
    # ret = s.db_create()
    s = SqLite(v.sD, params={'w': '7', 'p': 'Б', 'q': '3'})
    ret = s.ticket_create()
    print("ret=", ret)
    print("typeret=", type(ret))
    # s = SqLite(v.sD, params={'q': '1'})
    #ret = s.ticket_list_queue()
    # print("ret=", ret)
    # print("typeret=", type(ret))
    # print(v.sD)
    # s = SqLite.db_create(v.sD)
    # print(s)
