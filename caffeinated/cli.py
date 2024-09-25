import click
import math
from datetime import datetime
from importlib.metadata import version, PackageNotFoundError

# Retrieve the version from the package metadata
try:
    __version__ = version("caffeinated")
except PackageNotFoundError:
    __version__ = "unknown"

@click.command()
@click.version_option(version=__version__, prog_name="caffeinated")  # Adding the version option
@click.option('-c', '--caffeine', type=int, help='Amount of caffeine ingested in mg.')
@click.option('-b', '--bedtime', help='Bedtime in 12-hour format (e.g., 9pm) or 24-hour format (e.g., 2100).')
@click.option('-s', '--start-time', default=None, help='Time you start consuming caffeine in 12-hour format (e.g., 6AM) or 24-hour format (e.g., 0600). Defaults to current system time.')
@click.pass_context
def caffeinated(ctx, caffeine, bedtime, start_time):
    """
    Calculate the remaining caffeine in your system at bedtime based on current caffeine intake.
    """

    # Check if the required arguments are missing
    if not caffeine or not bedtime:
        click.echo(ctx.get_help())  
        ctx.exit(1)  

    # Convert bedtime to 24-hour format
    try:
        bedtime_24hr = convert_to_24_hour(bedtime)
    except ValueError as e:
        click.echo(f"Error: {e}")
        ctx.exit(1)

    # Convert start_time to 24-hour format if provided
    if start_time:
        try:
            start_time_24hr = convert_to_24_hour(start_time)
            start_time = datetime.strptime(start_time_24hr, "%H%M").time()
        except ValueError as e:
            click.echo(f"Error: {e}")
            ctx.exit(1)
    else:
        start_time = datetime.now().time()

    # Calculate the number of hours until bedtime
    try:
        hours_until_bedtime = calculate_hours_until_bedtime(bedtime_24hr, start_time)
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

def convert_to_24_hour(time_str):
    """
    Convert 12-hour format (e.g., 8PM or 6AM) to 24-hour format (e.g., 2000 or 0600).
    If already in 24-hour format (e.g., 2000 or 0600), return it as is.
    """
    time_str = time_str.strip().upper()
    try:
        if time_str[-2:] in ["AM", "PM"]:
            # Convert from 12-hour to 24-hour format
            return datetime.strptime(time_str, "%I%p").strftime("%H%M")
        elif len(time_str) == 4 and time_str.isdigit():
            # Assume it's already in 24-hour format
            return time_str
        else:
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Use e.g., 8PM, 6AM, or 0600.")

def calculate_hours_until_bedtime(bedtime_24hr, start_time):
    """
    Calculate the number of hours from the start time until the given bedtime.
    """
    # Convert bedtime and start time to total hours
    bedtime_hour = int(bedtime_24hr[:2]) + int(bedtime_24hr[2:]) / 60
    start_hour = start_time.hour + start_time.minute / 60

    # Calculate hours until bedtime
    hours_until_bedtime = (bedtime_hour - start_hour) % 24
    return hours_until_bedtime

def calculate_caffeine_level(caffeine_amount, hours_until_bedtime):
    """
    Calculate the remaining caffeine in the system at bedtime.
    """
    return caffeine_amount * 0.5 ** (hours_until_bedtime / 6)

if __name__ == '__main__':
    caffeinated()