import time

#this test for actions to push to main branch

# make a txt file and write to it Hello from actions at time now
with open("hello.txt", "w") as f:
    f.write(f"Hello from actions at {time.time()}")
    
    

