from database import engine

try:
    connection = engine.connect()
    print("Connected to MySQL!")
    connection.close()

except Exception as e:
    print("Error:", e)