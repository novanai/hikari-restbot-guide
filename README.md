# Register Commands

```bash
py register.py
```

# Run Bot

```
py bot.py
```

Then in another terminal run:
```bash
ssh -R 80:localhost:8080 localhost.run
```
and paste the produced URL into the `Interactions Endpoint URL` box on your Discord application's `General Information` page.

> **Note**: When developing, you don't need to restart the `localhost.run` service in between bot restarts. However each time you do restart the service, a new URL will be produced which you'll need to save as above.