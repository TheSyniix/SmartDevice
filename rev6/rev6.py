#importeren van de libraries
import time
import busio
import adafruit_ssd1306
import RPi.GPIO as GPIO
from board import SCL, SDA
from statistics import mean
from gpiozero import MCP3008
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# GPIO pin servo motor
servo_pin = 22

#LED stup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

# Connect Moisture Sensor to MCP3008 kanaal0
moisture_sensor = MCP3008(channel=0)

# Define function convert ADC value naar percentage
def convert_to_percentage(value, max_value= 0.6):
    return (value / max_value) * 100
# PWM servo
servo_pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frequency

# Function to set servo position
def set_servo_position(angle):
    duty_cycle = (angle / 18) + 2
    servo_pwm.start(duty_cycle)
    time.sleep(1)
    servo_pwm.stop()
    
# Lijsten aanmaken
value_list = []
timestamps = []

# Threshold for "water geven" message
threshold = 20

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Constants for drawing
padding = -2
top = padding
bottom = height - padding
x = 0

# Load default font.
font = ImageFont.load_default()

# Create a live plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, len(value_list))
ax.set_ylim(0, 1.0)  

try:
    while True:
        # Input moisture value en omzetten in percentage
        moisture_value = moisture_sensor.value
        moisture_percentage = convert_to_percentage(moisture_value)
        
        #opslaan values and timestamps
        value_list.append(moisture_percentage)
        timestamps.append(time.time())
        
        # Print de moisture percentage in console
        print(f"Moisture Level: {moisture_percentage:.2f}%")
        
        # lijst limiet
        max_points = 100
        if len(value_list) > max_points:
            value_list.pop(0)
            timestamps.pop(0)

        # Update the live plot
        line.set_data(range(len(value_list)), value_list)
        ax.relim()
        ax.autoscale_view()

        #clear display
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Check if the moisture value is below the threshold        
        draw.text((x, top + 0), f"Moisture Level: {moisture_percentage:.2f}%", font=font, fill=255)
        
        if moisture_percentage < threshold:
            print("Water geven")
            draw.text((x, top + 12), f"geef me water", font=font, fill=255)
            GPIO.output(18, True)
            GPIO.output(17, False)
            GPIO.output(12, False)
            GPIO.output(16, False)
            servo_pwm.start(7.5)  # Duty cycle for 90 degrees
            time.sleep(0.5)  # Wait for the servo to move
                        
        elif 21 <= moisture_percentage <= 40: 
            print("Aan het drinken")
            draw.text((x, top + 12), f"Geef me meer", font=font, fill=255)
            GPIO.output(12, True)
            GPIO.output(17, False)
            GPIO.output(18, False)
            GPIO.output(16, False)
            
        elif 41 <= moisture_percentage <= 60: 
            print("Aan het drinken")
            draw.text((x, top + 12), f"goed", font=font, fill=255)
            GPIO.output(12, False)
            GPIO.output(17, True)
            GPIO.output(18, False)
            GPIO.output(16, False)
                        
        else:   
            print("hydrated")
            draw.text((x, top + 12), f"blessed", font=font, fill=255)
            GPIO.output(17, False)
            GPIO.output(18, False)
            GPIO.output(12, False)
            GPIO.output(16, True)
            servo_pwm.start(2.5) # Duty cycle for 45 degrees
            time.sleep(0.5)  # Wait for the servo to move
                                
        # Append the highest moisture_value to the value_list
        if not value_list or moisture_percentage > max(value_list):
            value_list.append(moisture_percentage)

        # Display the highest value from value_list
        highest_value = max(value_list)
        gem_value = mean(value_list)
        draw.text((x, top + 24), f"hoogst: {highest_value:.2f}__{gem_value:.2f}", font=font, fill=255)
        
        # Display image.
        disp.image(image)
        disp.show()
        time.sleep(0.2)
        
except KeyboardInterrupt:
    # Exit the program when Ctrl+C is pressed
    pass

finally:
    #cleanen van gpio poorten
    servo_pwm.stop()
    GPIO.cleanup()
 
#plotten van grafiek
plt.figure()
plt.plot(timestamps, value_list)
plt.xlabel("Tijd in sec")
plt.ylabel("Moisture Level (%)")
plt.title("Moisture Level Over Time")
plt.grid(True)

# Save the plot as a PDF file
plt.savefig("moisture_plot.pdf")
plt.show()