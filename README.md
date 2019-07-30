# Escea Fireplace Python Client

Use this library to access and control Escea Fires over the local network using the proprietary Escea UDP message
protocol.

```py
# An example of all current methods and functionality
fires = escea.fires()

for fire in fires:
    print(fire.serial())
    # 66012
    print(fire.pin())
    # 6011
    print(fire.status())
    # {'current_temp': 19, 'on': False, 'target_temp': 23, 'fan_boost': False, 'flame_effect': False}
    fire.power_on()
    fire.fan_boost_on()
    fire.flame_effect_on()
    fire.set_temp(25)
    print(fire.status())
    # {'current_temp': 19, 'on': True, 'target_temp': 25, 'fan_boost': True, 'flame_effect': True}
    fire.fan_boost_off()
    fire.flame_effect_off()
    fire.power_off()
    print(fire.status())
    # {'current_temp': 19, 'on': False, 'target_temp': 25, 'fan_boost': False, 'flame_effect': False}
```

```py
# You can also create a Fire instance manually
fire = escea.Fire('192.168.1.22')
```

## API Protocol

The UDP protocol is described in the
[Escea Fireplace LAN Communications Protocol Specification Document](https://github.com/snikch/escea/files/644165/630260_3.Escea.Fireplace.LAN.Comms.Spec.pdf).

## Who

Created with ♥ by [Mal Curtis](http://github.com/snikch) ([@snikchnz](http://twitter.com/snikchnz))

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
