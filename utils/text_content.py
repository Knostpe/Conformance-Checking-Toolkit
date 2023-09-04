# text_content.py
welcome_message = """
Dear Participants,

We appreciate your willingness to participate in this research, which aims to assess the effectiveness of our prototype in supporting the visual representation of conformance checking results.

The prototype was created to aid users in extracting insights from conformance checking data. 
When using visual analytics in the context of conformance checking, your feedback will be critical in understanding user expectations.

Please complete the survey, which should still be open in another tab, and participate in the tasks provided. Thank you for your time and effort.
"""

bold_words = ["Process mining", "Conformance Checking", "event logs", "event log", "process models", "process model", "deviations", "deviation", "alignments", "alignment"]

process_mining_introduction = """
Process mining is a data-driven approach that uses event logs to uncover how business processes are executed, identify deviations, and measure performance. 
This aids organizations in optimizing efficiency, ensuring compliance, and making data-driven decisions. It comprises three key disciplines:

- Process Discovery: Automatically generates process models to visualize actual workflows, helping organizations understand the flow of activities.
- Conformance Checking: Compares the observed process behavior in event logs to predefined process models, highlighting deviations and ensuring alignment with intended processes.
- Process Enhancement: Analyzes event logs to find areas for process improvement, enabling optimization for efficiency and compliance.
"""
for word in bold_words:
    process_mining_introduction = process_mining_introduction.replace(word, f"<b>{word}</b>")

conformance_checking_introduction = """
Conformance Checking is a core discipline used in the field of process mining and business process management to assess the alignment between observed process 
behavior and the expected or intended behavior of a process. It involves comparing real-world execution traces of a process, often captured in event logs, 
with a predefined process model or specification.

The main goal of conformance checking is to identify and quantify discrepancies or deviations between the observed process executions and the expected 
behavior. These discrepancies are often referred to as "violations" or "deviations" and can highlight potential inefficiencies, non-compliance with regulations, or 
opportunities for process improvement.

Conformance Checking is an essential tool for organizations seeking to gain insights into their business processes' actual execution and identify 
areas for optimization and compliance assurance. The results of conformance checking help process analysts and managers make data-driven decisions to 
enhance process performance, identify bottlenecks, and ensure adherence to process standards.
"""

for word in bold_words:
    conformance_checking_introduction = conformance_checking_introduction.replace(word, f"<b>{word}</b>")

business_process_model_introduction = """
A (business) process model is a visual representation of how activities, tasks and information flow within an organisation to achieve specific business objectives. 
goals. It's widely used in Business Process Management (BPM) for documentation, analysis and improvement. 

Two common tools for creating these models are Petri nets and Business Process Model and Notation (BPMN), while this tool uses Petri nets. Petri nets 
provide a formal, mathematical approach, while BPMN provides a user-friendly, graphical notation. 

Petri nets were chosen for use in this tool primarily because of their suitability and ease of implementation for conformance checking. The inclusion of BPMN 
models would be desirable for a future version of CCTK.
"""

for word in bold_words:
    business_process_model_introduction = business_process_model_introduction.replace(word, f"<b>{word}</b>")

event_logs_introduction = """
Event logs are chronological records of events or activities within a system, process, or application. Event logs are commonly used for real-time monitoring, 
troubleshooting, security, compliance,  performance analysis, and business process analysis in various domains, including information technology and business process management.

In the context of this tool, event logs consist of the following set of essential attributes:
- Case ID: A unique identifier assigned to individual instances or cases of process executions, facilitating organization and tracking within event logs.
- Event Type: A classification that categorizes events or activities in event logs, offering insights into the nature of each recorded event.
- Timestamp: A Timestamp is a date and time value associated with each event in the log, providing chronological context and facilitating event sequence analysis.
- Event ID: An identifier linked to each event within the scope of an individual case, providing information about the order in which events occurred within cases.

These attributes provide crucial data for the tool's functionality.
"""

for word in bold_words:
    event_logs_introduction = event_logs_introduction.replace(word, f"<b>{word}</b>")
# Define other text strings here