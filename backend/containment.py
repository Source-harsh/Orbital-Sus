from schemas import (
    TelemetryData,
    ClassificationName,
    ThreatLevel,
    ResponseState,
    AssessmentResult,
    ScenarioName
)

class ContainmentEngine:
    """
    Automated Defense Containment Engine for Spacecraft Cyber-Physical Systems.
    Evaluates incoming telemetry and ML predictions to decide containment actions.
    """

    def evaluate_telemetry(self, telemetry: TelemetryData) -> AssessmentResult:
        # Rule-based heuristics / ML integration placeholder
        anomaly_score = 0.0
        threat_level = ThreatLevel.LOW
        classification = ClassificationName.NORMAL
        scenario = ScenarioName.NORMAL
        details = "System operating within nominal parameters."

        # Check for Cyber Anomaly Indicators
        if telemetry.command_type.upper() in ["UNAUTHORIZED", "SPOOFED", "MALFORMED"] or telemetry.communication_anomaly:
            anomaly_score += 0.55
            classification = ClassificationName.CYBER_ANOMALY
            scenario = ScenarioName.CYBER_ATTACK
            details = f"Detected suspicious command type: {telemetry.command_type} or comms anomaly flag."

        if telemetry.command_frequency > 10:
            anomaly_score += 0.35
            classification = ClassificationName.CYBER_ANOMALY
            scenario = ScenarioName.CYBER_ATTACK
            details += f" High command frequency ({telemetry.command_frequency}/s) detected."

        if telemetry.cpu_usage > 90.0:
            anomaly_score += 0.20
            details += f" High CPU usage ({telemetry.cpu_usage}%)."

        # Check for Hardware / Physical Anomaly Indicators
        if telemetry.battery < 20.0 or telemetry.temperature > 75.0 or abs(telemetry.attitude) > 15.0:
            if classification != ClassificationName.CYBER_ANOMALY:
                classification = ClassificationName.HARDWARE_FAULT
                scenario = ScenarioName.HARDWARE_FAULT
                details = f"Hardware degradation: Battery {telemetry.battery}%, Temp {telemetry.temperature}°C, Attitude error {telemetry.attitude}°."
            anomaly_score += 0.30

        anomaly_score = min(1.0, anomaly_score)

        # Map Anomaly Score to Threat Level
        if anomaly_score >= 0.85:
            threat_level = ThreatLevel.CRITICAL
        elif anomaly_score >= 0.60:
            threat_level = ThreatLevel.HIGH
        elif anomaly_score >= 0.35:
            threat_level = ThreatLevel.MEDIUM
        else:
            threat_level = ThreatLevel.LOW

        # Automated Containment State Policy
        response_state = self.determine_response_state(classification, threat_level)

        return AssessmentResult(
            satellite_id=telemetry.satellite_id,
            timestamp=telemetry.timestamp,
            scenario=scenario,
            classification=classification,
            threat_level=threat_level,
            recommended_response=response_state,
            anomaly_score=round(anomaly_score, 2),
            details=details
        )

    def determine_response_state(self, classification: ClassificationName, threat_level: ThreatLevel) -> ResponseState:
        if classification == ClassificationName.CYBER_ANOMALY:
            if threat_level == ThreatLevel.CRITICAL:
                return ResponseState.ISOLATE_CHANNEL
            elif threat_level == ThreatLevel.HIGH:
                return ResponseState.BLOCK_COMMAND
            elif threat_level == ThreatLevel.MEDIUM:
                return ResponseState.INCREASE_MONITORING
            else:
                return ResponseState.ALERT

        elif classification == ClassificationName.HARDWARE_FAULT:
            if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
                return ResponseState.SAFE_MODE
            else:
                return ResponseState.INCREASE_MONITORING

        elif classification == ClassificationName.ENVIRONMENTAL_DISTURBANCE:
            if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
                return ResponseState.INCREASE_MONITORING
            else:
                return ResponseState.ALERT

        return ResponseState.ALERT
