import time
import threading

users = []
threads = []
new_users = ["Alice", "Bob", "Charlie", "David", "Eve"]

def add_user(name):
    time.sleep(1)  
    users.append(name)

start_thread = time.time()
for name in new_users:
    thread = threading.Thread(target=add_user, args=(name,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_thread = time.time()

print("Users with threading:", users)
print(f"Time taken with threading: {end_thread - start_thread:.4f} seconds")

users_not_thread = []
new_users_not_thread = ["Alice", "Bob", "Charlie", "David", "Eve"]

def add_user_not_thread(name):
    time.sleep(1)
    users_not_thread.append(name)

start = time.time()

for name in new_users_not_thread:
    add_user_not_thread(name)

end = time.time()
print("Users added without threading:", users_not_thread)
print(f"Time taken without threading: {end - start:.4f} seconds")