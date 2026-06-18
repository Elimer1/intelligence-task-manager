from database.db_connection import DB_connection
#from agent_db import AgentDB

class MissionDB:
    def __init__(self):
        self.connection = DB_connection()
        self.db = self.connection.get_connection()

    
    def create_mission(self, data):
        values = list(data.values())
        difficulty = values[3]
        importance = values[4]
        risk_level_int = (difficulty * 2) + importance
        if risk_level_int >= 25:
            risk_level = "CRITICAL"
        elif risk_level_int >= 18:
            risk_level = "HIGH"
        elif risk_level_int >= 10:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        values.append(risk_level)
        sql = """INSERT INTO missions (title, description, location, difficulty, importance, risk_level)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, values)
            self.db.commit()
            return cursor.fetchone()
        
    def get_all_missions(self):
        sql = """SELECT * FROM missions"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
        
    def get_mission_by_id(self, id):
        sql = """SELECT * FROM missions WHERE id = %s"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()
        
    def assign_mission(self, m_id, a_id):
        sql = """UPDATE missions SET assigned_agent_id = %s, status = "ASSIGNED" WHERE id = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql, (a_id, m_id))
            if cursor.rowcount < 1:
                return "mission ID not found"
            
            self.db.commit()
            return "mission assigned to agent successfully"
        
    def update_mission_status(self, id, status):
        sql = """UPDATE missions SET status = %s WHERE id = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql, (status, id))
            if cursor.rowcount < 1:
                return "mission ID not found"
            
            self.db.commit()
            return "mission status updated successfully"
        
    def get_open_missions_by_agent(self, id):
        sql = """SELECT * FROM missions 
        WHERE assigned_agent_id = %s AND status IN ("ASSIGNED", "IN_PROGRESS")
        """
        #check if assinged agent eixsts elsewhere (fine if id exists but has nothing assigend etc)
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        
    def count_all_missions(self):
        sql = """SELECT COUNT(id) FROM missions"""
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
        
    def count_by_status(self, status):
        sql = """SELECT COUNT(id) FROM missions WHERE status = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql, (status, ))
            return cursor.fetchone()[0]


    def count_open_missions(self):
        sql = """SELECT COUNT (id) FROM missions 
        WHERE status IN ("NEW", "ASSIGNED", "IN_PROGRESS")
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
        

    def count_critical_missions(self):
        sql = """SELECT COUNT (id) FROM missions WHERE risk_level = "CRITICAL" """
        
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]
        
    
    def get_top_agent(self):
        sql = """SELECT assigned_agent_id
        FROM missions WHERE status = "COMPLETED" 
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            ids = cursor.fetchall()
            dict = {}
            most = 0
            most_id = 0
            for id in ids:
                for num in id:
                    current = id.count(num)
                    if current > most:
                        most = current
                        most_id = num
                return most_id
