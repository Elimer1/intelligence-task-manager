from db_connection import DB_connection

class AgentDB:
    def __init__(self):
        self.connection = DB_connection()
        self.db = self.connection.get_connection()
        
        
    def create_agent(self, data):
        sql = """INSERT INTO agents (name, specialty, agent_rank) VALUES(%s, %s, %s)"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, data)
            self.db.commit()
            return cursor.fetchone()



    def get_all_agents(self):
        sql = """SELECT * FROM agents"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()



    def get_agent_by_id(self, id):
        sql = """SELECT * FROM agents WHERE id = %s"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()


    def update_agent(self, id, data):
        set_dict = [f"{key} = %s" for key in data.keys()]
        set_string = ", ".join(set_dict)
        values = [data.values()] + [id]

        sql = f"""UPDATE agents SET {set_string} WHERE id = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql,values)
            if cursor.rowcount < 1:
                return "ID not found"
            
            self.db.commit()
            return "Agent added successfully"


    def deactivate_agent(self, id):
        sql = """UPDATE agents SET is_active = FALSE WHERE ID = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql,(id,))
            if cursor.rowcount < 1:
                return "ID not found"
            
            self.db.commit()
            return "Agent successfully deactivated"


    def increment_completed(self, id):
        sql = """UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql,(id,))
            if cursor.rowcount < 1:
                return "ID not found"
            
            self.db.commit()
            return "completed missions count successfully incremented"


    def increment_failed(self, id):
        sql = """UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"""
        with self.db.cursor() as cursor:
            cursor.execute(sql,(id,))
            if cursor.rowcount < 1:
                return "ID not found"
            
            self.db.commit()
            return "failed missions count successfully incremented"
        

    def get_agent_performance(self, id):
        sql = """SELECT completed_missions AS completed, failed_missions AS failed FROM agents WHERE id = %s"""
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            if cursor.rowcount < 1:
                return "ID not found"
            
            performance_dict = cursor.fetchone()
            total_missions = performance_dict["completed"] + performance_dict["failed"]
            success_rate = (performance_dict["completed_missions"] / total_missions) * 100
            performance_dict["total"] = total_missions
            performance_dict["success_rate"] = success_rate
            return performance_dict

    def count_active_agents(self):
        sql = """SELECT COUNT (id) FROM agents WHERE is_active = TRUE"""
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            active_agents = cursor.fetchone()[0]
            if active_agents:
                return active_agents
            return int(0)


if __name__ == "__main__":
    agent = AgentDB()
    print("success")


#create connection of db in the init?
#what has to be in init of agentdb
#data is just values?
#make sure upadte doesnt touch id
#maybe check if agnet was alrady deactiavted