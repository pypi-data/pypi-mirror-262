# HubAxle - control interface for the GL Hub

Exposes an HTTP API for controlling the GL Hub.

There are several primary functions:

- Update the configuration files which the GL Runtime is consuming
- Monitor status of the GL Runtime
- Discover and set up cameras that are accessible to the hub


## Using it.

1. Set up a user by setting the `HUB_LOGINS` env var to `username:password` 
   Either do this through the balena dashboard, or by running 
```
docker compose up -e HUB_LOGINS="username:password" hubaxle
```

2. Open the port on the hubaxle container.  (port 8000 inside the container, port 80 on the host)

3. Open `/admin/` page, and authenticate with your login

4. Create a config entry called `runtime.yaml`
5. Watch as the glruntime container does what you tell it to!

## Testing

```
./src/manage.py test
```

## Development:

If it's awkward to set the `HUB_LOGINS` env var, you can also run

```
./src/manage.py createsuperuser
```

from the hubaxle container, and then you can log in with the credentials you set.

