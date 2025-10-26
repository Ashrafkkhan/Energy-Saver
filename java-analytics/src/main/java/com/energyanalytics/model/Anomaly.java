package com.energyanalytics.model;

public class Anomaly {
    private String time;
    private String type;
    private double value;
    private double expectedValue;
    private String description;
    private String severity;

    public Anomaly(String time, String type, double value, double expectedValue, String description, String severity) {
        this.time = time;
        this.type = type;
        this.value = value;
        this.expectedValue = expectedValue;
        this.description = description;
        this.severity = severity;
    }

    // Getters
    public String getTime() { return time; }
    public String getType() { return type; }
    public double getValue() { return value; }
    public double getExpectedValue() { return expectedValue; }
    public String getDescription() { return description; }
    public String getSeverity() { return severity; }
}
