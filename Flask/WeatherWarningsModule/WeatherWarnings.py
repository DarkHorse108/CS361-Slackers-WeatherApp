BS_GENERAL_ALERT_CLASSES = 'alert alert-dismissible'
BS_ALERT_CLASS_INFO = BS_GENERAL_ALERT_CLASSES + ' ' + 'alert-info'
BS_ALERT_CLASS_WARNING = BS_GENERAL_ALERT_CLASSES + ' ' + 'alert-warning'
BS_ALERT_CLASS_DANGER = BS_GENERAL_ALERT_CLASSES + ' ' + 'alert-danger'

THUNDER_CODES = {'type': 'thunder', 'min': 200, 'max': 233,
                 'bootstrap_alert_class': BS_ALERT_CLASS_DANGER}
DRIZZLE_CODES = {'type': 'drizzle', 'min': 300, 'max': 302,
                 'bootstrap_alert_class': BS_ALERT_CLASS_INFO}
RAIN_CODES = {'type': 'rain', 'min': 500, 'max': 522,
              'bootstrap_alert_class': BS_ALERT_CLASS_WARNING}
SNOW_CODES = {'type': 'snow', 'min': 600, 'max': 623,
              'bootstrap_alert_class': BS_ALERT_CLASS_WARNING}
MIST_CODES = {'type': 'mist', 'min': 700, 'max': 700,
              'bootstrap_alert_class': BS_ALERT_CLASS_INFO}
SMOKE_CODES = {'type': 'smoke', 'min': 711, 'max': 711,
               'bootstrap_alert_class': BS_ALERT_CLASS_DANGER}
HAZE_CODES = {'type': 'haze', 'min': 721, 'max': 721,
              'bootstrap_alert_class': BS_ALERT_CLASS_INFO}
SAND_CODES = {'type': 'sand', 'min': 731, 'max': 731,
              'bootstrap_alert_class': BS_ALERT_CLASS_DANGER}
FOG_CODES = {'type': 'fog', 'min': 741, 'max': 751,
             'bootstrap_alert_class': BS_ALERT_CLASS_WARNING}

WEATHER_CODES = [THUNDER_CODES, DRIZZLE_CODES, RAIN_CODES, SNOW_CODES, MIST_CODES,
                 SMOKE_CODES, HAZE_CODES, SAND_CODES, FOG_CODES]

DAYS_IN_ROW_CONSIDERED_STORM = 2


def generate_warning_dict(storm_pattern_tracker):
    return {
        'type': storm_pattern_tracker.code['type'],
        'bootstrap_alert_class': storm_pattern_tracker.code['bootstrap_alert_class'],
        'days_till': storm_pattern_tracker.days_till,
        'duration_days': storm_pattern_tracker.duration
    }


class StormPatternTracker:
    def __init__(self, code, days_till):
        self.duration = 1
        self.code = code
        self.days_till = days_till

    def is_storm(self):
        if self.duration >= DAYS_IN_ROW_CONSIDERED_STORM:
            return True
        return False


def code_match(code_to_check, code):
    if code['min'] <= code_to_check <= code['max']:
        return True
    return False


def get_matching_weather_code(day):
    for code in WEATHER_CODES:
        if code_match(day['weather_code'], code):
            return code
    return None


class StormFinder:
    def __init__(self):
        self.weather_warnings = []
        self.days_till = 1
        self.storm_pattern_tracker = StormPatternTracker(None, None)

    def assess_weather_pattern(self):
        if self.storm_pattern_tracker.is_storm():
            self.log_storm()

    def log_storm(self):
        weather_storm = generate_warning_dict(self.storm_pattern_tracker)
        self.weather_warnings.append(weather_storm)


def find_storms(per_day_weather_data):
    storm_finder = StormFinder()
    # returns an empty list or a list of storm dictionaries

    for day in per_day_weather_data:
        process_day_weather(day, storm_finder)

    # if the loop ends and that last tracked pattern is a storm, track it
    storm_finder.assess_weather_pattern()

    return storm_finder.weather_warnings


def process_day_weather(day, storm_finder):
    todays_code = get_matching_weather_code(day)
    if todays_code is not None:
        # then we're tracking this code
        if storm_finder.storm_pattern_tracker.code is not None:
            assess_if_streak(day, storm_finder, todays_code)
        else:
            # start tracking the new code
            storm_finder.storm_pattern_tracker = StormPatternTracker(todays_code, storm_finder.days_till)
    else:
        # if we're not tracking the code so end any streak
        storm_finder.assess_weather_pattern()
        storm_finder.storm_pattern_tracker = StormPatternTracker(None, None)
    storm_finder.days_till += 1


def assess_if_streak(day, storm_finder, todays_code):
    if code_match(day['weather_code'], storm_finder.storm_pattern_tracker.code):
        # the streak continues
        storm_finder.storm_pattern_tracker.duration += 1
    else:
        # the streak has ended
        storm_finder.assess_weather_pattern()
        # start tracking the new code
        storm_finder.storm_pattern_tracker = StormPatternTracker(todays_code, storm_finder.days_till)
