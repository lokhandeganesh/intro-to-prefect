from pipeline.main import clean_stats_data


def test_clean_stats_data():
    test_input = {
        "sold": 550,
        "5456af6b-bbc5-4f12-87ba-51fd2751833a": 1,
        "INVALID_STATUS": 2,
        "Raphael": 1,
        "string": 4,
        "unavailable": 1,
        "Busy": 1,
        "pending": 116,
        "avalible": 1,
        "available": 182,
        "Not Available": 1,
        "SOLD": 2,
        "invalid_status": 1,
        "avaliable": 1,
        "APPROVED": 1,
        "pokemon gold": 1,
    }

    result_output = clean_stats_data.fn(test_input)

    # Define only the specific key-value pairs you want to validate
    expected_subset = {
        "sold": 552,
        "available": 184,
        "pending": 116,
        "unavailable": 2
    }

    # loop through them dynamically
    for key, expected_value in expected_subset.items():
        assert result_output.get(key) == expected_value
