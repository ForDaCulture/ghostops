import pytest
from tools.dns_exfil_classifier import classify_query

def test_low_entropy_flagged():
    assert classify_query("api.example.com") == "anomalous"

def test_high_entropy_passes():
    assert classify_query("a1b2c3x7y8z9.example.com") == "normal"
