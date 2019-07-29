# Escea Fireplace Python Client

Use this library to access and control Escea Fires over the local network using the proprietary Escea UDP message
protocol.

# Features

- [ ] Discover broadcasting fires
- [ ] Authenticate with pin code\*
- [x] Retrieve Fire State\*
- [x] Turn fire on\*
- [x] Increase / Decrease Target temperature\*
- [x] Turn on flame effect\*
- [x] Turn on fan boost\*
- [ ] Turn on schedules
- [ ] Parity Checking

\* Planned features

# Example

```py
fire = Fire(FIRE_IP, '47', '46')
fire.start(LOCAL_IP)

resp = fire.state()
print >>sys.stderr, resp
# {'current_temp': 19, 'on': False, 'target_temp': 23, 'fan_boost': False, 'flame_effect': False}

fire.power_on()
fire.fan_boost_on()
fire.flame_effect_on()

resp = fire.status()
print >>sys.stderr, resp
# {'current_temp': 19, 'on': True, 'target_temp': 23, 'fan_boost': True, 'flame_effect': True}

```

# API

I have only discovered the control api information by dumping udp traffic from the official Escea iPhone application
while talking to an [Escea DX1500](http://www.escea.com/nz/fireplaces/indoor-fireplaces/dx-series/dx1500/).

The api is a UDP "send / receive" api, where payloads are 15 bytes consisting of 15 hexadecimal commands codes. Commands
are sent and received on port 3300.

## API Protocol

Each portion of the message contains a code that has a certain meaning.

- 1: Unknown, perhaps a code specific to the pin? Perhaps received in the initial authentication. Mine is `47`.
- 2: Command code. This appears to describe what the entire messages function is.
- 3-13: Data codes. For a command message, this is all `00`, e.g. `00:00:00:00:00:00:00:00:00:00:00`. For a state
  response, each portion maps to a specific piece of information, e.g. `06:00:00:00:00:07:13:00:00:00:00`, where `07` is
  target temp and `13` is current temp (note this is hex for the decimal `19`).
- 14: This appears to be a parity command / digest command that confirms the entire message is correct. This can be best
  seen with either an increment response such as an info command when the temp increases by 1, as the parity bit also
  increases by 1, or in a command message where the parity bit matches the command (since the rest of the message is
  `00`).
- 15: Unknown, looks to somehow be related to the first command code? Mine is `46`.

## Who

Created with ♥ by [Mal Curtis](http://github.com/snikch) ([@snikchnz](http://twitter.com/snikchnz))

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
