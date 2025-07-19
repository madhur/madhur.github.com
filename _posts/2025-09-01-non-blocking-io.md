---
layout: blog-post
title: "Non Blocking I/O"
excerpt: "Non Blocking I/O"
disqus_id: /2025/09/01/non-blocking-io/
tags:
    - Linux
---


When I first learned about non-blocking I/O, I had a burning question: how does a process know when I/O operations complete? Is there some background kernel process constantly checking for data and then notifying user-space applications? The answer reveals one of the most elegant solutions in systems programming.

## The Problem with Blocking I/O

To understand non-blocking I/O, let's first examine what happens with traditional blocking I/O. When your program makes a system call like `read()` or `recv()`, the calling thread is suspended until the operation completes. For a web server handling thousands of connections, this means you'd need thousands of threads – each consuming memory and creating context-switching overhead.

```c
// Blocking I/O - thread waits here until data arrives
int bytes = recv(socket_fd, buffer, sizeof(buffer), 0);
```

This approach doesn't scale well. A server with 10,000 connections would need 10,000 threads, consuming gigabytes of memory just for thread stacks.

## How Non-Blocking I/O Works

Non-blocking I/O flips this model on its head. Instead of waiting for I/O to complete, operations return immediately with either data (if available) or an indication that no data is ready.

```c
// Non-blocking I/O - returns immediately
int flags = fcntl(socket_fd, F_GETFL, 0);
fcntl(socket_fd, F_SETFL, flags | O_NONBLOCK);

int bytes = recv(socket_fd, buffer, sizeof(buffer), 0);
if (bytes == -1 && errno == EAGAIN) {
    // No data available right now, try again later
}
```

But this raises the obvious question: how do you know when to "try again later"? The naive approach would be to continuously poll all file descriptors in a loop, but that would waste enormous amounts of CPU cycles.

## The Event Loop: Efficient I/O Multiplexing

Modern operating systems provide sophisticated APIs to efficiently monitor multiple file descriptors. This is where the "event loop" comes in – but it's far more elegant than a simple while loop.

### Linux: epoll

Linux provides `epoll`, which allows you to monitor hundreds or thousands of file descriptors efficiently:

```c
// Create an epoll instance
int epoll_fd = epoll_create1(0);

// Add a socket to the interest list
struct epoll_event event;
event.events = EPOLLIN;  // Monitor for readable data
event.data.fd = socket_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, &event);

// Wait for events (this blocks until data is available)
struct epoll_event events[MAX_EVENTS];
int ready_fds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);

for (int i = 0; i < ready_fds; i++) {
    // Process ready file descriptor
    handle_ready_socket(events[i].data.fd);
}
```

### The Key Optimization

Here's the crucial insight: `epoll_wait()` **blocks** until at least one file descriptor has data available. This means:

1. **No busy waiting**: The process sleeps when there's no work to do
2. **Efficient scaling**: Monitoring 1,000 FDs is nearly as fast as monitoring 10 FDs
3. **Event-driven**: You only process FDs that actually have data ready

The computational complexity is O(number of ready events), not O(total FDs monitored). You could monitor 100,000 connections, but if only 10 have data ready, you only process 10 events.

## Cross-Platform Event Mechanisms

Different operating systems provide similar but distinct APIs:

- **Linux**: `epoll` (edge-triggered and level-triggered modes)
- **BSD/macOS**: `kqueue` (supports files, network, timers, and more)
- **Windows**: I/O Completion Ports (IOCP) with a different asynchronous model
- **Portable**: `select` and `poll` (available everywhere but less efficient)

## Real-World Example: A Simple HTTP Server

Here's how a basic non-blocking HTTP server might work:

```c
int server_fd = socket(AF_INET, SOCK_STREAM, 0);
// Set up server socket and bind to port...
fcntl(server_fd, F_SETFL, O_NONBLOCK);
listen(server_fd, SOMAXCONN);

int epoll_fd = epoll_create1(0);
// Add server socket to epoll...

while (1) {
    int ready = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
    
    for (int i = 0; i < ready; i++) {
        if (events[i].data.fd == server_fd) {
            // New connection
            int client_fd = accept(server_fd, NULL, NULL);
            fcntl(client_fd, F_SETFL, O_NONBLOCK);
            // Add client to epoll...
        } else {
            // Data ready on existing connection
            handle_client_request(events[i].data.fd);
        }
    }
}
```

This single-threaded server can handle thousands of concurrent connections efficiently.

## Answering the Original Question

So, to answer the original question: there's no background kernel process constantly checking for data. Instead:

1. **The kernel maintains readiness state** for each file descriptor
2. **Your application explicitly asks** "which FDs are ready?" using `epoll_wait()` or similar
3. **The kernel efficiently returns** only the FDs that have data available
4. **Your application processes** those ready FDs and then asks again

It's a pull model, not a push model. The application pulls information about ready file descriptors when it's ready to process them.

## Modern Frameworks and Languages

This pattern is so fundamental that it's built into many high-level frameworks:

- **Node.js**: Uses libuv, which wraps epoll/kqueue/IOCP
- **Go**: Goroutines use an internal poller for network operations
- **Rust**: Tokio provides async I/O built on these primitives
- **Java**: NIO uses select/epoll under the hood
- **Python**: asyncio leverages these same mechanisms

Understanding non-blocking I/O helps you write more efficient programs and better understand how modern high-performance applications work under the hood.

## Key Takeaways

1. **Non-blocking I/O doesn't use callbacks at the kernel level** – it uses efficient polling mechanisms
2. **Event loops aren't constantly spinning** – they block until events are ready
3. **Modern OS APIs like epoll scale to thousands of connections** with minimal overhead
4. **Single-threaded event loops can outperform multi-threaded blocking approaches** for I/O-bound workloads
5. **The pattern is ubiquitous** in modern programming languages and frameworks

The elegance of non-blocking I/O lies in its simplicity: instead of creating threads for each connection, you let the kernel tell you when work is ready to be done.

---

**References:**
- [epoll(7) - Linux manual page](https://man7.org/linux/man-pages/man7/epoll.7.html)
- [kqueue(2) - FreeBSD manual page](https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2)
- [The C10K Problem](http://www.kegel.com/c10k.html)
- [How does non-blocking IO work under the hood](https://medium.com/ing-blog/how-does-non-blocking-io-work-under-the-hood-6299d2953c74)