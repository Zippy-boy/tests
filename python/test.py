import discord

webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1297933613131890729/K3JcQgeuWxfKs3WwOY3yxKaPtLorieMwTl-fBZbGlkbOzCEe-5b7teDPn-RJ4ff9nevI")
webhook.send("Hello World!")