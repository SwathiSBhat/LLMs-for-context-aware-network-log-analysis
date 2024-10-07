# LogSmart: Retrieval-Augmented Generation In Network Events

<img width="619" alt="Screenshot 2024-10-06 at 8 53 26 PM" src="https://github.com/user-attachments/assets/5f5fd9bd-3eaa-415b-b6bb-322054fc9bee">


## Summary
In modern network security, a Security Operations Center (SOC) must address both internal network activities and external threats. While sophisticated tools like Security Information and Event Management (SIEM) systems, firewalls, Intrusion Detection Systems (IDS), and Extended Detection and Response (XDR) solutions offer comprehensive visibility and threat detection, they often generate overwhelming numbers of alerts, many of which are false positives. These alerts typically rely on rule-based approaches and lack contextual network information, making it challenging for SOC operators to understand the exact nature of the events.
To address these issues, we propose a context-aware log data analysis platform that leverages the capabilities of large language models (LLMs). This system features an API layer to aggregate heterogeneous log events from state-of-the-art security tools, enriched with tailored prompts designed to encapsulate security events with contextual awareness of the network environment. Our main research contribution includes a methodology for integrating heterogeneous, stateful information into a foundational model to generate knowledge about network events. Unlike existing tools, our platform provides comprehensive contextualization of alerts, encompassing external threat intelligence, network events, and internally generated alerts.

## Components of system

### Infrastructure for network simulation
To rigorously test our LLM agent’s capability in context summarization, we utilized Terraform, a cloud provisioning automation tool, to construct various network emulations. Specifically, we designed a simplified network emulation representing a school environment. This emulation consisted of two Virtual Private Clouds (VPCs): one designated for students and the other for professors. Each VPC contained its own subnet, effectively segmenting the network to mirror real-
world scenarios of network segregation in educational institutions.Within this emulated environment, we conducted a series of both benign and malicious activities to evaluate the effectiveness of our log context summarization. By orchestrating these activities, we aimed to simulate typical and atypical network behaviors, thereby challenging our LLM agent to accurately differentiate and contextualize log data.

To automate the configurations on the provisioned network, we employed Ansible to manage and execute these operations efficiently. Ansible facilitated the installation of various necessary components, such as configuring Filebeat, which is used to aggregate logs and forward them to Elastic Cloud for further analysis.

### Log Aggregation

Aggregated logs are directly streamed to an Elasticsearch cluster hosted in the cloud, ensuring efficient storage and retrieval for the LLM agents as needed. Specifically, various Linux logs, including auditd, kern.log, and syslog, are continuously aggregated and transmitted to the cloud storage system. To facilitate this process, we employed the Filebeat application, which is adept at monitoring changes in the log files located in the /var/log directory.

### RAG

The LLM agent is designed and implemented as a Retrieval-Augmented Generation (RAG) module, allowing users to integrate either the OpenAI ChatGPT module or the Google Gemini model. Furthermore, we developed a set of specialized prompting modules specifically designed to extract contextual information from the logs. This development process involved extensive trial and error to refine these prompts for optimal performance. Additionally, our framework is modularized, enabling users to easily plug in their own custom prompts as needed.

### Attack automation

To thoroughly evaluate the system’s capabilities, we implemented a sophisticated attack automation component. This component facilitates the initiation of various attacks on the network, originating from both internal and external sources. By simulating a wide range of attack vectors, we can create a comprehensive assessment environment that mirrors real-world conditions.

## Results

| Month    | Benign filesystem activities | Benign network activities | SSH brute force | Aggresive port scan | Reverse shell and privilege escalation | Ping of death | 
| -------- | ------- | -------- | -------- | -------- | -------- | -------- |
| GPT | Success | Success | Success | Moderate | Moderate | Success |
| Gemini | Fail | Fail | Fail | Fail | Fail | Fail | 

