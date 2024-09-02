load("encoding/json.star", "json") # functions for loading and parsing json
load("humanize.star", "humanize") # functions for humanizing data (e.g. time)
load("time.star", "time") # functions for working with time

def main(config):
    # Load the data from the JSON file
    data = json.load("data/astro_events.json")

    timezone = config.get("timezone") or "America/Los_Angeles"
    now = time.now().in_location(timezone)

    # Find the next event
    next_event = None
    for event in data:
        #event_end_time = time.parse(event["time"])
        if event_end_time > now:
            next_event = event
            break

    # Print the next event
    #print(f"The next event is {next_event['name']} at {humanize.time(next_event['time'])}")
    return render.Root(
        child = render.Text("BTC: %d USD" % rate)
    )


def get_schema():
    return schema.Schema(
        version = "1",
        fields = [
            schema.Text(
                id = "who",
                name = "Who?",
                desc = "Who to say hello to.",
                icon = "user",
            ),
            schema.Toggle(
                id = "small",
                name = "Display small text",
                desc = "A toggle to display smaller text.",
                icon = "compress",
                default = False,
            ),
        ],
    )