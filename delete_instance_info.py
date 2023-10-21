import pymysql

# Database connection parameters
db_host = "ins-info.ch6tb7admtue.us-east-1.rds.amazonaws.com"
db_user = "kislay"
db_password = "Me_960866"
db_name = "ec2"

def delete_record(connection, instance_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM instance_info WHERE Instance_ID = %s", (instance_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False

def main():
    # Connect to the database
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        print("Connected to the database.")

        while True:
            cursor = connection.cursor()

            # Retrieve records from the database
            cursor.execute("SELECT * FROM instance_info")
            records = cursor.fetchall()

            if not records:
                print("No records found.")
                break

            print("Instance records:")
            print("Name\tInstance_ID\tPrivate_IP\tPublic_IP")
            for record in records:
                print(f"{record[1]}\t{record[0]}\t{record[2]}\t{record[3]}")

            instance_ids_to_delete = input("Enter Instance_ID(s) to delete (comma-separated, e.g., 'i-123,i-456') or type 'exit' to quit: ")

            if instance_ids_to_delete.lower() == "exit":
                break

            instance_ids = instance_ids_to_delete.split(',')
            deleted_records = []

            for instance_id in instance_ids:
                instance_id = instance_id.strip()
                if delete_record(connection, instance_id):
                    deleted_records.append(instance_id)

            if deleted_records:
                print(f"Deleted records with Instance_ID(s): {', '.join(deleted_records)}")
            else:
                print("No records were deleted.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
