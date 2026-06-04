from .orchestrator import run_healthguard_pipeline

history = [
    "headache",
    "fatigue",
    "chest discomfort"
]

result = run_healthguard_pipeline(
    "I have severe chest pain and shortness of breath",
    history
)

print(result)