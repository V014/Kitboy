from tkinter import messagebox
import connection

class Utils:
    @staticmethod
    def get_current_date():
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # retrieve combo box data function
    @staticmethod
    def get_options(table_name, column_name):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB:
            pass
        db_obj = DummyDB()
        dbcon_func(db_obj)
        options = []
        if db_obj.con:
            try:
                db_obj.cur.execute(f"SELECT {column_name} FROM {table_name}")
                options = [str(row[0]) for row in db_obj.cur.fetchall()]
            finally:
                db_obj.con.close()
        return options
    
    # delete records function
    @staticmethod
    def delete_record(table_name, table_id, callback=None):
        
        db = connection
        dbcon_func = db.dbcon
        class DummyDB:
            pass
        db_obj = DummyDB()
        dbcon_func(db_obj)
        if db_obj.con:
            if messagebox.askyesno("Delete Record", f"Are you sure you want to delete this record from {table_name}?"):
                try:
                    db_obj.cur.execute(f"DELETE FROM {table_name} WHERE id={table_id}")
                    db_obj.con.commit()
                    if messagebox.showinfo("Success", "record deleted!"):
                        if callback:
                            callback()
                except Exception as e:
                    messagebox.showerror("Database Error", f"Could not delete record: {e}")
                    db_obj.con.rollback()
                finally:
                    db_obj.con.close()