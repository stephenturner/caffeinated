import click
import math
import time
from datetime import datetime

__version__ = "0.1.0"

@click.command()
@click.version_option(version=__version__, prog_name="coffeetime")  # Adding the version option
@click.option('-c', '--caffeine', type=int, help='Amount of caffeine ingested in mg.')
@click.option('-b', '--bedtime',  help='Bedtime in 12-hour format (e.g. 9pm).')
@click.option('-t', '--current-time', default=None, help='Current time in 12-hour format (e.g., 3PM). Defaults to current system time.')
@click.pass_context
def coffeetime(ctx, caffeine, bedtime, current_time):
    """
    Calculate the remaining caffeine in your system at bedtime based on current caffeine intake.
    """
    # Check if the required arguments are missing
    if not caffeine or not bedtime:
        click.echo(ctx.get_help())  # Print the help message
        ctx.exit(1)  # Exit the program with an error status code
    
    # Convert bedtime to 24-hour format if it's in 12-hour format
    bedtime_24hr = convert_to_24_hour(bedtime)

    # Get the current time
    if current_time:
        current_time = datetime.strptime(current_time.upper(), "%I%p").time()
    else:
        current_time = datetime.now().time()

    # Calculate the number of hours until bedtime
    try:
        bedtime_hours = convert_bedtime_to_hours(bedtime_24hr, current_time)
    except ValueError as e:
        click.echo(f"Error: {e}")
        ctx.exit(1)

    # Calculate the caffeine level
    caffeine_level = coffee_half_life(caffeine, bedtime_hours)

    # Display the result
    click.echo(f"You would have {round(caffeine_level, 1)}mg of caffeine in your blood if you went to bed at {format_time(bedtime_24hr)} (in {round(bedtime_hours, 1)} hours).")
    click.echo(f"It's as if you had drank {round(caffeine_level / 90 * 100)}% of a cup of coffee before you went to bed.")

def format_time(time):
    """
    Format the time to a 12-hour format (e.g., 3PM).
    """
    return datetime.strptime(time, "%H%M").strftime("%I:%M%p").lstrip("0").lower()

def convert_to_24_hour(bedtime):
    """
    Convert 12-hour format (e.g., 8PM) to 24-hour format (e.g., 2000).
    If already in 24-hour format (e.g., 2000), return it as is.
    """
    try:
        bedtime = bedtime.upper()
        if bedtime[-2:] in ["AM", "PM"]:
            # 12-hour to 24-hour format
            return datetime.strptime(bedtime, "%I%p").strftime("%H%M")
        else:
            # Already in 24-hour format
            return bedtime
    except ValueError:
        raise ValueError(f"Invalid bedtime format: {bedtime}. Use e.g. 8PM or 2000.")

def convert_bedtime_to_hours(bedtime, current_time):
    """
    Convert bedtime to hours from the current time. Validate if the bedtime is within the 0000-2359 range.
    """
    # Validate bedtime format and range
    if not bedtime.isdigit() or not (0 <= int(bedtime) <= 2359):
        raise ValueError(f"Bedtime must be between 0000 and 2359. Got: {bedtime}")

    bedtime_hour = int(bedtime[:2]) + int(bedtime[2:]) / 60
    current_hour = current_time.hour + current_time.minute / 60

    # Calculate the number of hours until bedtime
    if bedtime_hour < current_hour:
        bedtime_hour += 24  # Adjust for the next day

    return bedtime_hour - current_hour


def coffee_half_life(caffeine_amount, hours_until_bedtime):
    """
    Calculate the remaining caffeine in the system at bedtime.
    """
    return caffeine_amount * 0.5 ** (hours_until_bedtime / 6)

if __name__ == '__main__':
    coffeetime()