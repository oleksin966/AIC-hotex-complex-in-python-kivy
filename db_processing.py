import sqlite3
class DBEvents():
    def __init__(self):
        self.con = sqlite3.connect("hotel.db")
        self.cur = self.con.cursor()

    def get_list_corpus_name(self):
        query = "SELECT corpus.title FROM corpus"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def get_list_company_name(self):
        query = "SELECT company.name FROM company"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def get_list_complaints(self):
        query = "SELECT complaints.text FROM complaints"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def get_list_people_name(self):
        query = "SELECT people.name FROM people"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def count_not_free_room(self):
        query = " SELECT COUNT(*) FROM capasity_room\
                  WHERE is_free = 0"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()[0][0]
        
    def count_free_room(self):
        query = " SELECT COUNT(*) FROM capasity_room\
                  WHERE is_free = 1"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()[0][0]

    def count_complaints(self):
        query = " SELECT COUNT(*) FROM complaints"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()[0][0]
        
    def first_query(self, date_start, date_end, num):
        if (date_start == "" or date_end == "" or num == "" or num.isdigit()==False):
            return []
        query = "SELECT company.id,company.name,\
                    SUM(capasity),\
                    room_history.date_start,\
                    room_history.date_end\
                    FROM company\
                    INNER JOIN room_history\
                    ON company.id = room_history.company_id\
                    INNER JOIN capasity_room\
                    ON capasity_room.id = room_history.room_id\
                    GROUP BY room_history.date_start\
                    HAVING SUM(capasity) > "+num+" \
                    AND room_history.date_start > '"+date_start+"' \
                    AND room_history.date_end < '"+date_end+"'\
                    UNION ALL\
                    SELECT company.id,\
                    company.name,\
                    SUM(capasity),\
                    booking.date_start,\
                    booking.date_end\
                    FROM company\
                    INNER JOIN booking \
                    ON company.id = booking.company_id\
                    INNER JOIN capasity_room\
                    ON capasity_room.booking_id = booking.id\
                    GROUP BY booking.date_start\
                    HAVING SUM(capasity) > "+num+"\
                    AND date_start > '"+date_start+"' \
                    AND date_end < '"+date_end+"'"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def second_query(self, instance, date_start_, date_end_, corpus, floor_num_):
        if ( date_start_ == None and date_end_ == None
            and corpus == "" and (floor_num_ == "" or int(floor_num_).isdigit() == False)):
            instance.ids["date_2"].text = "<<виберіть дату>>"
            instance.ids["corpus"].hint_text = "Введіть текст"
            instance.ids["floor_num"].hint_text = "Введіть число"
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id"
        elif( date_start_ == None and date_end_ == None ):
            instance.ids["date_2"].text = "<<виберіть дату>>"
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE corpus.title = '"+corpus+"'\
                    AND floor_num = "+str(floor_num_)+";"
        elif( floor_num_ == "" and corpus == "" ):
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE date_start > '"+date_start_+"' AND date_end < '"+date_end_+"'"
            #print(query)
        elif( corpus == "" ):
            instance.ids["corpus"].hint_text = "Введіть текст"
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE floor_num = "+str(floor_num_)+"\
                    AND date_start > '"+date_start_+"' \
                    AND date_end < '"+date_end_+"';"
        elif( floor_num_ == ""):
            instance.ids["floor_num"].hint_text = "Введіть число"
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE corpus.title = '"+corpus+"'\
                    AND date_start > '"+str(date_start_)+"'\
                    AND date_end < '"+str(date_end_)+"';"
        else:
            instance.ids["corpus"].hint_text = "Введіть текст"
            instance.ids["floor_num"].hint_text = "Введіть число"
            query = "SELECT people.id,people.name, \
                    corpus.title, corpus.class,\
                    floors.floor_num, room_history.room_id \
                    FROM people \
                    INNER JOIN room_history\
                    ON people.id = room_history.people_id\
                    INNER JOIN capasity_room\
                    ON room_history.room_id = capasity_room.id\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE corpus.title = '"+corpus+"'\
                    AND floor_num = "+str(floor_num_)+"\
                    AND date_start > '"+str(date_start_)+"'\
                    AND date_end < '"+str(date_end_)+"';"
        
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def third_query(self):
        query = "SELECT capasity_room.id,\
                    corpus.title,\
                    floors.floor_num,\
                    capasity\
                    from capasity_room\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    WHERE is_free = 1;"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def four_query(self,class_hotel, capasity, price):
        if (price == "" or class_hotel == "" or capasity == "" or
            price.isdigit() == False  or class_hotel.isdigit() == False or capasity.isdigit() == False):
            query = "SELECT 1, 'Помилка', 'Помилка', 'Помилка', 'Помилка', 'Помилка'"
        else:
            query = "SELECT \
                capasity_room.id,\
                corpus.title,\
                (capasity*100*corpus.class),\
                floors.floor_num,\
                corpus.class,\
                capasity\
                from capasity_room\
                INNER JOIN floors \
                ON floors.id = capasity_room.floor_id\
                INNER JOIN corpus\
                ON corpus.id = floors.corpus_id\
                WHERE is_free = 1\
                AND corpus.class = "+class_hotel+" \
                AND capasity = "+capasity+" \
                AND (capasity*100*corpus.class) < "+price+""
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()


    def five_query(self, room_id):
        if (room_id == "" or room_id.isdigit()==False or int(room_id) > 39):
            query = "SELECT null, null, null, null, null, null, null, null, null"
        else:
            query = "SELECT \
                    t.*,\
                    (CASE\
                    WHEN (julianday(t.'Дата Заселення Клієнта') - julianday('2022-11-18')) IS NULL\
                    THEN 'Броня Відсутня'\
                    WHEN (julianday(t.'Дата Заселення Клієнта') - julianday('2022-11-18')) <= 0.0\
                    THEN 'Броня Відсутня'\
                    ELSE CAST(julianday(t.'Дата Заселення Клієнта') - julianday('2022-11-18') AS TEXT) END) AS 'Днів до заселення в Номер залишилось'\
                    FROM (\
                    SELECT \
                    capasity_room.id,corpus.title, floor_num,\
                    capasity,  \
                    CASE WHEN is_free = 1\
                    THEN 'Вільний'\
                    ELSE 'Зайнятий' END,\
                    date_start AS 'Дата Заселення Клієнта',date_end,\
                    (capasity*100*corpus.class)\
                    FROM capasity_room\
                    INNER JOIN floors\
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    LEFT JOIN booking\
                    ON booking.id = capasity_room.booking_id\
                    WHERE capasity_room.id = "+room_id+"\
                    ) t"

        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def six_query(self,date_value):
        if (date_value == ""):
            query = "SELECT null, null, null, null"
        else:
            query = "SELECT \
                    corpus.title,\
                    floor_num,\
                    capasity_room.id,\
                    date_end\
                    FROM capasity_room\
                    INNER JOIN floors \
                    ON floors.id = capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id = floors.corpus_id\
                    LEFT JOIN booking\
                    ON booking.id = capasity_room.booking_id\
                    WHERE is_free = 0\
                    AND date_end <'"+date_value+"'"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()


    def seven_query(self,date_start_, date_end_, company_name):
        if (date_start_ == None or date_end_ == None or company_name == ""):
            return [[]]
        query = "SELECT t2.*\
                , max(counts)\
                FROM (\
                SELECT t.*\
                ,count(t.room_id) AS counts\
                FROM (\
                select company.name, room_id, date_start, date_end \
                from company\
                inner join room_history\
                on room_history.company_id=company.id\
                WHERE date_start > '"+date_start_+"' \
                AND date_end < '"+date_end_+"' \
                union all \
                select company.name, capasity_room.id, date_start, date_end \
                from company\
                inner join booking\
                on booking.company_id=company.id\
                inner join capasity_room\
                on booking.id=capasity_room.booking_id\
                WHERE date_start > '"+date_start_+"' \
                AND date_end < '"+date_end_+"'  ) t\
                GROUP by t.room_id, t.name\
                order by t.name ) t2\
                where t2.name = '"+company_name+"'\
                GROUP by  t2.name"

        query2 = "  select room_id from company\
                    inner join room_history\
                    on room_history.company_id=company.id\
                    WHERE date_start > '"+date_start_+"' \
                    AND date_end < '"+date_end_+"'\
                    and company.name = '"+company_name+"' \
                    union all \
                    select capasity_room.id from company\
                    inner join booking\
                    on booking.company_id=company.id\
                    inner join capasity_room\
                    on booking.id=capasity_room.booking_id\
                    where name = '"+company_name+"'\
                    and date_start > '"+date_start_+"' \
                    AND date_end < '"+date_end_+"'"
        res1 = self.cur.execute(query).fetchall()
        res2 = self.cur.execute(query2).fetchall()
        self.con.commit()
        return [res1 , res2]



    def eight_query(self):
        query = "SELECT people.id, people.name, complaints.text, complaints.date \
                from complaints\
                inner join people\
                on people.id=complaints.people_id"
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()


    def nine_query(self):
        query = "SELECT t.date_end, SUM(t.total) \
                FROM (\
                SELECT date_end,\
                (room_price+services_price) AS total\
                FROM room_history\
                GROUP BY date_end\
                ORDER BY date_end) t\
                GROUP BY strftime('%m', t.date_end)\
                ORDER BY t.date_end;"

        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def eleven_query(self):
        query = "SELECT t2.title, t2.name\
                , max(count1)\
                FROM (\
                SELECT t.* \
                , count(title) as count1\
                FROM (\
                SELECT company.name, corpus.title \
                FROM company\
                INNER JOIN room_history\
                ON room_history.company_id=company.id\
                INNER JOIN capasity_room\
                ON capasity_room.id=room_history.room_id\
                INNER JOIN floors\
                ON floors.id=capasity_room.floor_id\
                INNER JOIN corpus\
                ON corpus.id=floors.corpus_id\
                UNION ALL\
                SELECT company.name, corpus.title \
                FROM company \
                INNER JOIN booking\
                ON booking.company_id=company.id\
                INNER JOIN capasity_room\
                ON capasity_room.booking_id=booking.id\
                INNER JOIN floors\
                ON floors.id=capasity_room.floor_id\
                INNER JOIN corpus\
                ON corpus.id=floors.corpus_id\
                ) t\
                GROUP BY name,title\
                ) t2 \
                GROUP BY title\
                ORDER BY t2.title;"
        query2 = "SELECT t2.title, t2.name\
                    , max(count1)\
                    FROM (\
                    SELECT t.* \
                    , count(title) as count1\
                    FROM (\
                    SELECT people.name, capasity_room.id, floor_num, corpus.title \
                    FROM people \
                    INNER JOIN booking\
                    ON booking.people_id=people.id\
                    INNER JOIN capasity_room\
                    ON capasity_room.booking_id=booking.id\
                    INNER JOIN floors\
                    ON floors.id=capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id=floors.corpus_id\
                    UNION ALL\
                    SELECT people.name, room_id, floor_num, corpus.title \
                    FROM people\
                    INNER JOIN room_history\
                    ON room_history.people_id=people.id\
                    INNER JOIN capasity_room\
                    ON capasity_room.id=room_history.room_id\
                    INNER JOIN floors\
                    ON floors.id=capasity_room.floor_id\
                    INNER JOIN corpus\
                    ON corpus.id=floors.corpus_id\
                    ) t\
                    GROUP BY name,title\
                    ) t2 \
                    GROUP BY title\
                    ORDER BY t2.title;"

        res1 = self.cur.execute(query).fetchall()
        res2 = self.cur.execute(query2).fetchall()
        self.con.commit()
        return [res1, res2]


    def twelve_query(self, date_start_, date_end_):
        query = "SELECT ifnull(t2.people_id, t2.company_id) AS id\
                , t2.name\
                FROM (\
                SELECT *\
                , count(company_id) AS count_company\
                , count(people_id) AS count_people\
                FROM (\
                SELECT people_id,company_id,company.name, date_start, date_end FROM room_history\
                INNER JOIN company\
                ON room_history.company_id = company.id\
                AND date_end < '"+date_end_+"' \
                GROUP BY date_start \
                UNION ALL \
                SELECT people_id,company_id,company.name, date_start, date_end FROM booking\
                INNER JOIN company\
                ON booking.company_id = company.id\
                AND date_end < '"+date_end_+"' \
                GROUP BY date_start \
                ) t\
                GROUP BY people_id, company_id) t2\
                WHERE t2.count_company = 1\
                OR t2.count_people = 1\
                AND date_end < '"+date_end_+"' \
                AND date_start > '"+date_start_+"';"


        query2 = "SELECT ifnull(t2.people_id, t2.company_id) AS id\
                    , t2.name AS counts\
                    FROM (\
                    SELECT *\
                    , count(company_id) AS count_company\
                    , count(people_id) AS count_people\
                    FROM (\
                    SELECT people_id,company_id,people.name, date_start, date_end FROM room_history\
                    INNER JOIN people\
                    ON room_history.people_id = people.id\
                    AND date_end < '"+date_end_+"' \
                    GROUP BY date_start \
                    UNION ALL \
                    SELECT people_id,company_id,people.name, date_start, date_end FROM booking\
                    INNER JOIN people\
                    ON booking.people_id = people.id\
                    AND date_end < '"+date_end_+"' \
                    GROUP BY date_start \
                    ) t\
                    GROUP BY people_id, company_id) t2\
                    WHERE t2.count_company = 1\
                    OR t2.count_people = 1\
                    AND date_end < '"+date_end_+"' \
                    AND date_start > '"+date_start_+"';"

        res1 = self.cur.execute(query).fetchall()
        res2 = self.cur.execute(query2).fetchall()
        self.con.commit()
        return [res1, res2]

    def threteen_query(self, name):
        names = self.get_list_people_name()
        for i in names:
            if i[0]==name:
                query = "SELECT \
                        people.id,\
                        people.name,\
                        room_history.room_id, \
                        room_history.date_start, \
                        room_history.date_end, \
                        room_history.room_price, \
                        room_history.services_price,\
                        (room_price+services_price) AS total\
                        FROM people\
                        INNER JOIN room_history\
                        ON room_history.people_id=people.id\
                        WHERE name = '"+name+"'"
                break
            else:
                query = "SELECT 1, '"+name+"', 'відсутні дані', 'відсутні дані',  'відсутні дані',  'відсутні дані',  'відсутні дані',  'відсутні дані'"
            
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def fourteen_query(self, date_start_, date_end_, room_id):
        if (room_id == "" or room_id.isdigit() == False):
            return []
        if (room_id and date_start_ == "" and date_end_ == ""):
            query = "SELECT *\
                        FROM (\
                        select room_id, people.name, date_start, date_end\
                        from people\
                        INNER JOIN room_history\
                        ON people.id=room_history.people_id\
                        UNION ALL\
                        select room_id, company.name, date_start, date_end\
                        from company\
                        INNER JOIN room_history\
                        ON company.id=room_history.company_id\
                        ) t \
                        WHERE room_id = "+room_id+""
        else:
            query = "SELECT *\
                        FROM (\
                        select room_id, people.name, date_start, date_end\
                        from people\
                        INNER JOIN room_history\
                        ON people.id=room_history.people_id\
                        WHERE date_start >= '"+date_start_+"'\
                        AND date_end <= '"+date_end_+"'\
                        UNION ALL\
                        select room_id, company.name, date_start, date_end\
                        from company\
                        INNER JOIN room_history\
                        ON company.id=room_history.company_id\
                        WHERE date_start >= '"+date_start_+"'\
                        AND date_end <= '"+date_end_+"'\
                        ) t WHERE t.room_id = "+room_id+";"

        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()

    def fifteen_query(self):
        query = "SELECT ROUND((100*count(capasity_room.id))/39.0,2) AS counts\
                    FROM booking\
                    INNER JOIN capasity_room\
                    ON booking.id=capasity_room.booking_id\
                    INNER JOIN people\
                    ON people.id=booking.people_id\
                    UNION ALL\
                    SELECT ROUND((100*count(capasity_room.id))/39.0,2) AS counts\
                    FROM booking\
                    INNER JOIN capasity_room\
                    ON company.id=capasity_room.booking_id\
                    INNER JOIN company\
                    ON company.id=booking.company_id;" 
        res = self.cur.execute(query)
        self.con.commit()
        return res.fetchall()