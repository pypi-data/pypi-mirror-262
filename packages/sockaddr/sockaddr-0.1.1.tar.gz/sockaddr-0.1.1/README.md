
# sockaddr

Sockaddr helpers for Python.

For example, auditd logs log the socket address in hex form. This should help in decoding them: 

ie

```python3
s_in = sockaddr.from_hex("02000035898A1005000000000000000030BED20858D83A0010000000")
print(type(s_in))
# <class 'sockaddr.addr.sockaddr_in'>

# Using some helper functions for IPv4/6
print(sockaddr.inet_addr(s_in))
# '137.138.16.5'
print(sockaddr.inet_port(s_in))
# 13568
```


# Or unix sockets

```
s_un = sockaddr.from_hex("01002F7661722F72756E2F646F636B65722E736F636B00")
print(s_un.sun_path.decode("utf-8"))
# /var/run/docker.sock
```

