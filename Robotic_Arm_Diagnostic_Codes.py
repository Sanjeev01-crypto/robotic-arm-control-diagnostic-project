"""
Robotic Arm Diagnostic Codes
Task: Diagnose and confirm the reported delay in the rotate_joint command.

This file includes:
1. Command response-time simulation
2. check_response_time() function
3. Diagnostic table generation
4. Delay analysis using 0.15 second threshold
5. Graph 1: command response times
6. Graph 2: difference from delay threshold
"""

import time
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Expected / measured command response times from the task
# ------------------------------------------------------------

command_response_times = {
    "move_arm": 0.10,
    "rotate_joint": 0.18,
    "adjust_grip": 0.09
}

commands = ["move_arm", "rotate_joint", "adjust_grip"]

delay_threshold = 0.15


# ------------------------------------------------------------
# 2. Function to check response time
# ------------------------------------------------------------

def check_response_time(command):
    """
    Simulates execution of a robotic arm command and measures response time.

    Args:
        command (str): The robotic arm command name.

    Returns:
        float: Measured response time in seconds.
    """
    if command not in command_response_times:
        raise ValueError(f"Unknown command: {command}")

    start_time = time.time()

    # Simulated command execution delay
    time.sleep(command_response_times[command])

    response_time = time.time() - start_time
    return round(response_time, 2)


# ------------------------------------------------------------
# 3. Run diagnostic test for each command
# ------------------------------------------------------------

results = []

for command in commands:
    response_time = check_response_time(command)
    difference_from_threshold = round(response_time - delay_threshold, 2)
    status = "Delayed" if response_time > delay_threshold else "Normal"

    results.append({
        "Command": command,
        "Measured Response Time (s)": response_time,
        "Difference from 0.15s Threshold (s)": difference_from_threshold,
        "Status": status
    })

    print(f"{command}: {response_time} seconds - {status}")


# ------------------------------------------------------------
# 4. Create diagnostic table
# ------------------------------------------------------------

df = pd.DataFrame(results)
print("\nDiagnostic Results:")
print(df)


# ------------------------------------------------------------
# 5. Identify command needing optimization
# ------------------------------------------------------------

delayed_commands = df[df["Status"] == "Delayed"]

if not delayed_commands.empty:
    print("\nCommands needing optimization:")
    for command in delayed_commands["Command"]:
        print(f"- {command}")
else:
    print("\nNo commands exceeded the delay threshold.")


# ------------------------------------------------------------
# 6. Graph 1: Command response times
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))
bars = plt.bar(df["Command"], df["Measured Response Time (s)"])
plt.axhline(delay_threshold, linestyle="--", label="Delay threshold = 0.15 s")
plt.title("Robotic Arm Command Response Times")
plt.xlabel("Command")
plt.ylabel("Response Time (seconds)")
plt.ylim(0, 0.22)
plt.legend()

for bar, value in zip(bars, df["Measured Response Time (s)"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.005,
        f"{value:.2f}s",
        ha="center"
    )

plt.tight_layout()
plt.savefig("robotic_arm_response_times.png", dpi=200, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# 7. Graph 2: Difference from threshold
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))
bars = plt.bar(df["Command"], df["Difference from 0.15s Threshold (s)"])
plt.axhline(0, linestyle="--", label="Threshold boundary")
plt.title("Delay Check Against 0.15s Threshold")
plt.xlabel("Command")
plt.ylabel("Difference from Threshold (seconds)")
plt.ylim(-0.08, 0.06)
plt.legend()

for bar, value in zip(bars, df["Difference from 0.15s Threshold (s)"]):
    label = f"{value:+.2f}s"
    y_position = value + 0.004 if value >= 0 else value - 0.012

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        y_position,
        label,
        ha="center"
    )

plt.tight_layout()
plt.savefig("robotic_arm_delay_threshold_check.png", dpi=200, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# 8. Final conclusion
# ------------------------------------------------------------

print("\nFinal Conclusion:")
print(
    "The diagnostic data confirms that rotate_joint is delayed. "
    "It takes 0.18 seconds, which is 0.03 seconds above the 0.15-second "
    "delay threshold. Therefore, rotate_joint should be optimized first."
)
