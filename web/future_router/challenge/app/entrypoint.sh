cd /planktonsrouter1ba8b69e

# Loop to monitor and restart Gunicorn if it crashes
while true; do
    echo "Restarting Gunicorn..."
    gunicorn -w 4 --bind 0.0.0.0:8000 'app:app'
    sleep 1
done &

# Loop to monitor and restart customerservice.py if it crashes
while true; do
    python3 karen/customerservice.py
    echo "Restarting Customer Service..."
    sleep 1
done &

# Loop to clean up old files in /tmp every 15 seconds
while true; do
    find /tmp/* -type f -mmin +2 -exec rm -f {} +
    sleep 15
done
