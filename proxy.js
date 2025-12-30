const parseArgs = require('minimist');
const io = require('socket.io')();
const axios = require('axios');

const { python = 'http://127.0.0.1:5000' } = parseArgs(process.argv.slice(2));
const PORT = 4567;

io.on('connection', (socket) => {
  console.log('Simulator connected');

  socket.on('telemetry', async (telemetry) => {
    if (!telemetry) return;

    try {
      const { image, speed } = telemetry;

      // Send telemetry to Python model server
      const response = await axios.post(`${python}/predict`, { image, speed });

      const { steering_angle, throttle } = response.data;

      socket.emit('steer', {
        steering_angle: String(steering_angle),
        throttle: String(throttle)
      });

      console.log(`Steering: ${steering_angle}, Throttle: ${throttle}, Speed: ${speed}`);
    } catch (err) {
      console.error('Error communicating with Python server:', err.message);
    }
  });

  socket.on('disconnect', () => console.log('Simulator disconnected'));
});

io.listen(PORT);
console.log(`Proxy server listening on port ${PORT}, forwarding to ${python}`);
