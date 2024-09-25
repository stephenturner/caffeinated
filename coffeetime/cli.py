import click
import math
from datetime import datetime

__version__ = "0.1.0"

@click.command()
@click.version_option(version=__version__, prog_name="coffeetime")  # Adding the version option
@click.option('-c', '--caffeine', type=int, help='Amount of caffeine ingested in mg.')
@click.option('-b', '--bedtime', help='Bedtime in 12-hour format (e.g., 9pm) or 24-hour format (e.g., 2100).')
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

    # Convert bedtime to 24-hour format if necessary
    try:
        bedtime_24hr = convert_to_24_hour(bedtime)
    except ValueError as e:
        click.echo(f"Error: {e}")
        ctx.exit(1)

    # Get the current time in 24-hour format
    if current_time:
        try:
            current_time = datetime.strptime(current_time.upper(), "%I%p").time()
        except ValueError:
            click.echo(f"Error: Invalid current time format: {current_time}. Use e.g., 3PM.")
            ctx.exit(1)
    else:
        current_time = datetime.now().time()

    # Calculate the number of hours until bedtime
    try:
        hours_until_bedtime = calculate_hours_until_bedtime(bedtime_24hr, current_time)
    except ValueError as e:
        click.echo(f"Error: {e}")
        ctx.exit(1)

    # Calculate the caffeine level at bedtime
    caffeine_level = calculate_caffeine_level(caffeine, hours_until_bedtime)

    # Display the result
    formatted_bedtime = format_time(bedtime_24hr)
    click.echo(f"You would have {round(caffeine_level, 1)}mg of caffeine in your system if you went to bed at {formatted_bedtime} (in {round(hours_until_bedtime, 1)} hours).")
    click.echo(f"That's like having {round(caffeine_level / 90 * 100)}% of a cup of coffee before bed.")

def format_time(time_24hr):
    """
    Format the time to a 12-hour format (e.g., 3PM).
    """
    return datetime.strptime(time_24hr, "%H%M").strftime("%I:%M%p").lstrip("0").lower()

def convert_to_24_hour(bedtime):
    """
    Convert 12-hour format (e.g., 8PM) to 24-hour format (e.g., 2000).
    If already in 24-hour format (e.g., 2000), return it as is.
    """
    bedtime = bedtime.strip().upper()
    try:
        if bedtime[-2:] in ["AM", "PM"]:
            # Convert from 12-hour to 24-hour format
            return datetime.strptime(bedtime, "%I%p").strftime("%H%M")
        elif len(bedtime) == 4 and bedtime.isdigit():
            # Assume it's already in 24-hour format
            return bedtime
        else:
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid bedtime format: {bedtime}. Use e.g., 8PM or 2000.")

def calculate_hours_until_bedtime(bedtime_24hr, current_time):
    """
    Calculate the number of hours from the current time until the given bedtime.
    """
    # Convert bedtime and current time to total hours
    bedtime_hour = int(bedtime_24hr[:2]) + int(bedtime_24hr[2:]) / 60
    current_hour = current_time.hour + current_time.minute / 60

    # Calculate hours until bedtime
    hours_until_bedtime = (bedtime_hour - current_hour) % 24
    return hours_until_bedtime

def calculate_caffeine_level(caffeine_amount, hours_until_bedtime):
    """
    Calculate the remaining caffeine in the system at bedtime.
    """
    return caffeine_amount * 0.5 ** (hours_until_bedtime / 6)

if __name__ == '__main__':
    coffeetime()