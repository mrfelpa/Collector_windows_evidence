
- The main objective is to assist in forensic investigation and data preservation in cases of security incidents or other situations that require the analysis of an operating system.

# Features

- Recursive collection of files in a specified directory;
  
- Calculation of SHA-256 hashes for each collected file;
  
- Compression of collected files into a single ZIP file;
  
- Encryption of the ZIP file using the Fernet algorithm (optional);
  
- Generation of a CSV report with information about the collected files, including name, size, date and time of modification, hash and original path.

# Requirements

- Python 3.x;

- Fernet encryption key (optional, to encrypt the collected files).

# Installation

      git clone https://github.com/mrfelpa/Collector_windows_evidence

# Install the dependencies:

      cd Collector_windows_evidence

      pip install -r requirements.txt

# Use

Run the script with the following arguments:

      python collect.py <machine name> <evidence board> -k [ encryption key] [ -o <exit directory> ]

***- Machine name:*** Name of the machine to be analyzed (for logging purposes).

***- Evidence Directory:*** Directory where the evidence files are stored.

***-k encryption key (optional):*** Fernet encryption key to be used to encrypt the collected files.

***-the exit directory (optional):*** Destination directory for the processed files (compressed, encrypted and report). ***The default is output.***

# Remarks

- The tool must be run with administrative privileges on the Windows system.
  
- Make sure you have enough disk space to store the processed (compressed and encrypted) files.
  
- The Fernet encryption key must be stored in a secure location and must not be shared with anyone.

# Contributions

We value contributions to improve this tool. Feel free to contribute suggestions, bug fixes or new features through issues on GitHub.
