A quick and **dirty** notify component for home-assistant and [awtrix](https://awtrixdocs.blueforcer.de/#/).

Awtrix is a DIY 8x32 RGB Matrix display for text and icon. It has an [API](https://awtrixdocs.blueforcer.de/#/en-en/api) to use it with home-automation software. But it is able to run "stand-alone" with its java based server.

Long time ago i made a  [**hack**](https://forum.blueforcer.de/d/192-home-assistant-and-awtrix/32) to connect awtrix to home assitant. It worked but wasn't as nice as it should be.

Now there is this notify-component. Wich will work e.g. with the alert-component.

#Setup

```yaml
awtrix:
  url: "http://IP.IP.IP.IP:port/api/v3/"

notify:
  - name: "awtrix"
    platform: awtrix
```

#Usage
All parameters unter data will be pushed to awtrix so see the documentation there

The target parameter can be set to notify (default),temporaryapp or customapp

##simple notify
```yaml
service: notify.awtrix
data:
  data:
    force: true
    icon: 1023
  message: Hello from home-assistant
```

##update temporaryapp

note: the title parameter maps to the name parameter from awtrix

```yaml
service: notify.awtrix
data_template:
  data:
    icon: 6
  message: '{{ states("input_text.sample") }}'
  target: temporaryapp
  title: sample
```

##simple barchart

```yaml
service: notify.awtrix
data_template:
  data:
    icon: 12
    barchart: [10,100,20,100,30,100,40]
  message: forecast
```