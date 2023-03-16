# Import the Thread class from the threading module and the time module
from threading import Thread
import time

# Define a Site class
class Site:
    def __init__(self, site_id):
        # Initialize site with an ID, a clock, a request queue, a set of replies received, and an empty queue
        self.site_id = site_id
        self.clock = 0
        self.request_queue = []
        self.replies_received = set()
        self.queue = []

    def increment_clock(self):
        # Increment the clock of the site by 1
        self.clock += 1

    def send_request(self):
        # Increment the clock of the site, add the current timestamp and the site ID to the request queue,
        # and print the request message with the timestamp and site ID
        self.increment_clock()
        self.request_queue.append((self.clock, self.site_id))
        print(f"Site {self.site_id}: Sending REQUEST message with timestamp ({self.clock}, {self.site_id})")
        # Send the request message to all other sites
        for site in sites:
            if site.site_id != self.site_id:
                site.receive_request((self.clock, self.site_id))

    def receive_request(self, request):
         # Increment the clock of the site, add the received request to the request queue,
        # and print the received request message with the timestamp
        self.increment_clock()
        self.request_queue.append(request)
        print(f"Site {self.site_id}: Received REQUEST message with timestamp {request}")
        # Send a reply message to the site that sent the request
        self.send_reply(request)

    def send_reply(self, request):
        # Increment the clock of the site and print the reply message with the timestamp and the ID of the site that sent the request
        self.increment_clock()
        print(f"Site {self.site_id}: Sending REPLY message with timestamp ({self.clock}, {self.site_id}) to Site {request[1]}")
        # Send the reply message to the site that sent the request
        for site in sites:
            if site.site_id == request[1]:
                site.receive_reply((self.clock, self.site_id))

    def receive_reply(self, reply):
        # Add the ID of the site that sent the reply to the set of replies received and print the received reply message with the timestamp
        self.replies_received.add(reply[1])
        print(f"Site {self.site_id}: Received REPLY message with timestamp {reply}")
        # If all sites have replied and the site is at the front of the request queue, enter the critical section
        if len(self.replies_received) == len(sites) - 1 and self.request_queue[0][1] == self.site_id:
            self.enter_critical_section()

    def enter_critical_section(self):
        # Add the request at the front of the request queue to the site's queue, print the queue, enter the critical section, sleep for 2 seconds, and release the site's queue
        self.queue.append(self.request_queue.pop(0))
        print(f"Site {self.site_id}: Adding request ({self.queue[-1][0]}, {self.queue[-1][1]}) to queue: {self.queue}")
        print(f"Site {self.site_id}: Entering critical section at time {time.time()}")
        time.sleep(2)
        self.release()

    def release(self):
        # Increment the clock of the site, remove the request at the front of the site's queue, and print the release message with the timestamp
        self.increment_clock()
        print(f"Site {self.site_id}: Releasing critical section and sending RELEASE message with timestamp ({self.clock}, {self.site_id})")
        # Remove the request at the front of the site's request queue
        self.queue.pop(0)
        for site in sites:
            if site.site_id != self.site_id:
                site.receive_release((self.clock, self.site_id))

    def receive_release(self, release):
        print(f"Site {self.site_id}: Received RELEASE message with timestamp {release}")
        # Remove the RELEASE message from the site's request queue (if it is in the queue)
        self.request_queue = [r for r in self.request_queue if r != release]

# Create a list of Site objects, with IDs 0 through 2
sites = [Site(i) for i in range(3)]

# Create a list of threads, where each thread runs the 'send_request' method for a different Site object
threads = []
for site in sites:
    t = Thread(target=site.send_request)
    threads.append(t)

# Start each thread
for thread in threads:
    thread.start()

# Wait for each thread to finish executing
for thread in threads:
    thread.join()