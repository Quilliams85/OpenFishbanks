

# OpenFishbanks

**OpenFishbanks** is an open-source, online, and asynchronous adaptation of MIT Sloan's renowned Fishbanks simulation.  
This platform enables participants to engage in a dynamic, multiplayer game that simulates the complexities of managing renewable resources, particularly fisheries.  
Ideal for educational settings, workshops, and research, OpenFishbanks offers an interactive environment to explore concepts in sustainability, economics, and resource management.

---

## Features

- **Web-Based Interface**: Accessible through modern web browsers, eliminating the need for additional software installations.
- **Asynchronous Gameplay**: Participants can join and play at their convenience, accommodating diverse schedules.
- **Multiplayer Support**: Facilitates group participation, fostering collaborative decision-making and strategy development.
- **Educational Utility**: Serves as a practical tool for teaching and understanding the dynamics of resource management and sustainability.

---

## Getting Started

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **Virtual Environment** (recommended)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Quilliams85/OpenFishbanks.git
   cd OpenFishbanks
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Access the Application**

   Navigate to `http://localhost:8000` in your web browser to start using OpenFishbanks.

---

## Repository Structure

```plaintext
OpenFishbanks/
├── fishbanks/           # Core application logic
├── fishbanksapp/        # Frontend and user interface components
├── register/            # User registration and authentication
├── manage.py            # Django's command-line utility
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Submit a Pull Request**

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

OpenFishbanks is inspired by the original Fishbanks simulation developed by MIT Sloan School of Management.  
This adaptation aims to make the simulation more accessible and adaptable for various educational and research purposes.
